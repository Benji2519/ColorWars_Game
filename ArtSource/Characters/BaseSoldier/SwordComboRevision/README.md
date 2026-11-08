# Combo spada derivata dagli attacchi unarmed

Nota del 5 novembre 2026: i risultati descritti qui appartengono alla lavorazione
originaria. La riorganizzazione della directory principale conserva i report,
senza eseguire nuovamente l'importazione o le verifiche degli asset in Unreal.

Le tre Sequence sono adattamenti di AS_BaseSoldier_Attack_01, 02 e 03.
Conservano frame rate, durata, Root Motion, passi e tracce di gambe, bacino,
busto, testa e clavicole. Le modifiche riguardano braccia, mani e presa.

| Sequence | Base | Colpo | Durata | Avanzamento originale |
|---|---|---|---|---|
| AS_BaseSoldier_Attack_Sword_01 | Attack_01 | Fendente diagonale | 1 s | 102,25 cm |
| AS_BaseSoldier_Attack_Sword_02 | Attack_02 | Taglio di ritorno | 1 s | 61,10 cm |
| AS_BaseSoldier_Attack_Sword_03 | Attack_03 | Colpo dall'alto | 1,667 s | 146,64 cm |

Asset in `/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword`.
I tre Montage AM_BaseSoldier_Attack_Sword_01/02/03 derivano dai rispettivi
Montage originali e puntano alle nuove Sequence. Possono sostituire i Montage
unarmed nella selezione delle animazioni dell'arma. Il controllo delle tre
Sequence e dei tre Montage riaperti da disco è superato, comprese le pose
RAW e compresse a ogni frame. I Blueprint non sono modificati.
Le transizioni tra attacchi utilizzano il sistema di combo/blend del gioco,
come negli originali: le pose di tutto il corpo ai confini non sono identiche.

Preview mesh SKM_BaseSoldier e Sword_01 sullo SwordSocket esistente.
SwordCombo_Revised.gif mostra il risultato sul rig sorgente, con camera che segue
il personaggio e pavimento a scacchi per rendere visibile il movimento.

`BaseSoldier_SwordCombo_Adapted.blend` contiene le azioni modificabili.
`adapted_keys.json` contiene le sole modifiche delle braccia nel riferimento Unreal.
I report storici di controllo delle tracce e rilettura dei file salvati sono in
`Docs/Reports/2026-11-05/Codex/SwordComboRevision`.
Le copie precedenti degli asset sono in
`ArtSource/Archive/UnrealAssets/2026-11-05/SwordComboRevision`.
Gli originali restano in `Saved/Codex/SwordComboRevision` per i flussi esistenti.
La vecchia versione creata da zero resta nella cartella sorella `SwordCombo`;
questa cartella `SwordComboRevision` contiene la revisione da usare secondo
la documentazione della lavorazione originaria.
