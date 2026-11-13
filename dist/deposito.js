'use strict';
document.querySelectorAll('[data-copy-email]').forEach(button=>button.addEventListener('click',async()=>{
 const status=button.closest('section').querySelector('.deposit-copy-status');
 try{await navigator.clipboard.writeText(button.dataset.copyEmail);status.textContent='Indirizzo copiato. Puoi incollarlo nel campo destinatario della tua email.';}catch{status.textContent='Seleziona e copia l’indirizzo mostrato qui sopra.';}
}));
