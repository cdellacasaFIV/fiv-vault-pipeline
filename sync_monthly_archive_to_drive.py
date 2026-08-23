#!/usr/bin/env python3
"""
Archivio mensile FIV -> Google Drive (upload diretto via service account).

PERCHE' QUESTO SCRIPT ESISTE (2026-08-23):
La routine cloud Claude che sincronizza il vault Obsidian usa il connettore
Google-Drive, il quale NON supporta l'upload di un file locale: il contenuto
va passato come testo inline dentro la chiamata dello strumento. I due
registri sorgente (SportVela e Federvela, ~370-580KB) sono troppo grandi per
essere riprodotti in sicurezza in un'unica chiamata dal modello (rischio di
troncamento/corruzione). Questo script bypassa il problema parlando
direttamente con l'API Google Drive (upload da file, nessun limite di
"generazione testo").

Gira una volta al mese (il giorno 1, invocato dal workflow GitHub Actions
"Fetch FIV external data") e crea, se non esiste gia', uno snapshot datato
dei due registri sotto "Dati Strutturati FIV/Archivi Mensili/" nel vault
Obsidian FIV su Google Drive.

SETUP RICHIESTO (una tantum, da fare da parte di Carlo, non eseguibile da
Claude):
1. Creare un Service Account su Google Cloud Console (progetto qualsiasi),
   abilitare la "Google Drive API".
2. Scaricare la chiave JSON del Service Account.
3. Condividere la cartella del vault "Il mio Drive/vault obsidian/FIV" (e in
   particolare "Dati Strutturati FIV") con l'indirizzo email del Service
   Account (tipo ...@progetto.iam.gserviceaccount.com), ruolo "Editor".
4. Salvare il contenuto del file JSON come secret GitHub del repository,
   nome: GOOGLE_SERVICE_ACCOUNT_JSON.
Finche' questo setup non e' completo, lo script si ferma silenziosamente
(nessun errore bloccante per il resto del workflow di fetch) e stampa
un avviso chiaro nei log.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

DATI_STRUTTURATI_FOLDER_ID = "1X_xPbryNUap525AeITZxXfI81WZ3Kdgm"  # "Dati Strutturati FIV"
ARCHIVI_MENSILI_FOLDER_NAME = "Archivi Mensili"

SOURCES = {
    "SportVela": Path("_fetched/Fonti Esterne/SportVela News/01-Registro-Fonti.md"),
    "Federvela": Path("_fetched/Fonti Ufficiali/Federvela News/01-Registro-Fonti.md"),
}


def month_key(dt: datetime) -> str:
    return dt.strftime("%Y-%m")


def get_drive_service():
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        print("AVVISO: librerie google-api-python-client/google-auth non installate. "
              "Passo archivio mensile saltato (non bloccante).")
        return None

    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not raw:
        print("AVVISO: secret GOOGLE_SERVICE_ACCOUNT_JSON non configurato. "
              "Passo archivio mensile saltato (non bloccante) — vedi istruzioni "
              "di setup in cima a questo file.")
        return None

    try:
        info = json.loads(raw)
    except json.JSONDecodeError:
        print("ERRORE: GOOGLE_SERVICE_ACCOUNT_JSON non è un JSON valido. Saltato.")
        return None

    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)


def find_child_folder(service, parent_id: str, name: str):
    q = (
        f"'{parent_id}' in parents and name = '{name}' "
        "and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    )
    res = service.files().list(q=q, fields="files(id, name)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None


def create_child_folder(service, parent_id: str, name: str) -> str:
    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }
    created = service.files().create(body=metadata, fields="id").execute()
    return created["id"]


def find_file(service, parent_id: str, name: str):
    q = f"'{parent_id}' in parents and name = '{name}' and trashed = false"
    res = service.files().list(q=q, fields="files(id, name)").execute()
    files = res.get("files", [])
    return files[0]["id"] if files else None


def upload_file(service, parent_id: str, name: str, local_path: Path):
    from googleapiclient.http import MediaFileUpload

    media = MediaFileUpload(str(local_path), mimetype="text/markdown", resumable=True)
    existing_id = find_file(service, parent_id, name)
    if existing_id:
        print(f"  {name}: gia' presente su Drive (id={existing_id}), non lo tocco "
              "(l'archivio mensile non va mai sovrascritto).")
        return existing_id
    metadata = {"name": name, "parents": [parent_id]}
    created = service.files().create(body=metadata, media_body=media, fields="id").execute()
    print(f"  {name}: creato su Drive (id={created['id']}).")
    return created["id"]


def main() -> int:
    now = datetime.now(timezone.utc)
    ym = month_key(now)

    for name, path in SOURCES.items():
        if not path.exists():
            print(f"AVVISO: sorgente mancante per {name}: {path} — salto questa fonte.")

    service = get_drive_service()
    if service is None:
        return 0  # non bloccante: il resto del workflow di fetch prosegue comunque

    archivi_id = find_child_folder(service, DATI_STRUTTURATI_FOLDER_ID, ARCHIVI_MENSILI_FOLDER_NAME)
    if archivi_id is None:
        archivi_id = create_child_folder(service, DATI_STRUTTURATI_FOLDER_ID, ARCHIVI_MENSILI_FOLDER_NAME)
        print(f"Creata cartella '{ARCHIVI_MENSILI_FOLDER_NAME}' (id={archivi_id}).")

    tmp_dir = Path("/tmp/fiv_monthly_archive")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    any_done = False
    for name, src in SOURCES.items():
        if not src.exists():
            continue
        target_name = f"{name}-News-Registro-Completo-{ym}.md"
        if find_file(service, archivi_id, target_name):
            print(f"{target_name}: gia' esiste su Drive, salto (mai sovrascrivere gli archivi mensili).")
            continue
        tmp_path = tmp_dir / target_name
        header = f"> Snapshot mensile automatico del {now.strftime('%Y-%m-%d')}. Non modificare a mano.\n\n"
        with open(tmp_path, "w", encoding="utf-8") as out:
            out.write(header)
            with open(src, "r", encoding="utf-8") as f:
                out.write(f.read())
        upload_file(service, archivi_id, target_name, tmp_path)
        any_done = True

    if any_done:
        print(f"Archivio mensile {ym} completato.")
    else:
        print(f"Archivio mensile {ym}: nessun file nuovo da creare (gia' presenti o sorgenti mancanti).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
