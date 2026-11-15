"""Inserisce il collegamento alla timeline Africa tra i capitoli fotografici."""
from pathlib import Path

def apply_africa(root):
    root = Path(root)
    page = root / "dist/media-gallery.html"
    source = page.read_text(encoding="utf-8")

    nav_anchor = '<a href="#foto-giovanni">La famiglia di Giovanni</a>'
    nav_link = '<a href="africa-famiglia.html" class="africa-banner-link">Africa · Da Verona a Gondar</a>'
    if nav_link not in source and nav_anchor in source:
        source = source.replace(nav_anchor, nav_anchor + nav_link, 1)

    if 'id="nuove-foto-africa"' not in source:
        section = '''<section class="photo-chapter" id="nuove-foto-africa" aria-labelledby="africa-title"><header>
<h2 id="africa-title" class="chapter-heading">Africa · Da Verona a Gondar<span class="chapter-art" aria-hidden="true"><img loading="lazy" src="assets/africa-martinelli/08-matrimonio-due-coppie.jpg" alt=""></span></h2>
<p>9 fotografie restaurate · 1939 e altre date da verificare</p>
<p>Il soggiorno in Africa orientale di Giovanni Martinelli e della sua famiglia, i matrimoni di Annamaria ed Enrico Calenda e di Vera e Carlo Martucci.</p></header>
<p><a class="button primary" href="africa-famiglia.html">Sfoglia la timeline fotografica →</a></p></section>'''
        marker = '<section class="photo-chapter" id="foto-giovanni"'
        if marker in source:
            source = source.replace(marker, section + marker, 1)
        else:
            source = source.replace("</article>", section + "</article>", 1)

    page.write_text(source, encoding="utf-8")

if __name__ == "__main__":
    apply_africa(Path(__file__).resolve().parents[1])
