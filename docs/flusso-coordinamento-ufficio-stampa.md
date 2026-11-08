# Flusso di lavoro coordinato — Comunicazione FIV

Proposta di struttura in Notion per Ufficio Stampa, Social, settori e Presidenza.
Bozza dell'8 novembre 2026, da discutere con Carlo Dellacasa prima di costruirla.

---

## 1. Da dove parte l'analisi

Fonti lette:
- le circa 75 sessioni Claude Code dal 7 settembre all'8 novembre 2026 (solo titoli ed esiti; aperte per intero solo due);
- il database Notion «FIV — Planner Operativo / Task FIV»;
- il calendario Google «Comunicazione FIV» e l'elenco dei calendari condivisi;
- la skill `planner-operativo-mail-calendario-fiv` e le altre skill FIV installate;
- questo repository, cioè la pipeline del vault.

Non ho potuto leggere le chat di claude.ai: da qui non ho uno strumento per farlo. Il quadro viene quindi dalle sessioni di lavoro, da Notion e dal calendario. Le chat personali o fuori dal perimetro FIV, come il libro, sono state escluse.

### 1.1 Cosa fa l'ufficio, per famiglie di lavoro

| Famiglia | Esempi dalle sessioni (set–nov 2026) | Chi altro è coinvolto |
|---|---|---|
| Risultati e news sportive | Europeo Optimist a squadre, Team Race RS21, Middle Sea Race, Switch, Classi Foil, eSailing, Hansa, Melges 24, podi 2026 | Colivicchi (comunicati evento), circoli e classi, social |
| Testi istituzionali e a firma | intervista al Presidente per l'inserto del 31/10, frasi del Presidente, collari d'oro CONI, prefazioni e saluti, lettere, certificazione ISO | Crosta (Presidenza), Segretario Generale |
| Siti e sviluppo web | tema Sport Vela (versioni 0.1.3xx), velascuola.net, sito eSailing, sito dual career, «Voce delle zone», timeline Para Sailing, speciale Vilamoura, federvela.it | Massone (Velascuola), settori richiedenti |
| Video e TV | We Sail TV, reel Terra Maris, Velando 2, video UniCredit, sigla e stacchi, campionamento archivio TV FIV, streaming | Catalani (video), partner |
| Foto e archivio | digiKam, Flickr, accrediti fotografici, ritocchi, didascalie | Orsini (foto) |
| Dati e classifiche | programma classifiche FIV, lettore Sailwave, classifiche Primavela, Giovanili e Altura, conti dei premi, classifica Scuole Vela, pipeline World Sailing | settore tecnico, zone |
| Partner e marketing | UniCredit Navigare Insieme, Edison Next / CICO, AIRC, SailGP, Saloni, Italpress, studio Open Economics | Carrara, De Giuli, Freschi (Marketing) |
| Newsletter e contatti | campagne Brevo, contatti condivisi, API tessere | Marketing |
| Gestione ufficio | fatture e delibere (eXtrapola, Catalani), hosting, stampe, PC, formazione obbligatoria | Amministrazione |

Dato operativo ([INFERITO] dai titoli delle sessioni): in due mesi le sessioni web e video sono quasi quante quelle di scrittura. Il lavoro dell'ufficio non è più solo redazione. È redazione più produzione più sviluppo, e oggi passa quasi tutto da una persona sola.

### 1.2 Il planner Notion attuale: cosa non funziona

Numeri estratti dal database «Task FIV» l'8/11/2026:

| Voce | Valore |
|---|---|
| Righe totali dal 28 aprile | 833 |
| Ancora «Da fare» o «In corso» | 570 |
| Segnate «Fatto» | 1 |
| Righe «Regata in arrivo…» generate dal calendario | 207 |
| Righe «Valutare … comunicato» (comunicati di circoli e classi) | 111 |
| Righe per lo stesso Europeo Junior 49er | 19 |
| Righe per la stessa richiesta Open Economics (De Giuli) | 9 |
| Righe per la stessa formazione Whistleblowing | 6 |
| Progetto = «Altro» | circa 64% |
| Unico utente del workspace | Carlo |

