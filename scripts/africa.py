"""Integra la galleria Verona–Gondar nel catalogo fotografico; rieseguibile dopo build.py."""
from pathlib import Path

def apply_africa(root):
    root=Path(root)
    page=root/"dist/media-gallery.html"
    source=page.read_text(encoding="utf-8")
    if 'id="nuove-foto-africa"' in source:
        return
    section=('''<section id="nuove-foto-africa" class="photo-chapter" aria-labelledby="africa-title">
<header><p class="eyebrow">NUOVE MEMORIE DI FAMIGLIA</p>
<h2 id="africa-title">Da Verona a Gondar</h2>
<p>Nove fotografie restaurate: Giovanni, Lina, Annamaria, Vera, Enrico Calenda, Carlo Martucci e Graziella tra Verona e l’Africa orientale. Date non documentate indicate come provvisorie.</p></header>
<p><a class="button primary" href="africa-famiglia.html">Sfoglia la timeline fotografica →</a></p></section>''')
    marker='<section class="photo-chapter" id="foto-giovanni"'
    if marker in source:
        source=source.replace(marker,section+marker,1)
    else:
        source=source.replace("</article>",section+"</article>",1)
    page.write_text(source,encoding="utf-8")

if __name__=="__main__":
    apply_africa(Path(__file__).resolve().parents[1])
