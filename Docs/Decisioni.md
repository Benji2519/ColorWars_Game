# Registro delle decisioni

## M001 — Directory principale e documentazione

- **Data:** 5 novembre 2026.
- **Stato:** approvata dall'utente nella chat Management.
- **Ambito:** directory principale; nessuna modifica a `Content`.

### Decisione

Conservare la struttura standard di Unreal e mantenere `ArtSource` per i sorgenti
artistici. Introdurre `Docs` e il README principale. Predisporre `Tools` per gli
strumenti condivisi, mantenendo gli script specifici vicino ai rispettivi sorgenti.
Classificare i materiali in `Saved` e archiviare quelli utili fuori dall'area ignorata.
Rendere `Build` versionabile per le risorse originali e destinare i futuri pacchetti
distribuibili a `Releases`.

### Applicazione

Le copie recuperate da `Saved` sono datate e accompagnate da un manifesto con hash
SHA-256. Gli originali restano disponibili perché gli script esistenti usano ancora
alcuni percorsi in `Saved`. Questo intervento non esegue importatori, non cambia
configurazioni di gameplay e non rimuove file dalla cronologia Git.

### Conseguenze

Documentazione, riferimenti e report recuperati possono essere versionati. I nuovi
file soluzione `.slnx` sono ignorati, come le altre soluzioni rigenerabili. Le copie
storiche non rappresentano una verifica nuova degli asset attuali.

## Come registrare una nuova decisione

Usare un identificativo progressivo e indicare data, stato (proposta/approvata/superata),
ambito, scelta, motivo e conseguenze. Una proposta non diventa approvata per il solo
fatto di essere inserita in questo file.