Cause:
1. **Nessun controllo dei duplicati.** A ogni passaggio Claude crea una riga nuova per lo stesso thread email o evento, invece di aggiornare quella che esiste.
2. **Il calendario viene copiato nei task.** Ogni regata del calendario «Comunicazione FIV» diventa un task, e lo ridiventa ogni giorno.
3. **Nessuno chiude le righe.** Il database funziona come un registro di ingresso, non come una board: le righe entrano e non escono.
4. **Il campo «Chi» mescola persone e categorie** (Ettorre, Freschi, ma anche «Interno» ed «Esterno»), quindi non dice chi deve fare la cosa.
5. **Non esistono i settori.** «Progetto» mescola eventi (Vela Day), partner (UniCredit), canali (Social) e contenitori generici (Altro, Comunicazione).
6. **I colleghi non ci sono.** Il workspace ha un solo membro, quindi nessun altro può vedere, ricevere o chiudere un'attività.

Conclusione: aprire ai colleghi questo database così com'è peggiorerebbe la situazione. Prima va congelato e ripulito (§ 7, fase 0).

---

## 2. La regola che rende il sistema credibile

«Nessuno può dire che non sapeva» non dipende da Notion. Dipende da quattro condizioni, e Notion serve solo a tenerle in piedi:

1. **Un solo punto di ingresso.** Se una richiesta non è in Notion, per il gruppo non esiste. Mail, WhatsApp, telefonate e corridoio: chi riceve la richiesta la inserisce, oppure la gira a Carlo che la inserisce.
2. **Un solo responsabile per attività.** Una persona con nome e cognome, mai «Interno». Gli altri sono collaboratori.
3. **Uno stato sempre vero.** Lo stato si aggiorna quando cambia qualcosa, non a fine settimana.
4. **Un rito fisso.** Una riunione breve settimanale sulla stessa vista, più le notifiche personali. Senza rito anche il miglior database diventa un archivio.

A queste si aggiunge una regola di tracciabilità: ogni passaggio di mano (bozza consegnata, ok ricevuto, materiale girato) si registra con un @ alla persona interessata, nell'attività stessa. Così la notifica arriva e resta scritta.

---

## 3. Correzione alla tua impostazione: separare gli assi

Le categorie che hai indicato (programmato, a calendario, urgente, da studiare) sono utili, ma mescolano tre cose diverse:

| Tua categoria | Cosa misura davvero | Dove va |
|---|---|---|
| Da studiare | a che punto è il lavoro (non ancora deciso) | **Stato** |
| Programmato | a che punto è il lavoro (deciso e con data) | **Stato** |
| A calendario | se è legato a una data esterna fissa | **Data** + vista Calendario |
| Urgente | quanto è prioritario | **Priorità** |

Se restano tutte nello stesso campo, un'attività «urgente» che è anche «a calendario» e ancora «da studiare» non trova posto. Per questo propongo tre campi separati e le viste che li combinano.

### 3.1 Stati, cioè il flusso vero e proprio

```
📥 In arrivo → 🔍 Da studiare → 📅 Programmato → ✍️ In lavorazione → 👀 In revisione → ✅ Approvato → 🚀 Pubblicato / Consegnato → 🗄️ Archiviato
                                                    ↘ ⏸️ In attesa di altri (con «Da chi» e «Dal giorno»)
                                                    ↘ ✖️ Non si fa (con il motivo)
```

- **In arrivo**: è entrato ma nessuno l'ha ancora valutato. Va smaltito entro 48 ore.
- **Da studiare**: serve un'istruttoria, un dato, una decisione politica o un preventivo.
- **Programmato**: deciso, con responsabile e data.
- **In lavorazione**: qualcuno ci sta lavorando adesso.
- **In revisione**: bozza consegnata, aspetta l'ok di Carlo, del Presidente o del Segretario Generale.
- **Approvato**: pronto, aspetta solo la data di uscita.
- **Pubblicato / Consegnato**: uscito; si allega sempre il link o il file finale.
- **In attesa di altri**: bloccato da qualcuno esterno al passo corrente. È il campo che fa emergere i solleciti.
- **Non si fa**: chiuso con il motivo, per esempio un comunicato di circolo non rilanciato. Così la decisione resta tracciata.

