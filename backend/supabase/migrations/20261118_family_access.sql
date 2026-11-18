-- All personal accounts, grants and history stay outside the public Data API.
begin;
create schema if not exists family_private;
revoke all on schema family_private from public, anon, authenticated;
create table family_private.trees(id text primary key, data jsonb not null);
create table family_private.people(
 id text primary key, tree_id text not null references family_private.trees(id),
 data jsonb not null, revision integer not null default 1 check(revision>0),
 updated_at timestamptz not null default now(),
 check(data->>'id'=id), check(length(data->>'name') between 1 and 160)
);
create table family_private.parents(
 parent_id text references family_private.people(id), child_id text references family_private.people(id),
 primary key(parent_id,child_id), check(parent_id<>child_id)
);
create index on family_private.parents(child_id);
create table family_private.partners(
 person_a text references family_private.people(id),person_b text references family_private.people(id),
 primary key(person_a,person_b),check(person_a<person_b)
);
create table family_private.records(id text primary key,data jsonb not null);
create table family_private.admins(user_id uuid primary key references auth.users(id) on delete cascade);
create table family_private.branches(
 id uuid primary key default gen_random_uuid(),root_id text not null unique references family_private.people(id),label text not null
);
create table family_private.grants(
 branch_id uuid references family_private.branches(id),user_id uuid references auth.users(id) on delete cascade,
 enabled boolean not null default true,primary key(branch_id,user_id)
);
create table family_private.history(
 id uuid primary key default gen_random_uuid(),person_id text not null references family_private.people(id),
 actor_id uuid references auth.users(id),created_at timestamptz not null default now(),
 action text not null,before_data jsonb,after_data jsonb not null
);
create table family_private.access_history(
 id uuid primary key default gen_random_uuid(),actor_id uuid references auth.users(id),
 user_id uuid references auth.users(id),root_id text not null,enabled boolean not null,created_at timestamptz default now()
);
create table family_private.settings(id boolean primary key default true check(id),media_base text not null default '');
insert into family_private.settings(id) values(true);
alter table family_private.trees enable row level security;
alter table family_private.people enable row level security;
alter table family_private.parents enable row level security;
alter table family_private.partners enable row level security;
alter table family_private.records enable row level security;
alter table family_private.admins enable row level security;
alter table family_private.branches enable row level security;
alter table family_private.grants enable row level security;
alter table family_private.history enable row level security;
alter table family_private.access_history enable row level security;
alter table family_private.settings enable row level security;
revoke all on all tables in schema family_private from public,anon,authenticated;

create function family_private.require_user() returns uuid language plpgsql stable security definer set search_path='' as $$
begin
 if auth.uid() is null or not exists(select 1 from auth.users where id=auth.uid() and email_confirmed_at is not null) then
  raise exception 'Accesso richiesto' using errcode='42501';
 end if;
 return auth.uid();
end $$;
create function family_private.is_admin() returns boolean language sql stable security definer set search_path='' as $$
 select exists(select 1 from family_private.admins where user_id=auth.uid())
$$;
create function family_private.scope_ids() returns setof text language sql stable security definer set search_path='' as $$
 with recursive descendants(id) as (
  select b.root_id from family_private.branches b join family_private.grants g on g.branch_id=b.id
   where g.user_id=auth.uid() and g.enabled
  union
  select p.child_id from family_private.parents p join descendants d on p.parent_id=d.id
 ), included(id) as (
  select id from descendants union
  select case when p.person_a=d.id then p.person_b else p.person_a end
   from family_private.partners p join descendants d on d.id in (p.person_a,p.person_b)
 ) select id from included
$$;
create function family_private.can_edit(p_id text) returns boolean language sql stable security definer set search_path='' as $$
 select family_private.is_admin() or exists(select 1 from family_private.scope_ids() id where id=p_id)
