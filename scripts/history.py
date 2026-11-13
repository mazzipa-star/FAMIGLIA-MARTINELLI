"""Contesto documentato del diario: testo editoriale separato dalla fonte familiare."""
from pathlib import Path
import re

def apply_history(root):
 root=Path(root);p=root/'dist/diario-di-guerra.html';html=p.read_text()
 template=(root/'templates/diario-contesto.html').read_text()
 html=html.replace('<article class="page-content">','<article class="page-content diary-page">'+template,1)
 old=['006856926a-6644267.jpg','ca6586f7be-4847332.jpg','d2dd3a1d59-5470340.jpg','d3d8948a86-1031121.jpg','5369939e6c-3702436.jpg','422471e77a-5243458.jpg','8d143f9c38-5558907.jpg','7e9c4cb6db-5656636.jpg']
 for i,name in enumerate(old,1):
  html=html.replace('assets/'+name,'assets/diario/diario-guerra-'+str(i)+'.jpg')
  html=html.replace('<figure><a href="assets/diario/diario-guerra-'+str(i)+'.jpg">','<figure id="pagina-diario-'+str(i)+'"><a href="assets/diario/diario-guerra-'+str(i)+'.jpg">')
 css='''<style>
 .diary-page{max-width:1080px;margin-inline:auto}.diary-page section{scroll-margin-top:2rem}.diary-page h2{font-size:clamp(1.8rem,4vw,2.7rem);line-height:1.15}.diary-page h3{line-height:1.3}.diary-intro{padding:clamp(1.2rem,4vw,3rem);background:#eee5d7;border-radius:10px;margin-bottom:3rem}.diary-index{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.5rem}.diary-index a{padding:.5rem .9rem;border:1px solid #b6a38d;border-radius:30px;font-size:.95rem}.diary-context,.diary-days,.diary-sources{margin-block:3.5rem}.diary-note{border-left:3px solid #91694a;background:#efe8dc;padding:1rem 1.5rem;margin:1.7rem 0}.diary-note h3{margin-top:0}.diary-note p:last-child{margin-bottom:0}.diary-day{padding:1.3rem 0 1.7rem;border-top:1px solid #d6c8b5}.diary-day h3{font-size:1.5rem;margin:.5rem 0 1rem}.diary-comparison{display:grid;grid-template-columns:1fr 1fr;gap:2rem}.diary-comparison h4{font-family:inherit;text-transform:uppercase;letter-spacing:.1em;font-size:.75rem;color:#7d513b;margin:.5rem 0}.diary-comparison p{margin:.5rem 0}.diary-comparison>div+div{border-left:1px solid #d6c8b5;padding-left:1.5rem}.diary-key{font-style:italic}.diary-source-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.4rem;align-items:start}.history-photo,.diary-source-card{margin:0;background:#eee5d7;border-radius:8px;overflow:hidden}.history-photo img{display:block;width:100%;height:auto}.history-photo figcaption,.diary-source-card{padding:1.3rem}.history-photo figcaption,.diary-source-card p{font-size:.95rem;line-height:1.6}.source-kind{font-size:.7rem;letter-spacing:.12em;color:#7d513b}.diary-source-card h3{font-size:1.5rem}.diary-bibliography{padding-left:1.4rem;margin-top:2rem}.diary-bibliography li{padding:.65rem 0;scroll-margin-top:2rem;font-size:1rem;line-height:1.65}.diary-bibliography a,.diary-source-card a{overflow-wrap:anywhere}.diary-page .gallery figure{scroll-margin-top:1.5rem}.source-ref{font-size:.85em;white-space:nowrap}.diary-original-heading{border-top:1px solid #d6c8b5;padding-top:2rem}
 @media(max-width:680px){.diary-comparison,.diary-source-grid{grid-template-columns:1fr;gap:1rem}.diary-comparison>div+div{border-left:0;border-top:1px solid #d6c8b5;padding:1rem 0 0}.diary-index a{font-size:.85rem}.diary-note{padding:1rem}.diary-page p{overflow-wrap:break-word}}
 </style>'''
 html=html.replace('</head>',css+'</head>')
 html=html.replace('<p class="page-caption">Una pagina dell’album di famiglia.</p>','<p class="page-caption">Giovanni Martinelli · Val Miela e Melette · 15–22 novembre 1917</p>')
 p.write_text(html)
