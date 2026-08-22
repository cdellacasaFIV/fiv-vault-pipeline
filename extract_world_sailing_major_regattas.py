#!/usr/bin/env python3
import csv
import json

import extract_world_sailing_results as ws


ws.OUT = ws.VAULT / "World Sailing Major Regattas"
ws.CLASS_DIR = ws.OUT / "Classi"
ws.CSV_DIR = ws.OUT / "Dati CSV"
ws.RAW_DIR = ws.OUT / "Raw JSON"

REGATTA_SERIES = [
    {
        "slug": "Trofeo-Princesa-Sofia",
        "label": "Trofeo Princesa Sofia",
        "search": "Princesa Sofia",
        "max_editions": 6,
    },
    {
        "slug": "Semaine-Olympique-Francaise",
        "label": "Semaine Olympique Francaise",
        "search": "Semaine Olympique",
        "max_editions": 6,
    },
    {
        "slug": "Dutch-Water-Week",
        "label": "Dutch Water Week",
        "search": "Dutch Water Week",
        "max_editions": 6,
    },
    {
        "slug": "Kieler-Woche",
        "label": "Kieler Woche",
        "search": "Kieler Woche",
        "max_editions": 6,
    },
    {
        "slug": "Long-Beach-OCR",
        "label": "Long Beach Olympic Classes Regatta",
        "search": "Long Beach Olympic Classes Regatta",
        "max_editions": 6,
    },
    {
        "slug": "San-Pedro-OCR",
        "label": "San Pedro Olympic Classes Regatta",
        "search": "San Pedro Olympic Classes Regatta",
        "max_editions": 6,
    },
]

SKIP_WORDS = [
    "cancelled",
    "canceled",
    "no results",
    "junior",
    "youth",
    "u21",
    "under-21",
    "under 21",
    "master",
]


def regattas_for_series(series):
    params = {
        "filter[name]": series["search"],
        "filterOptions[name]": "subString",
        "include": "venue.country,level,season,events,events.boatClass,events.grade",
        "sort[startDate]": "desc",
        "paginate": "50",
    }
    payload, query_url = ws.request_json("/regatta", params)
    selected = []
    seen = set()
    for regatta in payload.get("data", []):
        name = ws.clean_text(regatta.get("name"))
        lowered = name.lower()
        end_date = ws.parse_date(regatta.get("endDate"))
        if not end_date or end_date > ws.TODAY or end_date < ws.RECENT_SINCE:
            continue
        if any(word in lowered for word in SKIP_WORDS):
            continue
        if regatta.get("worldSailingId") in seen:
            continue
        seen.add(regatta.get("worldSailingId"))
        selected.append(regatta)
        if len(selected) >= series["max_editions"]:
            break
    return selected, query_url


