"""Raccolta contributi: modulo esterno reale e alternativa email senza account Google."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse,urlencode,quote
import json,re

def apply_deposit(root):
 root=Path(root);dist=root/'dist';cfg=json.loads((root/'content/deposit-config.json').read_text());provider=cfg.get('provider','');url=cfg.get('form_url','').strip();enabled=cfg.get('enabled',False);email=cfg.get('contact_email','').strip()
 if email and not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+',email):raise ValueError('Indirizzo email del deposito non valido.')
 parsed=urlparse(url);valid=parsed.scheme=='https' and ((provider=='google' and ((parsed.hostname=='docs.google.com' and re.fullmatch(r'/forms/d/e/[A-Za-z0-9_-]+/viewform',parsed.path)) or (parsed.hostname=='forms.gle' and re.fullmatch(r'/[A-Za-z0-9]+',parsed.path)))) or (provider=='tally' and parsed.hostname=='tally.so' and re.fullmatch(r'/r/[A-Za-z0-9]+/?',parsed.path)) or (provider=='dropbox' and parsed.hostname in ('www.dropbox.com','dropbox.com') and parsed.path.startswith('/request/')))
 form_ready=bool(url and valid and cfg.get('notification_verified',False))
 if enabled and url and not valid:raise ValueError('Collegare un URL pubblico valido del modulo di deposito.')
 if enabled and url and not cfg.get('notification_verified',False):raise ValueError('Verificare le notifiche del modulo prima di pubblicarlo.')
 if enabled and not form_ready and not email:raise ValueError('Per pubblicare la pagina serve un modulo attivo o un indirizzo email.')
 if form_ready and provider=='google':
  primary='<p class="eyebrow">CON UN ACCOUNT GOOGLE</p><h3>Carica con Google.</h3><p>Compila il modulo e allega i materiali. I file vengono raccolti nel Drive dell’amministratore, che riceve una notifica per ogni nuovo invio.</p><p class="deposit-small">Per allegare file è necessario accedere al proprio account Google. Puoi allegare fino a 10 file per invio, da 10 MB ciascuno. Per file più grandi puoi indicare un collegamento nella descrizione.</p><a class="button primary" href="'+escape(url)+'" target="_blank" rel="noopener">Apri il modulo Google ↗</a>'
 elif form_ready:
  primary='<p class="eyebrow">DEPOSITO ONLINE</p><h3>Carica il materiale.</h3><p>Apri il modulo di raccolta per aggiungere descrizione e allegati. Il contributo sarà valutato prima della pubblicazione.</p><a class="button primary" href="'+escape(url)+'" target="_blank" rel="noopener">Apri il deposito ↗</a>'
 else:
  primary='<p class="eyebrow">CON UN ACCOUNT GOOGLE</p><h3>Carica con Google.</h3><p>Il collegamento al modulo Google è in preparazione. Per il momento puoi inviare i tuoi ricordi via email.</p><p class="deposit-status" role="status">Modulo Google non ancora attivo</p>'
 content='<div class="deposit-methods"><section class="deposit-method">'+primary+'</section>'
 if email:
  body='Nome e cognome:\n\nTitolo del ricordo:\n\nChe cosa contiene il materiale?\n(Persone, luoghi, episodio o storia)\n\nData o periodo, anche approssimativo:\n\nProvenienza del materiale e indicazioni per la condivisione:\n\nEventuale link a file di grandi dimensioni:\n\nPrima di inviare: aggiungi i file come allegati e conserva gli originali. Il materiale sarà valutato dall’amministratore prima della pubblicazione.'
  mailto='mailto:'+email+'?'+urlencode({'subject':'Un ricordo per l’album della famiglia Martinelli','body':body},quote_via=quote)
  content+='<section class="deposit-method email-method"><p class="eyebrow">ANCHE SENZA ACCOUNT GOOGLE</p><h3>Invia via email.</h3><p>Si apre il tuo programma di posta con destinatario, oggetto e una traccia del messaggio già pronti. Aggiungi i file come allegati e premi <strong>Invia</strong> nel programma di posta.</p><a class="button secondary" href="'+escape(mailto)+'">Scrivi un’email <span aria-hidden="true">↗</span></a><div class="deposit-address"><span>'+escape(email)+'</span><button type="button" data-copy-email="'+escape(email)+'">Copia indirizzo</button></div><p class="deposit-small">Se il pulsante non apre la posta, copia l’indirizzo e scrivi da Gmail o dal servizio che utilizzi. Se gli allegati sono troppo grandi, inserisci un collegamento per scaricarli.</p><p class="deposit-small">L’apertura del messaggio non invia nulla: il deposito arriva all’amministratore soltanto dopo che hai inviato l’email.</p><p class="deposit-copy-status" aria-live="polite"></p></section>'
 content+='</div><p class="deposit-service-note">I materiali inviati non vengono pubblicati automaticamente. L’amministratore li esamina prima di inserirli nell’album. Nome ed email servono a gestire il contributo e a chiedere eventuali chiarimenti.</p>'
 multiple='Sì. Via email puoi aggiungere più allegati. Per file troppo grandi rispetto ai limiti della tua posta, usa un collegamento per il download e indica nel messaggio che cosa contiene.'
 if form_ready:multiple+=' Nel modulo online puoi seguire i limiti di caricamento indicati dal servizio.'
 template=(root/'templates/contribuisci.html').read_text().replace('__DEPOSIT_SERVICE__',content).replace('__MULTIPLE_FILES_NOTE__',multiple)
 source=(dist/'index.html').read_text();header=re.search(r'<header.*?</header>',source,re.S).group(0);footer=re.search(r'<footer.*?</footer>',source,re.S).group(0);header=header.replace('aria-current="page" ','')
 head='<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Condividi fotografie, documenti e ricordi con l’album della famiglia Martinelli."><title>Contribuisci all’album · Famiglia Martinelli</title><link rel="stylesheet" href="style.css?v=contributi-20261113"><script src="deposito.js?v=20261113" defer></script><link rel="icon" href="assets/album/stemma-martinelli.webp" type="image/webp">'+('' if enabled else '<meta name="robots" content="noindex">')+'</head>'
 (dist/'contribuisci.html').write_text('<!doctype html><html lang="it">'+head+'<body class="inside-page"><a class="skip" href="#contenuto">Vai ai contenuti</a>'+header+template+footer+'</body></html>')
 if enabled:
  for p in dist.glob('*.html'):
   html=p.read_text();navlink='<a '+('aria-current="page" ' if p.name=='contribuisci.html' else '')+'href="contribuisci.html">Contribuisci</a>'
   html=html.replace('<a href="contact.html">Contatti</a></nav>',navlink+'<a href="contact.html">Contatti</a></nav>')
   html=html.replace('<div class="footer-links">','<div class="footer-links"><a href="contribuisci.html">Condividi un ricordo</a>')
   p.write_text(html)
 print('Contributi: email '+('attiva' if enabled and email else 'non attiva')+'; modulo '+('collegato' if form_ready else 'da collegare')+'.')
