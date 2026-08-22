# FIV Automation Runbook

Questo documento descrive il processo operativo per aggiornare il vault FIV in modo automatico, coerente e sicuro.

## Obiettivo

- aggiornare i risultati World Sailing
- aggiornare le news Federvela
- aggiornare le news SportVela
- aggiornare la rassegna stampa giornaliera
- mantenere il vault leggero, con poche fonti duplicate e molti link utili

## Regola base

Il vault non va riscritto tutto ogni volta.
Si aggiorna solo cio' che cambia, e si toccano gli indici o le mappe solo quando la struttura o i collegamenti cambiano davvero.

## Ordine di esecuzione consigliato

1. Import risultati World Sailing.
2. Import news Federvela.
3. Import news SportVela.
4. Aggiorna rassegna stampa giornaliera.
5. Aggiorna convocazioni e note operative legate alle email ufficiali.
6. Aggiorna gli indici tematici solo se sono comparsi nuovi fatti.
7. Aggiorna le mappe vault solo se sono cambiati i percorsi o i punti di ingresso.
8. Esegui un controllo di qualità finale.

## Controlli di sicurezza

- Non scrivere dati non verificati come se fossero certi.
- Se una fonte esterna non e' confermata da una fonte ufficiale, tenerla come contesto e non come fatto definitivo.
- Non duplicare lo stesso contenuto in piu' pagine.
- Se una nota e' gia' presente, aggiornarla invece di crearne una nuova.
- Per la rassegna stampa, assorbire solo articoli che aggiungono profondita' narrativa.
- Per le email, conservare solo dati stabili e verificabili, non il corpo completo.

## File chiave coinvolti

- `build_obsidian_connective_layer.py`
- `extract_world_sailing_results.py`
- `extract_world_sailing_european_results.py`
- `extract_world_sailing_major_regattas.py`
- `extract_world_sailing_youth_para_results.py`
- `build_federvela_news_archive.py`
- `build_sportvela_news_archive.py`
- `update_fiv_convocazioni_bodrato.py`
- `audit_content_integrity.py`
- `clean_editorial_residue.py`

## Output attesi

- schede atleta aggiornate
- archivi news aggiornati
- indici per tema aggiornati
- rassegna stampa giornaliera consultabile
- note di convocazione aggiornate
- mappe vault coerenti e leggere

## Quando rigenerare le mappe

Rigenera le mappe solo se:

- cambia la struttura delle cartelle
- cambia il punto di ingresso principale
- cambia il modo in cui una fonte va consultata
- viene introdotto un nuovo archivio primario

## Quando non rigenerare

Non rigenerare le mappe se:

- hai solo aggiunto nuove news
- hai solo aggiunto risultati
- hai solo aggiunto una nuova rassegna giornaliera
- non e' cambiato nessun collegamento di struttura

## Frequenza consigliata

- risultati World Sailing: giornaliera o settimanale
- news Federvela: giornaliera
- news SportVela: giornaliera
- rassegna stampa: giornaliera
- audit finale: giornaliero o settimanale
- rigenerazione completa mappe: solo quando serve

## Esportazione del processo

Se devi farlo eseguire da un altro sistema, passa questa sequenza:

1. sincronizza il vault Google Drive
2. lancia gli importatori
3. lancia i builder degli indici
4. lancia l'audit
5. salva solo le modifiche effettive

