# Struttura della directory principale

Convenzione adottata il 5 novembre 2026. Si applica alla radice di ColorWars;
l'organizzazione interna di `Content` resta fuori da questo intervento.

## Directory

| Percorso | Responsabilità | Conservazione |
| --- | --- | --- |
| `Source/` | Codice C++ e regole di compilazione | Git e backup |
| `Config/` | Configurazioni condivise del progetto | Git e backup; valutare separatamente le preferenze personali |
| `Content/` | Asset Unreal e mappe | Git/LFS e backup |
| `ArtSource/` | File artistici modificabili, esportazioni, riferimenti e anteprime da conservare | Git e backup |
| `Docs/` | Linee guida, decisioni e report utili | Git e backup |
| `Tools/` | Strumenti condivisi del progetto e archivio di script storici | Git e backup |
| `Build/` | Eventuali risorse originali per packaging e piattaforme, per esempio icone | Versionabile; non confondere con una build distribuibile |
| `Plugins/` | Eventuali plugin locali del progetto | Conservare sorgenti, descrittori e risorse; valutare dipendenze binarie |
| `Binaries/` | Moduli ed eseguibili compilati | Locale, esclusa da Git |
| `Intermediate/` | File intermedi della compilazione e dell'editor | Locale, esclusa da Git |
| `DerivedDataCache/` | Cache dei dati elaborati | Locale, esclusa da Git |
| `Saved/` | Autosalvataggi, log, configurazioni locali e lavoro temporaneo | Locale, esclusa da Git; controllare prima di pulire |
| `Releases/` | Futuri pacchetti del gioco da distribuire | Esclusa da Git; archiviare le consegne separatamente |

`Build`, `Plugins` e `Releases` si creano quando servono; non occorrono cartelle vuote.
I plugin presenti nell'installazione di Unreal non richiedono una copia in `Plugins`.

## File alla radice

- `ColorWars.uproject`: descrittore del progetto, versione del motore, modulo e plugin.
- `README.md`: ingresso alla documentazione e istruzioni di apertura.
- `.gitignore`: esclusioni per file generati e dati locali.
- `.gitattributes`: regole Git LFS, attualmente per `.uasset` e `.umap`.
- `.git/`: cronologia e stato del repository locale; non è una cartella di lavoro.
- `*.slnx` e `*.sln`: soluzioni dell'ambiente di sviluppo; rigenerabili. I nuovi file sono ignorati; quelli già tracciati restano tali finché non si decide esplicitamente di rimuoverli dall'indice.

## Regole operative

1. Mantenere i nomi e la posizione delle directory standard di Unreal.
2. Salvare gli originali artistici in `ArtSource`, non in `Saved`.
3. Salvare documentazione e report da conservare in `Docs`.
4. Salvare i nuovi strumenti riutilizzabili in `Tools`; gli script specifici di un asset possono restare vicini ai suoi sorgenti.
5. Usare `Saved` come area temporanea. Promuovere i risultati utili prima di una pulizia.
6. Conservare le risorse originali di `Build`; indirizzare i pacchetti distribuibili a `Releases` o a una destinazione esterna.
7. Non archiviare una nuova copia completa del progetto dentro il progetto stesso.

## Controllo versione e backup

Le esclusioni Git non sostituiscono un backup. Gli autosalvataggi e le copie di
lavoro in `Saved` sono locali. Prima di eliminarli, verificare che i risultati
necessari siano stati salvati e che le copie archiviate siano leggibili.

Per eventuali plugin distribuiti senza sorgenti, conservare anche i binari
necessari: le esclusioni generiche di `Plugins/**/Binaries` e `*.dll` andranno
adattate al plugin concreto. Non presumere che tali binari siano ricompilabili.

Per nuovi formati artistici grandi, valutare Git LFS prima dell'aggiunta. Questa
riorganizzazione non migra la cronologia Git degli originali artistici.

## Fonti

- [Epic: Directory Structure](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-directory-structure)
- [Epic: Managing Game Code](https://dev.epicgames.com/documentation/en-us/unreal-engine/managing-game-code-in-unreal-engine)
- [Epic: Plugins](https://dev.epicgames.com/documentation/en-us/unreal-engine/plugins-in-unreal-engine)

`ArtSource`, `Docs`, `Tools` e `Releases` sono convenzioni adottate per ColorWars,
non directory obbligatorie prescritte da Epic.
