# Combo spada derivata dagli attacchi unarmed

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
I report di controllo delle tracce e rilettura dei file salvati sono in
`Saved/Codex/SwordComboRevision`.
La vecchia versione creata da zero resta nella cartella ArtSource/SwordCombo;
questa cartella SwordComboRevision contiene la revisione da usare.
