# Famiglia Martinelli — archivio familiare

Migrazione pubblica dal sito Weebly, preparata il 12 novembre 2026. Consultare prima INVENTARIO.md e content/errors.json.

## Consultare il sito

Aprire dist/index.html nel browser, oppure dalla cartella del progetto eseguire:

    python3 -m http.server 8000 --directory dist

Visitare http://localhost:8000. Nessuna dipendenza aggiuntiva, nessun servizio Weebly necessario per immagini e PDF scaricati. Video e audio esterni richiedono Internet.

## Struttura

- dist/: sito statico pubblicabile, risorse locali e grafica responsive.
- archive/pages/: pagine originali conservate per confronto, con i riferimenti originali; non pubblicare questa cartella come sito.
- content/: inventario leggibile dalle applicazioni, testi, gallerie, URL e impronte dei file.
- scripts/build.py: rigenera le pagine dal materiale recuperato; richiede solo Python 3. Le modifiche manuali alle pagine generate vengono sovrascritte. Lo stile dist/style.css viene mantenuto.
- .github/workflows/pages.yml: pubblicazione manuale su GitHub Pages.

## Nuovo repository GitHub

Creare un repository vuoto, caricare il contenuto di questa cartella mantenendo anche .github, quindi scegliere Settings → Pages → Source → GitHub Actions. Avviare il workflow «Pubblica su GitHub Pages» dalla scheda Actions. Il workflow pubblica solo dist/. I percorsi relativi funzionano anche sotto il nome del repository. Il repository e il sito non sono stati creati o pubblicati durante questa preparazione.

Prima di rendere pubblico il repository controllare anche archive/ e content/: contengono la copia dei materiali familiari pubblici recuperati. Nessuna licenza aperta è attribuita a testi, fotografie o documenti.

## Completamento della migrazione

Confrontare l’inventario con l’editor Weebly e un eventuale export dall’account; aggiungere pagine private o non collegate solo se desiderato; sostituire scansioni con originali migliori se disponibili; verificare i media Vimeo/YouTube e le date delle didascalie. Controllare navigazione e leggibilità su telefono prima della pubblicazione definitiva. Il sito originale può restare online durante tutto il processo.

## Genealogia interattiva (13 novembre 2026)

La pagina genealogia conserva i due PDF e offre alberi navigabili, zoom, ricerca trasversale e schede leggibili. Dati in content/genealogia.json (11 presenze negli antenati, 38 nei discendenti; Giovanni compare in entrambi), modello in templates/genealogia.html, interazioni e stile in dist/genealogia.js e dist/genealogia.css. I ritratti sono ritagli dei PDF. Le date mancanti restano mancanti. Il generatore incorpora i dati per permettere anche apertura locale senza server. Aggiornare i dati e rigenerare con python3 scripts/build.py. La pubblicazione parte anche a ogni caricamento sul ramo main.

## Template Album di famiglia (13 novembre 2026)

Il template grafico viene applicato a tutte le pagine da scripts/album.py, richiamato al termine della generazione. La homepage è in templates/home-album.html. Stile comune in dist/style.css, visualizzatore delle gallerie in dist/album.js. La timeline iniziale usa le didascalie delle cartoline 1914, 1915, 1916 e 1919 da content/galleries.json; non attribuisce date alle fotografie non datate. Le immagini restaurate per la homepage sono in dist/assets/album/: sono rielaborazioni con IA, mentre il ritratto originale resta scaricabile dalla homepage e lo stemma originale è conservato in archive/brand/. La genealogia interattiva conserva il proprio comportamento. Per ricostruire tutte le pagine: python3 scripts/build.py. Il caricamento sul ramo main avvia GitHub Pages.
