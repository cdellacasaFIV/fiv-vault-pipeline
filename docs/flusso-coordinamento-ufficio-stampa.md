# Flusso di lavoro coordinato — Comunicazione FIV

Progetto di sistema condiviso per Ufficio Stampa, Social, settori e Presidenza.
Versione 2 dell'8 novembre 2026: ruoli confermati da Carlo Dellacasa, settori definiti, scelta della piattaforma.

---

## 1. Da dove parte l'analisi

Fonti lette:
- le circa 75 sessioni Claude Code dal 7 settembre all'8 novembre 2026 (solo titoli ed esiti; aperte per intero solo due);
- il database Notion «FIV — Planner Operativo / Task FIV»;
- il calendario Google «Comunicazione FIV» e l'elenco dei calendari condivisi;
- la skill `planner-operativo-mail-calendario-fiv` e le altre skill FIV installate;
- questo repository, cioè la pipeline del vault.

Non ho potuto leggere le chat di claude.ai: da qui non ho uno strumento per farlo. Il quadro viene quindi dalle sessioni di lavoro, da Notion e dal calendario. Le chat personali o fuori dal perimetro FIV sono state escluse.

### 1.1 Cosa fa l'ufficio, per famiglie di lavoro

| Famiglia | Esempi dalle sessioni (set–nov 2026) |
|---|---|
| Risultati e news sportive | Europeo Optimist a squadre, Team Race RS21, Middle Sea Race, Switch, Classi Foil, eSailing, Hansa, Melges 24, podi 2026 |
| Testi istituzionali e a firma | intervista al Presidente per l'inserto del 31/10, frasi del Presidente, collari d'oro CONI, prefazioni, saluti, lettere, certificazione ISO |
| Siti e sviluppo web | tema Sport Vela, velascuola.net, sito eSailing, sito dual career, «Voce delle zone», timeline Para Sailing, speciale Vilamoura, federvela.it |
| Video e TV | We Sail TV, reel Terra Maris, Velando 2, video UniCredit, sigla, archivio TV FIV, streaming |
| Foto e archivio | digiKam, Flickr, accrediti fotografici, ritocchi, didascalie |
| Dati e classifiche | programma classifiche FIV, lettore Sailwave, classifiche Primavela, Giovanili e Altura, conti dei premi, Scuole Vela, pipeline World Sailing |
| Partner e marketing | UniCredit Navigare Insieme, Edison Next / CICO, AIRC, SailGP, Saloni, Italpress, studio Open Economics |
| Newsletter e contatti | campagne Brevo, contatti condivisi, API tessere |
| Gestione ufficio | fatture, delibere, hosting, stampe, PC, formazione obbligatoria |

[INFERITO] Le sessioni su web e video sono quasi quante quelle di scrittura. Oggi il lavoro dell'ufficio è redazione più produzione più sviluppo, e passa quasi tutto da una persona sola.

### 1.2 Il planner Notion attuale

Numeri estratti dal database «Task FIV» l'8/11/2026:

| Voce | Valore |
|---|---|
| Righe totali dal 28 aprile | 833 |
| Ancora «Da fare» o «In corso» | 570 |
| — di cui «Regata in arrivo…», copiate dal calendario | 152 |
| — di cui altre attività | 418 |
| — — create prima del 1° ottobre | 127 |
| — — con scadenza già passata | 98 |
| Segnate «Fatto» | 1 |
| Righe per lo stesso Europeo Junior 49er | 19 |
| Righe per la stessa richiesta Open Economics | 9 |
| Righe per la stessa formazione Whistleblowing | 6 |
| Righe «Valutare … comunicato» | 111 |
| Utenti del workspace | 1 (Carlo) |

Cause: nessun controllo dei duplicati; regate del calendario copiate ogni giorno; nessuna chiusura; il campo «Chi» mescola persone e categorie; mancano i settori; nessun collega dentro.

[INFERITO] Le attività davvero aperte sono probabilmente tra 100 e 180. Il numero preciso esce solo dalla pulizia (§ 9, fase 0).

---

## 2. La regola che rende il sistema credibile

«Nessuno può dire che non sapeva» si regge su quattro condizioni. Lo strumento serve solo a tenerle in piedi:

1. **Un solo punto di ingresso.** Se una cosa non è nel sistema, per il gruppo non esiste.
2. **Un solo responsabile per attività**, con nome e cognome.
3. **Uno stato sempre vero**, aggiornato quando cambia qualcosa.
4. **Un rito fisso**: 20 minuti il lunedì sulla stessa vista.