$$;
create function family_private.person(p_id text) returns jsonb language plpgsql stable security definer set search_path='' as $$
declare result jsonb; partner_id text; partner_ids jsonb:='[]'; unions jsonb:='[]'; union_label text; children jsonb;
begin
 select data||jsonb_build_object('revision',revision,'tree_id',tree_id) into result from family_private.people where id=p_id;
 if result is null then return null;end if;
 for partner_id in
  select case when person_a=p_id then person_b else person_a end other from family_private.partners
  where p_id in(person_a,person_b) order by coalesce((select n from jsonb_array_elements(coalesce(result->'marriages','[]')) with ordinality m(value,n)
   where value->>'partner'=case when person_a=p_id then person_b else person_a end limit 1),9999),other
 loop
  partner_ids:=partner_ids||jsonb_build_array(partner_id);
  if result?'marriages' then
   select value->>'label' into union_label from jsonb_array_elements(result->'marriages') where value->>'partner'=partner_id limit 1;
   select coalesce(jsonb_agg(a.child_id order by a.child_id),'[]') into children from family_private.parents a
    join family_private.parents b on a.child_id=b.child_id where a.parent_id=p_id and b.parent_id=partner_id;
   unions:=unions||jsonb_build_array(jsonb_build_object('partner',partner_id,'label',coalesce(union_label,'Coniuge'),'children',children));
  end if;
 end loop;
 result:=result||jsonb_build_object('partners',partner_ids,'parents',coalesce((select jsonb_agg(parent_id order by parent_id) from family_private.parents where child_id=p_id),'[]'));
 if result?'marriages' then result:=result||jsonb_build_object('marriages',unions);end if;
 return result;
end
$$;
create function family_private.validate_parent() returns trigger language plpgsql set search_path='' as $$
begin
 if (select count(*) from family_private.parents where child_id=new.child_id)>=2 then raise exception 'Sono già presenti due genitori';end if;
 if exists(with recursive ancestors(id) as (select new.parent_id union select parent_id from family_private.parents p join ancestors a on p.child_id=a.id)
  select 1 from ancestors where id=new.child_id) then raise exception 'Il collegamento crea un ciclo genealogico';end if;
 if (select tree_id from family_private.people where id=new.parent_id)<>(select tree_id from family_private.people where id=new.child_id)
  then raise exception 'Persone appartenenti ad alberi differenti';end if;
 return new;
end $$;
create trigger check_family_parent before insert on family_private.parents for each row execute function family_private.validate_parent();

create function public.family_is_admin() returns boolean language plpgsql stable security definer set search_path='' as $$
begin perform family_private.require_user();return family_private.is_admin();end $$;
create function public.family_can_upload() returns boolean language plpgsql stable security definer set search_path='' as $$
begin
 perform family_private.require_user();
 return family_private.is_admin() or exists(select 1 from family_private.grants where user_id=auth.uid() and enabled);
