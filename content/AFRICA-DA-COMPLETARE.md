# Timeline Africa — integrazione in preparazione

Questa bozza è volutamente **non pubblicata**. Il ramo contiene la pagina `dist/africa-famiglia.html`, il catalogo `content/africa-martinelli-timeline.json`, lo script `scripts/africa.py` e il collegamento persistente nel generatore `scripts/build.py`.

## Immagini da aggiungere prima dell'unione con main

Estrarre i seguenti JPG dal pacchetto `Pacchetto_GitHub_Timeline_Africa.zip` e copiare tutti i file della sottocartella `dist/assets/africa-martinelli/` nella cartella omonima di questo ramo:

- 01-verona-anna-enrico.jpg
- 02-gondar-carlo-enrico-1939.jpg
- 03-anna-cerimonia-26-maggio.jpg
- 04-verso-cerimonia-26-maggio.jpg
- 05-matrimonio-anna-enrico.jpg
- 06-matrimonio-graziella-paggetta.jpg
- 07-matrimonio-gruppo.jpg
- 08-matrimonio-due-coppie.jpg
- 09-giovanni-figlie-generi.jpg

Conservare separatamente gli originali nell'archivio personale; nel pacchetto si trovano in `archive/africa-martinelli-originali/`.

Eseguire `python3 scripts/build.py` per rigenerare il sito e verificare `dist/media-gallery.html` e `dist/africa-famiglia.html`. La timeline è ordinata per narrazione, non pretende di datare gli eventi senza prove.

**Non unire questo ramo alla versione pubblica finché i nove file JPG non siano presenti e verificati.**
