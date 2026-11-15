"""Scheda dell'annuncio di nozze Martinelli–Calenda (1940)."""
from pathlib import Path

def apply_invito_nozze(root):
    dist=Path(root)/"dist"
    listing=dist/"documenti.html"
    html=listing.read_text(encoding="utf-8")
    feature='''<section class="archive-feature" id="invito-nozze-anna"><a class="archive-feature-image" href="invito-nozze-anna-enrico.html"><img src="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg" alt="Annuncio di nozze di Anna Maria Martinelli ed Enrico Calenda, 1940" loading="lazy" style="width:100%;height:auto;object-fit:contain"></a><div class="archive-feature-copy"><h2 class="feature-title">Le nozze di Anna Maria Martinelli ed Enrico Calenda · 1940</h2><div><p>L’annuncio di matrimonio delle famiglie Martinelli e Calenda, datato 30 dicembre 1940 ad Azozò, presso Gondar, nell’Africa Orientale Italiana. Sono conservate la fotografia originale e una versione migliorata per la lettura.</p></div><a class="text-link" href="invito-nozze-anna-enrico.html">Consulta l’annuncio <span aria-hidden="true">→</span></a></div></section>'''
    if 'id="invito-nozze-anna"' not in html:
        marker='<section class="archive-feature" id="stemma-casata">'
        if marker in html:html=html.replace(marker,feature+marker,1)
        else:html=html.replace('</article>',feature+'</article>',1)
        listing.write_text(html,encoding="utf-8")
    heading=html[:html.index('<main id="contenuto">')].replace('<title>Documenti · Famiglia Martinelli</title>','<title>Invito alle nozze di Anna Maria ed Enrico · Famiglia Martinelli</title>')
    body='''<main id="contenuto"><div class="page-heading"><p class="eyebrow">DOCUMENTI DI FAMIGLIA · 1940</p><h1>Le nozze di Anna Maria Martinelli ed Enrico Calenda</h1><p>Annuncio di matrimonio datato Azozò (Gondar), 30 dicembre 1940 – XIX.</p><p><a href="documenti.html">← Torna ai Documenti</a> · <a href="africa-famiglia.html">Fotografie di famiglia a Gondar</a></p></div><article class="page-content" style="max-width:1100px"><figure style="margin:0 0 28px;background:#f1ece3;padding:clamp(8px,2vw,20px)"><a href="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg" target="_blank" rel="noopener" aria-label="Apri l’annuncio restaurato in grande"><img src="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg" alt="Annuncio di matrimonio di Anna Maria Martinelli e del tenente Enrico Calenda, 30 dicembre 1940" style="display:block;width:100%;height:auto;max-height:none;object-fit:contain;border:0;box-shadow:none;padding:0;margin:0"></a><figcaption style="font:13px/1.7 system-ui,sans-serif;margin:10px 0 0;color:#675b4e">Annuncio di nozze · elaborazione conservativa della fotografia originale. Clicca sull’immagine per ingrandire.</figcaption></figure><h2>Il documento</h2><p>Le famiglie di Giovanni Martinelli e Lina Masoni, genitori di Anna Maria, e di Enea Calenda e Lodovica Calenda, genitori di Enrico, partecipano il matrimonio dei figli. Il testo indica per lo sposo il grado di tenente e per Giovanni Martinelli il titolo di patrizio di Salerno.</p><p>In fondo al documento compaiono la località <strong>Azozò (Gondar)</strong> e la data <strong>30 dicembre 1940 – XIX</strong>, oltre agli indirizzi delle famiglie a Verona e nel Napoletano.</p><p>Questa data è quella stampata sull’annuncio: il documento, da solo, non permette di stabilire con certezza il giorno della celebrazione.</p><p><a href="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-originale.jpg" target="_blank" rel="noopener">Confronta con la fotografia originale</a> · <a href="africa-famiglia.html">Vedi le fotografie dei matrimoni e del soggiorno in Africa</a></p></article></main>'''
    footer=html[html.index('</main>')+len('</main>'):]
    (dist/"invito-nozze-anna-enrico.html").write_text(heading+body+footer,encoding="utf-8")

if __name__=="__main__":
    apply_invito_nozze(Path(__file__).resolve().parents[1])