### 3.2 Priorità

🔴 Urgente (entro oggi o domani, blocca altro) · 🟠 Alta (questa settimana) · 🟡 Normale · ⚪ Quando possibile.

### 3.3 Date

- **Data di uscita o consegna**: quando deve essere fuori.
- **Scadenza interna**: quando deve essere pronta la bozza (di solito 1–2 giorni prima).
- **Evento collegato**: per esempio un Europeo dal 10 al 14/11. Si collega, non si duplica.

---

## 4. Settori: i quattro che hai indicato e quelli che emergono dal lavoro

Il punto più importante della struttura è separare tre cose:
- **Settore**: di chi o di cosa parla il lavoro;
- **Tipo di lavoro**: cosa si produce;
- **Canale di uscita**: dove finisce.

Se si mescolano, le implementazioni al sito non finiscono mai nella comunicazione esterna. Con i tre campi separati, invece, il passaggio diventa automatico (§ 5.3).

### 4.1 Settori (chi o cosa riguarda)

| Settore | Perché c'è | Riferimento (da confermare) |
|---|---|---|
| **Olimpico e Squadre nazionali** | classi olimpiche, convocazioni, Mondiali ed Europei, SailGP e America's Cup per la parte atleti | Carlo + direzione tecnica |
| **Giovanile** | Optimist, Techno, ILCA 4/6 Youth, Youth Worlds, Campionati Giovanili, Primavela | settore giovanile |
| **Istituzionale e Presidenza** | Presidente, Segretario Generale, Consiglio federale, CONI, Ministeri, Quirinale; lettere, saluti, prefazioni, dichiarazioni, interviste | Crosta (Presidenza) → Carlo |
| **Social media** | non è un settore di contenuto ma un canale con un proprio piano editoriale: lo tengo come area di lavoro | Calautti |
| *Proposti in aggiunta:* | | |
| **Para Sailing e inclusione** | Navigare Insieme, Para Sailing, Svelare senza barriere: comunicazione e referenti propri | Piraino |
| **Scuola, Velascuola e formazione** | progetti MIM, velascuola.net, Scuole Vela, corsi Allenatore di Club, dual career | Massone |
| **Altura, Offshore e Classi** | Campionato Altura, Route du Rhum, Middle Sea Race, RS21, Melges, monotipi, eSailing | Carlo |
| **Territorio, Zone e Circoli** | comunicati di circoli e zone (111 righe nel planner attuale), «Voce delle zone», presidenti di zona | Carlo + comitati |
| **Partner, Marketing ed Eventi federali** | UniCredit, Edison Next / CICO, AIRC, Italpress, Saloni, Vela Day, Velista dell'Anno, Giornata 10 dicembre, Calendario 2027 per i 100 anni | Carrara, De Giuli, Freschi |
| **Gestione ufficio** | fatture, delibere, contratti, strumenti, hosting, formazione obbligatoria | Carlo (vista privata) |

Nota: eSailing può stare in «Altura e Classi» o diventare un settore autonomo se cresce. È una scelta tua.

### 4.2 Tipo di lavoro (cosa si produce)

Comunicato / News · Risultato di regata · Testo a firma (lettera, saluto, prefazione) · Intervista / Dichiarazione · Post e piano social · Newsletter · Video · Foto / Gallery · Grafica / Locandina · **Intervento sito (web)** · Copertura evento · Dati / Report (per esempio Open Economics) · Richiesta esterna da valutare · Amministrativo · Studio / Analisi.

### 4.3 Canale di uscita (dove finisce)

federvela.it · Sport Vela · Social FIV · We Sail TV / YouTube · Newsletter Brevo · Stampa esterna / agenzie · Lettera / PEC / Protocollo · Uso interno · Partner.

