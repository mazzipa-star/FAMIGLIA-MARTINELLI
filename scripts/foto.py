"""Ripristina le otto raccolte fotografiche e l'ordine del sito Weebly."""
from pathlib import Path
from html import escape,unescape
import json,re

def apply_foto(root):
 root=Path(root);page=root/'dist/media-gallery.html';s=page.read_text();groups=json.loads((root/'content/foto-capitoli.json').read_text());assets={x['url']:x['file'] for x in json.loads((root/'content/assets.json').read_text())};enhanced_path=root/'content/foto-guerra-originali.json';enhanced=json.loads(enhanced_path.read_text()) if enhanced_path.exists() else {}
 nav='<nav class="photo-chapters" aria-label="Capitoli fotografici"><p>Scegli un capitolo</p>'+''.join(f'<a href="#foto-{g["id"]}">{escape(g["title"])}</a>' for g in groups)+'</nav>'
 descriptions={'bisnonni':'Sante Martinelli, Carola Antonelli, Amedeo Masoni, Emilia Conti.','nonni':'Giovanni Martinelli e Lina Masoni.','giovanni':'Foto di famiglia di Giovanni Martinelli, Lina Masoni e i figli Annamaria, Vera, Sante e Graziella.','sante':'Foto di famiglia di Sante Martinelli, Ines, i figli Roberto, Enrico e Piergiovanni (Pigi) e nipoti.','anna':'Foto di famiglia di Anna Martinelli (Mannina), Enrico Calenda, Mario Tortora, i figli Maria Pia, Stefano, Marcello, Andrea e nipoti.','vera':'Foto di famiglia di Vera Martinelli, Carlo Martucci, le figlie Patrizia (Pucci), Rossella, Susanna e nipoti.','graziella':'Foto di famiglia di Graziella Martinelli, Eros Mazzi, i figli Stefano, Paolo, Alberto e nipoti.'}
 sections=[]
 for g in groups:
  figs=[]
  for i,x in enumerate(g['images']):
   old=assets[x['url']];new=enhanced.get(x['url'],{});full=new.get('file',old);thumb=new.get('preview',old);caption=unescape(x.get('caption',''));alt=caption or f'{g["title"]} · fotografia {i+1}'
   extra=''
   if new:extra=f'<p class="photo-original"><a href="{escape(old)}" target="_blank" rel="noopener">Versione del vecchio sito ↗</a></p>'
   figs.append(f'<figure><a href="{escape(full)}"><img loading="lazy" src="{escape(thumb)}" alt="{escape(alt)}"></a><figcaption><span class="photo-label">{escape(caption) if caption else escape(alt)}</span>{extra}</figcaption></figure>')
  note='<p>Album fotografico di Giovanni Martinelli durante la prima guerra mondiale. Le scansioni originali disponibili sostituiscono le piccole copie del vecchio sito; puoi ingrandirle per osservare i dettagli. Sono conservati anche i collegamenti alle versioni precedenti.</p>' if g['id']=='guerra' else '<p>'+escape(descriptions[g['id']])+'</p>'
  sections.append(f'<section class="photo-chapter" id="foto-{g["id"]}" aria-labelledby="titolo-{g["id"]}"><header><h2 id="titolo-{g["id"]}">{escape(g["title"])}</h2><p>{len(g["images"])} fotografie · ordine della raccolta originale</p>{note}</header><div class="gallery" aria-label="{escape(g["title"])}">'+''.join(figs)+'</div><p><a href="#capitoli-foto">Torna ai capitoli ↑</a></p></section>')
 # Conserva il filmato e la sua descrizione, sostituisce la sequenza di titoli scollegati e la galleria unica.
 start=s.index('<h2>I bisnonni</h2>');end=s.index('</article>',start)
 s=s[:start]+'<div id="capitoli-foto">'+nav+'</div>'+''.join(sections)+s[end:]
 css='<style>.photo-chapters{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.5rem 0 3rem;padding:1.2rem;background:#eae0ce;border-radius:12px}.photo-chapters p{flex-basis:100%;margin:0;font-weight:600}.photo-chapters a{padding:.5rem .8rem;background:#fffaf0;border:1px solid #ccbda6;border-radius:6px}.photo-chapter{padding-top:1.5rem;margin-bottom:4rem;border-top:1px solid #cfbea5;scroll-margin-top:2rem}.photo-chapter header>p{color:#655749}.photo-chapter .gallery img{object-fit:contain;background:#e8e0d3}.photo-original{font-size:.8rem;margin:.6rem 0 0}.photo-chapter figcaption{overflow-wrap:anywhere}</style>'
 s=re.sub(r'album\.js\?v=[^\"]+', 'album.js?v=capitoli-20261113', s)
 s=s.replace('<title>Media Gallery', '<title>Foto e video').replace('<h1>Media Gallery</h1>', '<h1>Foto e video</h1>')
 s=s.replace('</head>',css+'</head>');page.write_text(s)
 print('Foto: ripristinati',len(groups),'capitoli e',sum(len(g['images']) for g in groups),'fotografie.')
