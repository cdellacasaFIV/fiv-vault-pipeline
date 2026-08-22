# FIV Vault Pipeline

Pipeline di aggiornamento automatico del vault Obsidian FIV (vela) di Carlo Dellacasa.

## Cosa fa

Esegue in sequenza (`fiv_vault_pipeline.py`):

1. `extract_world_sailing_results.py` — risultati World Sailing (World Championships)
2. `extract_world_sailing_european_results.py` — risultati Europei
3. `extract_world_sailing_major_regattas.py` — grandi regate (Princesa Sofia, Semaine Olympique, ecc.)
4. `extract_world_sailing_youth_para_results.py` — risultati Youth/Para
5. `build_federvela_news_archive.py` — archivio news federvela.it
6. `build_sportvela_news_archive.py` — archivio news sportvela.net
7. `update_fiv_convocazioni_bodrato.py` — convocazioni squadre nazionali
8. `build_obsidian_connective_layer.py` — mappe e collegamenti tra le pagine del vault

Vedi `FIV_AUTOMATION_RUNBOOK.md` per le regole operative complete.

## Dove scrive

Tutti gli script leggono il percorso del vault dalla variabile d'ambiente **`FIV_VAULT_ROOT`**
(se non impostata, usano di default il percorso locale sul Mac di Carlo — utile per continuare
a lanciarli in locale senza cambiare nulla).

In esecuzione cloud, `FIV_VAULT_ROOT` va puntata a una cartella locale del sandbox (scratch dir);
un passaggio successivo, guidato dall'agente tramite il connettore Google-Drive, sincronizza i file
nuovi/modificati nel vault reale su Google Drive (`Il mio Drive/vault obsidian/FIV`).

## Nota storica (2026-08-22)

I passi originali `audit_content_integrity.py` e `clean_editorial_residue.py` sono stati rimossi
dalla pipeline: i file con quel nome nella cartella condivisa di progetto appartengono in realtà
al progetto "guida vini" (path hardcoded su `guida-vini-site-local-ux-complete`), non al vault FIV.
Se in futuro servono un audit/pulizia dedicati al vault FIV, vanno scritti da zero.

## Setup locale

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 fiv_vault_pipeline.py
```
