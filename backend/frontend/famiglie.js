import {createClient} from '@supabase/supabase-js';

const $=id=>document.getElementById(id);
const fields=['name','birth','birth_place','death','death_place','notes'];
const labels={name:'Nome',birth:'Nascita',birth_place:'Luogo di nascita',death:'Morte',death_place:'Luogo di morte',notes:'Note',parents:'Genitori',partners:'Coniugi',portrait:'Fotografia'};
let api,context,selected,people=new Map(),relativeKind,needsPassword=false,busy=false;
const initialType=new URLSearchParams(location.hash.slice(1)).get('type');
needsPassword=['invite','recovery'].includes(initialType);
function status(text,error=false){$('family-status').textContent=text;$('family-status').classList.toggle('error',error);}
function message(error){
 if(error?.code==='40001')return 'La scheda è cambiata mentre la modificavi. Ricaricala prima di salvare.';
 if(error?.code==='42501')return 'L’accesso a questa scheda non è autorizzato. Il tuo referente può verificare i permessi.';
 if(error?.code==='P0001')return error.message;
 return 'Non è stato possibile completare l’operazione. Riprova dopo aver ricaricato i dati.';
}
async function rpc(name,args={}){const {data,error}=await api.rpc(name,args);if(error)throw error;return data;}
async function task(action){
 if(busy)return;busy=true;document.querySelectorAll('.family-workspace button[type=submit]').forEach(b=>b.disabled=true);
 try{await action();}catch(error){status(message(error),true);}finally{busy=false;document.querySelectorAll('.family-workspace button[type=submit]').forEach(b=>b.disabled=false);}
}
function option(value,text,chosen=false,disabled=false){const e=document.createElement('option');e.value=value;e.textContent=text;e.selected=chosen;e.disabled=disabled;return e;}
function names(ids){return (ids||[]).map(id=>people.get(id)?.name||id).join(', ');}
function renderList(){
 const query=$('person-filter').value.trim().toLocaleLowerCase('it'),root=$('branch-filter').value;
 let allowed=null;
 if(root){
  allowed=new Set([root]);let changed=true;
  while(changed){changed=false;for(const p of people.values())if(p.parents?.some(id=>allowed.has(id))&&!allowed.has(p.id)){allowed.add(p.id);changed=true;}}
  const descendants=[...allowed];for(const id of descendants)for(const partner of people.get(id)?.partners||[])allowed.add(partner);
 }
 const list=context.people.filter(p=>(!allowed||allowed.has(p.id))&&p.name.toLocaleLowerCase('it').includes(query));
 $('editable-people').replaceChildren();
 for(const p of list){const b=document.createElement('button');b.type='button';b.setAttribute('aria-pressed',String(selected?.id===p.id));b.textContent=p.name;
  if(p.birth){const small=document.createElement('small');small.textContent=p.birth;b.append(small);}b.addEventListener('click',()=>select(p.id));$('editable-people').append(b);}
 if(!list.length){const p=document.createElement('p');p.textContent='Nessuna scheda trovata.';$('editable-people').append(p);}
}
function select(id){
 selected=context.people.find(p=>p.id===id);if(!selected)return;
 $('choose-person').hidden=true;$('person-form').hidden=false;$('person-title').textContent=selected.name;$('person-version').textContent='SCHEDA DI FAMIGLIA';
 const img=$('person-portrait');img.hidden=Boolean(selected.portrait_missing);if(!img.hidden)img.src=selected.portrait_full||selected.portrait;
 for(const key of fields)$('person-form').elements[key].value=selected[key]||'';
 $('person-form').elements.photo.value='';
 for(const key of ['parents','partners']){
  const control=$('person-form').elements[key],current=selected[key]||[];control.replaceChildren();
  const options=new Map(context.people.filter(p=>p.id!==selected.id).map(p=>[p.id,p]));for(const id of current)if(people.has(id))options.set(id,people.get(id));
  for(const p of [...options.values()].sort((a,b)=>a.name.localeCompare(b.name,'it')))control.append(option(p.id,p.name,current.includes(p.id),!context.people.some(q=>q.id===p.id)));
 }
 renderList();
}
async function refresh(id=selected?.id){
 context=await rpc('family_context');const snapshot=await rpc('family_snapshot');people=new Map(snapshot.trees.flatMap(t=>t.people).map(p=>[p.id,p]));
 $('family-login').hidden=true;$('family-dashboard').hidden=false;$('password-setup').hidden=true;$('family-admin').hidden=!context.admin;
 const filter=$('branch-filter'),old=filter.value;filter.replaceChildren(option('','Tutti i rami assegnati'));for(const b of context.branches)filter.append(option(b.root_id,b.label));filter.value=old;
 if(!context.people.length){status('Il tuo account è attivo. L’amministratore deve ancora assegnarti un ramo familiare.');$('person-form').hidden=true;}
 else status('Puoi aggiornare le schede dei rami assegnati. Le modifiche vengono pubblicate subito.');
 if(context.admin){
  const root=$('grant-form').elements.root,oldRoot=root.value;root.replaceChildren();for(const p of context.people.filter(p=>p.tree_id==='discendenti').sort((a,b)=>a.name.localeCompare(b.name,'it')))root.append(option(p.id,p.name));if(oldRoot)root.value=oldRoot;updateBranchLabel();await renderAccesses();
 }
 renderList();if(id&&context.people.some(p=>p.id===id))select(id);else{selected=null;$('person-form').hidden=true;$('choose-person').hidden=false;}
}
async function renderAccesses(){
 const accesses=await rpc('family_accesses');$('family-access-list').replaceChildren();
 for(const a of accesses){const row=document.createElement('div');row.className='family-access-row';const text=document.createElement('div'),email=document.createElement('p'),label=document.createElement('small');email.textContent=a.email;label.textContent=a.label+(a.enabled?' · Accesso attivo':' · Accesso revocato');text.append(email,label);const b=document.createElement('button');b.type='button';b.textContent=a.enabled?'Revoca accesso':'Riattiva';b.addEventListener('click',()=>task(async()=>{await rpc('family_set_access',{p_email:a.email,p_root:a.root_id,p_label:a.label,p_enabled:!a.enabled});await renderAccesses();status(a.enabled?'Accesso revocato.':'Accesso riattivato.');}));row.append(text,b);$('family-access-list').append(row);}
}
function updateBranchLabel(){const f=$('grant-form');if(f.elements.root.selectedOptions[0])f.elements.label.value='Famiglia di '+f.elements.root.selectedOptions[0].textContent;}
function loginView(){context=null;selected=null;people.clear();$('family-dashboard').hidden=true;$('password-setup').hidden=true;$('family-login').hidden=false;status('Accedi con l’email autorizzata per aggiornare la tua famiglia.');}
async function image(file){
 if(!['image/jpeg','image/png','image/webp'].includes(file.type)||file.size>10*1024*1024)throw {code:'P0001',message:'Scegli una fotografia JPG, PNG o WebP fino a 10 MB.'};
 const {data:{user},error}=await api.auth.getUser();if(error||!user)throw {code:'42501'};
 const extension={'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[file.type],path=user.id+'/'+crypto.randomUUID()+'.'+extension;
 const result=await api.storage.from('family-portraits').upload(path,file,{contentType:file.type,upsert:false});if(result.error)throw result.error;
 return api.storage.from('family-portraits').getPublicUrl(path).data.publicUrl;
}
$('login-form').addEventListener('submit',e=>{e.preventDefault();task(async()=>{const f=e.currentTarget,email=f.elements.email.value.trim();const {error}=await api.auth.signInWithPassword({email,password:f.elements.password.value});f.elements.password.value='';if(error){status('Accesso non riuscito. Verifica email e password.',true);return;}await refresh();});});
$('logout').addEventListener('click',()=>task(async()=>{await api.auth.signOut();loginView();}));
$('recover-password').addEventListener('click',()=>task(async()=>{const email=$('login-form').elements.email.value.trim();if(!email){status('Indica prima il tuo indirizzo email.',true);return;}const {error}=await api.auth.resetPasswordForEmail(email,{redirectTo:new URL('area-famiglie.html',location.href).href});if(error)throw error;status('Se l’indirizzo è registrato, riceverai le istruzioni per impostare una nuova password.');}));
$('password-form').addEventListener('submit',e=>{e.preventDefault();const f=e.currentTarget;task(async()=>{if(f.elements.password.value!==f.elements.repeat.value){status('Le due password non coincidono.',true);return;}const {error}=await api.auth.updateUser({password:f.elements.password.value});if(error)throw error;f.reset();needsPassword=false;await refresh();});});
$('person-filter').addEventListener('input',()=>context&&renderList());$('branch-filter').addEventListener('change',()=>context&&renderList());
$('person-form').addEventListener('submit',e=>{e.preventDefault();const f=e.currentTarget;task(async()=>{
 const payload=Object.fromEntries(fields.map(key=>[key,f.elements[key].value.trim()]));const file=f.elements.photo.files[0];if(file)payload.portrait=await image(file);
 try{const saved=await rpc('family_save_person',{p_id:selected.id,p_fields:payload,p_parents:[...f.elements.parents.selectedOptions].map(o=>o.value),p_partners:[...f.elements.partners.selectedOptions].map(o=>o.value),p_revision:selected.revision});await refresh(saved.id);status('Modifiche salvate e pubblicate nella genealogia.');}
 catch(error){if(!error.code)status('Non ho ricevuto la conferma del salvataggio. Ricarica la scheda per verificarne lo stato.',true);else throw error;}
});});
function openRelative(kind){if(!selected)return;relativeKind=kind;$('relative-form').reset();$('relative-title').textContent=kind==='child'?'Aggiungi figlio o figlia':'Aggiungi coniuge';$('other-parent-field').hidden=kind!=='child';const other=$('relative-form').elements.other_parent;other.replaceChildren(option('','Non indicato'));for(const id of selected.partners||[])if(context.people.some(p=>p.id===id))other.append(option(id,people.get(id).name));$('relative-dialog').showModal();}
$('add-child').addEventListener('click',()=>openRelative('child'));$('add-partner').addEventListener('click',()=>openRelative('partner'));
$('relative-form').addEventListener('submit',e=>{e.preventDefault();const f=e.currentTarget;task(async()=>{const p=await rpc('family_add_relative',{p_anchor:selected.id,p_kind:relativeKind,p_fields:Object.fromEntries(['name','birth','birth_place'].map(k=>[k,f.elements[k].value.trim()])),p_other_parent:relativeKind==='child'?(f.elements.other_parent.value||null):null});$('relative-dialog').close();await refresh(p.id);status('Familiare aggiunto e pubblicato nella genealogia.');});});
$('show-history').addEventListener('click',()=>task(async()=>{
 const history=await rpc('family_history',{p_id:selected.id});$('history-content').replaceChildren();
 if(!history.length){const p=document.createElement('p');p.textContent='Questa scheda non ha ancora modifiche registrate.';$('history-content').append(p);}
 for(const h of history){const section=document.createElement('section');section.className='history-entry';const date=document.createElement('p');date.textContent=new Date(h.created_at).toLocaleString('it-IT')+' · '+(h.action==='create'?'Creazione':h.action==='restore'?'Ripristino':'Modifica');section.append(date);const dl=document.createElement('dl');
  for(const key of Object.keys(labels)){const before=h.before?.[key]||'',after=h.after?.[key]||'';if(JSON.stringify(before)===JSON.stringify(after))continue;const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=labels[key];dd.textContent=key==='portrait'?'Fotografia aggiornata':(Array.isArray(before)?names(before):before||'Non indicato')+' → '+(Array.isArray(after)?names(after):after||'Non indicato');dl.append(dt,dd);}section.append(dl);
  if(h.before){const b=document.createElement('button');b.type='button';b.textContent='Ripristina la versione precedente';b.addEventListener('click',()=>task(async()=>{const restored=await rpc('family_restore',{p_id:selected.id,p_history:h.id,p_revision:selected.revision});$('history-dialog').close();await refresh(restored.id);status('Versione precedente ripristinata e pubblicata.');}));section.append(b);}$('history-content').append(section);
 }$('history-dialog').showModal();
}));
document.querySelectorAll('[data-close]').forEach(b=>b.addEventListener('click',()=>$(b.dataset.close).close()));
$('grant-form').elements.root.addEventListener('change',updateBranchLabel);
$('grant-form').addEventListener('submit',e=>{e.preventDefault();const f=e.currentTarget;task(async()=>{const {data,error}=await api.functions.invoke('family-invite',{body:{email:f.elements.email.value.trim(),root_id:f.elements.root.value,label:f.elements.label.value.trim(),password:f.elements.password.value}});if(error)throw error;if(data?.error)throw {code:'P0001',message:data.error};await refresh();status('Password e ramo assegnati. Comunica personalmente le credenziali al referente.');f.elements.email.value='';f.elements.password.value='';});});
async function start(){
 try{
  const response=await fetch(new URL('family-access-config.json',location.href),{cache:'no-store'});if(!response.ok)throw new Error();const cfg=await response.json();
  if(!cfg.enabled){status('Gli accessi personali sono in preparazione. La genealogia pubblica resta consultabile.');return;}
  if(!/^https:\/\/[a-z0-9-]+\.supabase\.co$/.test(cfg.supabaseUrl)||!cfg.publishableKey)throw new Error();
  api=createClient(cfg.supabaseUrl,cfg.publishableKey,{auth:{persistSession:false,autoRefreshToken:true,detectSessionInUrl:true}});
  api.auth.onAuthStateChange(event=>{if(event==='PASSWORD_RECOVERY'){needsPassword=true;$('family-login').hidden=true;$('family-dashboard').hidden=true;$('password-setup').hidden=false;status('Scegli la tua nuova password personale.');}if(event==='SIGNED_OUT')loginView();});
  const {data:{session}}=await api.auth.getSession();
  if(session&&needsPassword){$('password-setup').hidden=false;status('Imposta la tua password personale per continuare.');}
  else if(session)await refresh();else loginView();
 }catch{status('L’area famiglie non è al momento disponibile. Riprova più tardi.',true);}
}
start();
