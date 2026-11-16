"""Tre fotografie storiche restaurate: Lina, Giovanni giovane ufficiale e Giovanni col padre."""
from pathlib import Path

def apply_ritratti_anteguerra(root):
    dist = Path(root) / "dist"
    gallery = dist / "media-gallery.html"
    s = gallery.read_text(encoding="utf-8")
    banner_link = '<a href="ritratti-lina-giovanni.html">Lina e Giovanni · ritratti storici</a>'
    nav_anchor = '<a class="matrimonio-banner-link" href="matrimonio-anna-vera.html">Il matrimonio di Anna e Vera</a>'
    if banner_link not in s:
        if nav_anchor in s:
            s = s.replace(nav_anchor, nav_anchor + banner_link, 1)
        else:
            s = s.replace('Africa · Da Verona a Gondar</a>', 'Africa · Da Verona a Gondar</a>' + banner_link, 1)
    block = '''<section class="photo-chapter" id="ritratti-lina-giovanni" aria-labelledby="titolo-ritratti-lina-giovanni"><header><h2 id="titolo-ritratti-lina-giovanni" class="chapter-heading">Lina e Giovanni · tre ritratti storici<span class="chapter-art" aria-hidden="true"><img loading="lazy" src="assets/famiglia-martinelli-storiche/giovanni-con-padre-restaurata.jpg" alt=""></span></h2><p>Tre fotografie dall’archivio di famiglia · date da accertare</p><p>Lina nel giorno del diploma di scuola superiore; Giovanni giovane ufficiale; Giovanni con il padre. Fotografie conservate in originale e in versione migliorata, senza ricostruzione artificiale dei volti.</p></header><p><a class="button primary" href="ritratti-lina-giovanni.html">Sfoglia i tre ritratti →</a></p></section>'''
    if 'id="ritratti-lina-giovanni"' not in s:
        marker = '<section class="photo-chapter" id="matrimonio-anna-vera"'
        if marker in s:
            s = s.replace(marker, block + marker, 1)
        else:
            s = s.replace('<section class="photo-chapter" id="foto-giovanni"', block + '<section class="photo-chapter" id="foto-giovanni"', 1)
    gallery.write_text(s, encoding="utf-8")

    head = s[:s.index('<main id="contenuto">')]
    foot = s[s.index('</main>') + len('</main>'):]
    head = head.replace('<title>Foto e video · Famiglia Martinelli</title>', '<title>Lina e Giovanni · Ritratti storici · Famiglia Martinelli</title>')
    head = head.replace('</head>', '''<style>.rtr-main{max-width:1080px;margin:35px auto 65px;padding:0 20px}.rtr-main h1{font:clamp(34px,5vw,58px)/1.14 Georgia,serif;margin:14px 0}.rtr-main p{line-height:1.75}.rtr-card{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:32px;align-items:center;margin:45px 0;padding-top:32px;border-top:1px solid #d3c4b1}.rtr-photo{background:#ede6da;padding:12px}.rtr-photo img{display:block;width:auto!important;max-width:100%!important;height:auto!important;max-height:620px!important;object-fit:contain;margin:auto}.rtr-note{color:#695c4d;font-size:13px}.rtr-card h2{font:clamp(24px,3vw,36px)/1.2 Georgia,serif}.rtr-photo figcaption{font-size:12px;line-height:1.6;color:#766a5b;margin:10px 0 0}@media(max-width:730px){.rtr-card{grid-template-columns:1fr;gap:15px}}</style></head>''')
    base = 'assets/famiglia-martinelli-storiche/'
    items = [
       ('lina-diploma', 'Lina Masoni nel giorno del diploma', 'Ritratto identificato dalla famiglia come Lina Masoni in occasione del diploma di scuola superiore. La data esatta non è ancora documentata.', 'La fotografia fornita era orientata lateralmente; la copia migliorata è stata ruotata e corretta soltanto nei toni.'),
       ('giovanni-giovane-ufficiale', 'Giovanni Martinelli giovane ufficiale', 'Ritratto militare di Giovanni Martinelli in cornice ovale, conservato dalla famiglia. L’anno e il grado al momento dello scatto sono da verificare.', 'Il restauro attenua la scarsa leggibilità della fotografia attraverso una correzione conservativa.'),
       ('giovanni-con-padre', 'Giovanni Martinelli con il padre', 'Ritratto di studio: Giovanni Martinelli in uniforme in piedi, accanto al padre seduto. Identificazione delle persone comunicata dalla famiglia; data da accertare.', 'Il restauro conserva la cornice e l’intera fotografia, senza modificare visi e abiti.')
    ]
    sections = []
    for key, title, caption, treatment in items:
        rest = base + key + '-restaurata.jpg'
        original = base + key + '-originale.jpg'
        sections.append('<section class="rtr-card"><figure class="rtr-photo"><a href="'+rest+'" target="_blank" rel="noopener"><img loading="lazy" src="'+rest+'" alt="'+title+'"></a><figcaption>Versione migliorata · Apri l’immagine per ingrandire</figcaption></figure><div><h2>'+title+'</h2><p>'+caption+'</p><p class="rtr-note">'+treatment+'</p><p><a href="'+original+'" target="_blank" rel="noopener">Confronta con la fotografia originale →</a></p></div></section>')
    body = '<main id="contenuto"><article class="rtr-main"><p class="eyebrow">FOTO E VIDEO · ARCHIVIO FAMILIARE</p><h1>Lina e Giovanni: tre ritratti storici</h1><p>Tre nuove fotografie che documentano i primi anni della storia familiare. I soggetti sono stati identificati dalla famiglia; le date degli scatti rimangono da verificare. Le versioni restaurate sono ottenute dalla fotografia ricevuta senza ricreare i volti.</p><p><a href="media-gallery.html">← Torna a Foto e video</a></p>' + ''.join(sections) + '<p><a href="media-gallery.html#foto-giovanni">La famiglia di Giovanni</a> · <a href="africa-famiglia.html">Da Verona a Gondar</a></p></article></main>'
    (dist / 'ritratti-lina-giovanni.html').write_text(head + body + foot, encoding="utf-8")

if __name__ == "__main__":
    apply_ritratti_anteguerra(Path(__file__).resolve().parents[1])
