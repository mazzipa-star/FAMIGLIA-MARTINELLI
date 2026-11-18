/* Galleries: inline carousel, full album and keyboard navigation. */
(() => {
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
    if(number) number.textContent='Fotografia '+(list[i].original_number || (i+1))+' di '+list.length;
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
