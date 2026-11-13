"""Pubblica la lettura parziale del taccuino senza confonderla con un'edizione integrale."""
from pathlib import Path
from html import escape
import json,re

def apply_prigionia(root):
 root=Path(root);data=json.loads((root/'content/prigionia-trascrizione.json').read_text());page=root/'dist/diario-di-prigionia.html';s=page.read_text()
 options=''.join(f'<option value="{i}">{escape(r["id"])} · {escape(r["date"])}</option>' for i,r in enumerate(data))
 full=''
 for r in data:
  full+=f'<article id="testo-{escape(r["id"])}"><h3>{escape(r["id"])} · {escape(r["date"])}</h3><p>{escape(r["status"])}</p><p><a href="{escape(r["image"])}" target="_blank" rel="noopener">Apri la scansione originale ↗</a></p><div class="prison-transcript">{escape(r["text"])}</div><p>{escape(r["notes"])}</p></article>'
 template=(root/'templates/prigionia-lettore.html').read_text().replace('__OPTIONS__',options).replace('__FIRST_TEXT__',escape(data[0]['text'])).replace('__FIRST_NOTES__',escape(data[0]['notes'])).replace('__FULL_TEXT__',full).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
 s=re.sub(r'<section class="gallery".*?</section>','',s,flags=re.S)
 s=s.replace('Tocca una fotografia per ingrandirla. Puoi sfogliare la raccolta senza uscire dalla pagina.','')
 s=re.sub(r'Inserirò le pagine originali.*?mano a mano che le avrò trascritte\.?','',s,flags=re.S)
 s=s.replace('<article class="page-content">','<article class="page-content">'+template+'<h2>Il campo e i documenti di approfondimento</h2>',1)
 s=s.replace('</head>','<link rel="stylesheet" href="prigionia.css?v=20261113"></head>')
 s=s.replace('<p class="page-caption">Una pagina dell’album di famiglia.</p>','<p class="page-caption">Il manoscritto di Giovanni, con una trascrizione parziale da revisionare.</p>')
 page.write_text(s)
 print('Diario di prigionia:',len(data),'scansioni e letture parziali.')
