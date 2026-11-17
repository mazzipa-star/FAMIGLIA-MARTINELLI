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
    let index=0;
    function show(n) {
      index=(n+list.length)%list.length;
      image.src=list[index].src;
      image.alt=list[index].caption || card.querySelector('h2').textContent;
      if(counter) counter.textContent=(index+1)+' / '+list.length;
    }
    card.querySelectorAll('.gallery-arrow').forEach(btn=>{
      btn.addEventListener('click',()=>show(index+(btn.classList.contains('next')?1:-1)));
    });
    show(0);
  });
  const album=document.querySelector('.full-album[data-items]');
  if(!album) return;
  const list=contents(album), image=album.querySelector('.album-stage img');
  const caption=album.querySelector('[data-caption]'), number=album.querySelector('[data-count]');
  const full=album.querySelector('[data-original]'), thumbs=album.querySelectorAll('[data-slide]');
  let i=0;
  function show(n) {
    if(!list.length) return;
    i=(n+list.length)%list.length;
    image.src=list[i].src;
    image.alt=list[i].caption || 'Fotografia dell’archivio';
    if(caption) caption.textContent=list[i].caption || 'Fotografia dell’archivio';
    if(number) number.textContent='Fotografia '+(i+1)+' di '+list.length;
    if(full) full.href=list[i].full || list[i].src;
    thumbs.forEach((b,k)=>b.setAttribute('aria-pressed',String(i===k)));
  }
  album.querySelectorAll('.album-stage button').forEach(b=>b.addEventListener('click',()=>show(i+(b.classList.contains('next')?1:-1))));
  thumbs.forEach((b,k)=>b.addEventListener('click',()=>show(k)));
  document.addEventListener('keydown',e=>{
    if(e.target.closest('input,textarea,select'))return;
    if(e.key==='ArrowLeft')show(i-1);
    if(e.key==='ArrowRight')show(i+1);
  });
  show(0);
})();
