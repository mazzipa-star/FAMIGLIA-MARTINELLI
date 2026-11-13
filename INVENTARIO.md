# Inventario di migrazione

Rilevazione: 12 novembre 2026. Origine: https://famiglia-martinelli.weebly.com/. Recupero in sola lettura delle pagine pubbliche raggiungibili dai collegamenti HTML.

15 pagine; 360 URL di risorse scaricate (355 file con contenuto distinto). Tipi: {'application/pdf': 3, 'image/png': 2, 'image/jpeg': 355}.

| Pagina | Percorso conservato | Risorse referenziate | Immagini slideshow |
|---|---|---:|---:|
| [Viaggio nella memoria](https://famiglia-martinelli.weebly.com/) | `index.html` | 1 | 0 |
| [La storia](https://famiglia-martinelli.weebly.com/la-storia.html) | `la-storia.html` | 2 | 0 |
| [Documenti](https://famiglia-martinelli.weebly.com/documenti.html) | `documenti.html` | 4 | 0 |
| [La memoria](https://famiglia-martinelli.weebly.com/la-memoria.html) | `la-memoria.html` | 3 | 0 |
| [Genealogia](https://famiglia-martinelli.weebly.com/genealogia.html) | `genealogia.html` | 3 | 0 |
| [Media Gallery](https://famiglia-martinelli.weebly.com/media-gallery.html) | `media-gallery.html` | 223 | 238 |
| [Contact](https://famiglia-martinelli.weebly.com/contact.html) | `contact.html` | 2 | 0 |
| [Cartoline 1914](https://famiglia-martinelli.weebly.com/cartoline-1914.html) | `cartoline-1914.html` | 45 | 44 |
| [Cartoline 1919](https://famiglia-martinelli.weebly.com/cartoline-1919.html) | `cartoline-1919.html` | 4 | 3 |
| [Cartoline 1915](https://famiglia-martinelli.weebly.com/cartoline-1915.html) | `cartoline-1915.html` | 19 | 18 |
| [Cartoline varie](https://famiglia-martinelli.weebly.com/cartoline-varie.html) | `cartoline-varie.html` | 24 | 23 |
| [Cartoline 1916](https://famiglia-martinelli.weebly.com/cartoline-1916.html) | `cartoline-1916.html` | 3 | 2 |
| [Diario di prigionia](https://famiglia-martinelli.weebly.com/diario-di-prigionia.html) | `diario-di-prigionia.html` | 17 | 13 |
| [Diario di guerra](https://famiglia-martinelli.weebly.com/diario-di-guerra.html) | `diario-di-guerra.html` | 9 | 8 |
| [Gli audio](https://famiglia-martinelli.weebly.com/gli-audio.html) | `gli-audio.html` | 1 | 0 |

## File e testi

`content/assets.json`: URL originale, percorso locale, dimensione, tipo e impronta SHA-256 di ciascun file. `content/pages.json`: testi integrali estratti e collegamenti delle pagine pubbliche, inclusa la navigazione originale. `content/*.html.txt`: contenuti del corpo della nuova pagina. `content/galleries.json`: ordine e didascalie originali delle presentazioni. `archive/pages/`: HTML originale per confronto; non destinato alla pubblicazione. `content/external-links.json`: riferimenti esterni da mantenere.

## Limiti e verifiche richieste

- La copia comprende il sito pubblico raggiungibile, non il pannello Weebly, bozze, pagine private o pagine non collegate. La completezza rispetto all’account richiede confronto con l’elenco pagine dell’editor e con un eventuale archivio esportato dall’account.
- Le immagini sono quelle servite pubblicamente. Le scansioni degli slideshow dichiarano spesso una larghezza di 400 pixel: non equivalgono necessariamente agli originali ad alta risoluzione. Testi dentro fotografie e PDF restano nei documenti, senza trascrizioni inventate.
- Sono preservate le didascalie, comprese eventuali incongruenze nelle date: ad esempio la raccolta 1914 contiene didascalie del 1915.
- Il collegamento MyHeritage conduce a un servizio con accesso: gli alberi privati presenti nell’account non sono stati recuperati.
- Vimeo e YouTube sono dipendenze esterne: sono conservati i link, non scaricati i video o le tracce audio. Disponibilità, permessi di download e originali vanno verificati con il titolare.
- Aggiornamento del 13 novembre 2026: i due PDF genealogici sono anche consultabili in una pagina interattiva. I dati trascritti e i collegamenti sono in `content/genealogia.json`; i PDF originali restano invariati.
- Nessun accesso a messaggi, contatti raccolti, statistiche o servizi lato server. Gli script Weebly, pubblicità e tracciamenti non sono trasferiti nella nuova versione.
- Il recapito pubblico offuscato da Cloudflare è stato ricostruito per il collegamento email della pagina Contatti.
- Non sono stati modificati dominio, DNS, sito Weebly o account GitHub. Prima della pubblicazione controllare i dati delle persone viventi e i diritti sulle fotografie. Nessuna licenza pubblica dei contenuti è presunta.
- I vecchi percorsi sono conservati per agevolare la transizione; il reindirizzamento dal sottodominio Weebly non è sotto il controllo di questo progetto.
