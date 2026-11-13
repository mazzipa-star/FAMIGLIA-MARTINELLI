"""Applica il template Album di famiglia alle pagine generate. Solo libreria standard."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import json,re
VERSION='album-20261113'
NAV=[('index.html','Home'),('la-storia.html','La storia'),('documenti.html','Documenti'),('la-memoria.html','La memoria'),('genealogia.html','Genealogia'),('media-gallery.html','Foto e video'),('contact.html','Contatti')]
def apply_album(root):
 root=Path(root);dist=root/'dist';assets=json.loads((root/'content/assets.json').read_text());lookup={a['url']:a['file'] for a in assets};galleries=json.loads((root/'content/galleries.json').read_text())
 def header(name):
  nav=''.join('<a '+('aria-current="page" ' if name==f else '')+'href="'+f+'">'+label+'</a>' for f,label in NAV)
  return '<header class="site-header"><div class="header-inner"><a class="brand" href="index.html"><img src="assets/album/stemma-martinelli.webp" width="1174" height="1340" alt=""><span class="brand-wordmark">Famiglia Martinelli<span class="brand-tagline">IL NOSTRO ALBUM DI FAMIGLIA</span></span></a><nav class="site-nav" aria-label="Navigazione principale">'+nav+'</nav></div></header>'
 def footer():
  return '<footer class="site-footer"><div><a class="footer-brand" href="index.html">Famiglia Martinelli</a><p>Custodire, ricordare, tramandare.</p></div><div class="footer-links"><a href="genealogia.html">Il nostro albero</a><a href="contact.html">Contatti</a><a href="https://famiglia-martinelli.weebly.com/" target="_blank" rel="noopener">Il sito originale ↗</a></div></footer>'
 current=(dist/'index.html').read_text();original=re.search(r'<article>(.*?)</article>',current,re.S).group(1);original=re.sub(r'<h2.*?</h2>','',original,flags=re.S,count=1)
 template=(root/'templates/home-album.html').read_text();portrait=lookup[galleries['media-gallery.html'][0]['url']]
 rows=[]
 for year,n in [('1914',1),('1915',0),('1916',0),('1919',0)]:
  item=galleries['cartoline-'+year+'.html'][n];url=lookup[item['url']];title='Le cartoline del '+year;caption=item.get('caption','');page='cartoline-'+year+'.html'
  rows.append('<article class="timeline-entry" id="ricordo-'+year+'"><div class="timeline-marker" aria-hidden="true"></div><a class="timeline-photo" href="'+page+'"><img src="'+escape(url)+'" loading="lazy" alt="Cartolina della raccolta '+year+', '+escape(caption)+'"><span class="photo-date">'+escape(caption)+'</span></a><div class="timeline-copy"><p class="timeline-year">'+year+'</p><h3>'+title+'</h3><p>Una pagina della corrispondenza di famiglia, da guardare e rileggere.</p><a class="text-link" href="'+page+'">Sfoglia la raccolta <span aria-hidden="true">↗</span></a></div></article>')
 template=template.replace('__TIMELINE__',''.join(rows)).replace('__PORTRAIT__',portrait).replace('__POSTCARD__',lookup[galleries['cartoline-1914.html'][1]['url']]).replace('__ORIGINAL_HOME__',original)
 for f in dist.glob('*.html'):
  html=f.read_text();html=re.sub(r'<header>.*?</header>',header(f.name),html,count=1,flags=re.S);html=re.sub(r'<footer>.*?</footer>',footer(),html,count=1,flags=re.S)
  html=html.replace('href="style.css"','href="style.css?v='+VERSION+'"').replace('</head>','<script src="album.js?v='+VERSION+'" defer></script><link rel="icon" href="assets/album/stemma-martinelli.webp" type="image/webp"></head>')
  if f.name=='index.html':
   html=re.sub(r'<main.*?</main>',lambda m:template,html,count=1,flags=re.S);html=html.replace('<body>','<body class="home-page">')
  else:
   html=html.replace('<body>','<body class="inside-page">')
   if f.name!='genealogia.html':
    html=html.replace('<article>','<article class="page-content">',1)
    match=re.search(r'<div class="page-heading">(.*?)</div>',html,re.S)
    if match:
     heading=match.group(0);heading=heading.replace('<p class="names">Vera, Mannina, Graziella, Sante</p>','<p class="page-caption">Una pagina dell’album di famiglia.</p>');html=html.replace(match.group(0),heading)
  f.write_text(html)
 print('Template Album di famiglia applicato a tutte le pagine.')