Il sistema proprietario (§ 6) permette un quinto elemento che gli strumenti generici non danno bene: la **presa visione registrata**. Quando un'attività viene assegnata o passa di mano, il destinatario riceve la mail e il sistema registra data e ora in cui l'ha aperta. È la prova concreta che la cosa è arrivata.

La regola del punto unico di ingresso va annunciata dal Segretario Generale (Volandri) o dal consigliere referente per la comunicazione (Leonardi), non dall'Ufficio Stampa.

---

## 3. Stati, priorità, date

Le tue categorie iniziali (programmato, a calendario, urgente, da studiare) mescolano tre cose diverse: a che punto è il lavoro, se dipende da una data, quanto è prioritario. Le separo così.

**Stato, cioè il flusso:**
```
📥 In arrivo → 🔍 Da studiare → 📅 Programmato → ✍️ In lavorazione → 👀 In revisione → ✅ Approvato → 🚀 Pubblicato / Consegnato
                                     ↘ ⏸️ In attesa di altri (chi + da quando)     ↘ ✖️ Non si fa (motivo)
```
**Priorità:** 🔴 Urgente · 🟠 Alta · 🟡 Normale · ⚪ Quando possibile.
**Date:** data di uscita · scadenza interna per la bozza · evento collegato (si collega dal calendario, non si duplica).

---

## 4. Persone e ruoli

### 4.1 Ruoli confermati

| Persona | Ruolo nel flusso |
|---|---|
| Carlo Dellacasa | Responsabile Ufficio Stampa; amministratore del sistema; approva tutto ciò che esce |
| Matteo Calautti | Social media manager; gestisce il calendario «Comunicazione FIV» |
| Fabio Colivicchi | Comunicati evento |
| Federica Piraino | Comunicazione Para Sailing |
| Eugenio Catalani | Video (collaboratore esterno) |
| Martina Orsini | Foto (collaboratrice esterna) |
| Elisa Crosta | Segreteria di Presidenza: richieste di testi a firma, programmi, lettere |
| Carrara, De Giuli, Freschi | Ufficio Marketing |
| Paola Massone | Velascuola e Scuola |
| Bodrato | Settore olimpico |
| Ciampolini | Settore giovanile |
| Valentina Balbi | Settore Para Sailing (parte sportiva) |
| Procopio | Confindustria Nautica e Velista dell'Anno |
| Volandri | Segretario Generale; news generiche, meno frequenti |
| Leonardi | Consigliere referente per la comunicazione |
| Foschini | Consigliere referente per giovanile, Team Race e Match Race |
| Belgrano | IT |

### 4.2 Quattro livelli di accesso

Non tutti devono lavorare la bacheca. Se si dà a 19 persone lo stesso accesso, il sistema diventa rumore. Propongo quattro livelli:

| Livello | Chi | Cosa fa |
|---|---|---|
| **Operativo** | Carlo, Calautti, Colivicchi, Piraino, Catalani, Orsini | lavora le attività, cambia gli stati, consegna |
| **Referente di settore** | Bodrato, Ciampolini, Balbi, Massone, Crosta, Volandri, Procopio, Marketing | apre richieste con un modulo, vede lo stato delle proprie, approva i contenuti del proprio settore quando serve |
| **Consigliere** | Leonardi (tutto ciò che non è riservato), Foschini (i suoi settori) | sola lettura + riepilogo settimanale via mail |
| **Tecnico** | Belgrano | accessi, sicurezza, backup; nessun contenuto |

Per i referenti il sistema è quasi invisibile: un modulo per chiedere e una mail quando la loro richiesta cambia stato. È il modo più realistico per farli partecipare.

---

## 5. Settori: struttura definitiva

### 5.1 Criterio

Un settore esiste solo se ha **un referente e un flusso regolare** di lavoro. Le cose rare non diventano settori: hanno un'etichetta di origine.

Ogni attività ha **un solo settore principale**. Una notizia Team Race U17 va in Team Race, non in Giovanile e Team Race insieme. Così è sempre chiaro chi la segue e chi la approva. Sotto il settore c'è un'**origine**, per sapere da dove arriva la richiesta.

### 5.2 Gli otto settori

