#!/usr/bin/env python3
import csv
import json

import extract_world_sailing_results as ws


ws.OUT = ws.VAULT / "World Sailing Youth Para Results"
ws.CLASS_DIR = ws.OUT / "Classi"
ws.CSV_DIR = ws.OUT / "Dati CSV"
ws.RAW_DIR = ws.OUT / "Raw JSON"

LEVELS = [
    ("World Championships", "568d0c5a-aa65-43b1-b9f0-a32f0b569a64"),
    ("Class Youth World Championship", "3f04830f-4b04-11ed-8d4b-0a5fae879f4b"),
    ("Youth Sailing World Championships", "89afe65b-9fd9-4fab-9c62-e96a57dca89a"),
    ("Continental", "b5bca920-933a-4845-9063-5e9f0952020e"),
    ("Para World Sailing Competition", "c41e3b16-591c-43cc-9441-2dbb7c790bdb"),
]

TARGETS = [
    ("IQFOiL", "IQFOiL", "97f58788-3109-408a-a3c3-9addf8a145a1", "youth"),
    ("iQFOiL-Youth-Junior", "iQFOiL Youth & Junior", "8f7556e7-83f2-4a7b-a22f-da804a6ea13d", "youth"),
    ("ILCA-4", "ILCA 4", "e030abed-ca01-43fb-855c-17b3ac99489a", "youth"),
    ("ILCA-6-Youth", "ILCA 6", "bfa92fb9-2ef1-450a-b292-29cbf4f6d755", "youth"),
    ("Nacra-15", "Nacra 15", "66930419-82a9-4790-9636-567f4911e758", "youth"),
    ("420", "420", "7cc89af3-0e30-4860-86ae-e7006c95a962", "youth"),
    ("29er", "29er", "d5757b58-d5cc-4c60-95a5-a757fc942f80", "youth"),
    ("KiteFoil", "IKA - Kite Foil", "e24567da-3bce-4c05-94b8-2ad783e5154b", "youth"),
    ("Formula-Kite-Youth", "IKA - Formula Kite", "4e1f06bf-915e-404c-8d1a-aa6b83ae5d60", "youth"),
    ("Formula-Wing", "Formula Wing", "f16e290b-23e1-47bd-abe6-ca1e3c832340", "youth"),
    ("Hansa-303", "Hansa 303", "3b1677c7-d0c3-4fd0-84b6-343f691ff242", "para"),
    ("Hansa-23", "Hansa 2.3", "3e05e816-b26b-4da5-b061-edd84b3f7189", "para"),
    ("Hansa-Liberty", "Hansa Liberty", "1f8e4717-51fc-42a2-a5f3-20774fa4cf5c", "para"),
    ("24-Metre", "2.4 Metre", "149beb76-b125-4958-9110-0be26db56e9a", "para"),
    ("RS-Feva", "RS Feva", "c6c2bc51-fd17-4f6d-b271-2605f0d901db", "youth-rs"),
    ("RS-Tera", "RS Tera", "b03b63ad-253c-4525-a356-31479f39649d", "youth-rs"),
    ("RS-Aero", "RS Aero", "607ef3a9-066f-46c7-ba5f-9a255dc5039b", "youth-rs"),
    ("RS-Venture-Connect", "RS Venture Connect", "58a70909-13a2-451c-9dba-935d7a4c1058", "para-rs"),
    ("RS-X-85-U19", "RS:X 8.5 U19", "0bb7093b-c199-4bfa-a42a-2847b96ef657", "youth-rs"),
]

SKIP_WORDS = ["cancelled", "canceled", "no results"]
MAX_REGATTAS_PER_LEVEL = 6


def is_good_regatta(regatta):
    name = ws.clean_text(regatta.get("name")).lower()
    if any(word in name for word in SKIP_WORDS):
        return False
    end_date = ws.parse_date(regatta.get("endDate"))
    return bool(end_date and ws.RECENT_SINCE <= end_date <= ws.TODAY)


def query_regattas(target, level):
    slug, label, boat_id, group = target
    level_label, level_id = level
    params = {
        "filter[level.id]": level_id,
        "filter[events.boatClass.id]": boat_id,
        "include": "venue.country,level,season,events,events.boatClass,events.grade",
        "sort[startDate]": "desc",
        "paginate": "50",
    }
    payload, query_url = ws.request_json("/regatta", params)
    selected = []
    for regatta in payload.get("data", []):
        if not is_good_regatta(regatta):
            continue
        events = [
            event for event in regatta.get("events", [])
            if ((event.get("boatClass") or {}).get("id") == boat_id)
        ]
        for event in events:
            selected.append({"regatta": regatta, "event": event, "level_label": level_label, "query_url": query_url})
        if len({x["regatta"].get("id") for x in selected}) >= MAX_REGATTAS_PER_LEVEL:
            break
    return selected


