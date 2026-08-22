#!/usr/bin/env python3
import csv
import json
from pathlib import Path

import extract_world_sailing_results as ws


ws.LEVEL_WORLD_CHAMPIONSHIPS = "b5bca920-933a-4845-9063-5e9f0952020e"
ws.OUT = ws.VAULT / "World Sailing European Results"
ws.CLASS_DIR = ws.OUT / "Classi"
ws.CSV_DIR = ws.OUT / "Dati CSV"
ws.RAW_DIR = ws.OUT / "Raw JSON"

SKIP_WORDS = [
    "cancelled",
    "canceled",
    "junior",
    "youth",
    "u21",
    "under-21",
    "under 21",
    "master",
    "eastern european",
]


def selected_regattas(target):
    params = {
        "filter[level.id]": ws.LEVEL_WORLD_CHAMPIONSHIPS,
        "filter[events.boatClass.id]": target["boat_id"],
        "filter[name]": "European",
        "filterOptions[name]": "subString",
        "include": "venue.country,level,season,events,events.boatClass,events.grade",
        "sort[startDate]": "desc",
        "paginate": "50",
    }
    payload, url = ws.request_json("/regatta", params)
    selected = []
    for regatta in payload.get("data", []):
        name = ws.clean_text(regatta.get("name"))
        end_date = ws.parse_date(regatta.get("endDate"))
        if not end_date or end_date > ws.TODAY:
            continue
        lowered = name.lower()
        if any(word in lowered for word in SKIP_WORDS):
            continue
        matching_events = [
            event for event in regatta.get("events", [])
            if ws.clean_text(event.get("_name")) in target["event_names"]
        ]
        for event in matching_events:
            selected.append({"regatta": regatta, "event": event})
        if len(selected) >= 6:
            break
    return selected[:6], url


def registry_markdown(registry):
    lines = [
        "# Registro campionati europei olimpici World Sailing",
        "",
        "Fonte: World Sailing API, livello `Continental`, risultati `Overall Results`.",
        "Filtro operativo: nome evento contenente `European`, esclusi junior/youth/U21/master/cancellati.",
        "Aggiornato: 2026-07-27.",
        "",
        "| Evento | Anno | Regata | Barche | CSV | Fonte |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in registry:
        lines.append(
            f"| {row['event_label']} | {row['year']} | {row['regatta_name']} | "
            f"{row['classified_crews']} | {row['csv']} | {row['source_url']} |"
        )
    return "\n".join(lines) + "\n"


def write_markdown(target, extracted):
    lines = [
        f"# {target['label']} - European Championships Overall Results",
        "",
        "Fonte primaria: World Sailing API / pagina Results > Overall Results.",
        "Criterio: ultimi 6 campionati europei senior passati disponibili, livello Continental.",
        "Uso: quadro europeo completo in CSV; in questa nota sintesi, podio e focus Italia.",
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
                f"### {meta['year']} - {meta['regatta_name']}",
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


def write_index_from_csv():
    items = []
    for path in sorted(ws.CSV_DIR.glob("*.csv")):
        with path.open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            continue
        first = rows[0]
        items.append({
            "event": first.get("event_label", ""),
            "year": first.get("start_date", "")[:4],
            "start": first.get("start_date", ""),
            "regatta": first.get("regatta_name", ""),
            "crews": len(rows),
            "csv": path.name,
            "source": first.get("source_url", ""),
        })
    grouped = {}
    for item in items:
        grouped.setdefault(item["event"], []).append(item)
    lines = [
        "# Indice classifiche finali Europei World Sailing",
        "",
        "Fonte: World Sailing `Results > Overall Results`.",
        "Uso: accesso rapido alle classifiche finali complete dei campionati europei olimpici estratti.",
        "",
        "Nota operativa: le classifiche complete restano in CSV per mantenere Obsidian veloce; le note di classe contengono podio e focus Italia.",
        "",
    ]
    for event in sorted(grouped):
        lines += [f"## {event}", "", "| Anno | Europeo | Equipaggi | Classifica completa | Fonte |", "| --- | --- | --- | --- | --- |"]
        for row in sorted(grouped[event], key=lambda x: x["start"], reverse=True):
            lines.append(
                f"| {row['year']} | {row['regatta']} | {row['crews']} | "
                f"[[Dati CSV/{row['csv']}|CSV]] | {row['source']} |"
            )
        lines.append("")
    (ws.OUT / "02-Indice-Classifiche-Finali.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ws.selected_regattas = selected_regattas
    ws.registry_markdown = registry_markdown
    ws.write_markdown = write_markdown
    ws.main()
    write_index_from_csv()


if __name__ == "__main__":
    main()
