import test from 'node:test';import assert from 'node:assert/strict';import {readFile} from 'node:fs/promises';import vm from 'node:vm';
const sandbox={};vm.runInNewContext(await readFile(new URL('../../dist/genealogia-completo.js',import.meta.url),'utf8'),sandbox);
const build=input=>JSON.parse(JSON.stringify(sandbox.FamilyTreeViews.withComplete(input)));
const source=JSON.parse(await readFile(new URL('../../content/genealogia.json',import.meta.url),'utf8'));
test('complete view unifies Giovanni and preserves source trees and relationships',()=>{
 const before=JSON.stringify(source),result=build(source),full=result[0],ids=new Set(full.people.map(p=>p.id));
 assert.equal(full.id,'completo');assert.equal(full.people.length,87);assert.equal(ids.size,87);
 assert.equal(full.people.filter(p=>p.catalog_id==='family-34').length,1);
 const g=full.people.find(p=>p.id==='discendenti-0');
 assert.deepEqual(g.parents,['antenati-8','antenati-9']);assert.deepEqual(g.partners,['discendenti-1']);
 assert.ok(full.families.some(f=>f.parents.includes('antenati-8')&&f.children.includes('discendenti-0')));
 assert.ok(full.families.some(f=>f.parents.includes('discendenti-0')&&f.children.includes('discendenti-6')));
 for(const p of full.people){assert.ok(Number.isFinite(p.x)&&Number.isFinite(p.y));for(const id of [...p.parents,...p.partners])assert.ok(ids.has(id));if(p.marriages)for(const m of p.marriages){assert.ok(ids.has(m.partner));for(const id of m.children)assert.ok(ids.has(id));}}
 for(const f of full.families)for(const id of [...f.parents,...f.children])assert.ok(ids.has(id));
 assert.equal(JSON.stringify(source),before);assert.deepEqual(result.filter(t=>['antenati','discendenti'].includes(t.id)),source);
});
test('live refresh rebuilds the full tree without accumulating duplicates and includes new people',()=>{
 const updated=structuredClone(source);updated[1].people.push({...updated[1].people.at(-1),id:'new-child',catalog_id:'new-child',parents:['discendenti-6'],partners:[],marriages:undefined});
 assert.equal(build(updated)[0].people.length,88);assert.equal(build(build(updated))[0].people.length,88);
 assert.equal(build(updated)[0].people.find(p=>p.id==='new-child').parents[0],'discendenti-6');
});
test('never merges people just because they have the same name',()=>{
 const changed=structuredClone(source);changed[0].people[0].name=changed[1].people[5].name;assert.equal(build(changed)[0].people.length,87);
});

test('four family branches are isolated, include spouses and all new children',()=>{
 const result=build(source);for(const key of ['vera','graziella','sante','annamaria']){const t=result.find(t=>t.id==='ramo-'+key),ids=new Set(t.people.map(p=>p.id));assert.ok(ids.has(t.root_id));for(const p of t.people)for(const id of [...p.parents,...p.partners])assert.ok(ids.has(id));}
 const anna=result.find(t=>t.id==='ramo-annamaria');assert.equal(anna.people.filter(p=>p.id.startsWith('discendenti-nuovo-')).length,11);assert.ok(!result.find(t=>t.id==='ramo-sante').people.some(p=>p.name==='Laura Uribe'));
 const people=result[0].people;assert.equal(people.find(p=>p.catalog_id==='family-10').birth,'25 settembre 1992');assert.equal(people.find(p=>p.catalog_id==='family-47').birth,'30 maggio 1994');
});

test('minimap viewport follows zoom and pan in tree coordinates',()=>{const v=sandbox.FamilyTreeViews.viewport({tx:-200,ty:-100,scale:2,width:800,height:600});assert.deepEqual(JSON.parse(JSON.stringify(v)),{x:100,y:50,width:400,height:300});});