end $$;
create function public.family_status() returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('schema_version',1,'ready',exists(select 1 from family_private.people))
$$;
create function public.family_snapshot() returns jsonb language plpgsql stable security definer set search_path='' as $$
declare result_trees jsonb; result_profiles jsonb;
begin
 select jsonb_agg(t.data || jsonb_build_object('people',
  coalesce((select jsonb_agg(family_private.person(p.id) order by p.data->>'name',p.id) from family_private.people p where p.tree_id=t.id),'[]'),
  'families',coalesce((
   with child_sets as (
    select child_id,array_agg(parent_id order by parent_id) ids from family_private.parents l
     join family_private.people p on p.id=l.child_id where p.tree_id=t.id group by child_id
   ), families as (
    select ids,jsonb_agg(child_id order by child_id) children from child_sets group by ids
    union all
    select array[p.person_a,p.person_b],'[]'::jsonb from family_private.partners p
     join family_private.people q on q.id=p.person_a where q.tree_id=t.id and not exists(
      select 1 from child_sets c where c.ids=array[p.person_a,p.person_b])
   ) select jsonb_agg(jsonb_build_object('parents',ids,'children',children)) from families
  ),'[]')) order by t.id) into result_trees from family_private.trees t;
 with public_people as (
  select distinct on (data->>'catalog_id') data->>'catalog_id' catalog_id,data,id from family_private.people
   order by data->>'catalog_id',tree_id desc
 ), profiles as (
  select r.data || case when p.id is null then '{}'::jsonb else jsonb_build_object(
   'name',p.data->>'name','birth',coalesce(p.data->>'birth',''),'birth_place',coalesce(p.data->>'birth_place',''),
   'death',coalesce(p.data->>'death',''),'notes',coalesce(p.data->>'notes',''),
   'photo',case when coalesce((p.data->>'portrait_missing')::boolean,false) then '' else p.data->>'portrait' end,
   'photo_full',case when coalesce((p.data->>'portrait_missing')::boolean,false) then '' else coalesce(p.data->>'portrait_full',p.data->>'portrait') end,
   'tree_ids',coalesce((select jsonb_agg(q.id) from family_private.people q where q.data->>'catalog_id'=r.id),'[]')) end data
  from family_private.records r left join public_people p on p.catalog_id=r.id
 ) select jsonb_agg(data order by data->>'name') into result_profiles from profiles;
 return jsonb_build_object('schema_version',1,'trees',coalesce(result_trees,'[]'),'profiles',coalesce(result_profiles,'[]'));
end $$;
create function public.family_context() returns jsonb language plpgsql stable security definer set search_path='' as $$
declare actor uuid; admin boolean;
begin
 actor:=family_private.require_user();admin:=family_private.is_admin();
 return jsonb_build_object('admin',admin,'user_id',actor,'publication','direct',
  'branches',coalesce((select jsonb_agg(jsonb_build_object('id',b.id,'root_id',b.root_id,'label',b.label) order by b.label)
   from family_private.branches b where admin or exists(select 1 from family_private.grants g where g.branch_id=b.id and g.user_id=actor and g.enabled)),'[]'),
  'people',coalesce((select jsonb_agg(family_private.person(p.id) order by p.data->>'name') from family_private.people p where family_private.can_edit(p.id)),'[]'));
