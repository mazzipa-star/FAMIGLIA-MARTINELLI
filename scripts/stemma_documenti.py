"""Scheda dello stemma familiare, rigenerabile dalla pagina Documenti."""
from pathlib import Path

def apply_stemma_documenti(root):
    root=Path(root)
    dist=root/"dist"
    path=dist/"documenti.html"
    source=path.read_text(encoding="utf-8")
    img="assets/stemma-casata/stemma-restaurato.png"
    feature=('''<section class="archive-feature" id="stemma-casata"><a class="archive-feature-image" href="stemma-casata.html"><img src="'''+img+'''" alt="Stemma della casata Martinelli, con la fenice, il sole e le spade incrociate" loading="lazy" style="width:100%;height:auto;max-height:340px;object-fit:contain"></a><div class="archive-feature-copy"><h2 class="feature-title">Lo stemma della casata Martinelli</h2><div><p>Lo stemma e una sintesi delle vicende della famiglia, dai rami di Mola e Monopoli al ramo napoletano, con la descrizione araldica e il rimando all’estratto de <em>L’Araldo</em> del 1911.</p></div><a class="text-link" href="stemma-casata.html">Esamina lo stemma e la storia <span aria-hidden="true">→</span></a></div></section>''')
    if 'id="stemma-casata"' not in source:
        marker='<section class="archive-feature"><a class="archive-feature-image" href="araldo-1911.html">'
        if marker in source:
            source=source.replace(marker,feature+marker,1)
        else:
            source=source.replace("</article>",feature+"</article>",1)
        path.write_text(source,encoding="utf-8")

    header=source[:source.index('<main id="contenuto">')]
    footer=source[source.index("</main>")+len("</main>"):]
    title='Stemma della casata Martinelli'
    header=header.replace('<title>Documenti · Famiglia Martinelli</title>','<title>'+title+' · Famiglia Martinelli</title>')
    page='''<main id="contenuto"><div class="page-heading"><p class="eyebrow">DOCUMENTI DELL’ARCHIVIO</p><h1>Lo stemma della casata Martinelli</h1><p>Riproduzione dello stemma, descrizione araldica e riferimenti storici alla famiglia.</p><p><a href="documenti.html">← Torna ai Documenti</a> · <a href="araldo-1911.html">Consulta L’Araldo 1911</a></p></div><article class="page-content" style="max-width:1080px"><div class="stemma-documento"><figure class="stemma-immagine"><a href="'''+img+'''" target="_blank" rel="noopener"><img src="'''+img+'''" alt="Stemma Martinelli con mantello e corona, fenice rivolta verso il sole e due spade incrociate" style="display:block;width:100%;height:auto;max-height:none;object-fit:contain;border:0;padding:0;box-shadow:none;margin:0"></a><figcaption>Stemma della casata Martinelli · Riproduzione già conservata nell’archivio del sito</figcaption></figure><div class="stemma-testo"><p class="eyebrow">STORIA E ARALDICA</p><h2>La famiglia Martinelli</h2><p>La ricostruzione genealogica conservata nella sezione <a href="la-storia.html">La storia</a> riconduce il ramo di Monopoli alla famiglia Martinelli presente a Mola fin dal XVI secolo. Nel corso del tempo si distinsero un ramo monopolitano e uno napoletano.</p><p>La storia familiare ricorda l’aggregazione al patriziato di Salerno, nel Sedile di Portaretese, e i legami con la monarchia borbonica. Queste notizie sono presentate come ricostruzione dell’archivio di famiglia, non come verifica indipendente dei titoli.</p><h3>Descrizione araldica</h3><p>Nella storia familiare lo scudo è descritto come d’argento, con un lambello a tre pendenti rossi, una <strong>fenice</strong> che fissa un <strong>sole d’oro</strong> e, nella parte inferiore, <strong>due spade incrociate a croce di Sant’Andrea</strong>.</p><p>La riproduzione mostra anche una corona e un mantello decorativo. La descrizione testuale qui riportata è una sintesi della pagina <em>La storia</em> del sito; per confrontarla con le fonti d’epoca si invita a consultare le sei pagine digitalizzate de <em>L’Araldo</em>, almanacco nobiliare del Napoletano del <strong>1911</strong>.</p><p><a class="text-link" href="araldo-1911.html">Sfoglia l’estratto dell’Araldo 1911 <span aria-hidden="true">→</span></a></p></div></div><p class="stemma-nota">Nota archivistica: l’immagine è una rielaborazione restaurata dello stemma fotografato, non la scansione del manufatto originale. Per verifiche storiche e araldiche consultare l’estratto dell’Araldo 1911.</p></article></main>'''
    style='''<style>.stemma-documento{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:clamp(24px,5vw,65px);align-items:start;margin:24px 0 48px}.stemma-immagine{margin:0;background:#f3e9d5;padding:16px;border:1px solid #d7c9b1}.stemma-immagine figcaption{font:12px/1.6 system-ui,sans-serif;color:#665c4f;text-align:center;margin:12px 0 0}.stemma-testo h2{margin:8px 0 22px}.stemma-testo h3{font-size:26px;margin:27px 0 10px}.stemma-testo p{font:16px/1.85 system-ui,sans-serif;margin:12px 0;color:#443c33}.stemma-nota{font:13px/1.7 system-ui,sans-serif;color:#706656;border-top:1px solid #d7c9b1;padding-top:18px}@media(max-width:750px){.stemma-documento{grid-template-columns:1fr}.stemma-immagine{max-width:450px;margin:auto}.stemma-testo p{font-size:15px}}</style>'''
    header=header.replace('</head>',style+'</head>')
    (dist/"stemma-casata.html").write_text(header+page+footer,encoding="utf-8")

if __name__=="__main__":
    apply_stemma_documenti(Path(__file__).resolve().parents[1])
