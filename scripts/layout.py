"""Immagini di apertura e capitoli coerenti per le pagine interne dell'album."""
from pathlib import Path
from html import escape
import json,re

def apply_layout(root):
 root=Path(root);dist=root/'dist'
 palace='assets/48d3299406-1927682799.jpg';letters='assets/8037f379e5-564509786.jpg';memory='assets/b44b29a45a-1568969512.jpg';camera='assets/46f93bc2df-1699293597.jpg';tree='assets/layout/albero-generazioni.webp';family='assets/album/famiglia-martinelli.webp';recorder='assets/278a001e82-registratore-a-bobine.jpg';writing='assets/74a7788a42-131511912-2794ded4-e6d5-4055-bd84-23ef5fb98a35.jpg';prison='assets/960bdf608a-3533534_orig.jpg';war='assets/62169b925c-9773419_orig.jpg';postcard='assets/57daa32a47-4810684_orig.jpg';crest='assets/album/stemma-martinelli.webp'
 config={
 'la-storia.html':(palace,'Palazzo Martinelli affacciato sul porto di Monopoli','Palazzo Martinelli · il porto di Monopoli','Le origini, i luoghi e i rami della famiglia.'),
 'documenti.html':(letters,'Una lettera dell’archivio familiare','Le carte conservano le nostre storie.','Cartoline e diari: le parole che attraversano il tempo.'),
 'la-memoria.html':(memory,'Fotografie dall’archivio della famiglia Martinelli','Volti, voci e ricordi di famiglia','Le voci dei protagonisti e i racconti da tramandare.'),
 'genealogia.html':(tree,'Un albero con radici, rami e cornici che evocano i legami tra generazioni','Radici e rami · illustrazione evocativa','Gli antenati e i discendenti di Giovanni Martinelli.'),
 'media-gallery.html':(camera,'Macchina fotografica e custodia, immagine della raccolta originale','Le immagini diventano memoria.','Fotografie e filmati, organizzati nei capitoli dell’album.'),
 'gli-audio.html':(recorder,'Registratore a bobine','Le voci dell’archivio','Ascoltare i ricordi, ritrovare le persone.'),
 'diario-di-guerra.html':(war,'Il documento del diario di guerra di Giovanni Martinelli','Il diario di Giovanni · novembre 1917','Le pagine, i luoghi e il contesto della guerra.'),
 'diario-di-prigionia.html':('assets/prigionia/pdf02.jpg','Due pagine del taccuino di prigionia','Il taccuino di Giovanni · 1918','Il manoscritto e la sua lettura parziale.'),
 'contact.html':(letters,'Una lettera dell’archivio familiare','Una storia che continua nel dialogo','Per informazioni e ricordi sulla famiglia Martinelli.'),
 'contribuisci.html':(family,'Fotografia della famiglia Martinelli','Ogni ricordo aggiunge una pagina.','Una fotografia, una lettera, una voce di famiglia.')}
 for name in ('cartoline-1914.html','cartoline-1915.html','cartoline-1916.html','cartoline-1919.html','cartoline-varie.html'):
  config[name]=(letters,'Cartolina dell’archivio familiare','Le parole di Giovanni e Lina','Cartoline da sfogliare, ingrandire e leggere.')
 def feature(title,img,alt,body,href,label):
  return '<section class="archive-feature"><a class="archive-feature-image" href="'+href+'"><img src="'+img+'" alt="'+alt+'" loading="lazy"></a><div class="archive-feature-copy"><h2 class="feature-title">'+title+'</h2><div>'+body+'</div><a class="text-link" href="'+href+'">'+label+' <span aria-hidden="true">→</span></a></div></section>'
 for name,(img,alt,caption,lead) in config.items():
  p=dist/name
  if not p.exists():continue
  s=p.read_text()
  if name=='documenti.html':
   body=feature('Cartoline',postcard,'Cartolina della Croce Rossa indirizzata a Giovanni Martinelli','<p>Raccolta di cartoline scritte da Giovanni Martinelli a Lina Masoni tra il 1914 e il 1919. Una storia d’amore d’altri tempi, raccontata attraverso parole scritte di getto all’amata lontana.</p><nav class="collection-years" aria-label="Raccolte di cartoline">'+''.join('<a href="cartoline-'+y+'.html">'+('Varie' if y=='varie' else y)+'</a>' for y in ['1914','1915','1916','1919','varie'])+'</nav>','cartoline-1914.html','Leggi le cartoline')
   body+=feature('Diario di prigionia',prison,'Un documento della prigionia di Giovanni Martinelli','<p>Il taccuino della prigionia di Giovanni, con le scansioni, la trascrizione parziale e fotografie del campo.</p>','diario-di-prigionia.html','Apri il diario')
   body+=feature('Diario di guerra',war,'Il diario di guerra manoscritto','<p>Gli avvenimenti dal 15 al 22 novembre 1917: le pagine originali e il contesto storico sulle Melette.</p>','diario-di-guerra.html','Apri il diario')
   body+=feature('Giovanni Martinelli · Medaglia d’argento','assets/medaglia-giovanni/medaglia.svg','Icona illustrativa di una medaglia d’argento al valor militare','<p>La motivazione per l’azione a Meletta Davanti del 17 novembre 1917, quando Giovanni era capitano del 129° reggimento fanteria.</p>','medaglia-argento-giovanni.html','Leggi la motivazione')
   body+=feature('Giovanni Martinelli · Atto di nascita','assets/atto-nascita-giovanni/atto-405.png','Atto di nascita numero 405 di Giovanni Martinelli, Monopoli, 1882','<p>Nato il 23 giugno 1882; dichiarazione registrata il 25 giugno. Il documento originale e il riferimento al registro dello Stato civile.</p>','atto-nascita-giovanni.html','Consulta l’atto')
   body+=feature('L’Araldo · 1911','assets/araldo-1911/pagina-1.jpg','Frontespizio de L’Araldo, almanacco nobiliare del Napoletano, 1911','<p>L’estratto dedicato alla famiglia Martinelli: sei pagine da sfogliare e ingrandire, con lo stemma e le notizie genealogiche dell’epoca.</p>','araldo-1911.html','Sfoglia il documento')
   s=re.sub(r'<article class="page-content">.*?</article>',lambda m:'<article class="page-content feature-list">'+body+'</article>',s,flags=re.S,count=1)
  if name=='la-memoria.html':
   body=feature('Le testimonianze audio',recorder,'Registratore a bobine, simbolo delle testimonianze audio','<p>La storia della famiglia Martinelli raccontata dai protagonisti: un archivio di voci da riascoltare.</p>','gli-audio.html','Ascolta le testimonianze')
   body+=feature('Racconti ed aneddoti',writing,'Una penna scrive a mano su un foglio','<p>Ricordi, episodi e parole di famiglia: un patrimonio che merita di essere tramandato, organizzato e custodito.</p>','contribuisci.html','Condividi un racconto')
   # Conserva il collegamento ai racconti già presente nella pagina originale.
   old=re.findall(r'<a href="([^"]+)">\s*vai\s*</a>',s,re.I)
   if old and old[-1] not in ('javascript:;','#'):body=body.replace('contribuisci.html',old[-1]).replace('Condividi un racconto','Leggi i racconti')
   s=re.sub(r'<article class="page-content">.*?</article>',lambda m:'<article class="page-content feature-list">'+body+'</article>',s,flags=re.S,count=1)
  if name=='media-gallery.html':
   video=re.search(r'<video\b.*?</video>',s,re.S).group(0);video=video.replace('<video ','<video id="family-film" hidden ',1)
   start=s.index('<article class="page-content">')+len('<article class="page-content">');end=s.index('<div id="capitoli-foto">',start)
   archive='<section class="album-video" aria-labelledby="video-title"><h2 class="feature-title" id="video-title">Video</h2><p>La storia della famiglia Martinelli di Monopoli, dalle origini fino ai giorni nostri, raccontata attraverso le immagini.</p><button class="family-play" id="start-family-film" type="button" aria-controls="family-film" aria-label="Avvia il video della famiglia Martinelli"><img src="'+family+'" alt="La famiglia Martinelli"><span class="play-disc" aria-hidden="true">▶</span><span class="play-label">Guarda il filmato</span></button><div class="family-film-wrap">'+video+'</div><p><a href="assets/media/famiglia-martinelli.mp4" download>Scarica il filmato MP4</a></p></section><section class="album-photo-intro" aria-labelledby="photos-title"><div><p class="eyebrow">I CAPITOLI DELL’ALBUM</p><h2 class="feature-title" id="photos-title">Foto</h2><p>Dai bisnonni alle famiglie di oggi. Le raccolte mantengono la suddivisione e l’ordine del sito originale.</p></div><img src="'+memory+'" alt="Fotografie dall’album di famiglia" loading="lazy"></section>'
   film='<section class="album-video" aria-labelledby="video-title"><h2 class="feature-title" id="video-title">Video</h2><article class="family-film-card" id="giovanni-lina"><p class="eyebrow">1914–1919 · 5 minuti e 23 secondi</p><h3>Giovanni e Lina — Un amore oltre la distanza</h3><p>Le cartoline, le fotografie e il diario raccontano un amore attraverso gli anni della guerra e della lontananza, fino alla nascita di Anna Maria e al ritorno.</p><video controls playsinline preload="none" poster="assets/media/giovanni-lina-un-amore-oltre-la-distanza.jpg" aria-label="Giovanni e Lina — Un amore oltre la distanza"><source src="assets/media/giovanni-lina-un-amore-oltre-la-distanza.mp4?v=crediti-20261114" type="video/mp4">Il browser non supporta la riproduzione del video. <a href="assets/media/giovanni-lina-un-amore-oltre-la-distanza.mp4?v=crediti-20261114">Apri il filmato</a>.</video><p><a href="assets/media/giovanni-lina-un-amore-oltre-la-distanza.mp4?v=crediti-20261114" download>Scarica il filmato MP4</a></p></article></section>'
   film=film.replace('<article class="family-film-card" id="giovanni-lina">','<article class="family-film-card" id="origini-antenati"><p class="eyebrow">Le origini e gli antenati · 4 minuti e 16 secondi</p><h3>La famiglia Martinelli — Le origini e gli antenati</h3><p>Lo stemma animato apre un viaggio dalle radici a Mola ai commerci e ai luoghi di Monopoli, fino ai ritratti degli antenati, di Giovanni e di Lina. Con timeline storica, fotografie dei luoghi e crediti finali.</p><video controls playsinline preload="none" poster="assets/media/martinelli-origini-e-antenati.jpg" aria-label="La famiglia Martinelli — Le origini e gli antenati"><source src="assets/media/martinelli-origini-e-antenati.mp4" type="video/mp4">Il browser non supporta la riproduzione del video. <a href="assets/media/martinelli-origini-e-antenati.mp4">Apri il filmato</a>.</video><p><a href="assets/media/martinelli-origini-e-antenati.mp4" download>Scarica il filmato MP4</a></p></article>'+'<article class="family-film-card" id="giovanni-lina">',1)
   split=archive.index('<section class="album-photo-intro"')
   original=archive[:split].replace('<h2 class="feature-title" id="video-title">Video</h2>','<h3>Il filmato originale della famiglia</h3>').replace(' aria-labelledby="video-title"','')
   content=film+'<details class="archive-film"><summary>Il filmato originale dell’archivio</summary>'+original+'</details>'+archive[split:]
   s=s[:start]+content+s[end:];s=s.replace('</head>','<script src="layout.js?v=20261113" defer></script></head>')
  if name=='la-storia.html':
   s=s.replace('<h2>La storia della famiglia</h2>','')
   for label in ('La casata','Il Patriziato di Salerno','Panorama storico'):s=s.replace('<div class="paragraph">'+label+'</div>','<h2>'+label+'</h2>')
  if name=='genealogia.html':s=s.replace('<h1>La famiglia, da vicino.</h1>','<h1>Genealogia</h1>')
  if name=='contact.html':s=s.replace('<h1>Contact</h1>','<h1>Contatti</h1>').replace('<div class="paragraph">Contact</div>','')
  match=re.search(r'<div class="page-heading">(.*?)</div>',s,re.S)
  if match:
   copy=match[1];copy=copy.replace('Una pagina dell’album di famiglia.',lead)
   hero='<div class="page-heading visual-heading"><div class="visual-heading-copy">'+copy+'</div><figure class="visual-heading-image"><img src="'+img+'" alt="'+alt+'" fetchpriority="high"><figcaption>'+caption+'</figcaption></figure></div>'
   s=s[:match.start()]+hero+s[match.end():]
  # Un richiamo visivo per i sottocapitoli; le schede con immagine propria non vengono duplicate.
  groups=json.loads((root/'content/foto-capitoli.json').read_text());assets={x['url']:x['file'] for x in json.loads((root/'content/assets.json').read_text())};chapter_images={g['title']:assets[g['images'][0]['url']] for g in groups}
  def chapter(m):
   attrs,title=m.group(1),m.group(2)
   if 'feature-title' in attrs:return m[0]
   plain=re.sub('<[^>]+>','',title).strip();art=chapter_images.get(plain,img)
   if any(t in plain.lower() for t in ('antenati','casata','patriziato')):art=crest
   if 'origini' in plain.lower():art=palace
   if 'trascrizion' in plain.lower() or 'lettura' in plain.lower():art=writing
   if 'fotograf' in plain.lower() and 'campo' in plain.lower():art='assets/campo/comando-anteprima.jpg'
   return '<h2'+attrs+' class="chapter-heading">'+title+'<span class="chapter-art" aria-hidden="true"><img loading="lazy" src="'+art+'" alt=""></span></h2>' if 'class=' not in attrs else '<h2'+attrs+'>'+title+'<span class="chapter-art" aria-hidden="true"><img loading="lazy" src="'+art+'" alt=""></span></h2>'
  s=re.sub(r'<h2([^>]*)>(.*?)</h2>',chapter,s,flags=re.S)
  s=s.replace('</head>','<link rel="stylesheet" href="layout.css?v=20261114-video"></head>');p.write_text('\n'.join(line.rstrip() for line in s.split('\n')))
 print('Layout visivo applicato alle',len(config),'pagine interne; home conservata.')
