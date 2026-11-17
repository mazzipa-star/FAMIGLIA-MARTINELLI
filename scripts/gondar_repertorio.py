"""Cartella di collegamenti ai filmati d'archivio di Gondar, nella sezione Foto e video."""
from pathlib import Path

def apply_gondar_repertorio(root):
    page = Path(root) / "dist" / "media-gallery.html"
    html = page.read_text(encoding="utf-8")
    if 'id="gondar-archivi"' in html:
        return

    css = """<style>
.gondar-folder{margin:1.5rem 0 2rem;border:1px solid #d3c0a7;border-radius:11px;background:#f3ede3;overflow:hidden}
.gondar-folder summary{display:flex;gap:.7rem;align-items:center;cursor:pointer;padding:1.05rem 1.2rem;font-weight:650;font-size:1.08rem;list-style:none}
.gondar-folder summary::-webkit-details-marker{display:none}
.gondar-folder summary:after{content:"▾";margin-left:auto;color:#795d40}
.gondar-folder[open] summary:after{content:"▴"}
.gondar-folder .gondar-contents{padding:.25rem 1.2rem 1.3rem}
.gondar-folder .gondar-film{padding:1rem 0;border-top:1px solid #d5c8b6}
.gondar-folder .gondar-film h4{margin:0 0 .3rem;font-size:1.03rem}
.gondar-folder .gondar-film p{margin:.25rem 0 .7rem;line-height:1.6}
.gondar-folder .gondar-meta{font-size:.84rem;color:#685a4b}
.gondar-folder a{overflow-wrap:anywhere}
</style>"""
    html = html.replace('</head>', css + '</head>', 1)

    section = """<details id="gondar-archivi" class="gondar-folder">
<summary><span aria-hidden="true">📁</span><span>Gondar durante l’occupazione italiana in Africa</span></summary>
<div class="gondar-contents">
<p>Filmati storici consultabili presso gli archivi che li conservano. I collegamenti si aprono sui siti originali; i video non sono copiati né ripubblicati qui. Le riprese rispecchiano il punto di vista e il contesto della loro produzione.</p>
<article class="gondar-film"><h4>Gondar, antica capitale etiopica</h4>
<p class="gondar-meta">Archivio storico Istituto Luce · 12 febbraio 1936 · Prima dell’occupazione italiana della città</p>
<p>Vedute della città e scene di vita quotidiana, come documentate dal cinegiornale d’epoca.</p>
<p><a href="https://patrimonio.archivioluce.com/luce-web/detail/IL5000061569/2/gondar-antica-capitale-etiopica.html%26jsonVal%3D" target="_blank" rel="noopener noreferrer">Apri il filmato all’Archivio Luce ↗</a></p></article>
<article class="gondar-film"><h4>Governo dell’Amhara — Gondar</h4>
<p class="gondar-meta">Archivio storico Istituto Luce · 1937 · Durante l’occupazione italiana</p>
<p>Vedute della regione e documentazione della presenza e dell’amministrazione coloniale italiana.</p>
<p><a href="https://patrimonio.archivioluce.com/luce-web/detail/IL5000095912/2/-5818.html?startPage=0" target="_blank" rel="noopener noreferrer">Apri il filmato all’Archivio Luce ↗</a></p></article>
<article class="gondar-film"><h4>Abyssinia — Gondar, 1941</h4>
<p class="gondar-meta">Imperial War Museums · 9 dicembre 1941 · Dopo la fine dell’occupazione italiana</p>
<p>Vedute di Gondar e documentazione militare britannica, per il capitolo sulla guerra e sulle sue conseguenze.</p>
<p><a href="https://film.iwmcollections.org.uk/record/10175" target="_blank" rel="noopener noreferrer">Apri la scheda del filmato IWM ↗</a></p></article>
<p class="gondar-meta">Nota sui diritti: prima di utilizzare estratti nel documentario è necessario verificare le condizioni di licenza con i rispettivi archivi.</p>
</div></details>"""
    marker = '</section><details class="archive-film">'
    if marker not in html:
        raise ValueError("Impossibile individuare la fine della sezione Video")
    html = html.replace(marker, section + marker, 1)
    page.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    apply_gondar_repertorio(Path(__file__).resolve().parents[1])
