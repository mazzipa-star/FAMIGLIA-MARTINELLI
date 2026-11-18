"""Album dei quattro fratelli: visualizzatore fermo e miniature per generazione."""
from html import escape
import json

LABELS={1:'Prima generazione',2:'Seconda generazione',3:'Terza generazione',None:'Da collocare'}
SUBTITLES={1:'I fratelli Martinelli e i rispettivi coniugi',2:'I loro figli e coniugi',3:'I nipoti',None:'Fotografie in attesa di conferma della generazione'}

def render_family_album(collection,config):
    source=collection['images'];records=config['photos']
    assert len(source)==len(records),collection['id']
    pictures=[]
    for generation in [1,2,3,None]:
        for photo,record in zip(source,records):
            if record['generation']!=generation:continue
            pictures.append(dict(photo,original_number=record['original_number'],generation=generation,generation_label=LABELS[generation]))
    lead={'sante':2,'vera':38,'graziella':11}.get(collection['id'])
    initial=next((i for i,p in enumerate(pictures) if p['original_number']==lead),0)
    first=pictures[initial]
    buttons=[];bands=[]
    for generation in [1,2,3,None]:
        group=[(i,p) for i,p in enumerate(pictures) if p['generation']==generation]
        if generation is None and not group:continue
        key='generazione-'+str(generation or 'da-collocare')
        buttons.append('<button type="button" data-generation-target="'+key+'">'+LABELS[generation]+' <span>'+str(len(group))+'</span></button>')
        thumbs=[]
        for i,p in group:
            name='Foto '+str(p['original_number'])+' · '+p['caption']
            thumbs.append('<button type="button" data-slide="'+str(i)+'" aria-label="'+escape(name,quote=True)+'" aria-pressed="'+('true' if i==initial else 'false')+'"><img src="'+escape(p['src'],quote=True)+'" loading="lazy" alt=""><span>'+escape(name)+'</span></button>')
        bands.append('<section class="generation-band" id="'+key+'" aria-labelledby="titolo-'+key+'"><h3 id="titolo-'+key+'">'+LABELS[generation]+'</h3><p>'+SUBTITLES[generation]+'</p>'+('<div class="album-thumbs">'+''.join(thumbs)+'</div>' if thumbs else '<p class="generation-empty">Le fotografie saranno collocate qui dopo l’identificazione.</p>')+'</section>')
    dataset=escape(json.dumps(pictures,ensure_ascii=False,separators=(',',':')),quote=True)
    return '<article class="full-album family-album" data-initial-index="'+str(initial)+'" data-items="'+dataset+'"><div class="album-viewer"><div class="album-stage"><img src="'+escape(first['src'],quote=True)+'" alt="'+escape(first['caption'],quote=True)+'"><button class="prev" type="button" aria-label="Fotografia precedente">‹</button><button class="next" type="button" aria-label="Fotografia successiva">›</button></div><div class="album-copy" aria-live="polite"><p class="album-photo-number" data-count>Fotografia '+str(first['original_number'])+' · '+str(len(pictures))+' fotografie nell’album</p><p class="album-generation" data-generation-label>'+first['generation_label']+'</p><h2>'+escape(collection['title'])+'</h2><p data-caption>'+escape(first['caption'])+'</p><a data-original href="'+escape(first['full'],quote=True)+'" target="_blank" rel="noopener">Ingrandisci l’originale ↗</a></div></div><div class="album-browse"><h2>Le fotografie</h2><nav class="generation-tabs" aria-label="Generazioni">'+''.join(buttons)+'</nav><div class="album-thumbs-panel" tabindex="0" role="region" aria-label="Miniature delle fotografie per generazione">'+''.join(bands)+'</div></div></article>'
