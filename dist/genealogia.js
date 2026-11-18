'use strict';
(() => {
const trees=JSON.parse(document.getElementById('genealogy-data').textContent);
const $=id=>document.getElementById(id), map=$('tree-map'),canvas=$('tree-canvas');
let tree=trees[0], selected=null, mode='map', scale=1, tx=0,ty=0, bounds={w:1,h:1};
const positions=new Map(),pointers=new Map();let gesture=null,moved=false;
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const year=value=>String(value||'').match(/\b\d{4}\b/)?.[0]||value;
const date=p=>(p.birth||p.death)?[p.birth?'n. '+year(p.birth):'',p.death?'† '+year(p.death):''].filter(Boolean).join(' · '):(!p.date||p.date==='?-?'?'Date non indicate':p.date.replace(/\?/g,'…'));
const person=id=>tree.people.find(p=>p.id===id);
const root=()=>tree.people.find(p=>p.name==='Giovanni Martinelli');
function transform(){canvas.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;$('zoom-level').value=Math.round(scale*100)+'%';}
function zoom(value,x=map.clientWidth/2,y=map.clientHeight/2){const next=Math.max(.06,Math.min(2.5,value));tx=x-(x-tx)*next/scale;ty=y-(y-ty)*next/scale;scale=next;transform();}
function focusPerson(id,zoomLevel=1){const p=positions.get(id);if(!p)return;scale=zoomLevel;tx=map.clientWidth/2-(p.x+108)*scale;ty=map.clientHeight/2-(p.y+90)*scale;transform();}
function fit(){scale=Math.min(1,(map.clientWidth-55)/bounds.w,(map.clientHeight-55)/bounds.h);tx=(map.clientWidth-bounds.w*scale)/2;ty=(map.clientHeight-bounds.h*scale)/2;transform();}
function node(p,kind){return `<img src="${p.portrait}" alt="" draggable="false"><${kind==='map'?'strong':'span'}>${kind==='map'?escape(p.name):`<strong>${escape(p.name)}</strong><small>${escape(date(p))}</small>`}</${kind==='map'?'strong':'span'}>${kind==='map'?`<span>${escape(date(p))}</span>`:''}`;}
function render(){
 positions.clear();const minX=Math.min(...tree.people.map(p=>p.x)),minY=Math.min(...tree.people.map(p=>p.y));
 tree.people.forEach(p=>positions.set(p.id,{x:(p.x-minX)*1.65+45,y:(p.y-minY)*1.7+55}));
 bounds={w:Math.max(...[...positions.values()].map(p=>p.x))+260,h:Math.max(...[...positions.values()].map(p=>p.y))+225};
 canvas.style.width=bounds.w+'px';canvas.style.height=bounds.h+'px';
 let paths='';const line=d=>{paths+=`<path d="${d}"/>`;};
 tree.families.forEach(f=>{const [a,b]=f.parents.map(id=>positions.get(id));const mid=(a.x+b.x)/2+108,y=a.y+90;line(`M ${a.x+216} ${y} H ${b.x}`);const kids=f.children.map(id=>positions.get(id));const branchY=Math.min(...kids.map(p=>p.y))-30;line(`M ${mid} ${y} V ${branchY}`);const xs=kids.map(p=>p.x+108);line(`M ${Math.min(mid,...xs)} ${branchY} H ${Math.max(mid,...xs)}`);kids.forEach(p=>line(`M ${p.x+108} ${branchY} V ${p.y}`));});
 canvas.innerHTML=`<svg width="${bounds.w}" height="${bounds.h}" aria-hidden="true">${paths}</svg>`+tree.people.map(p=>{const xy=positions.get(p.id);return `<button type="button" class="map-node ${p.id===root().id?'root':''}" data-person="${p.id}" style="left:${xy.x}px;top:${xy.y}px" aria-label="${escape(p.name)}, ${escape(date(p))}">${node(p,'map')}</button>`;}).join('');
 $('cards-view').innerHTML=tree.people.map(p=>`<button type="button" class="person-card" data-person="${p.id}">${node(p,'card')}</button>`).join('');
 $('tree-summary').textContent=`${tree.title} di Giovanni Martinelli · ${tree.people.length} persone nell’albero`;
 document.querySelectorAll('[data-tree]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tree===tree.id)));
 $('person-detail').hidden=true; selected=null;focusPerson(root().id,window.innerWidth<650?.95:1);
}
function relatives(ids){return ids.map(id=>`<button type="button" data-person="${id}">${escape(person(id).name)}</button>`).join('');}
function showPerson(id,scroll=true){
 const p=person(id);if(!p)return;selected=id;
 canvas.querySelectorAll('[data-person]').forEach(b=>b.classList.toggle('selected',b.dataset.person===id));
 const children=tree.people.filter(q=>q.parents.includes(id)).map(q=>q.id);
 const section=(title,ids)=>ids.length?`<h3>${title}</h3><div class="relative-links">${relatives(ids)}</div>`:'';
 const unions=p.marriages?'<h3>Matrimoni</h3>'+p.marriages.map(m=>`<div class="family-marriage"><p><strong>${escape(m.label)}</strong></p><div class="relative-links">${relatives([m.partner])}</div><p>${m.children.length===1?'Figlia':'Figli'}</p><div class="relative-links">${relatives(m.children)}</div></div>`).join(''):section('Coniugi e partner',p.partners);
 $('person-detail').innerHTML=`<div class="detail-header"><a href="${p.portrait_full||p.portrait}" target="_blank" rel="noopener"><img src="${p.portrait_full||p.portrait}" alt="${escape(p.portrait_source||'Ritratto nel documento')}"><span>Apri il ritratto ↗</span></a><div><p class="eyebrow">${tree.title.toUpperCase()} · SCHEDA DI FAMIGLIA</p><h2 id="detail-name" tabindex="-1">${escape(p.name)}</h2><p class="detail-dates">Nascita: ${escape(p.birth||'Data non riportata')}<br>Morte: ${escape(p.death||(p.deceased_recorded?'Indicata senza data':'Data non riportata'))}</p>${p.record_name&&p.record_name!==p.name?'<p class="detail-record-name">Nella scheda familiare: '+escape(p.record_name)+'</p>':''}<p class="detail-note">${escape(p.date_source||'Albero genealogico originale')}</p></div></div>${section('Genitori',p.parents)}${unions}${p.marriages?'':section('Figli presenti in questo albero',children)}${!p.parents.length&&!p.partners.length&&!children.length?'<p>Il documento non riporta ulteriori collegamenti per questa persona.</p>':''}<div class="detail-actions"><button type="button" id="locate-person">Mostra nell’albero</button><button type="button" id="close-detail">Chiudi scheda</button></div><p class="detail-note">I collegamenti integrano gli alberi genealogici originali con le correzioni comunicate dalla famiglia. Ritratti e date sono integrati dalle schede e dalle fotografie dell’archivio familiare; le date mancanti non sono state ricostruite.</p>`;
 $('person-detail').hidden=false;
 $('locate-person').onclick=()=>{setMode('map');focusPerson(id);map.scrollIntoView({behavior:'smooth',block:'center'});};
 $('close-detail').onclick=()=>{$('person-detail').hidden=true;const b=canvas.querySelector(`[data-person="${selected}"]`);if(mode==='map'){focusPerson(selected);b?.focus({preventScroll:true});}else $('cards-mode').focus();};
 if(scroll){$('person-detail').scrollIntoView({behavior:'smooth',block:'start'});$('detail-name').focus({preventScroll:true});}
}
function setMode(value){mode=value;$('map-view').hidden=value!=='map';$('cards-view').hidden=value!=='cards';$('map-mode').setAttribute('aria-pressed',String(value==='map'));$('cards-mode').setAttribute('aria-pressed',String(value==='cards'));if(value==='map')focusPerson(selected||root().id);}
document.addEventListener('click',e=>{const p=e.target.closest('[data-person]');if(p){if(!moved||!map.contains(p)){if(p.dataset.sourceTree&&p.dataset.sourceTree!==tree.id){tree=trees.find(t=>t.id===p.dataset.sourceTree);render();}showPerson(p.dataset.person);focusPerson(p.dataset.person);$('search-results').replaceChildren();}moved=false;return;}const t=e.target.closest('[data-tree]');if(t){tree=trees.find(x=>x.id===t.dataset.tree);render();$('person-search').value='';$('search-results').replaceChildren();}if(!e.target.closest('.search-field'))$('search-results').replaceChildren();});
$('person-search').addEventListener('input',e=>{const q=e.target.value.trim().toLocaleLowerCase('it');if(!q){$('search-results').replaceChildren();return;}const matches=trees.flatMap(t=>t.people.filter(p=>p.name.toLocaleLowerCase('it').includes(q)).map(p=>({p,t})));$('search-results').innerHTML=matches.length?matches.map(({p,t})=>`<button type="button" data-person="${p.id}" data-source-tree="${t.id}">${escape(p.name)}<small>${t.title} · ${escape(date(p))}</small></button>`).join(''):'<p>Nessuna persona trovata. Prova con una parte del nome.</p>';});
$('person-search').addEventListener('keydown',e=>{if(e.key==='Escape')$('search-results').replaceChildren();if(e.key==='ArrowDown'){e.preventDefault();$('search-results').querySelector('button')?.focus();}});
$('search-results').addEventListener('keydown',e=>{const b=[...$('search-results').querySelectorAll('button')],i=b.indexOf(document.activeElement);if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();b[(i+(e.key==='ArrowDown'?1:-1)+b.length)%b.length]?.focus();}if(e.key==='Escape'){$('search-results').replaceChildren();$('person-search').focus();}});
$('map-mode').onclick=()=>setMode('map');$('cards-mode').onclick=()=>setMode('cards');$('zoom-in').onclick=()=>zoom(scale*1.25);$('zoom-out').onclick=()=>zoom(scale/1.25);$('fit-tree').onclick=fit;$('home-person').onclick=()=>{focusPerson(root().id);};
if(!document.fullscreenEnabled)$('fullscreen').hidden=true;
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('map-view').requestFullscreen();}catch{$('fullscreen').textContent='Non disponibile';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Esci da schermo intero':'Schermo intero';focusPerson(selected||root().id);});
canvas.addEventListener('focusin',e=>{const b=e.target.closest('[data-person]');if(b)focusPerson(b.dataset.person);});
map.addEventListener('keydown',e=>{if(e.target!==map)return;const delta=70;if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','-','=','0'].includes(e.key)){e.preventDefault();if(e.key==='ArrowLeft')tx+=delta;if(e.key==='ArrowRight')tx-=delta;if(e.key==='ArrowUp')ty+=delta;if(e.key==='ArrowDown')ty-=delta;if(['+','='].includes(e.key))zoom(scale*1.25);if(e.key==='-')zoom(scale/1.25);if(e.key==='0')fit();transform();}});
function beginGesture(){const pts=[...pointers.values()];gesture={points:pts,tx,ty,scale};}
map.addEventListener('pointerdown',e=>{if(e.button!==0)return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});moved=false;beginGesture();});
map.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId)||!gesture)return;const old=pointers.get(e.pointerId);if(Math.hypot(e.clientX-old.x,e.clientY-old.y)>3)moved=true;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});const pts=[...pointers.values()];if(pts.length===1){const dx=pts[0].x-gesture.points[0].x,dy=pts[0].y-gesture.points[0].y;if(Math.hypot(dx,dy)>5){moved=true;map.setPointerCapture(e.pointerId);}tx=gesture.tx+dx;ty=gesture.ty+dy;transform();}else if(pts.length>=2&&gesture.points.length>=2){moved=true;const d=a=>Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y);const rect=map.getBoundingClientRect(),cx=(pts[0].x+pts[1].x)/2-rect.left,cy=(pts[0].y+pts[1].y)/2-rect.top,ox=(gesture.points[0].x+gesture.points[1].x)/2-rect.left,oy=(gesture.points[0].y+gesture.points[1].y)/2-rect.top;scale=Math.max(.06,Math.min(2.5,gesture.scale*d(pts)/Math.max(1,d(gesture.points))));tx=cx-(ox-gesture.tx)*scale/gesture.scale;ty=cy-(oy-gesture.ty)*scale/gesture.scale;transform();}});
function endPointer(e){pointers.delete(e.pointerId);if(pointers.size)beginGesture();else gesture=null;}
map.addEventListener('pointerup',endPointer);map.addEventListener('pointercancel',endPointer);window.addEventListener('pointerup',endPointer);
map.addEventListener('wheel',e=>{e.preventDefault();const r=map.getBoundingClientRect();if(e.ctrlKey||e.metaKey)zoom(scale*Math.exp(-e.deltaY*.008),e.clientX-r.left,e.clientY-r.top);else{tx-=e.deltaX;ty-=e.deltaY;transform();}},{passive:false});
window.addEventListener('resize',()=>{if(mode==='map')focusPerson(selected||root().id);});
render();
})();