def event_url(regatta):
    return ws.event_url(regatta)


def write_csv(path, rows, race_columns):
    base_fields = [
        "group",
        "level_label",
        "class_label",
        "event_label",
        "regatta_name",
        "world_sailing_id",
        "start_date",
        "end_date",
        "venue",
        "source_url",
        "rank",
        "country",
        "country_name",
        "crew",
        "world_sailing_ids",
        "sail_number",
        "total_points",
        "net_points",
    ]
    fields = base_fields + race_columns
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def make_stem(target_slug, meta, event_id):
    return (
        f"{target_slug}__{ws.slugify(meta['level_label'])}__{meta['year']}__"
        f"{ws.slugify(meta['event_label'])}__{ws.slugify(meta['regatta_name'])}__{event_id[:8]}"
    )


def write_class_note(target, items):
    slug, label, boat_id, group = target
    lines = [
        f"# {label} - Youth/Para World Sailing Results",
        "",
        "Fonte primaria: World Sailing API / pagina Results > Overall Results.",
        "Criterio: eventi passati, non cancellati, con classifica finale disponibile.",
        "Uso: memoria profonda per classi giovanili, RS e Para Sailing.",
        "",
        "## File dati completi",
        "",
    ]
    for item in items:
        lines.append(f"- `{item['csv_name']}`")
    lines.extend(["", "## Sintesi eventi", ""])
    for item in items:
        meta = item["meta"]
        rows = item["rows"]
        italy = [r for r in rows if r.get("country") == "ITA"]
        podium = [r for r in rows if str(r.get("rank")) in {"1", "2", "3"}]
        lines.extend([
            f"### {meta['year']} - {meta['level_label']} - {meta['event_label']}",
            "",
            f"Regata: {meta['regatta_name']}",
            f"Fonte: {meta['source_url']}",
            f"Date: {meta['start_date']} - {meta['end_date']}",
            f"Sede: {meta['venue']}",
            f"Equipaggi/barche classificati: {len(rows)}",
            "",
            "#### Podio",
            "",
            ws.md_table(podium, ["rank", "country", "crew", "net_points", "total_points"]) if podium else "Nessun podio disponibile.",
            "",
            "#### Italiani",
            "",
            ws.md_table(italy, ["rank", "crew", "sail_number", "net_points", "total_points"]) if italy else "Nessun italiano trovato nella classifica.",
            "",
        ])
    (ws.CLASS_DIR / f"{slug}.md").write_text("\n".join(lines), encoding="utf-8")


