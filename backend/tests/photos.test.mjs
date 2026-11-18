import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import {PGlite} from '@electric-sql/pglite';
const db=new PGlite(),uid='22222222-2222-4222-8222-222222222222';
await db.exec("create role anon;create role authenticated;create schema auth;create table auth.users(id uuid primary key,email text,email_confirmed_at timestamptz);create function auth.uid() returns uuid language sql stable as $$select (nullif(current_setting('request.jwt.claims',true),'')::jsonb->>'sub')::uuid$$;");
for(const f of ['20261118_family_access.sql','20261118192805_family_photo_albums.sql'])await db.exec(await readFile(new URL('../supabase/migrations/'+f,import.meta.url),'utf8'));
await db.exec(`insert into auth.users values('${uid}','editor@example.test',now());
insert into family_private.trees values('t','{}');
insert into family_private.people(id,tree_id,data) values('sante','t','{"id":"sante","name":"Sante"}'),('vera','t','{"id":"vera","name":"Vera"}');
insert into family_private.branches(root_id,label) values('sante','Sante');
insert into family_private.grants select id,'${uid}',true from family_private.branches;
insert into family_private.photo_albums(id,root_id,title) values('sante','sante','Sante'),('vera','vera','Vera');
insert into family_private.album_photos(id,album_id,src,full_url,caption,position) values('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','sante','assets/a.jpg','assets/a.jpg','Prima',1);
update family_private.settings set media_base='https://project.supabase.co/storage/v1/object/public/family-portraits/';`);
async function as(role,sql,args=[]){await db.exec('begin');try{await db.query("select set_config('request.jwt.claims',$1,true)",[JSON.stringify({sub:role==='authenticated'?uid:null})]);await db.exec('set local role '+role);const r=await db.query(sql,args);await db.exec('commit');return r.rows;}catch(e){await db.exec('rollback');throw e;}}
const pid='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
test('only assigned albums are editable; anonymous users cannot read editor context',async()=>{
assert.deepEqual((await as('authenticated','select public.family_photo_context() c'))[0].c.map(a=>a.id),['sante']);
await assert.rejects(()=>as('authenticated',"select public.family_save_album('vera','x',1)"),e=>e.code==='42501');
await assert.rejects(()=>as('anon','select public.family_photo_context()'),e=>e.code==='42501');
await assert.rejects(()=>as('authenticated','select * from family_private.album_photos'),e=>e.code==='42501');
});
test('caption edits enforce revision and hidden photos disappear from public data',async()=>{
await as('authenticated','select public.family_save_photo($1,$2,$3,1,false,null,1)',['sante',pid,'Nuova']);
await assert.rejects(()=>as('authenticated','select public.family_save_photo($1,$2,$3,1,true,null,1)',['sante',pid,'Stale']),e=>e.code==='40001');
await assert.rejects(()=>as('authenticated','select public.family_save_photo($1,$2,$3,1,true,null,null)',['sante',pid,'Bypass']),e=>e.code==='40001');
const snapshot=(await as('anon','select public.family_photo_snapshot() c'))[0].c;assert.equal(snapshot.find(a=>a.id==='sante').photos.length,0);
assert.equal((await db.query('select count(*)::int n from family_private.photo_history')).rows[0].n,1);
});
test('new images accept only the current user upload path',async()=>{
await assert.rejects(()=>as('authenticated',"select public.family_save_photo('sante',null,'x',1,true,'https://evil.example/a.jpg',null)"));
await as('authenticated','select public.family_save_photo($1,null,$2,2,true,$3,null)',['sante','Caricata','https://project.supabase.co/storage/v1/object/public/family-portraits/'+uid+'/new.jpg']);
});
test('revocation applies immediately to the same user',async()=>{
await db.exec('update family_private.grants set enabled=false');
assert.deepEqual((await as('authenticated','select public.family_photo_context() c'))[0].c,[]);
await assert.rejects(()=>as('authenticated',"select public.family_save_album('sante','x',1)"),e=>e.code==='42501');
});
test.after(()=>db.close());