---

## 5. Architettura in Notion

### 5.1 Database

```
🏠 Comunicazione FIV — Home (pagina condivisa)
│
├── 📋 Attività          ← il database centrale: una riga = un lavoro
├── 🎯 Progetti ed Eventi ← Vela Day, Giornata 10/12, Velista dell'Anno, CICO, UniCredit, Calendario 2027…
├── 🗓️ Riunioni          ← verbali settimanali, decisioni, attività nate in riunione
├── 📚 Procedure          ← come si fa un comunicato, una lettera, un intervento web (dal Metodo Ufficio Stampa)
└── 🗄️ Archivio 2026      ← le 833 righe attuali, congelate
```

**Attività**: campi.

| Campo | Tipo | Note |
|---|---|---|
| Titolo | titolo | verbo + oggetto: «Comunicato finale Europeo Junior 49er» |
| Stato | stato | § 3.1 |
| Priorità | selezione | § 3.2 |
| Settore | selezione multipla | § 4.1 |
| Tipo | selezione | § 4.2 |
| Canali | selezione multipla | § 4.3 |
| Responsabile | persona (una sola) | obbligatorio da «Programmato» in poi |
| Collaboratori | persone | |
| Approva | selezione | Carlo · Presidente · Segretario Generale · Nessuno |
| Data uscita | data | |
| Scadenza interna | data | |
| Progetto / Evento | relazione → Progetti | |
| Origine | relazione → Attività | collega l'attività figlia a quella che l'ha generata (§ 5.3) |
| In attesa di | testo + data | chi blocca e da quando |
| Prossimo passo | testo, una riga | la riga di contesto della tua skill planner |
| Fonte | selezione | Email · Calendario · Riunione · WhatsApp · Telefono · Manuale |
| Link fonte | URL | link al thread Gmail o all'evento: **è la chiave antiduplicato** |
| Esito | URL / file | link pubblicato, file consegnato |
| Aggiornato | ultima modifica | automatico |

### 5.2 Viste, cioè l'identità di ogni sezione

Ogni settore ha una sua pagina con una vista filtrata del database Attività. Non si fanno database separati: se ogni settore avesse il suo, si perderebbe la vista d'insieme.

| Vista | Per chi | Filtro e forma |
|---|---|---|
| **📥 Da smistare** | Carlo | Stato = In arrivo; elenco |
| **🔴 Urgenti** | tutti | Priorità = Urgente, non chiuse |
| **📅 Calendario editoriale** | tutti | per Data uscita; calendario mensile |
| **🗂️ Flusso** | tutti | bacheca per Stato |
| **👤 Le mie attività** | ognuno | Responsabile = io; raggruppate per Stato |
| **⏸️ Solleciti** | Carlo | In attesa da più di 3 giorni |
| **🔍 Da studiare** | riunione | Stato = Da studiare |
| **Pagina di settore** (una per settore) | referente | Settore = X; bacheca + calendario |
| **📱 Social** | Calautti | Canali contiene Social; calendario |
| **🌐 Web** | Carlo | Tipo = Intervento sito |
| **✍️ Presidenza** | Carlo, Crosta | Approva = Presidente o Settore = Istituzionale |
| **🧾 Gestione ufficio** | solo Carlo | Settore = Gestione ufficio (vista privata) |

### 5.3 I passaggi automatici tra sezioni

Questo è il cuore del flusso: quando un lavoro finisce, genera il lavoro successivo nel settore giusto e notifica chi deve farlo.

