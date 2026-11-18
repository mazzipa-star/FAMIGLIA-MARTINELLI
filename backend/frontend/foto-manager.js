export function setupPhotos({rpc,task,status,image}){
 const $=id=>document.getElementById(id), form=$('album-photo-form');
 let albums=[],album=null,photo=null;
 const labels={1:'Prima generazione',2:'Seconda generazione',3:'Terza generazione'};
 function choose(id){
  photo=album?.photos.find(p=>p.id===id)||null;form.hidden=false;form.reset();
  $('photo-edit-title').textContent=photo?'Modifica fotografia':'Aggiungi fotografia';
  form.elements.caption.value=photo?.caption||'';form.elements.generation.value=photo?.generation||'';
  form.elements.visible.checked=photo?.visible??true;form.elements.file.required=!photo;
  $('album-photo-preview').hidden=!photo;if(photo)$('album-photo-preview').src=photo.full_url;
 }
 function render(){
  album=albums.find(a=>a.id===$('photo-album').value)||null;
  $('photo-album-controls').hidden=!album;form.hidden=true;photo=null;
  $('album-photo-list').replaceChildren();if(!album)return;
  $('album-description').value=album.description;
  $('public-album-link').href='album-'+album.id+'.html';
  for(const p of album.photos){
   const button=document.createElement('button');button.type='button';button.className='album-edit-thumb';
   const img=document.createElement('img');img.src=p.src;img.alt='';img.loading='lazy';
   const caption=document.createElement('span');caption.textContent=p.caption||'Senza descrizione';
   const meta=document.createElement('small');meta.textContent=(labels[p.generation]||'Da collocare')+(p.visible?'':' · Nascosta');
   button.append(img,caption,meta);button.addEventListener('click',()=>{choose(p.id);form.scrollIntoView({behavior:'smooth',block:'start'});});$('album-photo-list').append(button);
  }
 }
 async function refresh(){
  const old=$('photo-album').value;albums=await rpc('family_photo_context');
  $('photo-album').replaceChildren();
  for(const a of albums){const o=document.createElement('option');o.value=a.id;o.textContent=a.title;$('photo-album').append(o);}
  const requested=new URLSearchParams(location.search).get('album');
  $('photo-album').value=albums.some(a=>a.id===old)?old:albums.some(a=>a.id===requested)?requested:albums[0]?.id||'';
  $('family-photos').hidden=!albums.length;render();
  if(requested&&albums.some(a=>a.id===requested))$('family-photos').scrollIntoView({block:'start'});
 }
 $('photo-album').addEventListener('change',render);
 $('new-album-photo').addEventListener('click',()=>choose(null));
 $('reload-album').addEventListener('click',()=>task(refresh));
 $('album-description-form').addEventListener('submit',e=>{e.preventDefault();task(async()=>{
  await rpc('family_save_album',{p_album:album.id,p_description:$('album-description').value.trim(),p_revision:album.revision});
  await refresh();status('Descrizione della raccolta salvata e pubblicata.');
 });});
 form.addEventListener('submit',e=>{e.preventDefault();task(async()=>{
  const albumId=album.id,id=photo?.id||null,revision=photo?.revision||null;
  const file=form.elements.file.files[0],url=file?await image(file):null;
  await rpc('family_save_photo',{p_album:albumId,p_id:id,p_caption:form.elements.caption.value.trim(),
   p_generation:form.elements.generation.value?Number(form.elements.generation.value):null,
   p_visible:form.elements.visible.checked,p_url:url,p_revision:revision});
  await refresh();status('Fotografia salvata. La raccolta pubblica è aggiornata.');
 });});
 $('cancel-photo-edit').addEventListener('click',()=>{form.hidden=true;photo=null;});
 return {refresh};
}
