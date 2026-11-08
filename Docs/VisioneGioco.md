# Visione del gioco

Documento iniziale del 5 novembre 2026. Le scelte di design non ancora discusse
restano aperte: la presenza di un asset non costituisce una decisione di gameplay.

## Stato osservato

- Nome del progetto e del modulo C++: `ColorWars`.
- Versione associata nel `.uproject`: Unreal Engine 5.8.
- Mappa iniziale configurata: `/Game/ColorWars/Maps/Lvl_Proto`.
- GameMode predefinito configurato: `/Game/ColorWars/Core/BP_ColorWarsGameMode`.
- Sono presenti sorgenti artistici del BaseSoldier e delle animazioni con spada.
- Sono presenti nel codice le varianti Combat, Platforming e SideScrolling; il loro ruolo nel gioco finale non è definito da questa documentazione.

## Da definire insieme

| Tema | Decisione da prendere |
| --- | --- |
| Identità | Descrizione del gioco e ruolo dei colori |
| Esperienza principale | Cosa fa il giocatore e quale obiettivo persegue |
| Modalità | Singolo giocatore, multigiocatore o entrambe |
| Piattaforme e comandi | Dispositivi di destinazione e sistemi di input supportati |
| Combattimento | Armi, regole, ritmo e condizioni di vittoria/sconfitta |
| Direzione artistica | Stile, proporzioni, palette e riferimenti approvati |
| Primo prototipo | Funzionalità minime e criteri di completamento |

Le decisioni approvate vengono registrate in [Decisioni.md](Decisioni.md) e poi
integrate qui. Non sono ancora fissate scadenze o priorità di gameplay.
