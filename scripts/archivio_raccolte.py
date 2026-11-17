"""Due indici compatti, anteprime sfogliabili e album completi, rigenerabili da build.py."""
from pathlib import Path
from html import escape
import json,re

def J(data): return escape(json.dumps(data,ensure_ascii=False,separators=(',',':')),quote=True)

def apply_collections(root):
    root=Path(root);dist=root/'dist'
    source=(dist/'media-gallery.html').read_text(encoding='utf-8')
    head=source[:source.index('<main id="contenuto">')]
    footer=source[source.index('</main>')+len('</main>'):]
    head=head.replace('</head>','<link rel="stylesheet" href="collections.css?v=2"><script src="collections.js?v=2" defer></script></head>')
    base='https://famiglia-martinelli.weebly.com'
    assets={x['url']:x['file'] for x in json.loads((root/'content/assets.json').read_text(encoding='utf-8'))}
    enhanced_path=root/'content/foto-guerra-originali.json'
    enhanced=json.loads(enhanced_path.read_text(encoding='utf-8')) if enhanced_path.exists() else {}
    groups=json.loads((root/'content/foto-capitoli.json').read_text(encoding='utf-8'))
    africa=json.loads((root/'content/africa-martinelli-timeline.json').read_text(encoding='utf-8'))
    collections=[]
    for g in groups:
        pics=[]
        for photo in g['images']:
            original=assets.get(photo['url'])
            if not original: continue
            improve=enhanced.get(photo['url'],{})
            pics.append(dict(src=improve.get('preview',original),full=improve.get('file',original),
                             caption=photo.get('caption') or g['title']))
        collections.append(dict(id=g['id'],title=g['title'],desc='Album originale della famiglia Martinelli',images=pics,
                                href='album-'+g['id']+'.html'))
    africa_images=[dict(src=p['path'],full=p['path'],caption=p['title']+' — '+p['caption']) for p in africa['entries']]
    collections.append(dict(id='africa',title='Africa · Da Verona a Gondar',desc='Fotografie familiari tra Verona e Gondar, con date da verificare.',images=africa_images,href='album-africa.html',more='africa-famiglia.html'))
    invito='assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg'
    wedding_paths=[('Le nozze di Annamaria ed Enrico','assets/africa-martinelli/05-matrimonio-anna-enrico.jpg'),
       ('Graziella paggetta','assets/africa-martinelli/06-matrimonio-graziella-paggetta.jpg'),
       ('La famiglia riunita','assets/africa-martinelli/07-matrimonio-gruppo.jpg'),
       ('Le due coppie di sposi','assets/africa-martinelli/08-matrimonio-due-coppie.jpg'),
       ('Giovanni, le figlie e i generi','assets/africa-martinelli/09-giovanni-figlie-generi.jpg'),
       ('Invito alle nozze · 1940',invito),
       ('Invito originale','assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-originale.jpg')]
    wedding=[dict(src=p,full=p,caption=t) for t,p in wedding_paths]
    collections.append(dict(id='matrimoni',title='Il matrimonio di Anna e Vera',desc='Fotografie delle due coppie, famiglia e invito di nozze.',images=wedding,href='album-matrimoni.html',more='matrimonio-anna-vera.html'))
    portrait_base='assets/famiglia-martinelli-storiche/'
    portraits=[dict(src=portrait_base+x+'-restaurata.jpg',full=portrait_base+x+'-restaurata.jpg',caption=t)
               for x,t in [('lina-diploma','Lina Masoni al diploma'),('giovanni-giovane-ufficiale','Giovanni giovane ufficiale'),('giovanni-con-padre','Giovanni con il padre')]]
    if all((dist/i['src']).is_file() for i in portraits):
        collections.append(dict(id='ritratti',title='Lina e Giovanni · Ritratti storici',desc='Tre ritratti restaurati con originali.',images=portraits,href='album-ritratti.html',more='ritratti-lina-giovanni.html'))
    else:
        collections.append(dict(id='ritratti',title='Lina e Giovanni · Ritratti storici',desc='Scheda già presente; le nuove fotografie originali e restaurate devono ancora essere caricate.',images=[],href='ritratti-lina-giovanni.html',cover='assets/1b8375d93e-enrico-calenda.jpg',missing=True))
    menu='<nav class="collection-tabs" aria-label="Sezioni dell’archivio"><a href="foto.html">Foto</a><a href="video.html">Video</a></nav>'
    def shell(title,subtitle,body,filename):
        h=head.replace('Foto e video · Famiglia Martinelli',escape(title)+' · Famiglia Martinelli')
        m='<main id="contenuto"><div class="collection-intro"><p class="eyebrow">L’ARCHIVIO DI FAMIGLIA</p><h1>'+escape(title)+'</h1><p>'+escape(subtitle)+'</p>'+menu+'</div><div class="collection-shell">'+body+'</div></main>'
        (dist/filename).write_text(h+m+footer,encoding='utf-8')
    def card(c):
        pics=c['images'];cover=pics[0]['src'] if pics else c.get('cover','assets/album/famiglia-martinelli.webp')
        slides=[dict(src=x['src'],caption=x['caption']) for x in pics]
        buttons=('''<button type="button" class="gallery-arrow prev" aria-label="Fotografia precedente">‹</button><button type="button" class="gallery-arrow next" aria-label="Fotografia successiva">›</button><span class="gallery-counter">1 / '''+str(len(slides))+'''</span>''') if len(slides)>1 else ''
        return '<article class="collection-card" id="raccolta-'+escape(c['id'])+'" data-items="'+J(slides)+'"><div class="collection-media"><img src="'+escape(cover,quote=True)+'" loading="lazy" alt="'+escape(c['title'],quote=True)+'">'+buttons+'</div><div class="collection-info"><h2>'+escape(c['title'])+'</h2><p>'+str(len(slides))+' fotografie'+(' · caricamento da completare' if c.get('missing') else '')+'</p><p class="collection-description">'+escape(c['desc'])+'</p><div class="collection-actions"><a href="'+escape(c['href'])+'">'+('Apri la scheda' if c.get('missing') else 'Apri la cartella')+' →</a>'+('<a class="secondary" href="'+escape(c['more'])+'">Approfondimento</a>' if c.get('more') else '')+'</div></div></article>'
    index='<nav class="collection-index" aria-label="Indice fotografico">'+''.join('<a href="#raccolta-'+escape(c['id'])+'">'+escape(c['title'])+'</a>' for c in collections)+'</nav>'
    shell('Foto','Scegli una raccolta: sfogliala direttamente nella scheda con le frecce, oppure apri l’album con tutte le miniature.',index+'<section class="collection-grid" aria-label="Cartelle delle fotografie">'+''.join(card(c) for c in collections)+'</section>','foto.html')

    for c in collections:
        if c.get('missing'):continue
        pictures=c['images']
        first=pictures[0]
        thumbs=''.join('<button type="button" data-slide="'+str(i)+'" aria-label="Mostra fotografia '+str(i+1)+'" aria-pressed="'+('true' if i==0 else 'false')+'"><img src="'+escape(x['src'],quote=True)+'" loading="lazy" alt=""><span>'+str(i+1)+'. '+escape(x['caption'][:50])+'</span></button>' for i,x in enumerate(pictures))
        viewer='<article class="full-album" data-items="'+J(pictures)+'"><div class="album-viewer"><div class="album-stage"><img src="'+escape(first['src'])+'" alt="'+escape(first['caption'])+'"><button class="prev" type="button" aria-label="Precedente">‹</button><button class="next" type="button" aria-label="Successiva">›</button></div><div class="album-copy"><p data-count>Fotografia 1 di '+str(len(pictures))+'</p><h2>'+escape(c['title'])+'</h2><p data-caption>'+escape(first['caption'])+'</p><p><a data-original href="'+escape(first['full'])+'" target="_blank" rel="noopener">Ingrandisci l’originale ↗</a></p><p>Seleziona una miniatura oppure usa le frecce per sfogliare.</p></div></div><h2 class="collection-heading">Tutte le fotografie · '+str(len(pictures))+'</h2><div class="album-thumbs">'+thumbs+'</div></article>'
        shell(c['title'],c['desc'],'<a class="collection-back" href="foto.html#raccolta-'+escape(c['id'])+'">← Torna a tutte le raccolte fotografiche</a>'+viewer,'album-'+c['id']+'.html')

    movies=[
     dict(title='Le origini e gli antenati',description='Dalle radici della casata alle generazioni di Giovanni e Lina.',slug='martinelli-origini-e-antenati'),
     dict(title='Giovanni e Lina — Un amore oltre la distanza',description='Cartoline, fotografie e diario dalla Grande Guerra al ritorno.',slug='giovanni-lina-un-amore-oltre-la-distanza'),
     dict(title='La storia della famiglia Martinelli',description='Il filmato originale dell’archivio di famiglia.',slug='famiglia-martinelli'),
     dict(title='La marmellata di Caprino',description='Un filmato conservato nell’archivio familiare.',slug='marmellata-di-caprino'),
     dict(title='Una giornata particolare',description='Un ricordo filmato dell’archivio di famiglia.',slug='una-giornata-particolare')
    ]
    links=[
     dict(title='Gondar, antica capitale etiopica',year='1936 · Archivio Luce',url='https://patrimonio.archivioluce.com/luce-web/detail/IL5000061569/2/gondar-antica-capitale-etiopica.html%26jsonVal%3D',description='Vedute della città prima dell’occupazione italiana.',poster='assets/africa-martinelli/02-gondar-carlo-enrico-1939.jpg'),
     dict(title='Governo dell’Amhara — Gondar',year='1937 · Archivio Luce',url='https://patrimonio.archivioluce.com/luce-web/detail/IL5000095912/2/-5818.html?startPage=0',description='Materiale di repertorio durante l’occupazione italiana.',poster='assets/africa-martinelli/08-matrimonio-due-coppie.jpg'),
     dict(title='Abyssinia — Gondar',year='1941 · Imperial War Museums',url='https://film.iwmcollections.org.uk/record/10175',description='Immagini della città nella fase successiva alla presenza italiana.',poster='assets/africa-martinelli/09-giovanni-figlie-generi.jpg')
    ]
    def video_card(c):
        pictures=c['images'];slides=[dict(src=x['src'],caption=x.get('caption','')) for x in pictures]
        return '<article class="collection-card" id="raccolta-'+c['id']+'" data-items="'+J(slides)+'"><div class="collection-media"><img src="'+escape(slides[0]['src'])+'" loading="lazy" alt="'+escape(c['title'])+'"><button type="button" class="gallery-arrow prev" aria-label="Precedente">‹</button><button type="button" class="gallery-arrow next" aria-label="Successivo">›</button><span class="gallery-counter">1 / '+str(len(slides))+'</span></div><div class="collection-info"><h2>'+escape(c['title'])+'</h2><p>'+escape(c['desc'])+'</p><div class="collection-actions"><a href="'+c['href']+'">Apri la cartella →</a></div></div></article>'
    videos=[
      dict(id='film-famiglia',title='I film della famiglia Martinelli',desc='Filmati originali del sito, riproducibili direttamente; 5 video.',href='video-famiglia.html',
           images=[dict(src='assets/media/'+m['slug']+'.jpg',caption=m['title']) for m in movies]),
      dict(id='gondar-storica',title='Gondar durante l’occupazione italiana in Africa',desc='Tre filmati storici presso Archivio Luce e Imperial War Museums.',href='video-gondar.html',
           images=[dict(src=x['poster'],caption=x['title']) for x in links])
    ]
    idx='<nav class="collection-index" aria-label="Indice video">'+''.join('<a href="#raccolta-'+v['id']+'">'+escape(v['title'])+'</a>' for v in videos)+'</nav>'
    shell('Video','Scegli una cartella di filmati. Usa le frecce sulle anteprime oppure apri la raccolta per vedere tutti i video e i collegamenti alle fonti.',idx+'<section class="collection-grid" aria-label="Cartelle video">'+''.join(video_card(v) for v in videos)+'</section>','video.html')
    movie_cards=[]
    for m in movies:
       base='assets/media/'+m['slug']
       movie_cards.append('<article class="video-gallery-card" id="'+escape(m['slug'])+'"><h2>'+escape(m['title'])+'</h2><p>'+escape(m['description'])+'</p><video controls preload="none" playsinline poster="'+base+'.jpg"><source src="'+base+'.mp4" type="video/mp4">Il tuo browser non supporta il video.</video><p><a href="'+base+'.mp4" download>Scarica MP4</a></p></article>')
    shell('I film della famiglia Martinelli','Tutti i film conservati nel sito, pronti per la riproduzione.','<a class="collection-back" href="video.html">← Torna alle cartelle video</a><nav class="collection-index">'+''.join('<a href="#'+escape(m['slug'])+'">'+escape(m['title'])+'</a>' for m in movies)+'</nav>'+''.join(movie_cards),'video-famiglia.html')
    link_cards=[]
    for i,l in enumerate(links,1):
       link_cards.append('<article class="video-gallery-card" id="repertorio-'+str(i)+'"><h2>'+escape(l['title'])+'</h2><p class="video-source">'+escape(l['year'])+'</p><p>'+escape(l['description'])+'</p><p><a href="'+escape(l['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">Apri il filmato nell’archivio che lo conserva ↗</a></p></article>')
    shell('Gondar durante l’occupazione italiana in Africa','Repertorio storico collegato agli archivi originali; i filmati non sono ripubblicati sul nostro sito.','<a class="collection-back" href="video.html">← Torna alle cartelle video</a><nav class="collection-index">'+''.join('<a href="#repertorio-'+str(i)+'">'+escape(l['title'])+'</a>' for i,l in enumerate(links,1))+'</nav>'+''.join(link_cards)+'<p>Nota: il primo filmato è precedente all’occupazione italiana di Gondar e il terzo è successivo. Per il riutilizzo delle riprese occorre verificare i diritti presso gli archivi.</p>','video-gondar.html')
    # Preserve existing media-gallery.html and its historic #foto-* anchors for old links.
    # Refresh the global menu after every generator has finished, including special pages.
    nav_items=[('index.html','Home'),('la-storia.html','La storia'),('documenti.html','Documenti'),('la-memoria.html','La memoria'),('genealogia.html','Genealogia'),('foto.html','Foto'),('video.html','Video'),('contribuisci.html','Contribuisci'),('contact.html','Contatti')]
    for file in dist.glob('*.html'):
        content=file.read_text(encoding='utf-8')
        current='foto.html' if file.name.startswith('album-') or file.name in ('foto.html','africa-famiglia.html','matrimonio-anna-vera.html','ritratti-lina-giovanni.html') else 'video.html' if file.name in ('video.html','video-famiglia.html','video-gondar.html') else file.name
        links_nav=''.join('<a '+('aria-current="page" ' if key==current else '')+'href="'+key+'">'+label+'</a>' for key,label in nav_items)
        content=re.sub(r'<nav class="site-nav" aria-label="Navigazione principale">.*?</nav>',lambda _: '<nav class="site-nav" aria-label="Navigazione principale">'+links_nav+'</nav>',content,count=1,flags=re.S)
        # No long list on the main menu; shortcuts to the new split pages stay visible in the legacy gallery.
        if file.name=='media-gallery.html':
            top='<div style="max-width:1120px;margin:15px auto;padding:16px 20px;background:#efe5d7;border-radius:12px"><strong>Nuova organizzazione dell’archivio:</strong> <a href="foto.html">Apri Foto e album</a> · <a href="video.html">Apri Video e filmati</a></div>'
            content=content.replace('<article class="page-content">',top+'<article class="page-content">',1)
        file.write_text(content,encoding='utf-8')
    print('Nuove pagine Foto e Video; album:',len(collections),' e filmati:',len(movies))

if __name__=='__main__':
    apply_collections(Path(__file__).resolve().parents[1])
