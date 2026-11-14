from pathlib import Path
import re

def apply_araldo(root):
 dist=Path(root)/'dist';s=(dist/'documenti.html').read_text()
 s=s.replace('<title>Documenti · Famiglia Martinelli</title>','<title>L’Araldo 1911 · Famiglia Martinelli</title>')
 start=s.index('<main id="contenuto">');end=s.index('</main>',start)+len('</main>')
 body='<main id="contenuto"><div class="page-heading"><p class="eyebrow">DOCUMENTI DELL’ARCHIVIO</p><h1>L’Araldo · 1911</h1><p>Almanacco nobiliare del Napoletano — estratto della famiglia Martinelli.</p><p><a href="documenti.html">← Torna ai Documenti</a> · <a href="assets/araldo-1911/araldo-1911-estratto-martinelli.pdf" target="_blank" rel="noopener">Apri il PDF completo</a> · <a href="assets/araldo-1911/araldo-1911-estratto-martinelli.pdf" download>Scarica il PDF</a></p></div><article class="page-content"><p>Il documento è conservato nella scansione originale. Tocca una pagina per aprirla a piena risoluzione e ingrandirla.</p><nav class="collection-years" aria-label="Pagine del documento">'+''.join('<a href="#pagina-'+str(i)+'">'+str(i)+'</a>' for i in range(1,7))+'</nav>'
 for i in range(1,7):
  path='assets/araldo-1911/pagina-'+str(i)+'.jpg'
  body+='<figure id="pagina-'+str(i)+'" style="margin:40px 0"><figcaption>Pagina '+str(i)+' di 6</figcaption><a href="'+path+'" target="_blank" rel="noopener" aria-label="Ingrandisci pagina '+str(i)+'"><img src="'+path+'" alt="L’Araldo 1911, pagina '+str(i)+' dell’estratto Martinelli" loading="lazy" style="display:block;width:100%;height:auto;max-height:none;object-fit:contain"></a><p><a href="#pagina-'+str(max(1,i-1))+'">← Precedente</a> · <a href="#pagina-'+str(min(6,i+1))+'">Successiva →</a></p></figure>'
 body+='</article></main>'
 (dist/'araldo-1911.html').write_text(s[:start]+body+s[end:])
