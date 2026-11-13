"""Scansioni e letture delle cartoline, conservando raccolte e sequenza originali."""
from pathlib import Path
from html import escape,unescape
import json,re

def apply_cartoline(root):
 root=Path(root);source=root/'content/cartoline-lettura.json'
 if not source.exists():return
 collections=json.loads(source.read_text());nav='<nav class="postcard-collections" aria-label="Raccolte di cartoline">'+''.join(f'<a href="{escape(k)}">{escape(k.removesuffix(".html").replace("-"," ").capitalize())}</a>' for k in collections)+'</nav>'
 for name,rows in collections.items():
  p=root/'dist'/name;s=p.read_text();opts=''.join(f'<option value="{i}">{i+1} · {escape(r["caption"] or "Senza didascalia")}</option>' for i,r in enumerate(rows));r=rows[0]
  intro='<p>Consulta le scansioni ingrandite e la lettura del testo. Le trascrizioni recuperate dai documenti familiari sono indicate come tali; le letture recuperate automaticamente dal testo dattiloscritto nelle scansioni sono bozze da verificare. Non costituiscono una nuova edizione critica del manoscritto. Date, nomi e parole dubbie restano da controllare sugli originali.</p>'
  download='<p><a href="assets/cartoline/'+name.removesuffix('.html')+'-trascrizioni.md" download>Scarica le trascrizioni della raccolta</a></p>'
  reader=f'''{nav}{intro}{download}<section class="postcard-reader" id="lettore-cartoline" aria-label="Lettore delle cartoline"><h2>Leggi una cartolina</h2><div class="postcard-controls"><button id="card-prev" type="button">← Precedente</button><label for="card-select">Cartolina</label><select id="card-select">{opts}</select><button id="card-next" type="button">Successiva →</button><span id="card-count" aria-live="polite"></span></div><div class="postcard-columns"><div class="postcard-scan"><div class="postcard-controls"><label for="card-zoom">Zoom</label><input type="range" min="100" max="500" step="25" value="100" id="card-zoom"><output id="card-zoom-value">100%</output><button id="card-fit" type="button">Adatta</button></div><div class="postcard-frame" id="card-frame"><img id="card-image" src="{escape(r['preview'])}" alt="Cartolina"></div><p><a id="card-full" href="{escape(r['image'])}" target="_blank" rel="noopener">Apri la scansione a piena risoluzione ↗</a></p><p class="postcard-notes">Aumenta lo zoom e scorri l’immagine nelle due direzioni. Il file a piena risoluzione si apre separatamente.</p><a id="card-old" href="{escape(r['old'])}" target="_blank" rel="noopener">Copia del vecchio sito ↗</a></div><div class="postcard-reading"><h3 id="card-title">{escape(r['caption'])}</h3><p id="card-status" class="postcard-status"></p><div id="card-text" class="postcard-text"></div><p id="card-note" class="postcard-notes"></p></div></div></section>'''
  thumbs='<h2>Sfoglia la raccolta</h2><div class="postcard-thumbnails">'+''.join(f'<figure><a href="#cartolina-{i+1}" data-card-index="{i}"><img loading="lazy" src="{escape(r["thumbnail"])}" alt="{escape(r["caption"] or "Cartolina "+str(i+1))}"></a><figcaption>{i+1} · {escape(r["caption"] or "Senza didascalia")}</figcaption></figure>' for i,r in enumerate(rows))+'</div>'
  fallback='<noscript><h2>Trascrizioni disponibili</h2>'+''.join('<article><h3>'+escape(r['caption'] or 'Cartolina '+str(i+1))+'</h3><p>'+escape(r['status'])+'</p><div class="postcard-text">'+escape(r['text'])+'</div><a href="'+escape(r['image'])+'">Apri la scansione</a></article>' for i,r in enumerate(rows))+'</noscript>'
  s=re.sub(r'<section class="gallery".*?</section>',lambda m:reader+thumbs+fallback,s,flags=re.S)
  s=s.replace('<body','<body class="postcard-page"',1) if '<body>' in s else s.replace('<body class="','<body class="postcard-page ',1)
  s=s.replace('</head>','<link rel="stylesheet" href="cartoline.css?v=20261113"><script src="cartoline.js?v=20261113" defer></script></head>')
  s=s.replace('</body>','<script id="postcard-data" type="application/json">'+json.dumps(rows,ensure_ascii=False).replace('</','<\\/')+'</script></body>');p.write_text('\n'.join(line.rstrip() for line in s.split('\n')))
 print('Cartoline: lettore e trascrizioni per',sum(map(len,collections.values())),'immagini.')
