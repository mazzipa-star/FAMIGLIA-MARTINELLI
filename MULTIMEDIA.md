# Audio e video ospitati nel sito

I filmati pubblicati sono copie per il web degli originali presenti nell’archivio del titolare. Gli originali MOV non sono stati modificati né aggiunti al repository.

- La storia della famiglia Martinelli: originale `FAMIGLIA MARTINELLI.mov`, durata 9 minuti e 14 secondi circa. La copia YouTube e quella Vimeo erano riferimenti allo stesso filmato.
- La marmellata di Caprino: originale `videoclip/Marmellata di Caprino.mov`, durata 1 minuto e 23 secondi circa.
- Una giornata particolare: originale `videoclip/Matrimonio Anna e Vera.mov`, durata 2 minuti e 41 secondi circa. Utilizzata la versione originale 720p, non il duplicato 480p.

Le copie MP4 usano H.264 e audio AAC, pixel format yuv420p e intestazione faststart. Il primo filmato è stato portato da 60 a 30 fotogrammi al secondo; le dimensioni delle immagini sono conservate. I due racconti hanno anche una traccia M4A per l’ascolto senza video.

Le pagine `media-gallery.html` e `gli-audio.html` usano lettori HTML nativi con comandi, riproduzione inline su telefono, schermo intero video e collegamenti per scaricare i file. Nessuna riproduzione automatica e nessun precaricamento dei filmati all’apertura delle pagine. I poster sono fotogrammi dei filmati.

Per spostare i file in futuro, aggiornare la funzione `media_player` in `scripts/build.py`. L’elenco delle copie e le impronte SHA-256 sono in `content/local-media.json`.
