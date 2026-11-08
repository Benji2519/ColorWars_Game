# ColorWars

Progetto di gioco per **Unreal Engine 5.8**, con un modulo C++ e asset Blueprint.
Questo documento descrive l'apertura del progetto e la sua directory principale.

## Aprire il progetto

1. Installare Unreal Engine 5.8 e, per compilare il codice, Visual Studio con gli strumenti C++ per Unreal.
2. Se il progetto viene recuperato da Git, installare Git LFS ed eseguire `git lfs pull` dalla directory principale: `.uasset` e `.umap` sono gestiti tramite LFS.
3. Aprire `ColorWars.uproject`. Se Unreal richiede di ricostruire il modulo ColorWars, consentire la compilazione dopo aver installato gli strumenti necessari.
4. Per lavorare sul C++, generare i file Visual Studio dal menu contestuale del `.uproject` quando necessario, poi aprire la soluzione generata.

La configurazione attuale apre `/Game/ColorWars/Maps/Lvl_Proto` e usa
`/Game/ColorWars/Core/BP_ColorWarsGameMode` come GameMode predefinito.
Queste informazioni derivano da `Config/DefaultEngine.ini`, non da una nuova prova del gioco.

## Dove trovare le informazioni

| Percorso | Contenuto |
| --- | --- |
| [Docs](Docs/README.md) | Indice delle linee guida e delle decisioni |
| [Struttura del progetto](Docs/StrutturaProgetto.md) | Ruolo delle directory, conservazione e Git |
| [Flusso di lavoro](Docs/FlussoDiLavoro.md) | Regole per modifiche, verifiche e consegna |
| [Visione del gioco](Docs/VisioneGioco.md) | Dati confermati e scelte di design ancora aperte |
| [Decisioni](Docs/Decisioni.md) | Scelte organizzative approvate |
| [Materiali recuperati da Saved](Docs/MaterialiSaved.md) | Classificazione e archivio del 5 novembre 2026 |
| [ArtSource](ArtSource/README.md) | Sorgenti artistici, riferimenti e anteprime |
| [Tools](Tools/README.md) | Convenzioni per strumenti condivisi e script storici |

## File originali e dati generati

Conservare `ColorWars.uproject`, `Source`, `Config`, `Content`, `ArtSource`, `Docs`,
`Tools` e le configurazioni Git. Conservare anche eventuali risorse originali in
`Build` e plugin locali in `Plugins`, quando presenti.

`Binaries`, `Intermediate` e `DerivedDataCache` sono dati ricostruibili. `Saved`
contiene anche autosalvataggi e materiali di lavoro: controllarne il contenuto prima
di una pulizia. I pacchetti distribuibili futuri vanno in `Releases`, esclusa da Git.

La riorganizzazione del 5 novembre 2026 riguarda la directory principale e la
documentazione. Non modifica gli asset in `Content`.

Riferimento: [struttura delle directory Unreal, documentazione Epic](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-directory-structure).
