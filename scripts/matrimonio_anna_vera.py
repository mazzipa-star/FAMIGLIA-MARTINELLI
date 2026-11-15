"""Raccoglie le fotografie e i documenti delle nozze di Anna e Vera."""
from pathlib import Path
from html import escape
import re

PHOTOS = [["Anna ed Enrico nel giardino di Verona","Prima della partenza per l’Africa; data da verificare.","assets/africa-martinelli/01-verona-anna-enrico.jpg"],["Carlo Martucci ed Enrico Calenda a Gondar","Fotografia del 1939 secondo la tradizione familiare.","assets/africa-martinelli/02-gondar-carlo-enrico-1939.jpg"],["Le nozze di Annamaria ed Enrico","Fotografia della cerimonia in Africa orientale; data da verificare.","assets/africa-martinelli/05-matrimonio-anna-enrico.jpg"],["Graziella paggetta","Graziella Martinelli durante le nozze di Annamaria ed Enrico.","assets/africa-martinelli/06-matrimonio-graziella-paggetta.jpg"],["La famiglia riunita per il matrimonio","Foto di gruppo; alcuni riconoscimenti restano da verificare.","assets/africa-martinelli/07-matrimonio-gruppo.jpg"],["Le due coppie di sposi","Da sinistra Carlo Martucci, Vera Martinelli, Annamaria Martinelli ed Enrico Calenda.","assets/africa-martinelli/08-matrimonio-due-coppie.jpg"],["Giovanni, le figlie e i generi","Giovanni Martinelli, Annamaria, Vera, Enrico Calenda e Carlo Martucci.","assets/africa-martinelli/09-giovanni-figlie-generi.jpg"],["Matrimonio Enrico e Mannina · archivio storico","Versione conservata nella raccolta «La famiglia di Giovanni».","assets/5e1b0fff76-matrimonio-mannina.jpg"],["Matrimonio Vera e Carlo · archivio storico","Fotografia già catalogata nella raccolta «La famiglia di Giovanni».","assets/88ec072495-adobe-photoshop-cs6-macintosh-2479x3426-000568.jpg"],["Foto di gruppo alle nozze di Anna e Vera · archivio storico","Immagine originale già presente nell’album di famiglia.","assets/c02c989c15-matrimonio-anna-e-vera.jpg"]]

