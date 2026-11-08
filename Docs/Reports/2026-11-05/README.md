# Recupero dei materiali da Saved

Il 5 novembre 2026 sono stati conservati fuori da `Saved` 57 file preesistenti.
Ogni copia è stata confrontata con l'origine tramite hash SHA-256. Gli originali
sono mantenuti e nessuno script di importazione è stato eseguito.

## Report storici

La sottocartella `Codex` conserva 11 file JSON nella struttura originale:

- `inspect_anim.json`, `inspect_blender_rig.json`, `inspect_tracks.json`: ispezioni storiche.
- `SwordCombo/`: report della prima combo, rig, materiali, preparazione e anteprima.
- `SwordComboRevision/`: sorgenti delle tracce, risultato dell'importazione e verifica dei file salvati della revisione.

I report possono descrivere versioni precedenti degli asset. La data dell'archivio
è la data della copia, non una nuova esecuzione dei controlli descritti nei file.
Gli errori o i risultati presenti nei report non sono stati modificati.

## Provenienza e destinazioni

- [ManifestoRecupero.json](ManifestoRecupero.json): elenco completo delle 57 copie con hash.
- [MaterialiSaved.md](../../MaterialiSaved.md): classificazione e regole di conservazione.
- [Archivio script](../../../Tools/Archive/BaseSoldier/2026-11-05/README.md): script e configurazione storici.
- [Archivio asset](../../../ArtSource/Archive/README.md): copie precedenti di asset Unreal.

I log grezzi, gli autosalvataggi e i dati diagnostici dell'editor rimangono in
`Saved`; non sono stati eliminati né aggiunti all'archivio dei report.
