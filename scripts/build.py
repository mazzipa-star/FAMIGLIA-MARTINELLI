from pathlib import Path
from html.parser import HTMLParser
from html import escape,unescape
from urllib.parse import urljoin,urlparse
import json,re,collections
R=Path(__file__).resolve().parents[1]; BASE='https://famiglia-martinelli.weebly.com'; pages=json.loads((R/'content/pages.json').read_text()); assets=json.loads((R/'content/assets.json').read_text()); galleries=json.loads((R/'content/galleries.json').read_text()); amap={a['url']:a['file'] for a in assets}
class N:
 def __init__(self,t='',a=()):self.t=t;self.a=dict(a);self.c=[]
class DOM(HTMLParser):
 def __init__(self):super().__init__();self.root=N();self.stack=[self.root];self.main=None
 def handle_starttag(self,t,a):
  n=N(t,a);self.stack[-1].c.append(n)
  if n.a.get('id')=='wsite-content':self.main=n
  if t not in ('img','br','hr','input','meta','link','source','embed','wbr'):self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].t==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].c.append(d)
def local(u):
 full=urljoin(BASE,u)
 if full in amap:return amap[full]
 p=urlparse(full)
 if p.netloc==urlparse(BASE).netloc and (p.path=='/' or p.path.endswith('.html')):return 'index.html' if p.path=='/' else p.path.lstrip('/')
 return full
external=set()
def render(n):
 if isinstance(n,str):return escape(n)
 t=n.t;a=n.a
 if t in ('script','style','form','input','button'):return ''
 inner=''.join(render(c) for c in n.c)
 if t=='img':return '<img loading="lazy" src="'+escape(local(a.get('src','')))+'" alt="'+escape(a.get('alt') or 'Fotografia dell’archivio familiare')+'">'
 if t=='a':
  if a.get('data-cfemail'):
   b=bytes.fromhex(a['data-cfemail']);mail=''.join(chr(x^b[0]) for x in b[1:]);return '<a href="mailto:'+escape(mail)+'">'+escape(mail)+'</a>'
  if not a.get('href'):return inner
  u=local(a['href'])
  if u.endswith('.pdf'):inner='Apri il documento PDF · '+escape(a['href'].split('/')[-1])
  if u.startswith('http') and not u.startswith(BASE):external.add(u)
  return '<a href="'+escape(u)+'">'+inner+'</a>'
 if t=='iframe':
  u=local(a.get('src',''));external.add(u);return '<p class="media-link"><a href="'+escape(u)+'" target="_blank" rel="noopener">Apri il video sul sito esterno ↗</a></p>'
 if t in ('h1','h2','h3','p','blockquote','strong','em','ul','ol','li','br','hr'):return '<'+t+'>'+inner+('' if t in ('br','hr') else '</'+t+'>')
 if t=='div' and 'paragraph' in a.get('class',''):return '<div class="paragraph">'+inner+'</div>'
 return inner
nav=[('index.html','Home'),('la-storia.html','La storia'),('documenti.html','Documenti'),('la-memoria.html','La memoria'),('genealogia.html','Genealogia'),('media-gallery.html','Media Gallery'),('contact.html','Contatti')]
rows=[]
for p in pages:
 name='index.html' if p['path']=='/' else p['path'].lstrip('/'); d=DOM();d.feed((R/'archive/pages'/name).read_text());body=render(d.main).replace('Your browser does not support viewing this document. Click ', '').replace(' to download the document.', ''); title=unescape(p['title'].split(' - ')[0]); title='Viaggio nella memoria' if name=='index.html' else title
 gal=galleries.get(name,[])
 if gal:
  body+='<section class="gallery" aria-label="Documenti digitalizzati">'+''.join('<figure><a href="'+escape(local(i['url']))+'"><img loading="lazy" src="'+escape(local(i['url']))+'" alt="'+escape(i.get('caption') or 'Documento digitalizzato')+'"></a><figcaption>'+escape(i.get('caption',''))+'</figcaption></figure>' for i in gal)+'</section>'
 hero=''
 if name=='index.html':
  photo=next(a['file'] for a in assets if 'famiglia_orig.jpg' in a['url']);hero='<figure class="hero-photo"><img src="'+photo+'" alt="Ritratto storico della famiglia"></figure>'
 menu=''.join('<a '+('aria-current="page" ' if name==f else '')+'href="'+f+'">'+l+'</a>' for f,l in nav)
 html='<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Archivio della famiglia Martinelli: storia, documenti, fotografie e ricordi."><title>'+escape(title)+' · Famiglia Martinelli</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#contenuto">Vai ai contenuti</a><header><a class="brand" href="index.html">Famiglia Martinelli<span>STORIE, VOLTI E MEMORIE</span></a><nav aria-label="Navigazione principale">'+menu+'</nav></header><main id="contenuto"><div class="page-heading"><p class="eyebrow">L’ARCHIVIO DI FAMIGLIA</p><h1>'+escape(title)+'</h1><p class="names">Vera, Mannina, Graziella, Sante</p></div>'+hero+'<article>'+body+'</article></main><footer><span>Famiglia Martinelli · Custodire, ricordare, tramandare.</span><a href="'+p['url']+'">Pagina originale ↗</a></footer></body></html>'
 (R/'dist'/name).write_text(html)
 text=DOM();text.feed('<div id="wsite-content">'+body+'</div>')
 (R/'content'/(name+'.txt')).write_text(re.sub('<[^>]+>',' ',body))
 imgs=[a for a in assets if a['url'].replace(BASE,'') in unescape((R/'archive/pages'/name).read_text()) or any(i['url']==a['url'] for i in gal)]
 rows.append('| ['+title+']('+p['url']+') | `'+name+'` | '+str(len(imgs))+' | '+str(len(gal))+' |')
