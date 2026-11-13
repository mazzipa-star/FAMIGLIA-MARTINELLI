# Raccolta materiali — email e Google Drive

Indirizzo confermato dall’amministratore: pamazzi59@gmail.com.

## Stato

- Pagina Contribuisci all’album predisposta e alternativa email configurata.
- Il pulsante email apre la posta con destinatario, oggetto e traccia del messaggio. Non invia automaticamente né allega file da solo.
- È disponibile il pulsante Copia indirizzo per chi usa la webmail.
- Il modulo Google deve ancora essere creato nell’account pamazzi59@gmail.com; è richiesto l’accesso del titolare.
- Finché non viene collegato un modulo reale, la pagina indica chiaramente che il caricamento Google non è ancora attivo.

## Modulo Google da creare

Titolo: Condividi un ricordo — Famiglia Martinelli.
Campi: nome e cognome, email, titolo del ricordo, descrizione, persone/luogo/data anche approssimativa, file allegati (multipli), eventuale link a file grandi, conferma di poter condividere il materiale per la valutazione prima della pubblicazione.

Creare il modulo in Il mio Drive dell’account pamazzi59@gmail.com e scegliere Caricamento di file per gli allegati. I visitatori dovranno accedere con il proprio account Google. Non rendere pubbliche le risposte né la cartella degli allegati. Pubblicare l’accesso per i rispondenti senza limitare ai soli utenti di una organizzazione, se l’account lo permette.

Nella scheda Risposte, menu a tre puntini, attivare Ricevi notifiche email per le nuove risposte. Le email normali arrivano invece direttamente a pamazzi59@gmail.com e i loro allegati vanno salvati nel Drive dall’amministratore.

Verificare un invio di prova e la ricezione della notifica con il titolare. Poi copiare il link pubblico del modulo in content/deposit-config.json, form_url; mantenere provider=google e impostare notification_verified=true. Non pubblicare il link di modifica del modulo.

Il sito apre il modulo in una nuova finestra per agevolare accesso Google e allegati, anziché incorporare un modulo di caricamento non utilizzabile in alcuni contesti.

Rigenerare con python3 scripts/build.py e caricare su main per aggiornare GitHub Pages.

Fonti Google:
- https://support.google.com/docs/answer/7322334
- https://support.google.com/docs/answer/139706?hl=it
- https://support.google.com/docs/answer/15473134?hl=en-GB
