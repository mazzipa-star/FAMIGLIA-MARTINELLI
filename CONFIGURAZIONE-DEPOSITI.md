# Raccolta materiali — email e Google Drive

Aggiornamento del 13 novembre 2026: modulo pubblicato e raccolta attiva.

## Stato verificato

- Pagina Contribuisci collegata al modulo Google e alternativa email a pamazzi59@gmail.com.
- Modulo creato nell’account pamazzi59@gmail.com; i file vengono raccolti nel Drive di quell’account.
- Link di compilazione: https://docs.google.com/forms/d/e/1FAIpQLSdnmBtVMwouI4kzbyh0KtIthRhpPaYe_-O5CnEpLbGsqhqxyQ/viewform
- Rispondenti: chiunque abbia il link, con accesso a Google necessario per gli allegati. Il riepilogo delle risposte NON è pubblico.
- Fino a 10 file per invio, da 10 MB ciascuno. Tipi consentiti: documenti, PDF, immagini, audio e video. Limite cumulativo iniziale del modulo: 1 GB. Al raggiungimento del limite il servizio interrompe la raccolta di nuove risposte; l’amministratore può gestirlo nelle impostazioni Google in base allo spazio disponibile sul proprio Drive.
- Nome, email, titolo, descrizione e conferma di poter condividere sono obbligatori. Allegati facoltativi per consentire anche racconti solo scritti. Nella descrizione si possono indicare periodo e link a file grandi.
- Notifiche email abilitate nel menu Risposte. Verificato un invio tecnico con verifica-deposito.txt, senza immagini o dati familiari: il modulo ha confermato la ricezione, è comparsa 1 risposta e l’avviso di Moduli Google è stato trovato nella casella dell’amministratore. La prova è etichettata esplicitamente come non destinata alla pubblicazione e resta separata dai contenuti del sito.
- Nessuna pubblicazione automatica dei contributi.

## Gestione

Accedere a Google con pamazzi59@gmail.com e aprire il modulo da Moduli Google. La scheda Risposte mostra i nuovi contributi; il campo degli allegati permette di aprire la cartella Drive. Non condividere la cartella con accesso pubblico. Per pubblicare materiale selezionato nel sito, copiarlo nel progetto e aggiungere descrizione, provenienza e data quando note.

Le email normali arrivano direttamente a pamazzi59@gmail.com; gli allegati email vanno salvati nel Drive dall’amministratore.

Il pulsante email apre la posta e NON allega o invia automaticamente: chi contribuisce deve completare il messaggio e premere Invia. Il pulsante Copia indirizzo consente di usare una webmail.

## Configurazione del sito

content/deposit-config.json contiene il solo URL pubblico del modulo e l’indirizzo scelto per ricevere i materiali, senza credenziali. Il generatore valida il link e richiede notification_verified=true prima di attivare il modulo. notification_delivery_confirmed documenta la verifica della consegna. Per aggiornare il collegamento, modificare form_url, rigenerare con python3 scripts/build.py e caricare su main.

Fonti Google:
- https://support.google.com/docs/answer/7322334
- https://support.google.com/docs/answer/139706?hl=it
- https://support.google.com/docs/answer/15473134?hl=en-GB
