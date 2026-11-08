# Flusso di lavoro

## Prima di una modifica

1. Leggere il README e la guida relativa all'attività.
2. Controllare le modifiche già presenti; non sovrascrivere il lavoro in corso.
3. Definire l'ambito e l'esito atteso. Per una modifica artistica indicare il sorgente, l'esportazione e l'asset di destinazione.

## Durante il lavoro

- Tenere i sorgenti artistici e le anteprime utili in `ArtSource`.
- Documentare i requisiti di ogni nuovo strumento: applicazione, dipendenze, input, output ed eventuali scritture di asset.
- Usare percorsi relativi alla radice del progetto nei nuovi strumenti, evitando il nome utente o percorsi del computer dell'autore.
- Tenere il lavoro temporaneo in `Saved`; al termine conservare i risultati necessari nelle destinazioni descritte in [MaterialiSaved.md](MaterialiSaved.md).
- Aggiornare la documentazione quando cambia una procedura.

## Verifica e consegna

Le verifiche devono corrispondere alla modifica: per documentazione controllare
collegamenti e percorsi; per codice compilare il modulo coinvolto; per asset
controllare importazione e comportamento nell'editor quando l'attività lo richiede.
Un report storico non dimostra che la versione attuale del gioco sia stata verificata.

Riportare cosa è cambiato, quali verifiche sono state eseguite e cosa resta aperto.
Non dichiarare un'importazione riuscita sulla sola base dell'esportazione da Blender.

## Pulizia e distribuzione

- Prima di pulire cartelle generate, chiudere Unreal e i processi di compilazione.
- Controllare autosalvataggi, screenshot e materiali unici di `Saved`.
- Non eliminare originali in `ArtSource`, risorse di `Build` o binari di plugin senza sorgenti considerandoli cache.
- Una build del gioco da consegnare va in `Releases` o fuori dal progetto; conservarla separatamente dal repository dei sorgenti.

## Ambito di questa riorganizzazione

Il 5 novembre 2026 sono autorizzate modifiche esterne a `Content`; `Content` è
esclusa. Gli script storici capaci di scrivere asset vengono solo conservati e
documentati, senza eseguirli. Attività future devono dichiarare il proprio ambito.