(R/'content/external-links.json').write_text(json.dumps(sorted(external),indent=2))
counts=collections.Counter(a['type'].split(';')[0] for a in assets)
report='# Inventario di migrazione\n\nRilevazione: 12 novembre 2026. Origine: '+BASE+'/. Recupero in sola lettura delle pagine pubbliche raggiungibili dai collegamenti HTML.\n\n'+str(len(pages))+' pagine; '+str(len(assets))+' URL di risorse scaricate ('+str(len({a['sha256'] for a in assets}))+' file con contenuto distinto). Tipi: '+str(dict(counts))+'.\n\n| Pagina | Percorso conservato | Risorse referenziate | Immagini slideshow |\n|---|---|---:|---:|\n'+'\n'.join(rows)+'\n\n## File e testi\n\n`content/assets.json`: URL originale, percorso locale, dimensione, tipo e impronta SHA-256 di ciascun file. `content/pages.json`: testi integrali estratti e collegamenti delle pagine pubbliche, inclusa la navigazione originale. `content/*.html.txt`: contenuti del corpo della nuova pagina. `content/galleries.json`: ordine e didascalie originali delle presentazioni. `archive/pages/`: HTML originale per confronto; non destinato alla pubblicazione. `content/external-links.json`: riferimenti esterni da mantenere.\n\n## Limiti e verifiche richieste\n\n- La copia comprende il sito pubblico raggiungibile, non il pannello Weebly, bozze, pagine private o pagine non collegate. La completezza rispetto all’account richiede confronto con l’elenco pagine dell’editor e con un eventuale archivio esportato dall’account.\n- Le immagini sono quelle servite pubblicamente. Le scansioni degli slideshow dichiarano spesso una larghezza di 400 pixel: non equivalgono necessariamente agli originali ad alta risoluzione. Testi dentro fotografie e PDF restano nei documenti, senza trascrizioni inventate.\n- Sono preservate le didascalie, comprese eventuali incongruenze nelle date: ad esempio la raccolta 1914 contiene didascalie del 1915.\n- Il collegamento MyHeritage conduce a un servizio con accesso: gli alberi privati presenti nell’account non sono stati recuperati.\n- Vimeo e YouTube sono dipendenze esterne: sono conservati i link, non scaricati i video o le tracce audio. Disponibilità, permessi di download e originali vanno verificati con il titolare.\n- Aggiornamento del 13 novembre 2026: i due PDF genealogici sono anche consultabili in una pagina interattiva. I dati trascritti e i collegamenti sono in `content/genealogia.json`; i PDF originali restano invariati.\n- Nessun accesso a messaggi, contatti raccolti, statistiche o servizi lato server. Gli script Weebly, pubblicità e tracciamenti non sono trasferiti nella nuova versione.\n- Il recapito pubblico offuscato da Cloudflare è stato ricostruito per il collegamento email della pagina Contatti.\n- Non sono stati modificati dominio, DNS, sito Weebly o account GitHub. Prima della pubblicazione controllare i dati delle persone viventi e i diritti sulle fotografie. Nessuna licenza pubblica dei contenuti è presunta.\n- I vecchi percorsi sono conservati per agevolare la transizione; il reindirizzamento dal sottodominio Weebly non è sotto il controllo di questo progetto.\n'
(R/'INVENTARIO.md').write_text(report)
print(counts);print('Pagine generate:',len(pages));print('Errori recupero:',(R/'content/errors.json').read_text())

# Pagina interattiva: i dati sono incorporati per funzionare anche senza server.
genealogy_template=R/"templates/genealogia.html"
if genealogy_template.exists():
 data=(R/"content/genealogia.json").read_text()
 (R/"dist/genealogia.html").write_text(genealogy_template.read_text().replace("__GENEALOGY_DATA__",data.replace("</", "<\\/")))

from album import apply_album
apply_album(R)

from deposit import apply_deposit
apply_deposit(R)
