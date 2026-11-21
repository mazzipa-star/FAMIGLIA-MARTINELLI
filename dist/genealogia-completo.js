/* Combine the two source trees by explicit catalog identity; never by name. */
(function(root){
 function withComplete(input){
  const sources=input.filter(t=>t.id!=='completo');
  const ancestors=sources.find(t=>t.id==='antenati'),descendants=sources.find(t=>t.id==='discendenti');
  if(!ancestors||!descendants)return sources;
  const descendantRoot=descendants.people.find(p=>p.id==='discendenti-0');
  const ancestorRoot=ancestors.people.find(p=>p.id==='antenati-10');
  if(!descendantRoot||!ancestorRoot||!descendantRoot.catalog_id||descendantRoot.catalog_id!==ancestorRoot.catalog_id)return sources;
  const canonical=new Map(descendants.people.filter(p=>p.catalog_id).map(p=>[p.catalog_id,p.id]));
  const aliases=new Map(descendants.people.map(p=>[p.id,p.id]));
  for(const p of ancestors.people)aliases.set(p.id,canonical.get(p.catalog_id)||p.id);
  const resolve=id=>aliases.get(id)||id;
  const dx=Number(descendantRoot.x)-Number(ancestorRoot.x),dy=Number(descendantRoot.y)-Number(ancestorRoot.y);
  const people=new Map();
  for(const source of [descendants,ancestors])for(const original of source.people){
   const id=resolve(original.id),offset=source===ancestors;
   const p={...original,id,x:Number(original.x)+(offset?dx:0),y:Number(original.y)+(offset?dy:0),
    parents:[...new Set((original.parents||[]).map(resolve))].filter(x=>x!==id),
    partners:[...new Set((original.partners||[]).map(resolve))].filter(x=>x!==id)};
   if(original.marriages)p.marriages=original.marriages.map(m=>({...m,partner:resolve(m.partner),children:(m.children||[]).map(resolve)}));
   const existing=people.get(id);
   if(existing){existing.parents=[...new Set([...existing.parents,...p.parents])];existing.partners=[...new Set([...existing.partners,...p.partners])];}
   else people.set(id,p);
  }
  const families=[],seen=new Set();
  for(const source of [ancestors,descendants])for(const f of source.families){
   const family={...f,parents:[...new Set(f.parents.map(resolve))],children:[...new Set(f.children.map(resolve))]};
   const key=JSON.stringify([[...family.parents].sort(),[...family.children].sort()]);
   if(!seen.has(key)){seen.add(key);families.push(family);}
  }
  return [{id:'completo',title:'Albero completo',people:[...people.values()],families},...sources];
 }
 root.FamilyTreeViews={withComplete};
})(globalThis);
