'use strict';
(()=>{
 const paths=[...document.querySelectorAll('[data-help-path]')],links=[...document.querySelectorAll('[data-help-topic]')];
 const indexes=new Map(paths.map(p=>[p.dataset.helpPath,0]));
 function show(path,index,focus=false){
  const steps=[...path.querySelectorAll('[data-help-step]')];index=Math.max(0,Math.min(steps.length-1,index));indexes.set(path.dataset.helpPath,index);
  paths.forEach(p=>p.hidden=p!==path);steps.forEach((s,i)=>s.hidden=i!==index);
  path.querySelector('.help-progress').textContent='Passaggio '+(index+1)+' di '+steps.length;
  path.querySelector('.help-step-controls').hidden=false;path.querySelector('[data-help-prev]').disabled=index===0;
  path.querySelector('[data-help-next]').hidden=index===steps.length-1;path.querySelector('[data-help-restart]').hidden=index!==steps.length-1;
  links.forEach(l=>{if(l.dataset.helpTopic===path.dataset.helpPath)l.setAttribute('aria-current','step');else l.removeAttribute('aria-current');});
  if(focus)steps[index].querySelector('h3').focus({preventScroll:true});
 }
 function openHash(focus=false){const path=paths.find(p=>p.id===location.hash.slice(1))||paths[0];show(path,indexes.get(path.dataset.helpPath),focus);}
 links.forEach(l=>l.addEventListener('click',e=>{e.preventDefault();history.replaceState(null,'','#'+l.dataset.helpTopic);openHash();document.getElementById(l.dataset.helpTopic).scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});}));
 paths.forEach(p=>{p.querySelector('[data-help-prev]').addEventListener('click',()=>show(p,indexes.get(p.dataset.helpPath)-1,true));p.querySelector('[data-help-next]').addEventListener('click',()=>show(p,indexes.get(p.dataset.helpPath)+1,true));p.querySelector('[data-help-restart]').addEventListener('click',()=>show(p,0,true));});
 window.addEventListener('hashchange',()=>openHash());openHash();
 document.getElementById('help-search').addEventListener('input',e=>{const q=e.target.value.trim().toLocaleLowerCase('it');let count=0;document.querySelectorAll('.help-faq details').forEach(d=>{const match=d.textContent.toLocaleLowerCase('it').includes(q);d.hidden=!match;if(match)count++;d.open=Boolean(q&&match);});document.getElementById('faq-empty').hidden=count>0;});
})();
