# Base Soldier v3 - mani a guanto

Aprire `CW_BaseSoldier_v3.blend`. Il file v2 e la sua esportazione sono conservati.

Le quattro dita di ciascuna mano sono sostituite da un volume arrotondato chiuso,
con un piccolo pollice integrato nella stessa superficie. Colore e proporzioni del
personaggio sono invariati. Ogni mano segue il rispettivo osso `hand.L` / `hand.R`.
Le ossa delle dita sono mantenute per compatibilita della gerarchia, ma non hanno
piu vertici assegnati. Il pollice non si articola separatamente.

Il file FBX v3 contiene la mesh aggiornata e il rig. La reimportazione in Blender e
i controlli dei pesi sono riportati in `CW_BaseSoldier_v3_validation.json`.
L'importazione in Unreal non e stata ancora verificata.

La collection nascosta `01_EDITABLE_PARTS` contiene anche le nuove mani sorgenti.
La collection `02_CHARACTER_AND_RIG` contiene il personaggio completo.
Le anteprime v3 sono nella cartella `Design/Characters` del progetto.

Per future prese di armi si potra adattare la posa della mano o creare una variante
chiusa; questa versione presenta una forma rilassata senza dita individuali.