def registry_markdown(registry):
    lines = [
        "# Registro grandi regate World Sailing",
        "",
        "Fonte: World Sailing API, risultati `Overall Results`.",
        "Perimetro: grandi regate Olympic Classes / Sailing Grand Slam disponibili su World Sailing.",
        f"Aggiornato: {ws.TODAY.isoformat()}.",
        "",
        "| Regata | Evento | Anno | Edizione | Barche | CSV | Fonte |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in registry:
        lines.append(
            f"| {row['series_label']} | {row['event_label']} | {row['year']} | "
            f"{row['regatta_name']} | {row['classified_crews']} | {row['csv']} | {row['source_url']} |"
        )
    return "\n".join(lines) + "\n"


def write_markdown_by_series(registry):
    grouped = {}
    for row in registry:
        grouped.setdefault(row["series_label"], []).append(row)
    lines = [
        "# Indice classifiche finali grandi regate",
        "",
        "Fonte: World Sailing `Results > Overall Results`.",
        "Uso: accesso rapido alle classifiche finali complete delle maggiori regate Olympic Classes.",
        "",
    ]
    for series in sorted(grouped):
        lines += [f"## {series}", "", "| Anno | Classe | Edizione | Equipaggi | Classifica completa | Fonte |", "| --- | --- | --- | --- | --- | --- |"]
        for row in sorted(grouped[series], key=lambda x: (x["start_date"], x["event_label"]), reverse=True):
            lines.append(
                f"| {row['year']} | {row['event_label']} | {row['regatta_name']} | "
                f"{row['classified_crews']} | [[Dati CSV/{row['csv']}|CSV]] | {row['source_url']} |"
            )
        lines.append("")
    (ws.OUT / "02-Indice-Classifiche-Finali.md").write_text("\n".join(lines), encoding="utf-8")


def write_markdown_by_class(target, extracted):
    lines = [
        f"# {target['label']} - Major Regattas Overall Results",
        "",
        "Fonte primaria: World Sailing API / pagina Results > Overall Results.",
        "Criterio: grandi regate Olympic Classes selezionate, edizioni passate disponibili, classifica finale.",
        "",
        "## File dati completi",
        "",
    ]
    for item in extracted:
        lines.append(f"- `{item['csv_name']}`")
    lines.extend(["", "## Sintesi eventi", ""])
    for item in extracted:
        meta = item["meta"]
        rows = item["rows"]
        italy = [r for r in rows if r.get("country") == "ITA"]
        podium = [r for r in rows if str(r.get("rank")) in {"1", "2", "3"}]
        lines.extend(
            [
                f"### {meta['year']} - {meta['series_label']} - {meta['regatta_name']}",
                "",
                f"Fonte: {meta['source_url']}",
                f"Date: {meta['start_date']} - {meta['end_date']}",
                f"Sede: {meta['venue']}",
                f"Evento: {target['label']}",
                f"Barche classificate: {len(rows)}",
                "",
                "#### Podio",
                "",
                ws.md_table(podium, ["rank", "country", "crew", "net_points", "total_points"]) if podium else "Nessun podio disponibile.",
                "",
                "#### Italiani",
                "",
                ws.md_table(italy, ["rank", "crew", "sail_number", "net_points", "total_points"]) if italy else "Nessun equipaggio italiano trovato nella classifica.",
                "",
            ]
        )
    (ws.CLASS_DIR / f"{target['slug']}.md").write_text("\n".join(lines), encoding="utf-8")


def write_csv(path, rows, race_columns):
    base_fields = [
        "series_label",
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
        for row in rows:
            writer.writerow(row)


def main():
    ws.CLASS_DIR.mkdir(parents=True, exist_ok=True)
    ws.CSV_DIR.mkdir(parents=True, exist_ok=True)
    ws.RAW_DIR.mkdir(parents=True, exist_ok=True)
    registry = []
    failures = []
    extracted_by_class = {target["slug"]: {"target": target, "items": []} for target in ws.TARGETS}

    for series in REGATTA_SERIES:
        regattas, query_url = regattas_for_series(series)
        print(f"{series['label']}: {len(regattas)} editions", flush=True)
        for regatta in regattas:
            events_by_name = {ws.clean_text(event.get("_name")): event for event in regatta.get("events", [])}
            for target in ws.TARGETS:
                for event_name in target["event_names"]:
                    event = events_by_name.get(event_name)
                    if not event:
                        continue
                    venue = regatta.get("venue") or {}
                    country = venue.get("country") or {}
                    venue_text = ", ".join(x for x in [venue.get("name"), country.get("name")] if x)
                    meta = {
                        "series_label": series["label"],
                        "series_slug": series["slug"],
                        "event_label": target["label"],
                        "regatta_name": ws.clean_text(regatta.get("name")),
                        "world_sailing_id": ws.clean_text(regatta.get("worldSailingId")),
                        "start_date": ws.clean_text(regatta.get("startDate"))[:10],
                        "end_date": ws.clean_text(regatta.get("endDate"))[:10],
                        "year": ws.clean_text(regatta.get("startDate"))[:4],
                        "venue": venue_text,
                        "source_url": ws.event_url(regatta),
                        "event_api_url": "",
                        "regatta_query_url": query_url,
                        "event_id": event["id"],
                    }
                    stem = f"{series['slug']}__{target['slug']}__{meta['year']}__{ws.slugify(meta['regatta_name'])}"
                    csv_name = f"{stem}.csv"
                    raw_name = f"{stem}.json"
                    raw_path = ws.RAW_DIR / raw_name
                    try:
                        if raw_path.exists():
                            details, cached_meta = ws.read_cached_event(raw_path)
                            meta.update(cached_meta)
                            print("  cache", series["label"], target["label"], meta["year"], flush=True)
                        else:
                            details, event_api_url = ws.event_results(event["id"])
                            meta["event_api_url"] = event_api_url
                        rows, race_columns = ws.build_rows(details)
                    except Exception as exc:
                        failures.append({**meta, "error": str(exc), "event_name": event_name})
                        print("  ERROR", series["label"], target["label"], meta["year"], exc, flush=True)
                        continue
                    if not rows:
                        csv_path = ws.CSV_DIR / csv_name
                        if csv_path.exists():
                            csv_path.unlink()
                        if raw_path.exists():
                            raw_path.unlink()
                        print("  skip-empty", series["label"], target["label"], meta["year"], flush=True)
                        continue
                    enriched = [{**meta, **row} for row in rows]
                    write_csv(ws.CSV_DIR / csv_name, enriched, race_columns)
                    (ws.RAW_DIR / raw_name).write_text(json.dumps({"meta": meta, "event": details}, ensure_ascii=False, indent=2), encoding="utf-8")
                    item = {"meta": meta, "rows": rows, "csv_name": csv_name, "raw_name": raw_name}
                    extracted_by_class[target["slug"]]["items"].append(item)
                    registry.append({**meta, "csv": csv_name, "raw_json": raw_name, "classified_crews": len(rows)})
                    print(" ", series["label"], target["label"], meta["year"], len(rows), "crews", flush=True)

    for data in extracted_by_class.values():
        if data["items"]:
            write_markdown_by_class(data["target"], data["items"])
    (ws.OUT / "01-Registro-Grandi-Regate.csv").write_text("", encoding="utf-8")
    if registry:
        fields = list(registry[0].keys())
        with (ws.OUT / "01-Registro-Grandi-Regate.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(registry)
    (ws.OUT / "01-Registro-Grandi-Regate.md").write_text(registry_markdown(registry), encoding="utf-8")
    write_markdown_by_series(registry)
    if failures:
        (ws.OUT / "03-Errori-Estrazione.md").write_text(ws.failures_markdown(failures), encoding="utf-8")
    print(f"Registry rows: {len(registry)}", flush=True)


if __name__ == "__main__":
    main()
