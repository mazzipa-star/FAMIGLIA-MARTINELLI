begin;
create table family_private.photo_albums(
 id text primary key, root_id text not null references family_private.people(id),
 title text not null, description text not null default '', revision integer not null default 1);
create table family_private.album_photos(
 id uuid primary key default gen_random_uuid(), album_id text not null references family_private.photo_albums(id),
 src text not null, full_url text not null, caption text not null default '',
 generation integer check(generation between 1 and 3), position integer not null,
 visible boolean not null default true, revision integer not null default 1);
create index album_photos_album_position on family_private.album_photos(album_id,position);
create table family_private.photo_history(
 id uuid primary key default gen_random_uuid(), actor_id uuid references auth.users(id),
 album_id text not null references family_private.photo_albums(id), photo_id uuid,
 created_at timestamptz not null default now(), before_data jsonb, after_data jsonb not null);
alter table family_private.photo_albums enable row level security;
alter table family_private.album_photos enable row level security;
alter table family_private.photo_history enable row level security;
revoke all on family_private.photo_albums,family_private.album_photos,family_private.photo_history from public,anon,authenticated;
create function family_private.can_edit_album(p_album text) returns boolean language sql stable security definer set search_path='' as $$
 select family_private.is_admin() or exists(
 select 1 from family_private.photo_albums a join family_private.branches b on b.root_id=a.root_id
 join family_private.grants g on g.branch_id=b.id where a.id=p_album and g.user_id=auth.uid() and g.enabled)
$$;
revoke all on function family_private.can_edit_album(text) from public,anon,authenticated;
create function public.family_photo_snapshot() returns jsonb language sql stable security definer set search_path='' as $$
 select coalesce(jsonb_agg(jsonb_build_object('id',a.id,'title',a.title,'description',a.description,'photos',
 coalesce((select jsonb_agg(jsonb_build_object('id',p.id,'src',p.src,'full',p.full_url,'caption',p.caption,
 'generation',p.generation,'original_number',p.position) order by p.position,p.id)
 from family_private.album_photos p where p.album_id=a.id and p.visible),'[]'::jsonb)) order by a.id),'[]'::jsonb)
 from family_private.photo_albums a
$$;
create function public.family_photo_context() returns jsonb language plpgsql stable security definer set search_path='' as $$
begin
 perform family_private.require_user();
 return coalesce((select jsonb_agg(to_jsonb(a)||jsonb_build_object('photos',
 coalesce((select jsonb_agg(to_jsonb(p) order by p.position,p.id) from family_private.album_photos p where p.album_id=a.id),'[]'::jsonb)) order by a.title)
 from family_private.photo_albums a where family_private.can_edit_album(a.id)),'[]'::jsonb);
end $$;
create function public.family_save_album(p_album text,p_description text,p_revision integer) returns void
 language plpgsql security definer set search_path='' as $$
declare actor uuid; old family_private.photo_albums;
begin
 actor:=family_private.require_user();perform pg_advisory_xact_lock(821841901);
 if not family_private.can_edit_album(p_album) then raise exception 'Album non autorizzato' using errcode='42501';end if;
 if p_description is null or length(p_description)>20000 then raise exception 'Descrizione non valida';end if;
 select * into strict old from family_private.photo_albums where id=p_album for update;
 if p_revision is null or old.revision<>p_revision then raise exception 'Album modificato: ricarica i dati' using errcode='40001';end if;
 update family_private.photo_albums set description=p_description,revision=revision+1 where id=p_album;
 insert into family_private.photo_history(actor_id,album_id,before_data,after_data)
 values(actor,p_album,to_jsonb(old),jsonb_build_object('description',p_description,'revision',p_revision+1));
end $$;
create function public.family_save_photo(p_album text,p_id uuid,p_caption text,p_generation integer,p_visible boolean,p_url text,p_revision integer)
 returns uuid language plpgsql security definer set search_path='' as $$
declare actor uuid; old family_private.album_photos; result uuid; n integer;
begin
 actor:=family_private.require_user();perform pg_advisory_xact_lock(821841901);
 if not family_private.can_edit_album(p_album) then raise exception 'Album non autorizzato' using errcode='42501';end if;
 if p_caption is null or length(p_caption)>4000 or p_visible is null or (p_generation is not null and p_generation not between 1 and 3)
 then raise exception 'Dati fotografia non validi';end if;
 if p_id is not null then
  select * into strict old from family_private.album_photos where id=p_id and album_id=p_album for update;
  if p_revision is null or old.revision<>p_revision then raise exception 'Fotografia modificata: ricarica i dati' using errcode='40001';end if;
 end if;
 if p_url is not null then
  perform family_private.clean_fields(jsonb_build_object('portrait',p_url),'{}'::jsonb);
 elsif p_id is null then raise exception 'Scegli una fotografia';end if;
 if p_id is null then
  select coalesce(max(position),0)+1 into n from family_private.album_photos where album_id=p_album;
  insert into family_private.album_photos(album_id,src,full_url,caption,generation,visible,position)
  values(p_album,p_url,p_url,p_caption,p_generation,p_visible,n) returning id into result;
 else
  update family_private.album_photos set caption=p_caption,generation=p_generation,visible=p_visible,
   src=coalesce(p_url,src),full_url=coalesce(p_url,full_url),revision=revision+1 where id=p_id returning id into result;
 end if;
 insert into family_private.photo_history(actor_id,album_id,photo_id,before_data,after_data)
 select actor,p_album,result,case when p_id is null then null else to_jsonb(old) end,to_jsonb(p)
 from family_private.album_photos p where id=result;
 return result;
end $$;
revoke all on function public.family_photo_snapshot(),public.family_photo_context(),public.family_save_album(text,text,integer),
 public.family_save_photo(text,uuid,text,integer,boolean,text,integer) from public,anon,authenticated;
grant execute on function public.family_photo_snapshot() to anon,authenticated;
grant execute on function public.family_photo_context(),public.family_save_album(text,text,integer),
 public.family_save_photo(text,uuid,text,integer,boolean,text,integer) to authenticated;
commit;
