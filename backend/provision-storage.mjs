import {createClient} from '@supabase/supabase-js';
const {SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY}=process.env;
if(!SUPABASE_URL||!SUPABASE_SERVICE_ROLE_KEY)throw Error('Configurare URL e chiave segreta solo nell’ambiente di amministrazione.');
const api=createClient(SUPABASE_URL,SUPABASE_SERVICE_ROLE_KEY,{auth:{persistSession:false,autoRefreshToken:false}});
const options={public:true,fileSizeLimit:10485760,allowedMimeTypes:['image/jpeg','image/png','image/webp']};
const existing=await api.storage.getBucket('family-portraits');
if(existing.error){if(String(existing.error.statusCode)!=='404')throw Error('Verifica archivio fotografie non riuscita.');const result=await api.storage.createBucket('family-portraits',options);if(result.error)throw Error('Creazione archivio fotografie non riuscita.');}
else if(!existing.data.public||Number(existing.data.file_size_limit)!==options.fileSizeLimit||JSON.stringify([...existing.data.allowed_mime_types||[]].sort())!==JSON.stringify([...options.allowedMimeTypes].sort()))throw Error('Archivio esistente con impostazioni differenti: verificare prima di modificarlo.');
console.log('Archivio fotografie pronto.');
