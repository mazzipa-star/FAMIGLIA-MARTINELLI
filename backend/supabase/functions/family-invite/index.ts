import {createClient} from 'npm:@supabase/supabase-js@2.119.1';

const site=Deno.env.get('FAMILY_SITE_URL')||'https://mazzipa-star.github.io/FAMIGLIA-MARTINELLI/area-famiglie.html';
const origin=new URL(site).origin;
Deno.serve(async request=>{
 const cors={'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Headers':'authorization, apikey, content-type, x-client-info','Access-Control-Allow-Methods':'POST, OPTIONS','Vary':'Origin','Content-Type':'application/json'};
 const reply=(status:number,data:unknown)=>new Response(JSON.stringify(data),{status,headers:cors});
 if(request.headers.get('origin')!==origin)return reply(403,{error:'Origine non autorizzata'});
 if(request.method==='OPTIONS')return new Response(null,{status:204,headers:cors});
 if(request.method!=='POST')return reply(405,{error:'Metodo non consentito'});
 const authorization=request.headers.get('authorization')||'';
 if(!authorization.startsWith('Bearer '))return reply(401,{error:'Accedi come amministratore'});
 const url=Deno.env.get('SUPABASE_URL')!,key=Deno.env.get('SUPABASE_ANON_KEY')!,secret=Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
 const caller=createClient(url,key,{global:{headers:{Authorization:authorization}},auth:{persistSession:false,autoRefreshToken:false}});
 const user=await caller.auth.getUser();if(user.error||!user.data.user)return reply(401,{error:'Accesso non valido'});
 const admin=await caller.rpc('family_is_admin');if(admin.error||admin.data!==true)return reply(403,{error:'Solo gli amministratori possono assegnare accessi'});
 try{
  const body=await request.json(),email=String(body.email||'').trim(),root=String(body.root_id||''),label=String(body.label||'').trim();
  if(email.length>254||!/^\S+@\S+\.\S+$/.test(email)||!root||!label||label.length>160)return reply(400,{error:'Controlla email e ramo familiare'});
  const password=String(body.password||'');
  if(password.length<12||password.length>128)return reply(400,{error:'La password deve contenere da 12 a 128 caratteri'});
  const context=await caller.rpc('family_context');if(context.error||!context.data.people.some((p:{id:string})=>p.id===root))return reply(400,{error:'Ramo non trovato'});
  const lookup=await caller.rpc('family_account',{p_email:email});
  if(lookup.error)return reply(503,{error:'Verifica account non riuscita'});
  if(lookup.data?.admin)return reply(403,{error:'Le password degli amministratori si modificano dal proprio account'});
  const trusted=createClient(url,secret,{auth:{persistSession:false,autoRefreshToken:false}});
  let target=lookup.data?.id,created=false;
  if(!target){
   const account=await trusted.auth.admin.createUser({email,password,email_confirm:true});
   if(account.error||!account.data.user)return reply(400,{error:'Account non creato. Verifica email e password.'});
   target=account.data.user.id;created=true;
  }
  const grant=await caller.rpc('family_set_access',{p_email:email,p_root:root,p_label:label,p_enabled:true});
  if(grant.error){if(created)await trusted.auth.admin.deleteUser(target);return reply(503,{error:'Accesso non assegnato. Riprova.'});}
  if(!created){
   const update=await trusted.auth.admin.updateUserById(target,{password,email_confirm:true});
   if(update.error)return reply(503,{error:'Ramo assegnato; password non aggiornata. Ripeti l’operazione.'});
  }
  return reply(200,{assigned:true});
 }catch{return reply(400,{error:'Richiesta non valida'});}
});
