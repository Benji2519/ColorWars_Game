# Materiali in Saved

Classificazione eseguita il 5 novembre 2026. `Saved` rimane esclusa da Git.
Non sono state eliminate cartelle o copie di lavoro.

## Materiali conservati fuori da Saved

Sono stati recuperati **57 file** con copia verificata tramite SHA-256.
Il [manifesto](Reports/2026-11-05/ManifestoRecupero.json) riporta per ogni file
origine, destinazione, categoria, dimensione e hash.

| Origine | File | Destinazione stabile |
| --- | ---: | --- |
| `Saved/Codex/**/*.json` | 11 | `Docs/Reports/2026-11-05/Codex/` |
| `Saved/Codex/*.py` | 10 | `Tools/Archive/BaseSoldier/2026-11-05/` |
| `Saved/CodexWeaponRefs/import_weapon_icons.json` | 1 | `Tools/Archive/BaseSoldier/2026-11-05/WeaponIcons/` |
| Backup `.uasset` in `Saved/Codex` | 9 | `ArtSource/Archive/UnrealAssets/2026-11-05/` |
| FBX e texture esportate in `Saved/Codex/SwordCombo` | 5 | `ArtSource/Items/Weapons/Sword_01/UnrealExports/2026-11-05/` |
| `Saved/Codex/SwordCombo/preview_*.png` | 11 | `ArtSource/Characters/BaseSoldier/SwordCombo/UnrealPreview/2026-11-05/` |
| Immagini in `Saved/CodexWeaponRefs` | 8 | `ArtSource/References/Weapons/2026-11-05/` |
| `Saved/Screenshots` e `Saved/AutoScreenshot.png` | 2 | `ArtSource/References/Screenshots/2026-11-05/` |

Queste destinazioni sono l'archivio della fotografia del 5 novembre. I file non
sono stati riscritti: eventuali percorsi interni e risultati si riferiscono alla
lavorazione originaria. Le copie `.uasset` sono fuori da `Content` e non entrano
nel gioco. La corrispondenza delle copie non è una nuova validazione del gameplay.

## Perché gli originali restano

Gli script `create_sword_combo.py`, `revise_sword_combo.py` e gli importatori in
`ArtSource/Characters/BaseSoldier` fanno ancora riferimento a `Saved/Codex`.
Alcuni leggono report o esportazioni da lì; altri vi scrivono risultati o backup.
Gli asset Unreal possono inoltre conservare riferimenti ai percorsi di importazione.
Le copie stabili permettono di conservare i dati senza cambiare questi flussi.

Le copie non si aggiornano automaticamente. Una futura lavorazione deve produrre
un nuovo report o un nuovo archivio datato, senza sovrascrivere questo storico.
Prima di eliminare gli originali, aggiornare e verificare i percorsi dei flussi
interessati nell'ambito di un'attività dedicata.

## Classificazione dei dati rimasti

| Percorso o tipo | Ruolo | Regola |
| --- | --- | --- |
| `Autosaves/` | Recupero di lavoro non salvato | Controllare prima di eliminare; non usarla come unico backup |
| `Config/` | Impostazioni locali e dell'utente | Condividere in `Config/` alla radice soltanto le impostazioni deliberate del progetto |
| `Logs/`, `Crashes/` | Diagnostica dell'editor | Locali; conservare in Docs solo gli estratti necessari a un problema documentato |
| `Codex/*.log` | Log e tentativi storici delle lavorazioni | Lasciati locali; i report JSON sono archiviati, i log grezzi non sono stati copiati |
| `ShaderDebugInfo/`, `UnrealBuildTool/` | Diagnostica di shader e compilazione | Locali e rigenerabili secondo il flusso che li produce |
| `SourceControl/` | Dati locali di integrazione con il controllo versione | Non sostituisce `.git` e la cronologia del repository |
| File `*.tmp` | File temporanei dell'editor | Non considerarli risultati finali; valutarli solo dopo chiusura e verifica dei salvataggi |
| `CodexVideoFrames/`, `Collections/`, `Interchange/` | Cartelle risultate vuote all'inventario | Nessun materiale da recuperare in questa operazione |

## Regola per i prossimi lavori

Usare `Saved` per elaborazione e diagnosi temporanea. Prima di concludere un'attività:

1. Conservare sorgenti e riferimenti utili in `ArtSource`.
2. Conservare gli strumenti riutilizzabili in `Tools` o accanto all'asset specifico.
3. Conservare report finali e istruzioni in `Docs`.
4. Verificare le copie e annotarne la provenienza.
5. Eliminare eventuali residui solo dopo aver controllato autosalvataggi e dipendenze dei percorsi.