end $$;
create function family_private.clean_fields(p_fields jsonb,p_old jsonb) returns jsonb language plpgsql stable security definer set search_path='' as $$
declare value jsonb; k text; media text; portrait text;
begin
 if jsonb_typeof(p_fields)<>'object' or p_fields-array['name','birth','birth_place','death','death_place','notes','portrait']<>'{}'::jsonb
  then raise exception 'Campi non modificabili';end if;
 for k,value in select * from jsonb_each(p_fields) loop
  if jsonb_typeof(value)<>'string' then raise exception 'Valore non valido';end if;
  if length(value#>>'{}')>(case when k='notes' then 20000 when k='portrait' then 2048 else 160 end) then raise exception 'Testo troppo lungo';end if;
 end loop;
 if p_fields?'name' and length(btrim(p_fields->>'name'))=0 then raise exception 'Indicare il nome';end if;
 if p_fields?'portrait' and p_fields->>'portrait' is distinct from p_old->>'portrait' then
  portrait:=p_fields->>'portrait';select media_base into media from family_private.settings where id;
  if media='' or left(portrait,length(media || auth.uid()::text || '/'))<>media || auth.uid()::text || '/'
   or portrait !~ '\.(jpg|jpeg|png|webp)$' or portrait ~ '["<>[:space:]]' then raise exception 'Fotografia non valida';end if;
 end if;
 return p_fields;
end $$;
create function public.family_save_person(p_id text,p_fields jsonb,p_parents text[],p_partners text[],p_revision integer)
 returns jsonb language plpgsql security definer set search_path='' as $$
declare actor uuid; old jsonb; after_person jsonb; row_data family_private.people; reference text; old_parents text[]; old_partners text[];
begin
 actor:=family_private.require_user();
 -- Serialize graph changes: authorizations cannot race a reparenting or revocation.
 perform pg_advisory_xact_lock(821841901);
 if not family_private.can_edit(p_id) then raise exception 'Non sei autorizzato a modificare questa scheda' using errcode='42501';end if;
 select * into strict row_data from family_private.people where id=p_id for update;
 if row_data.revision<>p_revision then raise exception 'La scheda è stata modificata. Ricaricala prima di salvare.' using errcode='40001';end if;
 old:=family_private.person(p_id);perform family_private.clean_fields(p_fields,old);
 p_parents:=coalesce(p_parents,array[]::text[]);p_partners:=coalesce(p_partners,array[]::text[]);
 if cardinality(p_parents)>2 or cardinality(p_partners)>8 or p_id=any(p_parents||p_partners)
  or cardinality(p_parents)<>(select count(distinct x) from unnest(p_parents) x)
  or cardinality(p_partners)<>(select count(distinct x) from unnest(p_partners) x) then raise exception 'Collegamenti non validi';end if;
 select coalesce(array_agg(x),array[]::text[]) into old_parents from jsonb_array_elements_text(old->'parents') x;
 select coalesce(array_agg(x),array[]::text[]) into old_partners from jsonb_array_elements_text(old->'partners') x;
 for reference in select x from (
  (select unnest(old_parents) x except select unnest(p_parents))
  union (select unnest(p_parents) x except select unnest(old_parents))
  union (select unnest(old_partners) x except select unnest(p_partners))
  union (select unnest(p_partners) x except select unnest(old_partners))
 ) changes loop
  if not family_private.can_edit(reference) then raise exception 'Il collegamento riguarda un altro ramo familiare' using errcode='42501';end if;
 end loop;
 for reference in select unnest(p_partners) loop
  if exists(with recursive descendants(id) as (select p_id union select child_id from family_private.parents p join descendants d on p.parent_id=d.id)
   select 1 from descendants where id=reference) or exists(with recursive ancestors(id) as (select p_id union select parent_id from family_private.parents p join ancestors d on p.child_id=d.id)
   select 1 from ancestors where id=reference) then raise exception 'Un antenato o discendente non può essere un coniuge';end if;
 end loop;
 if not(old_parents @> p_parents and p_parents @> old_parents) then
  delete from family_private.parents where child_id=p_id;
  insert into family_private.parents(parent_id,child_id) select unnest(p_parents),p_id;
 end if;
 if not(old_partners @> p_partners and p_partners @> old_partners) then
  delete from family_private.partners where p_id in(person_a,person_b);
  insert into family_private.partners select least(p_id,x),greatest(p_id,x) from unnest(p_partners) x;
  update family_private.people set revision=revision+1,updated_at=now() where id=any(old_partners||p_partners) and id<>p_id;
 end if;
 update family_private.people set data=data||p_fields||jsonb_build_object('date_source','Aggiornato da un referente familiare il '||to_char(current_date,'DD/MM/YYYY'))
  ||case when p_fields?'portrait' then jsonb_build_object('portrait_full',p_fields->>'portrait','portrait_missing',false,'portrait_source','Archivio familiare') else '{}'::jsonb end,
  revision=revision+1,updated_at=now() where id=p_id;
 after_person:=family_private.person(p_id);
 insert into family_private.history(person_id,actor_id,action,before_data,after_data) values(p_id,actor,'update',old,after_person);
 return after_person;
end $$;
create function public.family_add_relative(p_anchor text,p_kind text,p_fields jsonb,p_other_parent text default null)
 returns jsonb language plpgsql security definer set search_path='' as $$
declare actor uuid; person_id text; anchor family_private.people; fields jsonb; result jsonb; y integer; x numeric;
begin
 actor:=family_private.require_user();perform pg_advisory_xact_lock(821841901);
 if not family_private.can_edit(p_anchor) then raise exception 'Ramo non autorizzato' using errcode='42501';end if;
 if p_kind not in('child','partner') then raise exception 'Tipo di legame non valido';end if;
 select * into strict anchor from family_private.people where id=p_anchor;
 fields:=family_private.clean_fields(p_fields,'{}');
 if not(fields?'name') then raise exception 'Indicare il nome';end if;
 if p_other_parent is not null and (p_kind<>'child' or not family_private.can_edit(p_other_parent) or p_other_parent=p_anchor)
  then raise exception 'Secondo genitore non autorizzato' using errcode='42501';end if;
 person_id:='family-'||gen_random_uuid()::text;y:=(anchor.data->>'y')::integer+case when p_kind='child' then 156 else 0 end;
 x:=(anchor.data->>'x')::numeric+case when p_kind='partner' then 185 else 0 end;
 while exists(select 1 from family_private.people where tree_id=anchor.tree_id and (data->>'y')::integer=y and abs((data->>'x')::numeric-x)<140) loop x:=x+200;end loop;
 insert into family_private.people(id,tree_id,data) values(person_id,anchor.tree_id,
  jsonb_build_object('id',person_id,'catalog_id',person_id,'x',x,'y',y,'birth','','death','','deceased_recorded',false,
   'portrait','assets/genealogia/ritratto-non-disponibile.svg','portrait_missing',true,
   'date_source','Dati inseriti da un referente familiare')||fields);
 if p_kind='child' then
  insert into family_private.parents values(p_anchor,person_id);
  if p_other_parent is not null then insert into family_private.parents values(p_other_parent,person_id);end if;
 else insert into family_private.partners values(least(p_anchor,person_id),greatest(p_anchor,person_id));end if;
 if not family_private.can_edit(person_id) then raise exception 'Il nuovo familiare non rientra nel ramo assegnato' using errcode='42501';end if;
 insert into family_private.records values(person_id,jsonb_build_object('id',person_id,'name',fields->>'name','birth','','death','',
  'aliases',jsonb_build_array(),'collection','Nuovi familiari','photo','','photo_full','','source','Dati inseriti dalla famiglia','source_pdf','','tree_ids',jsonb_build_array(person_id)));
 update family_private.people set revision=revision+1 where id=p_anchor;
 result:=family_private.person(person_id);
 insert into family_private.history(person_id,actor_id,action,after_data) values(person_id,actor,'create',result);
 return result;
end $$;
create function public.family_history(p_id text) returns jsonb language plpgsql stable security definer set search_path='' as $$
begin
 perform family_private.require_user();if not family_private.can_edit(p_id) then raise exception 'Accesso non autorizzato' using errcode='42501';end if;
 return coalesce((select jsonb_agg(jsonb_build_object('id',id,'created_at',created_at,'action',action,'before',before_data,'after',after_data) order by created_at desc)
  from (select * from family_private.history where person_id=p_id order by created_at desc limit 50) h),'[]');
end $$;
create function public.family_restore(p_id text,p_history uuid,p_revision integer) returns jsonb language plpgsql security definer set search_path='' as $$
declare snapshot jsonb; result jsonb;
begin
 perform family_private.require_user();if not family_private.can_edit(p_id) then raise exception 'Accesso non autorizzato' using errcode='42501';end if;
 select before_data into snapshot from family_private.history where id=p_history and person_id=p_id;
 if snapshot is null then raise exception 'Versione precedente non disponibile';end if;
 result:=public.family_save_person(p_id,jsonb_build_object('name',snapshot->>'name','birth',coalesce(snapshot->>'birth',''),
  'birth_place',coalesce(snapshot->>'birth_place',''),'death',coalesce(snapshot->>'death',''),'death_place',coalesce(snapshot->>'death_place',''),'notes',coalesce(snapshot->>'notes','')),
  array(select jsonb_array_elements_text(snapshot->'parents')),array(select jsonb_array_elements_text(snapshot->'partners')),p_revision);
 -- These image values come from immutable server history, never from client input.
 update family_private.people set data=data||jsonb_build_object('portrait',snapshot->>'portrait',
  'portrait_full',coalesce(snapshot->>'portrait_full',snapshot->>'portrait'),
  'portrait_missing',coalesce((snapshot->>'portrait_missing')::boolean,false)) where id=p_id;
 result:=family_private.person(p_id);
 update family_private.history set action='restore',after_data=result
  where person_id=p_id and actor_id=auth.uid() and (after_data->>'revision')::integer=(result->>'revision')::integer;
 return result;
end $$;
create function public.family_accesses() returns jsonb language plpgsql stable security definer set search_path='' as $$
begin
 perform family_private.require_user();if not family_private.is_admin() then raise exception 'Solo amministratori' using errcode='42501';end if;
 return coalesce((select jsonb_agg(jsonb_build_object('email',u.email,'root_id',b.root_id,'label',b.label,'enabled',g.enabled) order by u.email,b.label)
  from family_private.grants g join family_private.branches b on b.id=g.branch_id join auth.users u on u.id=g.user_id),'[]');
end $$;
create function public.family_set_access(p_email text,p_root text,p_label text,p_enabled boolean) returns jsonb language plpgsql security definer set search_path='' as $$
declare actor uuid; target uuid; branch uuid;
begin
 actor:=family_private.require_user();perform pg_advisory_xact_lock(821841901);
 if not family_private.is_admin() then raise exception 'Solo amministratori' using errcode='42501';end if;
 select id into target from auth.users where lower(email)=lower(btrim(p_email));
 if target is null then raise exception 'Account non trovato' using errcode='P0002';end if;
 if length(btrim(p_label)) not between 1 and 160 then raise exception 'Nome del ramo non valido';end if;
 insert into family_private.branches(root_id,label) values(p_root,btrim(p_label)) on conflict(root_id) do update set label=excluded.label returning id into branch;
 insert into family_private.grants(branch_id,user_id,enabled) values(branch,target,p_enabled) on conflict(branch_id,user_id) do update set enabled=excluded.enabled;
 insert into family_private.access_history(actor_id,user_id,root_id,enabled) values(actor,target,p_root,p_enabled);
 return jsonb_build_object('email',p_email,'root_id',p_root,'enabled',p_enabled);
end $$;

create function public.family_account(p_email text) returns jsonb language plpgsql stable security definer set search_path='' as $$
declare result jsonb;
begin
 perform family_private.require_user();if not family_private.is_admin() then raise exception 'Solo amministratori' using errcode='42501';end if;
 select jsonb_build_object('id',id,'admin',exists(select 1 from family_private.admins a where a.user_id=u.id)) into result from auth.users u where lower(email)=lower(btrim(p_email));
 return result;
end $$;
revoke all on function public.family_account(text) from public,anon,authenticated;
grant execute on function public.family_account(text) to authenticated;

revoke all on all functions in schema family_private from public,anon,authenticated;
revoke all on function public.family_is_admin(),public.family_can_upload(),public.family_context(),public.family_save_person(text,jsonb,text[],text[],integer),
 public.family_add_relative(text,text,jsonb,text),public.family_history(text),public.family_restore(text,uuid,integer),
 public.family_accesses(),public.family_set_access(text,text,text,boolean),public.family_snapshot(),public.family_status() from public,anon,authenticated;
grant execute on function public.family_snapshot(),public.family_status() to anon,authenticated;
grant execute on function public.family_is_admin(),public.family_can_upload(),public.family_context(),public.family_save_person(text,jsonb,text[],text[],integer),
 public.family_add_relative(text,text,jsonb,text),public.family_history(text),public.family_restore(text,uuid,integer),
 public.family_accesses(),public.family_set_access(text,text,text,boolean) to authenticated;
commit;
