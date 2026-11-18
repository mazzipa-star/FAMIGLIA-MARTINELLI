"""Build the family workspace. Disabled until the real backend is provisioned."""
import base64,json,re
from pathlib import Path

def apply_family_access(root):
 root=Path(root);config=json.loads((root/'content/family-access-config.json').read_text())
 enabled=config.get('enabled') is True;url=config.get('supabaseUrl','');key=config.get('publishableKey','')
 if enabled:
  if not re.fullmatch(r'https://[a-z0-9-]+\.supabase\.co',url):raise ValueError('Indirizzo del servizio famiglie non valido')
  valid=key.startswith('sb_publishable_')
  if key.count('.')==2:
   try:valid=json.loads(base64.urlsafe_b64decode(key.split('.')[1]+'==='))['role']=='anon'
   except (ValueError,KeyError):valid=False
  if not valid:raise ValueError('Configurare solo una chiave pubblica del servizio famiglie')
 public={'enabled':enabled,'supabaseUrl':url if enabled else '', 'publishableKey':key if enabled else ''}
 (root/'dist/family-access-config.json').write_text(json.dumps(public))
 p=root/'dist/genealogia.html';page=p.read_text()
 page=re.sub(r'genealogia.css\?v=[^"\s]+','genealogia.css?v=modifica-20261118',page)
 page=re.sub(r'genealogia.js\?v=[^"\s]+','genealogia.js?v=modifica-20261118',page)
 page=re.sub(r'ritratti.js\?v=[^"\s]+','ritratti.js?v=accessi-20261118',page)
 page=page.replace('Esplora l’albero oppure consulta le schede, una persona alla volta.','Usa i simboli + e − nelle schede per aprire e chiudere i rami. Puoi anche cercare una persona o consultare le schede.')
 if enabled:
  page=page.replace('class="genealogy"','class="genealogy" data-family-access="enabled"',1)
  page=page.replace('<button type="button" id="cards-mode" aria-pressed="false">Schede</button>','<button type="button" id="cards-mode" aria-pressed="false">Schede</button><a class="family-update-button" href="area-famiglie.html"><span aria-hidden="true">✎</span> Aggiorna famiglie</a>',1)
  page=page.replace('</head>','<script src="genealogia-live.js?v=20261118" defer></script></head>')
 p.write_text(page)
 prefix=page.split('<main',1)[0];footer=page.split('</main>',1)[1].split('<script',1)[0]
 prefix=prefix.replace('<title>Genealogia · Famiglia Martinelli</title>','<title>Area famiglie · Famiglia Martinelli</title>')
 prefix=re.sub(r'<script[^>]*src="(?:genealogia|ritratti|genealogia-live)\.js[^>]*></script>','',prefix)
 prefix=prefix.replace('</head>','<link rel="stylesheet" href="famiglie.css?v=20261118"><script src="famiglie.js?v=modifica-20261118" defer></script></head>')
 (root/'dist/area-famiglie.html').write_text(prefix+(root/'templates/area-famiglie.html').read_text()+footer+'</body></html>')
