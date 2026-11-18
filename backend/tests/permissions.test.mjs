import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {PGlite} from '@electric-sql/pglite';

const ids={admin:'11111111-1111-4111-8111-111111111111',editor:'22222222-2222-4222-8222-222222222222',outsider:'33333333-3333-4333-8333-333333333333'};
const db=new PGlite();
await db.exec(`create role anon;create role authenticated;create schema auth;
create table auth.users(id uuid primary key,email text,email_confirmed_at timestamptz);
create function auth.uid() returns uuid language sql stable as $$select (nullif(current_setting('request.jwt.claims',true),'')::jsonb->>'sub')::uuid$$;`);
await db.exec(await readFile(new URL('../supabase/migrations/20261118_family_access.sql',import.meta.url),'utf8'));
await db.exec(`insert into auth.users values ('${ids.admin}','owner@example.test',now()),('${ids.editor}','editor@example.test',now()),('${ids.outsider}','outsider@example.test',now());
insert into family_private.admins values('${ids.admin}');
insert into family_private.trees values('discendenti','{"id":"discendenti","title":"Discendenti","pdf":"original.pdf"}');
insert into family_private.people(id,tree_id,data) select id,'discendenti',jsonb_build_object('id',id,'catalog_id',id,'name',id,'x',x,'y',y,'portrait','assets/avatar.svg') from (values('ancestor',0,0),('root',0,156),('spouse',185,156),('child',0,312),('child-spouse',185,312),('grandchild',0,468),('other',600,156),('stepchild',600,312)) p(id,x,y);
insert into family_private.parents values('ancestor','root'),('root','child'),('spouse','child'),('child','grandchild'),('spouse','stepchild'),('other','stepchild');
insert into family_private.partners values('root','spouse'),('child','child-spouse');
insert into family_private.records select id,jsonb_build_object('id',id,'name',id,'aliases','[]'::jsonb) from family_private.people;
insert into family_private.branches(id,root_id,label) values('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','root','Family root');
insert into family_private.grants values('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','${ids.editor}',true);
update family_private.settings set media_base='https://project.supabase.co/storage/v1/object/public/family-portraits/';`);

async function as(user,sql,args=[]){
 await db.exec('begin');
 try{await db.query("select set_config('request.jwt.claims',$1,true)",[JSON.stringify({sub:user||null})]);await db.exec('set local role '+(user?'authenticated':'anon'));const result=await db.query(sql,args);await db.exec('commit');return result.rows;}
 catch(error){await db.exec('rollback');throw error;}
}
async function person(id){return (await db.query('select family_private.person($1) p',[id])).rows[0].p;}
async function save(user,id,fields,parents,partners,revision){const p=await person(id);return as(user,'select public.family_save_person($1,$2,$3,$4,$5) p',[id,JSON.stringify(fields),parents||p.parents,partners||p.partners,revision||p.revision]);}

