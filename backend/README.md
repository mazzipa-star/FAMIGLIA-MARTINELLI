# Accessi alle famiglie

Il sito resta statico finché `content/family-access-config.json` ha `enabled: false`. Nessuna password è contenuta nel sito. I pulsanti +/− dell’albero funzionano indipendentemente dagli accessi.

## Attivazione una tantum

1. Collegare un progetto Supabase del titolare. Applicare nell’ordine le due migrazioni in `supabase/migrations`, poi `supabase/seed.sql`. Il secondo import si interrompe prima di sovrascrivere eventuali modifiche già pubblicate.
2. Creare l’account personale del titolare in Supabase Auth. Confermare con lui l’indirizzo; inserire il suo UUID in `family_private.admins` dalla console amministrativa. Nessun utente può nominarsi amministratore dal sito.
3. Creare il bucket fotografie tramite `node provision-storage.mjs`, fornendo URL e chiave segreta nelle variabili d’ambiente. La chiave segreta non va salvata in file pubblici o nel repository. Impostare `family_private.settings.media_base` a `https://PROJECT.supabase.co/storage/v1/object/public/family-portraits/`.
4. Pubblicare la funzione `supabase/functions/family-invite` (il nome è conservato; ora assegna password e non invia inviti). Configurare `FAMILY_SITE_URL` con l’URL completo di `area-famiglie.html`. La funzione valida esplicitamente JWT e ruolo amministratore; per chiavi Supabase nuove configurare `verify_jwt = false` nel gateway, mantenendo obbligatori i controlli nel codice. I segreti Supabase restano esclusivamente nel servizio.
5. In Auth disabilitare le registrazioni pubbliche, abilitare email/password e impostare password minima 12 caratteri. Configurare URL sito e redirect esatto dell’area famiglie. Il recupero password richiede il servizio email configurato. Il titolare crea gli account dal pannello, assegna password e ramo e comunica personalmente le credenziali.
6. Inserire esclusivamente URL pubblico e chiave **publishable/anon** nella configurazione, attivare `enabled`, eseguire `npm ci && npm test && npm run build` nella cartella backend, poi `python scripts/build.py` dalla radice e pubblicare il sito.
7. Prima di consegnare: verificare sul servizio reale login amministratore, assegnazione account, accesso referente, aggiornamento pubblico da una seconda finestra, fotografia, revoca e recupero password. I test locali non sostituiscono questa verifica.

## Permessi

Pubblicazione diretta. Il referente modifica il capostipite assegnato, i discendenti e i loro coniugi; non i genitori del capostipite o gli altri figli dei coniugi. È possibile assegnare rami più piccoli ai singoli capi famiglia. Ruoli, email e cronologia rimangono privati. Ogni scrittura controlla nuovamente il ramo; la revoca opera anche sulle sessioni già aperte. Versioni e controlli di concorrenza evitano sovrascritture silenziose. La cronologia conserva anche fotografie precedenti; gli utenti non cancellano i file già caricati.

Il proprietario assegna o reimposta le password dal modulo amministrativo. Le password non sono conservate in tabelle applicative, restitute dalle API o scritte nei log del codice. Le credenziali non vengono inviate via email dalla funzione. Il recupero password personale resta disponibile tramite Auth.

## Verifiche locali

`npm test` esegue le migrazioni in PostgreSQL tramite PGlite e prova isolamento, utenti anonimi, revoca, genealogie cicliche, campi protetti, versioni e ripristini. `python seed.py` rigenera l’import iniziale dai contenuti correnti; non eseguirlo sul database già operativo.