| # | Settore | Referente | Cosa ci finisce | Origini / sotto-voci |
|---|---|---|---|---|
| 1 | **Olimpico** | Bodrato | classi olimpiche, squadre nazionali, convocazioni, Mondiali ed Europei, Youth Olympic Games | per classe |
| 2 | **Giovanile** | Ciampolini (cons. Foschini) | Optimist, Techno, ILCA 4/6, Campionati Giovanili, Primavela, Youth Worlds | per classe |
| 3 | **Team Race e Match Race** | cons. Foschini | Team Race U17, Sardinia TR World, RS21 TR, Match Race | — |
| 4 | **Para Sailing** | Balbi (sport), Piraino (comunicazione) | Para Sailing, Navigare Insieme, inclusione | — |
| 5 | **Altura, Offshore e Classi** | Carlo | Campionato Altura, Route du Rhum, Middle Sea Race, monotipi, eSailing | Altura · Offshore · Classi · eSailing |
| 6 | **Scuola e Territorio** | Massone (Scuola) | Velascuola, Scuole Vela, progetti MIM, comunicati di circoli e zone, «Voce delle zone» | Scuola · Zone · Circoli |
| 7 | **Istituzionale** | Crosta / Volandri (cons. Leonardi) | testi del Presidente, news della Segreteria Generale e di altri settori federali, CONI, Ministeri | Presidenza · Segreteria Generale · Consiglio federale · Altri settori |
| 8 | **Eventi, Partner e Marketing** | Marketing; Procopio | UniCredit, Edison Next / CICO, AIRC, Italpress, SailGP, Saloni, Confindustria Nautica, Velista dell'Anno, Vela Day, Giornata 10 dicembre, Calendario 2027 per i 100 anni | Partner · Evento federale · Saloni |
| — | **Gestione ufficio** (riservato, solo Carlo) | Carlo | fatture, delibere, contratti, strumenti, formazione | — |

Scelte fatte:
- **Social non è un settore.** È il canale di Calautti: ha una sua vista e riceve in automatico i passaggi dalle news, ma i contenuti appartengono ai settori.
- **Team Race e Match Race sono separati da Giovanile**, perché hanno un referente proprio e un flusso frequente: nel planner attuale sono tra le voci più presenti di ottobre.
- **Scuola e Territorio sono uniti**: la promozione di base passa da circoli e zone, e i 111 comunicati esterni da valutare arrivano quasi tutti da lì.
- **Le news della Segreteria Generale e di altri settori** vanno in Istituzionale con l'origine indicata: sono poche e non servono un settore proprio.
- **Foto, video e web non sono settori.** Sono tipi di lavoro (§ 5.3).

### 5.3 Tipo di lavoro e canale di uscita

**Tipo:** Comunicato / News · Risultato · Testo a firma · Intervista / Dichiarazione · Post social · Newsletter · Video · Foto / Gallery · Grafica / Locandina · Intervento sito · Copertura evento · Dati / Report · Comunicato esterno da valutare · Amministrativo · Studio.

**Canale:** federvela.it · Sport Vela · Social FIV · We Sail TV / YouTube · Newsletter Brevo · Stampa esterna / agenzie · Lettera / Protocollo · Uso interno · Partner.

### 5.4 Passaggi automatici tra sezioni

| Quando… | …nasce o succede | Chi riceve |
|---|---|---|
| un **intervento sito** va online con «Serve comunicazione esterna» | attività figlia «News / avviso» | Ufficio Stampa |
| una **news** è approvata e tra i canali c'è Social | attività figlia «Post social», con link | Calautti |
| una **news** con canale Newsletter è pubblicata | attività figlia «Invio Brevo» | Ufficio Stampa |
| un **testo a firma** va in revisione con approvazione del Presidente | mail a Crosta, attività «In attesa di Presidenza» | Carlo |
| un'attività resta in attesa oltre 3 giorni | entra nei Solleciti | Carlo |
| un **evento** del calendario viene scelto per la copertura | si crea il progetto con le sotto-attività prima, durante e dopo | referente del settore |
| un referente invia una **richiesta** | attività «In arrivo» + mail di conferma al referente | Carlo |

### 5.5 Modelli con sotto-passaggi

1. **Risultato / News sportiva:** fonte ufficiale verificata → bozza → verifica dei fatti → ok di Carlo → pubblicazione → post social (figlia) → newsletter se prevista → link in Esito.
2. **Testo a firma:** richiesta (destinatario, occasione, lunghezza, scadenza) → materiali di contesto → bozza → revisione di Carlo → invio in Presidenza → correzioni → firma, invio, protocollo → archivio.
3. **Intervento sito:** richiesta → analisi → sviluppo → verifica desktop e mobile **sulla pagina pubblica** → online → serve comunicazione? → risposta a chi aveva chiesto.
4. **Comunicato esterno da valutare:** in arrivo → valutazione entro 48 ore → pubblica su federvela / Sport Vela / solo social / non si fa (motivo).
5. **Copertura evento:** prima (presentazione, accrediti, incarico foto e video, piano social) → durante (comunicato del giorno, foto, storie) → dopo (finale, gallery, video, rassegna, archivio) → chiusura (fatture dei collaboratori).
6. **Video:** brief → materiali → montaggio → revisione → esportazione per i canali → pubblicazione → archivio TV FIV.
7. **Dati / Report:** richiesta e formato → raccolta → verifica dei calcoli → consegna → conferma di ricezione.