test('public snapshot contains genealogy, not account details',async()=>{
 const rows=await as(null,'select public.family_snapshot() result');const text=JSON.stringify(rows);assert.ok(text.includes('ancestor'));assert.ok(!text.includes('example.test'));assert.ok(!text.includes(ids.editor));
});
test('anonymous and outsiders cannot write or read private tables',async()=>{
 await assert.rejects(()=>as(null,"select public.family_context()"));
 await assert.rejects(()=>save(ids.outsider,'root',{name:'intruder'}),e=>e.code==='42501');
 await assert.rejects(()=>as(ids.editor,'select * from family_private.admins'),e=>e.code==='42501');
});
test('scope includes descendants and their spouses, not ancestors, siblings or a spouse’s other children',async()=>{
 const context=(await as(ids.editor,'select public.family_context() c'))[0].c;
 assert.deepEqual(context.people.map(p=>p.id).sort(),['root','spouse','child','child-spouse','grandchild'].sort());
 await save(ids.editor,'grandchild',{birth:'1 gennaio 2020'});
 for(const id of ['ancestor','other','stepchild'])await assert.rejects(()=>save(ids.editor,id,{name:'forbidden'}),e=>e.code==='42501');
});
test('ancestor references are preserved when editing root details',async()=>{
 await save(ids.editor,'root',{name:'Root updated'});assert.deepEqual((await person('root')).parents,['ancestor']);
 await assert.rejects(()=>save(ids.editor,'root',{name:'hijack'},[],['ancestor','spouse']),e=>e.code==='42501');
});
test('an editor cannot grant their own account permissions or forge protected fields',async()=>{
 await assert.rejects(()=>as(ids.editor,'select public.family_set_access($1,$2,$3,true)',['editor@example.test','other','Other family']),e=>e.code==='42501');
 await assert.rejects(()=>save(ids.editor,'root',{id:'other'}));
 await assert.rejects(()=>save(ids.editor,'root',{admin:true}));
});
test('optimistic locking prevents stale overwrites and audits the previous state',async()=>{
 const before=await person('child');await save(ids.editor,'child',{name:'Child updated'},null,null,before.revision);
 await assert.rejects(()=>save(ids.editor,'child',{name:'stale'},null,null,before.revision),e=>e.code==='40001');
 assert.equal((await person('child')).name,'Child updated');
 const history=(await as(ids.editor,'select public.family_history($1) h',['child']))[0].h;assert.equal(history[0].before.name,'child');
 const current=await person('child');await as(ids.editor,'select public.family_restore($1,$2,$3)',['child',history[0].id,current.revision]);assert.equal((await person('child')).name,'child');
});
test('new children and partners inherit exactly the assigned branch',async()=>{
 const child=(await as(ids.editor,'select public.family_add_relative($1,$2,$3,$4) p',['root','child','{"name":"New child"}','spouse']))[0].p;
 assert.deepEqual(new Set(child.parents),new Set(['root','spouse']));await save(ids.editor,child.id,{birth_place:'Verona'});
 const partner=(await as(ids.editor,'select public.family_add_relative($1,$2,$3,null) p',[child.id,'partner','{"name":"New spouse"}']))[0].p;
 await save(ids.editor,partner.id,{name:'New spouse updated'});
 const count=(await db.query('select count(*)::integer c from family_private.people')).rows[0].c;
 await assert.rejects(()=>as(ids.editor,'select public.family_add_relative($1,$2,$3,null)',['spouse','child','{"name":"Outside child"}']));
 assert.equal((await db.query('select count(*)::integer c from family_private.people')).rows[0].c,count);
});
test('cyclic ancestry and cross-branch reparenting are rejected atomically',async()=>{
 await assert.rejects(()=>save(ids.editor,'child',{},['grandchild'],['child-spouse']));
 await assert.rejects(()=>save(ids.editor,'child',{},['other'],['child-spouse']),e=>e.code==='42501');
 assert.deepEqual(new Set((await person('child')).parents),new Set(['root','spouse']));
});
test('image updates accept only own uploads in the configured bucket',async()=>{
 for(const url of ['javascript:alert(1)','https://evil.example/photo.jpg',`https://project.supabase.co/storage/v1/object/public/family-portraits/${ids.outsider}/photo.jpg`])await assert.rejects(()=>save(ids.editor,'child',{portrait:url}));
 await save(ids.editor,'child',{portrait:`https://project.supabase.co/storage/v1/object/public/family-portraits/${ids.editor}/photo.jpg`});
 const h=(await as(ids.editor,'select public.family_history($1) h',['child']))[0].h[0];await as(ids.editor,'select public.family_restore($1,$2,$3)',['child',h.id,(await person('child')).revision]);assert.equal((await person('child')).portrait,'assets/avatar.svg');
});
test('revoking access is immediate even with the same authenticated session',async()=>{
 await as(ids.admin,'select public.family_set_access($1,$2,$3,false)',['editor@example.test','root','Family root']);
 await assert.rejects(()=>save(ids.editor,'root',{name:'revoked'}),e=>e.code==='42501');
 assert.equal((await as(ids.editor,'select public.family_can_upload() value'))[0].value,false);
 await as(ids.admin,'select public.family_set_access($1,$2,$3,true)',['editor@example.test','root','Family root']);
});
test('owner retains access to all branches while editors cannot enumerate account emails',async()=>{
 await save(ids.admin,'other',{birth:'2 febbraio 1980'});
 await assert.rejects(()=>as(ids.editor,'select public.family_accesses()'),e=>e.code==='42501');
 const grants=(await as(ids.admin,'select public.family_accesses() a'))[0].a;assert.equal(grants[0].email,'editor@example.test');
});
test.after(()=>db.close());
test('only the owner can look up an account to assign a password',async()=>{
 await assert.rejects(()=>as(ids.editor,'select public.family_account($1)',['owner@example.test']),e=>e.code==='42501');
 const account=(await as(ids.admin,'select public.family_account($1) a',['editor@example.test']))[0].a;assert.equal(account.id,ids.editor);assert.equal(account.admin,false);
});