| Quando… | …nasce automaticamente | Responsabile |
|---|---|---|
| un **intervento sito** passa a «Pubblicato» e ha la casella «Serve comunicazione esterna» | attività figlia «News / avviso» in Programmato | Ufficio Stampa |
| una **news** passa ad «Approvato» e tra i canali c'è Social | attività figlia «Post social» con link alla news | Calautti |
| una **news** con canale Newsletter va in «Pubblicato» | attività figlia «Invio Brevo» | Ufficio Stampa |
| un **testo a firma** passa a «In revisione» con Approva = Presidente | notifica a Crosta + attività in «In attesa di» | Carlo |
| un'attività resta «In attesa di» per più di 3 giorni | compare in Solleciti | Carlo |
| un **evento** entra in Progetti | si applica il modello «Copertura evento» con le sotto-attività già pronte (§ 6.5) | referente del settore |

Le automazioni di database («quando una proprietà cambia → crea pagina / notifica») richiedono un piano Notion a pagamento. Prezzi e limiti attuali vanno verificati sul sito Notion: non li ho controllati. Senza piano a pagamento lo stesso passaggio si fa con un pulsante nel modello oppure con Claude durante il giro quotidiano.

---

## 6. Sotto-passaggi: modelli per tipo di lavoro

Ogni Tipo ha un modello di pagina con la sua lista di controllo. Le voci sono quelle che già segui nelle sessioni.

### 6.1 Risultato di regata / News sportiva
1. Fonte ufficiale verificata (classifica finale, non provvisoria; comunicato del circolo incrociato con i risultati)
2. Bozza (skill `fiv-news-risultato`)
3. Verifica di nomi, punteggi, classi e circoli (skill `fiv-verifica-fatti`)
4. Ok di Carlo
5. Pubblicazione su federvela.it e/o Sport Vela (categorie, tag, SEO, foto con credito)
6. → Post social (figlia, a Calautti)
7. → Newsletter, se prevista
8. Link pubblicato in «Esito»

### 6.2 Testo a firma (lettera, saluto, prefazione, dichiarazione)
1. Richiesta registrata (di solito da Crosta): destinatario, occasione, lunghezza, scadenza
2. Materiali di contesto (testi già esistenti, per esempio quello di Buonfiglio nella prefazione di Ponti)
3. Bozza (skill `fiv-dichiarazione` / `fiv-voce-carlo`)
4. Revisione di Carlo
5. Invio in Presidenza → «In revisione», Approva = Presidente
6. Correzioni del Presidente recepite
7. Firma, invio, protocollo
8. Versione finale archiviata in Esito

### 6.3 Intervento sito (web)
1. Richiesta: chi la fa, cosa serve, per quale settore
2. Analisi e stima
3. Sviluppo o caricamento
4. Verifica su desktop e mobile, **controllo della pagina pubblica**: nelle sessioni manca spesso, per esempio «pagina pubblica non verificata»
5. Online
6. **Serve comunicazione esterna?** Sì → nasce la News collegata. No → si annota il motivo
7. Comunicazione di ritorno a chi ha chiesto

### 6.4 Richiesta esterna da valutare (comunicati di circoli, classi, zone)
1. In arrivo → valutazione entro 48 ore
2. Esito, uno solo: Pubblica su federvela · Pubblica su Sport Vela · Solo rilancio social · Non si fa (motivo)
3. Se si pubblica → diventa una News (6.1)

Questo modello da solo assorbe le 111 righe «Valutare comunicato» del planner attuale.

### 6.5 Copertura evento (Progetto con sotto-attività)
- **Prima**: presentazione o comunicato di apertura; accrediti; incarico foto (Orsini) e video (Catalani); piano social
- **Durante**: comunicato giornaliero, foto del giorno, storie e post
- **Dopo**: comunicato finale, gallery, montaggio video, rassegna, archiviazione dei materiali su TV FIV e Flickr
- **Chiusura**: fatture e rimborsi dei collaboratori, se previsti

### 6.6 Video
Brief → materiali (grezzi, loghi, musica con licenza) → montaggio → revisione → correzioni → esportazione nei formati per i canali → pubblicazione → archivio.

### 6.7 Dati e report (Open Economics, conti premi, classifiche)
Richiesta e formato atteso → raccolta → verifica dei calcoli → consegna → conferma di ricezione.

---

## 7. Avvio graduale

