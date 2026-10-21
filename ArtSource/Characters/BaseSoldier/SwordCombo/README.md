# BaseSoldier: combo con spada

Tre Animation Sequence originali, animate sul rig di BaseSoldier a 30 fps:

| Asset | Movimento | Durata |
|---|---|---:|
| AS_BaseSoldier_Attack_Sword_01 | Fendente diagonale dalla destra del personaggio | 0,70 s |
| AS_BaseSoldier_Attack_Sword_02 | Taglio di ritorno | 0,70 s |
| AS_BaseSoldier_Attack_Sword_03 | Colpo dall'alto e ritorno in guardia | 1,10 s |

Le pose finali di 01 e 02 coincidono con le pose iniziali del colpo successivo.
Gli attacchi sono in-place, con piedi appoggiati. La traslazione verso il nemico
resta affidata al movimento del personaggio.

## Asset Unreal

Cartella: `/Game/ColorWars/Characters/BaseSoldier/Animations/Anim/Attack/Sword`

`AM_BaseSoldier_Sword_Combo` contiene 01, 02 e 03 consecutivamente nel `DefaultSlot`,
per una durata totale di 2,50 secondi. Aprilo per vedere tutta la combo. Per usarlo
nel gioco, assegnalo alla logica di attacco del personaggio: la generazione degli
asset non modifica i Blueprint di combattimento, gli input o le finestre di danno.

Preview Mesh: `SKM_BaseSoldier`. Lo scheletro esistente mantiene `Sword_01`
come asset di anteprima sul `SwordSocket`, inclusi offset e scala del socket.
La spada rimane un asset separato: non viene incorporata nelle animazioni.

## Sorgenti e anteprime

- `BaseSoldier_SwordCombo.blend`: rig originale e quattro azioni; le prime tre
  sono i singoli attacchi, la quarta è l'anteprima continua della combo.
- I tre FBX corrispondenti alle Animation Sequence permettono il reimport.
- `BaseSoldier_SwordCombo_Preview.gif`: anteprima animata della combo.
- `BaseSoldier_SwordCombo_ContactSheet.png`: pose principali.

Gli script di creazione, importazione e anteprima sono nella cartella superiore.
Le tre copie precedenti sono conservate in
`Saved/Codex/SwordCombo/previous_assets`, esternamente alla cartella Content.
I report di verifica sono in `Saved/Codex/SwordCombo`.