def apply_matrimonio_anna_vera(root):
    dist = Path(root) / "dist"
    page = dist / "media-gallery.html"
    html = page.read_text(encoding="utf-8")
    doc = dist / "documenti.html"
    docs = doc.read_text(encoding="utf-8")
    docs = re.sub(r'<section class="archive-feature" id="invito-nozze-anna">.*?</section>', '', docs, count=1, flags=re.S)
    doc.write_text(docs, encoding="utf-8")

    nav = '<a class="matrimonio-banner-link" href="matrimonio-anna-vera.html">Il matrimonio di Anna e Vera</a>'
    anchor = '<a href="africa-famiglia.html" class="africa-banner-link">Africa · Da Verona a Gondar</a>'
    if nav not in html:
        if anchor in html:
            html = html.replace(anchor, anchor + nav, 1)
        else:
            html = html.replace('</nav></div><section class="photo-chapter"', nav + '</nav></div><section class="photo-chapter"', 1)

    banner = '''<section class="photo-chapter" id="matrimonio-anna-vera" aria-labelledby="matrimonio-anna-vera-title"><header><h2 id="matrimonio-anna-vera-title" class="chapter-heading">Il matrimonio di Anna e Vera<span class="chapter-art" aria-hidden="true"><img loading="lazy" src="assets/africa-martinelli/08-matrimonio-due-coppie.jpg" alt=""></span></h2><p>Fotografie delle due coppie, immagini d’archivio e invito di nozze del 1940</p><p>Annamaria Martinelli ed Enrico Calenda; Vera Martinelli e Carlo Martucci. Una raccolta delle immagini e dei documenti conservati nell’archivio familiare.</p></header><p><a class="button primary" href="matrimonio-anna-vera.html">Sfoglia la raccolta dei matrimoni →</a></p></section>'''
    if 'id="matrimonio-anna-vera"' not in html:
        marker = '<section class="photo-chapter" id="nuove-foto-africa"'
        if marker in html:
            html = html.replace(marker, banner + marker, 1)
        else:
            html = html.replace('<section class="photo-chapter" id="foto-giovanni"', banner+'<section class="photo-chapter" id="foto-giovanni"', 1)
    page.write_text(html, encoding="utf-8")

    invitation = dist / "invito-nozze-anna-enrico.html"
    inv = invitation.read_text(encoding="utf-8")
    inv = inv.replace('← Torna ai Documenti', '← Torna alla raccolta dei matrimoni')
    inv = inv.replace('<a href="documenti.html">← Torna alla raccolta dei matrimoni</a>', '<a href="matrimonio-anna-vera.html">← Torna alla raccolta dei matrimoni</a>')
    inv = inv.replace('DOCUMENTI DI FAMIGLIA · 1940', 'FOTO E VIDEO · DOCUMENTO DEL 1940')
    inv = inv.replace('<a aria-current="page" href="documenti.html">Documenti</a>', '<a href="documenti.html">Documenti</a>')
    inv = inv.replace('<a href="media-gallery.html">Foto e video</a>', '<a aria-current="page" href="media-gallery.html">Foto e video</a>')
    invitation.write_text(inv, encoding="utf-8")

    head = html[:html.index('<main id="contenuto">')]
    tail = html[html.index('</main>')+len('</main>'):]
    head = head.replace('Foto e video · Famiglia Martinelli', 'Il matrimonio di Anna e Vera · Famiglia Martinelli')
    head = head.replace('</head>', '''<style>.matr-head{max-width:1100px;margin:40px auto 30px;padding:0 24px}.matr-head h1{font:clamp(34px,5vw,62px)/1.14 Georgia,serif}.matr-head p{line-height:1.75}.matr-wrap{max-width:1110px;margin:0 auto 80px;padding:0 24px}.matr-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin:20px 0 55px}.matr-item{margin:0;padding:12px;background:#f0e7db;border:1px solid #d4c5b1}.matr-item img{display:block;max-width:100%!important;width:auto!important;height:auto!important;max-height:630px!important;object-fit:contain;margin:0 auto}.matr-item figcaption{font:14px/1.65 system-ui,sans-serif;padding:13px 5px}.matr-item figcaption strong{display:block;margin-bottom:4px}.matr-section{border-top:1px solid #c8b9a2;padding-top:20px;margin-top:38px}.matr-section h2{font:clamp(25px,3vw,36px)/1.2 Georgia,serif;margin:10px 0}.matr-section p{line-height:1.75}.matr-invito{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:25px;align-items:start;background:#f1e9df;padding:18px}.matr-invito img{display:block;width:100%;height:auto;object-fit:contain}.matr-invito p{line-height:1.7}@media(max-width:730px){.matr-grid,.matr-invito{grid-template-columns:1fr}}</style></head>''')

    def figure(item):
        name, caption, src = item
        return '<figure class="matr-item"><a href="'+escape(src,quote=True)+'" target="_blank" rel="noopener"><img src="'+escape(src,quote=True)+'" loading="lazy" alt="'+escape(name,quote=True)+'"></a><figcaption><strong>'+escape(name)+'</strong>'+escape(caption)+'</figcaption></figure>'

    primary = ''.join(figure(x) for x in PHOTOS[2:])
    context = ''.join(figure(x) for x in PHOTOS[:2])
    body = '''<main id="contenuto"><div class="matr-head"><p class="eyebrow">FOTO E VIDEO · ARCHIVIO DI FAMIGLIA</p><h1>Il matrimonio di Anna e Vera</h1><p>Le nozze di <strong>Annamaria (Mannina) Martinelli ed Enrico Calenda</strong> e di <strong>Vera Martinelli e Carlo Martucci</strong>, nella memoria del periodo trascorso dalla famiglia in Africa orientale.</p><p><a href="media-gallery.html">← Torna a Foto e video</a> · <a href="africa-famiglia.html">Africa: da Verona a Gondar</a></p></div><article class="matr-wrap"><section class="matr-section"><h2>Le fotografie dei matrimoni</h2><p>Raccogliamo le immagini delle due coppie, di Graziella paggetta e delle fotografie di gruppo. Le fotografie provenienti dall’album storico sono conservate accanto alle versioni già disponibili nella timeline africana: possono rappresentare riproduzioni differenti dello stesso soggetto.</p><div class="matr-grid">'''+primary+'''</div></section><section class="matr-section"><h2>L’invito di nozze di Anna Maria ed Enrico</h2><p>Annuncio datato <strong>30 dicembre 1940 – XIX</strong>, ad Azozò (Gondar). È la data riportata sul documento, non necessariamente quella della celebrazione.</p><div class="matr-invito"><a href="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg" target="_blank" rel="noopener"><img src="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-restaurato.jpg" loading="lazy" alt="Invito di nozze di Annamaria Martinelli ed Enrico Calenda, versione migliorata"></a><div><h3>L’annuncio originale e restaurato</h3><p>La versione migliorata facilita la lettura del documento; la fotografia originale rimane consultabile per preservarne la testimonianza storica.</p><p><a href="assets/documenti/matrimonio-anna-enrico/invito-nozze-1940-originale.jpg" target="_blank" rel="noopener">Apri la fotografia originale ↗</a></p><p><a href="invito-nozze-anna-enrico.html">Leggi la scheda completa dell’invito →</a></p></div></div></section><section class="matr-section"><h2>Prima delle nozze: Verona e Gondar</h2><p>Due immagini utili per contestualizzare i protagonisti. Le date sono quelle riportate nelle didascalie familiari e richiedono, dove indicato, ulteriori verifiche.</p><div class="matr-grid">'''+context+'''</div></section><section class="matr-section"><h2>Altri documenti e fotografie</h2><p><a href="africa-famiglia.html">La timeline fotografica «Da Verona a Gondar»</a> · <a href="media-gallery.html#foto-giovanni">La famiglia di Giovanni</a>. Le fotografie già presenti nei capitoli originali dell’album rimangono consultabili senza duplicare i file.</p></section></article></main>'''
    (dist / 'matrimonio-anna-vera.html').write_text(head+body+tail, encoding="utf-8")

if __name__ == "__main__":
    apply_matrimonio_anna_vera(Path(__file__).resolve().parents[1])