| Fase | Cosa | Chi | Durata |
|---|---|---|---|
| **0. Pulizia** | congelare «Task FIV» in Archivio; Claude propone l'elenco delle attività davvero aperte, senza duplicati; Carlo conferma | Carlo + Claude | 1–2 giorni |
| **1. Costruzione** | database Attività, Progetti, Riunioni; modelli § 6; viste § 5.2; pagine di settore | Claude, su ok di Carlo | 1 giorno |
| **2. Prova a due** | Carlo + Calautti (social): è il passaggio più frequente, News → Post | 2 persone | 2 settimane |
| **3. Allargamento** | Crosta (Presidenza), Colivicchi, Marketing, referenti di settore; foto e video come ospiti | team | dopo la prova |
| **4. Rito** | lunedì, 20 minuti sulla vista «Flusso» + «Da studiare»; si possono agganciare alle riunioni del lunedì già convocate dal Segretario Generale | tutti | stabile |

### 7.1 Cosa cambia per Claude

La skill `planner-operativo-mail-calendario-fiv` va aggiornata così:
- **cerca prima di creare**: se esiste un'attività con lo stesso Link fonte (thread Gmail) o lo stesso evento, aggiorna «Prossimo passo» e lo stato, senza aprire una riga nuova;
- **le nuove righe entrano solo in «In arrivo»**, mai direttamente in lavorazione;
- **le regate del calendario non diventano task**: diventa task solo la copertura che Carlo decide, una per evento, con il modello 6.5;
- **le chiusure si propongono**: se un thread mostra che una cosa è fatta, Claude la propone come «Pubblicato» con il link, e Carlo conferma;
- il planner del giorno continua a essere scritto come oggi, ma legge le viste «Le mie attività» e «Solleciti».

La richiesta WhatsApp → Notion (sessione del 15/10, rimasta in sospeso) entra qui: i messaggi con una richiesta vanno in «In arrivo» con Fonte = WhatsApp.

---

## 8. Rischi e punti da verificare

- **Adozione.** Se i colleghi continuano a chiedere per WhatsApp e nessuno inserisce, il sistema torna a essere solo di Carlo. La regola «se non è in Notion non esiste» va detta dal Segretario Generale o dal Presidente, non solo dall'Ufficio Stampa.
- **Account e piano Notion.** Oggi il workspace ha un solo membro. Servono inviti come membri o come ospiti (i collaboratori esterni come Catalani e Orsini possono essere ospiti). Va verificato quale piano serve per membri, ospiti e automazioni, e chi lo paga.
- **Alternativa da considerare.** FIV usa già Google Workspace (calendari condivisi su federvela.it). Se Notion non è accettabile per l'ente, lo stesso schema si può riprodurre, con meno comodità, in un Foglio Google condiviso più il calendario. Raccomando comunque Notion: c'è già e Claude ci scrive.
- **Riservatezza.** Le lettere del Presidente e le questioni amministrative non devono essere visibili a tutti: servono pagine con permessi ristretti.
- **Sovraccarico iniziale.** Meglio pochi campi obbligatori (Titolo, Stato, Responsabile, Data) e il resto facoltativo, piuttosto che un modulo che nessuno compila.

---

## 9. Domande aperte per Carlo

1. **Persone e ruoli.** Ruoli dedotti dai materiali: Calautti social; Colivicchi comunicati evento; Catalani video; Orsini foto; Crosta segreteria di Presidenza; Carrara, De Giuli e Freschi Marketing; Massone Velascuola; Piraino Para Sailing. Sono corretti? Chi segue il settore olimpico e chi il giovanile? Ruolo di Procopio, Leonardi, Belgrano e Foschini?
2. **Settori aggiuntivi.** Tieni Para Sailing, Scuola, Altura e Classi, Territorio, Partner ed Eventi come settori separati, o ne accorpi qualcuno?
3. **Accessi.** I colleghi entrano come membri del workspace o come ospiti su una sola pagina? FIV ha già un piano Notion?
4. **Pilota.** Parto con te e Calautti, o con un altro collega?
