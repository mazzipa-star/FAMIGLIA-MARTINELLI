import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import vm from 'node:vm';
const sandbox={};vm.runInNewContext(await readFile(new URL('../../dist/genealogia-completo.js',import.meta.url),'utf8'),sandbox);
const build=input=>JSON.parse(JSON.stringify(sandbox.FamilyTreeViews.withComplete(input)));
const source=JSON.parse(await readFile(new URL('../../content/genealogia.json',import.meta.url),'utf8'));
test('complete view unifies Giovanni and preserves source trees and relationships',()=>{
 const before=JSON.stringify(source),result=build(source),full=result[0],ids=new Set(full.people.map(p=>p.id));
 assert.equal(full.id,'completo');assert.equal(full.people.length,76);assert.equal(ids.size,76);
 assert.equal(full.people.filter(p=>p.catalog_id==='family-34').length,1);
 const g=full.people.find(p=>p.id==='discendenti-0');
 assert.deepEqual(g.parents,['antenati-8','antenati-9']);assert.deepEqual(g.partners,['discendenti-1']);
 assert.ok(full.families.some(f=>f.parents.includes('antenati-8')&&f.children.includes('discendenti-0')));
 assert.ok(full.families.some(f=>f.parents.includes('discendenti-0')&&f.children.includes('discendenti-6')));
 for(const p of full.people){assert.ok(Number.isFinite(p.x)&&Number.isFinite(p.y));for(const id of [...p.parents,...p.partners])assert.ok(ids.has(id));if(p.marriages)for(const m of p.marriages){assert.ok(ids.has(m.partner));for(const id of m.children)assert.ok(ids.has(id));}}
 for(const f of full.families)for(const id of [...f.parents,...f.children])assert.ok(ids.has(id));
 assert.equal(JSON.stringify(source),before);assert.deepEqual(result.slice(1),source);
});
test('live refresh rebuilds the full tree without accumulating duplicates and includes new people',()=>{
 const updated=structuredClone(source);updated[1].people.push({...updated[1].people.at(-1),id:'new-child',catalog_id:'new-child',parents:['discendenti-6'],partners:[],marriages:undefined});
 assert.equal(build(updated)[0].people.length,77);assert.equal(build(build(updated))[0].people.length,77);
 assert.equal(build(updated)[0].people.find(p=>p.id==='new-child').parents[0],'discendenti-6');
});
test('never merges people just because they have the same name',()=>{
 const changed=structuredClone(source);changed[0].people[0].name=changed[1].people[5].name;assert.equal(build(changed)[0].people.length,76);
});
