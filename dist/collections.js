/* Galleries: inline carousel, full album and keyboard navigation. */
(async () => {
  async function loadFamilyAlbums(){
    const familyIds=['sante','anna','vera','graziella'];
    if(!document.querySelector('.full-album.family-album')&&!document.querySelector('#raccolta-sante'))return;
    try{
      const config=await fetch('family-access-config.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error();return r.json();});
      if(!config.enabled)return;
      const response=await fetch(config.supabaseUrl+'/rest/v1/rpc/family_photo_snapshot',{method:'POST',
        headers:{apikey:config.publishableKey,'Content-Type':'application/json'},body:'{}',signal:AbortSignal.timeout(8000)});
      if(!response.ok)throw Error();const albums=await response.json();
      const labels={1:'Prima generazione',2:'Seconda generazione',3:'Terza generazione'};
      for(const a of albums){
        if(!familyIds.includes(a.id))continue;
        const pictures=a.photos.map(p=>({...p,generation_label:labels[p.generation]||'Da collocare'}));
        const card=document.getElementById('raccolta-'+a.id);
        if(card){
          card.dataset.items=JSON.stringify(pictures);
          card.querySelector('.collection-description').textContent=a.description;
          card.querySelector('.collection-info > p').textContent=pictures.length+' fotografie';
          if(!pictures.length){card.querySelector('.collection-media').hidden=true;}
          const edit=document.createElement('a');edit.href='area-famiglie.html?album='+encodeURIComponent(a.id);
          edit.textContent='✎ Gestisci fotografie';edit.className='secondary';card.querySelector('.collection-actions').append(edit);
        }
        const album=document.querySelector('.full-album.family-album');
        if(!album||!location.pathname.endsWith('/album-'+a.id+'.html'))continue;
        pictures.sort((x,y)=>(x.generation||4)-(y.generation||4)||x.original_number-y.original_number);
        album.dataset.items=JSON.stringify(pictures);album.dataset.initialIndex='0';
        const intro=document.querySelector('.collection-intro');
        if(intro){const description=[...intro.querySelectorAll('p')].find(p=>!p.classList.contains('eyebrow'));if(description)description.textContent=a.description;}
        const edit=document.createElement('a');edit.href='area-famiglie.html?album='+encodeURIComponent(a.id);
        edit.textContent='✎ Gestisci fotografie della famiglia';edit.className='button';album.before(edit);
        const panel=album.querySelector('.album-thumbs-panel');panel.replaceChildren();
        for(const generation of [1,2,3,null]){
          const entries=pictures.map((p,i)=>({p,i})).filter(x=>x.p.generation===generation);
          const key='generazione-'+(generation||'da-collocare'),band=document.createElement('section');
          band.className='generation-band';band.id=key;const title=document.createElement('h3');
          title.textContent=labels[generation]||'Da collocare';band.append(title);
          const thumbs=document.createElement('div');thumbs.className='album-thumbs';
          for(const {p,i} of entries){
            const b=document.createElement('button');b.type='button';b.dataset.slide=String(i);b.setAttribute('aria-label','Foto '+p.original_number+' · '+p.caption);
            const img=document.createElement('img');img.src=p.src;img.loading='lazy';img.alt='';
            const text=document.createElement('span');text.textContent='Foto '+p.original_number+' · '+p.caption;b.append(img,text);thumbs.append(b);
          }
          band.append(thumbs);panel.append(band);
          const count=album.querySelector('[data-generation-target="'+key+'"] span');if(count)count.textContent=entries.length;
        }
        if(!pictures.length){album.querySelector('.album-viewer').hidden=true;const note=document.createElement('p');note.textContent='Non ci sono fotografie pubblicate in questa raccolta.';panel.append(note);}
      }
    }catch{
      const notice=document.createElement('p');notice.textContent='Aggiornamenti fotografici temporaneamente non disponibili: è mostrata la copia di archivio.';
      notice.setAttribute('role','status');document.querySelector('.collection-intro')?.append(notice);
    }
  }
  await loadFamilyAlbums();

  function contents(node) {
    try { return JSON.parse(node.dataset.items || '[]'); }
    catch (_) { return []; }
  }
  document.querySelectorAll('.collection-card[data-items]').forEach(card => {
    const list=contents(card), image=card.querySelector('.collection-media img');
    const counter=card.querySelector('.gallery-counter');
    if(!list.length || !image) return;
    let index=card.dataset.cover ? -1 : 0;
    function show(n) {
      index=(n+list.length)%list.length;
      image.src=list[index].src;
      image.alt=list[index].caption || card.querySelector('h2').textContent;
      if(counter) counter.textContent=(index+1)+' / '+list.length;
    }
    card.querySelectorAll('.gallery-arrow').forEach(btn=>{
      btn.addEventListener('click',()=>show(index===-1 ? (btn.classList.contains('next')?0:list.length-1) : index+(btn.classList.contains('next')?1:-1)));
    });
    if(card.dataset.cover){
      image.src=card.dataset.cover;
      if(counter)counter.textContent='Copertina · '+list.length+' foto';
    }else show(0);
  });
  const album=document.querySelector('.full-album[data-items]');
  if(!album) return;
  const list=contents(album), image=album.querySelector('.album-stage img');
  const caption=album.querySelector('[data-caption]'), number=album.querySelector('[data-count]');
  const full=album.querySelector('[data-original]'), thumbs=album.querySelectorAll('[data-slide]');
  let i=Number(album.dataset.initialIndex || 0);
  function show(n) {
    if(!list.length) return;
    i=(n+list.length)%list.length;
    image.src=list[i].src;
    image.alt=list[i].caption || 'Fotografia dell’archivio';
    if(caption) caption.textContent=list[i].caption || 'Fotografia dell’archivio';
    if(number) number.textContent=album.classList.contains('family-album') ? 'Foto '+list[i].original_number+' · '+list.length+' fotografie nell’album' : 'Fotografia '+(i+1)+' di '+list.length;
    const generation=album.querySelector('[data-generation-label]');
    if(generation)generation.textContent=list[i].generation_label || '';
    if(full) full.href=list[i].full || list[i].src;
    thumbs.forEach((b,k)=>b.setAttribute('aria-pressed',String(i===k)));
    const panel=album.querySelector('.album-thumbs-panel'), active=thumbs[i];
    if(panel && active){
      const box=active.getBoundingClientRect(), viewport=panel.getBoundingClientRect();
      if(box.top<viewport.top || box.bottom>viewport.bottom)panel.scrollTop+=box.top-viewport.top-20;
    }
  }
  album.querySelectorAll('.album-stage button').forEach(b=>b.addEventListener('click',()=>show(i+(b.classList.contains('next')?1:-1))));
  thumbs.forEach((b,k)=>b.addEventListener('click',()=>show(k)));
  document.addEventListener('keydown',e=>{
    if(e.target.closest('input,textarea,select'))return;
    if(e.key==='ArrowLeft')show(i-1);
    if(e.key==='ArrowRight')show(i+1);
  });
  album.querySelectorAll('[data-generation-target]').forEach(button=>button.addEventListener('click',()=>{
    const panel=album.querySelector('.album-thumbs-panel'), section=album.querySelector('#'+button.dataset.generationTarget);
    if(panel && section)panel.scrollTo({top:panel.scrollTop+section.getBoundingClientRect().top-panel.getBoundingClientRect().top,behavior:'smooth'});
  }));
  show(i);
})();