---

## 6. Piattaforma: gratuita o proprietaria

### 6.1 Cosa ho verificato

| Opzione | Limite rilevante per FIV | Esito |
|---|---|---|
| **Notion Free** | Con più di un membro il workspace ha un tetto di circa 1.000 blocchi in totale; ospiti fino a 10; automazioni di database a pagamento. Fonti di terze parti concordi; pagina ufficiale da confermare. | Non regge: le sole 833 righe attuali superano già il tetto. |
| **Trello Free** | 10 collaboratori per workspace, ospiti e inviti compresi; con 11 o più le board diventano di sola lettura; 10 board. Fonte: supporto ufficiale Atlassian. | Non regge 19 persone; al massimo il nucleo operativo. |
| **Altri SaaS gratuiti** (Asana, ClickUp, Monday…) | Non verificati uno per uno. Lo schema tipico è lo stesso: gratis fino a pochi utenti, automazioni e permessi a pagamento. | Non raccomandati senza verifica. |
| **AppSheet Core** (Google) | Incluso senza costi nelle edizioni Business Starter, Standard e Plus ed Enterprise di Google Workspace, con dominio verificato. Fonte: Google. Edizione di FIV da verificare con Belgrano. | Possibile, ma è uno strumento no-code: interfaccia generica, poco adattabile, e Claude può aiutare poco a costruirlo. |
| **Sistema proprietario dentro Google Workspace FIV** | Nessuna licenza aggiuntiva; login con gli account federvela.it; dati nel dominio FIV. Da verificare con Belgrano che le web app Apps Script siano abilitate. | **Raccomandato** |
| **Web app su hosting esterno** (es. WordPress su SiteGround) | Server, sicurezza, backup e aggiornamenti tutti a carico nostro. Se stesse sull'hosting di Sport Vela, i dati interni FIV finirebbero sull'infrastruttura di una testata esterna alla Federazione. | Sconsigliato |

### 6.2 Raccomandazione

**Sì al sistema proprietario, ma costruito dentro Google Workspace FIV**: web app Google Apps Script con un Foglio Google come archivio dati, su un Drive condiviso FIV.

Perché:
1. **Costo zero e nessun server.** Gira sull'infrastruttura Google che FIV già usa: niente hosting, niente aggiornamenti di sistema, niente backup da organizzare a parte.
2. **Gli accessi esistono già.** Login con gli account federvela.it; i collaboratori esterni (Catalani, Orsini) entrano con un account Google autorizzato in un elenco.
3. **I dati restano della Federazione.** Il file sta in un Drive condiviso FIV, non nel Drive personale di Carlo. Se un giorno l'ufficio cambia, il sistema resta.
4. **È fatto sulle nostre esigenze**: presa visione registrata, passaggi automatici tra settori, modulo per i referenti, riepiloghi diversi per consiglieri e operativi. Nessuno strumento gratuito li dà tutti insieme.
5. **Calendario e mail sono già lì.** Legge il calendario «Comunicazione FIV» senza duplicarlo e invia notifiche dalle caselle federvela.it.
6. **Claude ci lavora sopra.** Il planner quotidiano legge e aggiorna lo stesso archivio, con il controllo dei duplicati sul thread email.

Limiti, da dire subito:
- **Va costruito e mantenuto.** Il primo pilota è piccolo, ma ogni funzione nuova è lavoro. Serve un responsabile tecnico (Belgrano) oltre a Carlo, per non legare il sistema a una persona sola.
- **L'interfaccia sarà più essenziale di Notion**: funzionale, non ricca di effetti.
- **Ci sono quote di uso** (mail inviate al giorno, tempo di esecuzione). Per il volume dell'ufficio non dovrebbero essere un problema, ma vanno verificate sull'edizione Workspace di FIV.
- **Dipende dalle impostazioni dell'amministratore** del dominio: va chiesto a Belgrano prima di partire.

### 6.3 Architettura

