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
