# Sorgenti artistici

Questa cartella conserva il materiale modificabile e i risultati artistici che
devono sopravvivere alla pulizia delle cartelle generate di Unreal.

| Percorso | Contenuto |
| --- | --- |
| [Characters/BaseSoldier](Characters/BaseSoldier/README_v3.md) | Sorgenti del personaggio e script specifici |
| [Characters/BaseSoldier/SwordCombo](Characters/BaseSoldier/SwordCombo/README.md) | Prima versione della combo con spada, conservata come storico |
| [Characters/BaseSoldier/SwordComboRevision](Characters/BaseSoldier/SwordComboRevision/README.md) | Revisione indicata dalla documentazione esistente come versione da usare |
| `Characters/BaseSoldier/SwordCombo/UnrealPreview/2026-11-05/` | Fotogrammi storici recuperati da Saved |
| `Items/Weapons/Sword_01/UnrealExports/2026-11-05/` | Esportazione FBX e texture recuperate da Saved; non un nuovo sorgente artistico originale |
| `References/Weapons/2026-11-05/` | Immagini di riferimento storiche delle armi |
| `References/Screenshots/2026-11-05/` | Screenshot conservati per riferimento |
| [Archive/README.md](Archive/README.md) | Copie precedenti di asset Unreal, fuori dal contenuto caricato dal gioco |

## Regole

- Tenere insieme sorgente, esportazioni e istruzioni specifiche dell'asset.
- Distinguere originali modificabili, esportazioni da Unreal e semplici riferimenti.
- Documentare applicazione richiesta, scala, rig e destinazione di importazione quando noti.
- Conservare le versioni precedenti con un nome esplicito, senza sovrascriverle incidentalmente.
- Gli script di un singolo personaggio possono restare nella sua cartella. Gli strumenti riutilizzabili del progetto vanno in `Tools`.
- Tenere i fotogrammi intermedi riproducibili in `Saved`; conservare qui le anteprime scelte e i materiali unici.

Le immagini e gli asset recuperati il 5 novembre 2026 sono copie dei file locali
preesistenti. Provenienza e hash sono nel [manifesto](../Docs/Reports/2026-11-05/ManifestoRecupero.json).
La copia non attribuisce nuove licenze ai materiali di riferimento.