```
Drive condiviso FIV «Comunicazione»
└── Foglio «Flusso Comunicazione FIV»   (archivio dati)
    ├── Attività      una riga = un lavoro (campi come § 5)
    ├── Progetti      eventi e progetti continuativi
    ├── Persone       nome, mail, livello di accesso, settori seguiti
    ├── Registro      ogni modifica: chi, cosa, quando; prese visione
    └── Impostazioni  settori, tipi, canali, modelli di sotto-passaggi

Web app (Apps Script, eseguita come ufficiostampa@federvela.it)
├── Bacheca per stato            ├── Le mie attività
├── Calendario editoriale        ├── Pagina di settore (×8)
├── Da smistare (Carlo)          ├── Solleciti
├── Scheda attività: sotto-passaggi spuntabili, commenti, registro, presa visione
└── Modulo richieste per i referenti

Automazioni
├── mail all'assegnazione e a ogni passaggio di mano
├── passaggi automatici § 5.4
├── riepilogo del lunedì mattina: a ciascuno le sue attività; ai consiglieri il quadro del settore
└── lettura del calendario «Comunicazione FIV»: eventi visibili, copertura creata solo su scelta

Claude
└── planner quotidiano: legge le viste, propone nuove voci in «In arrivo» controllando i duplicati, propone le chiusure
```

Riservatezza: il Foglio è condiviso solo con l'account tecnico e con Carlo. Tutti gli altri passano dalla web app, che mostra a ciascuno solo ciò che il suo livello consente. Le attività marcate «Riservato» (Presidenza, Gestione ufficio) le vedono solo Carlo e chi è indicato.

---

## 7. Pilota: Carlo + Calautti, due settimane

Funzioni minime del pilota:
1. archivio Attività con stati, priorità, settore, tipo, canali, responsabile, date;
2. bacheca, Le mie attività, calendario editoriale;
3. mail all'assegnazione e presa visione registrata;
4. passaggio automatico News approvata → Post social a Calautti;
5. registro delle modifiche.

Cosa misurare alla fine delle due settimane:
- quante news hanno generato il post senza solleciti a voce o su WhatsApp;
- quante attività sono state chiuse davvero;
- se Calautti lo usa senza che Carlo glielo ricordi.

Poi si allarga a Colivicchi, Piraino e Crosta. I referenti arrivano con il modulo richieste; i consiglieri con il riepilogo settimanale.

---

## 8. Cosa cambia per Claude

La skill `planner-operativo-mail-calendario-fiv` va riscritta per il nuovo sistema:
- **cerca prima di creare**: stesso thread Gmail o stesso evento significa aggiornare l'attività che c'è già, non crearne un'altra;
- le nuove voci entrano solo in «In arrivo»;
- le regate del calendario non diventano attività: diventa attività solo la copertura scelta da Carlo;
- le chiusure si propongono con il link di uscita, e Carlo conferma;
- WhatsApp: i messaggi con una richiesta entrano in «In arrivo» con fonte WhatsApp (sospeso dalla sessione del 15/10).

---

## 9. Piano di lavoro

| Fase | Cosa | Chi | Prerequisito |
|---|---|---|---|
| **0. Verifica tecnica** | chiedere a Belgrano: edizione Google Workspace, Apps Script web app abilitate, Drive condiviso disponibile, uso di ufficiostampa@ come account del sistema | Carlo → Belgrano | — |
| **1. Pulizia** | dalle 418 attività aperte (regate escluse): archiviare quelle create prima del 1/10 senza movimenti e quelle con evento passato; fondere i duplicati; Carlo conferma l'elenco finale, che diventa il primo contenuto del nuovo archivio | Claude + Carlo | — |
| **2. Costruzione del pilota** | Foglio, web app e funzioni del § 7; codice in un repository dedicato, separato da questo | Claude, con Carlo | fase 0 |
| **3. Pilota** | due settimane con Calautti | Carlo, Calautti | fase 2 |
| **4. Allargamento** | operativi, poi modulo per i referenti e riepiloghi per i consiglieri | — | esito del pilota |
| **5. Nuovo planner Claude** | skill riscritta sul nuovo archivio | Claude | fase 2 |

Il vecchio database Notion resta consultabile in sola lettura come archivio fino alla fine del pilota.

---

## Fonti sui piani gratuiti

- Atlassian, *Collaborator limit for free Workspaces*: https://support.atlassian.com/trello/docs/workspace-user-limit/
- Google Workspace Updates, *AppSheet Core licenses included by default for more Google Workspace editions*: https://workspaceupdates.googleblog.com/2023/07/appsheet-core-licenses-included-by-default-for-more-google-workspace-editions.html
- Google, *Manage AppSheet in your organization*: https://support.google.com/a/answer/10100275?hl=en
- Notion, limiti del piano Free (fonti di terze parti, da confermare su notion.com/pricing): https://superdupr.com/blog/is-notion-free · https://www.usecarly.com/blog/notion-free-plan-limits/