def write_registry(registry):
    if registry:
        fields = list(registry[0].keys())
        with (ws.OUT / "01-Registro-Youth-Para.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(registry)
    lines = [
        "# Registro Youth e Para Sailing World Sailing",
        "",
        "Fonte: World Sailing API, risultati `Overall Results`.",
        "Perimetro: classi giovanili, RS, Wing/Kite e Para Sailing richieste.",
        f"Aggiornato: {ws.TODAY.isoformat()}.",
        "",
        "| Gruppo | Classe | Livello | Anno | Evento | Barche | CSV | Fonte |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in registry:
        lines.append(
            f"| {row['group']} | {row['class_label']} | {row['level_label']} | {row['year']} | "
            f"{row['event_label']} | {row['classified_crews']} | {row['csv']} | {row['source_url']} |"
        )
    (ws.OUT / "01-Registro-Youth-Para.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_index(registry):
    grouped = {}
    for row in registry:
        grouped.setdefault(row["class_label"], []).append(row)
    lines = [
        "# Indice classifiche finali Youth e Para Sailing",
        "",
        "Fonte: World Sailing `Results > Overall Results`.",
        "Uso: accesso rapido a classifiche finali complete di classi giovanili, RS, Wing/Kite e Para Sailing.",
        "",
    ]
    for label in sorted(grouped):
        lines += [f"## {label}", "", "| Anno | Livello | Evento | Equipaggi/barche | Classifica completa | Fonte |", "| --- | --- | --- | --- | --- | --- |"]
        for row in sorted(grouped[label], key=lambda x: (x["start_date"], x["level_label"], x["event_label"]), reverse=True):
            lines.append(
                f"| {row['year']} | {row['level_label']} | {row['event_label']} | {row['classified_crews']} | "
                f"[[Dati CSV/{row['csv']}|CSV]] | {row['source_url']} |"
            )
        lines.append("")
    (ws.OUT / "02-Indice-Classifiche-Finali.md").write_text("\n".join(lines), encoding="utf-8")


def write_not_found():
    lines = [
        "# Classi richieste non trovate o da verificare",
        "",
        f"- **Waszp**: non risulta presente nell'elenco `boatClass` dell'API World Sailing interrogata il {ws.TODAY.isoformat()}. Da gestire con fonte alternativa, probabilmente sito di classe WASZP.",
        "- **RS**: World Sailing distingue piu classi RS. In questa estrazione sono incluse RS Feva, RS Tera, RS Aero, RS Venture Connect e RS:X 8.5 U19 dove presenti.",
        "- **WingFoil**: mappato come `Formula Wing`; eventuali risultati `Inclusive Wing` sono nel perimetro Para/Inclusion ma non sempre classificati come Formula Wing.",
    ]
    (ws.OUT / "03-Note-Copertura-e-Classi-Non-Trovate.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    ws.CLASS_DIR.mkdir(parents=True, exist_ok=True)
    ws.CSV_DIR.mkdir(parents=True, exist_ok=True)
    ws.RAW_DIR.mkdir(parents=True, exist_ok=True)
    registry = []
    failures = []
    by_class = {target[0]: {"target": target, "items": []} for target in TARGETS}
    seen_event_ids = set()

    for target in TARGETS:
        target_slug, class_label, boat_id, group = target
        print(f"{class_label}: extracting", flush=True)
        for level in LEVELS:
            selections = query_regattas(target, level)
            if not selections:
                continue
            print(f"  {level[0]}: {len(selections)} events", flush=True)
            for selection in selections:
                regatta = selection["regatta"]
                event = selection["event"]
                event_id = event["id"]
                dedupe = (target_slug, selection["level_label"], event_id)
                if dedupe in seen_event_ids:
                    continue
                seen_event_ids.add(dedupe)
                venue = regatta.get("venue") or {}
                country = venue.get("country") or {}
                venue_text = ", ".join(x for x in [venue.get("name"), country.get("name")] if x)
                meta = {
                    "group": group,
                    "level_label": selection["level_label"],
                    "class_label": class_label,
                    "event_label": ws.clean_text(event.get("_name")),
                    "regatta_name": ws.clean_text(regatta.get("name")),
                    "world_sailing_id": ws.clean_text(regatta.get("worldSailingId")),
                    "start_date": ws.clean_text(regatta.get("startDate"))[:10],
                    "end_date": ws.clean_text(regatta.get("endDate"))[:10],
                    "year": ws.clean_text(regatta.get("startDate"))[:4],
                    "venue": venue_text,
                    "source_url": event_url(regatta),
                    "event_api_url": "",
                    "regatta_query_url": selection["query_url"],
                    "event_id": event_id,
                }
                stem = make_stem(target_slug, meta, event_id)
                csv_name = f"{stem}.csv"
                raw_name = f"{stem}.json"
                raw_path = ws.RAW_DIR / raw_name
                try:
                    if raw_path.exists():
                        details, cached_meta = ws.read_cached_event(raw_path)
                        meta.update(cached_meta)
                    else:
                        details, event_api_url = ws.event_results(event_id)
                        meta["event_api_url"] = event_api_url
                    rows, race_columns = ws.build_rows(details)
                except Exception as exc:
                    failures.append({**meta, "error": str(exc), "event_name": meta["event_label"]})
                    print("    ERROR", meta["year"], meta["event_label"], exc, flush=True)
                    continue
                if not rows:
                    print("    skip-empty", meta["year"], meta["event_label"], flush=True)
                    continue
                enriched = [{**meta, **row} for row in rows]
                write_csv(ws.CSV_DIR / csv_name, enriched, race_columns)
                (ws.RAW_DIR / raw_name).write_text(json.dumps({"meta": meta, "event": details}, ensure_ascii=False, indent=2), encoding="utf-8")
                item = {"meta": meta, "rows": rows, "csv_name": csv_name, "raw_name": raw_name}
                by_class[target_slug]["items"].append(item)
                registry.append({**meta, "csv": csv_name, "raw_json": raw_name, "classified_crews": len(rows)})
                print("    ", meta["year"], meta["event_label"], len(rows), "rows", flush=True)

    for data in by_class.values():
        if data["items"]:
            write_class_note(data["target"], data["items"])
    write_registry(registry)
    write_index(registry)
    write_not_found()
    if failures:
        (ws.OUT / "04-Errori-Estrazione.md").write_text(ws.failures_markdown(failures), encoding="utf-8")
    print(f"Registry rows: {len(registry)}", flush=True)


if __name__ == "__main__":
    main()
