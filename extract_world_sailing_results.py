#!/usr/bin/env python3
import csv
import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path


API = "https://datafeed.sailing.org/stats/api"
LEVEL_WORLD_CHAMPIONSHIPS = "568d0c5a-aa65-43b1-b9f0-a32f0b569a64"
TODAY = date.today()
RECENT_SINCE = TODAY - timedelta(days=60)

# FIV_VAULT_ROOT permette di puntare a una cartella diversa (es. sandbox cloud)
# senza toccare il path di default usato in locale sul Mac di Carlo.
VAULT = Path(os.environ.get(
    "FIV_VAULT_ROOT",
    "/Users/carlodellacasa/Library/CloudStorage/GoogleDrive-c.dellacasa@federvela.it/"
    "Il mio Drive/vault obsidian/FIV",
))
OUT = VAULT / "World Sailing Results"
CLASS_DIR = OUT / "Classi"
CSV_DIR = OUT / "Dati CSV"
RAW_DIR = OUT / "Raw JSON"

TARGETS = [
    {
        "slug": "49er",
        "label": "49er Men",
        "boat_class": "49er",
        "boat_id": "e33a39e8-fbd3-45b4-a249-0ffbe429d69c",
        "event_names": ["49er Men"],
    },
    {
        "slug": "49erFX",
        "label": "49erFX Women",
        "boat_class": "49erFX",
        "boat_id": "cfe2f66b-fb39-474e-b9b1-cbc439f0f49d",
        "event_names": ["49erFX Women"],
    },
    {
        "slug": "Nacra-17",
        "label": "Nacra 17 Mixed",
        "boat_class": "Nacra 17",
        "boat_id": "1e137f82-7f75-4d14-a286-7e8ac6f93939",
        "event_names": ["Nacra 17 Mixed"],
    },
    {
        "slug": "470",
        "label": "470 Mixed",
        "boat_class": "470",
        "boat_id": "70949fd4-bc75-434c-ac1c-d1763b6d0e67",
        "event_names": ["470 Mixed"],
    },
    {
        "slug": "ILCA-7",
        "label": "ILCA 7 Men",
        "boat_class": "ILCA 7",
        "boat_id": "08f69112-1aef-40be-afeb-7e606f8b27a0",
        "event_names": ["ILCA 7 Men"],
    },
    {
        "slug": "ILCA-6",
        "label": "ILCA 6 Women",
        "boat_class": "ILCA 6",
        "boat_id": "bfa92fb9-2ef1-450a-b292-29cbf4f6d755",
        "event_names": ["ILCA 6 Women"],
    },
    {
        "slug": "IQFOiL-Men",
        "label": "IQFOiL Men",
        "boat_class": "IQFOiL",
        "boat_id": "97f58788-3109-408a-a3c3-9addf8a145a1",
        "event_names": ["IQFOiL Men"],
    },
    {
        "slug": "IQFOiL-Women",
        "label": "IQFOiL Women",
        "boat_class": "IQFOiL",
        "boat_id": "97f58788-3109-408a-a3c3-9addf8a145a1",
        "event_names": ["IQFOiL Women"],
    },
    {
        "slug": "Formula-Kite-Men",
        "label": "Formula Kite Men",
        "boat_class": "IKA - Formula Kite",
        "boat_id": "4e1f06bf-915e-404c-8d1a-aa6b83ae5d60",
        "event_names": ["IKA - Formula Kite Men"],
    },
    {
        "slug": "Formula-Kite-Women",
        "label": "Formula Kite Women",
        "boat_class": "IKA - Formula Kite",
        "boat_id": "4e1f06bf-915e-404c-8d1a-aa6b83ae5d60",
        "event_names": ["IKA - Formula Kite Women"],
    },
]


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def slugify(value):
    value = value.replace("&", "and")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value or "event"


def request_json(path, params=None):
    params = params or {}
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    ctx = ssl._create_unverified_context()
    headers = {"User-Agent": "FIV-Obsidian-Research/1.0"}
    headers["Connection"] = "close"
    req = urllib.request.Request(url, headers=headers)
    last_error = None
    for _ in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=90) as res:
                return json.loads(res.read().decode("utf-8")), url
        except Exception as exc:
            last_error = exc
            time.sleep(1.5)
    raise RuntimeError(f"API request failed: {url} ({last_error})")


def clean_text(value):
    if value is None:
        return ""
    return str(value).replace("\n", " ").strip()


def crew_name(crew):
    sailors = sorted(
        crew.get("sailors", []),
        key=lambda s: 0 if (s.get("crewRole") or {}).get("name") == "skipper" else 1,
    )
    return " / ".join(clean_text(s.get("name")) for s in sailors if s.get("name"))


def sailor_ids(crew):
    return " / ".join(
        clean_text(s.get("worldSailingId")) for s in crew.get("sailors", []) if s.get("worldSailingId")
    )


def race_output(result):
    if not result:
        return "-"
    placing = result.get("awardPlacing")
    if placing is None:
        placing = result.get("placing")
    status = ((result.get("crewCompetingStatus") or {}).get("sourceId")) or ""
    value = "-" if placing is None else str(placing)
    if clean_text(result.get("discarded")).lower().startswith("y"):
        value = f"({value})"
    return f"{value} {status}".strip()


def rank_key(crew):
    pos = crew.get("position")
    try:
        return int(pos)
    except Exception:
        return 99999


def selected_regattas(target):
    params = {
        "filter[level.id]": LEVEL_WORLD_CHAMPIONSHIPS,
        "filter[events.boatClass.id]": target["boat_id"],
        "include": "venue.country,level,season,events,events.boatClass,events.grade",
        "sort[startDate]": "desc",
        "paginate": "50",
    }
    payload, url = request_json("/regatta", params)
    selected = []
    for regatta in payload.get("data", []):
        name = clean_text(regatta.get("name"))
        end_date = parse_date(regatta.get("endDate"))
        if not end_date or end_date > TODAY or end_date < RECENT_SINCE:
            continue
        lowered = name.lower()
        if "cancelled" in lowered or "canceled" in lowered:
            continue
        if any(word in lowered for word in ["junior", "u19", "youth", "under-21", "under 21"]):
            continue
        matching_events = [
            event for event in regatta.get("events", [])
            if clean_text(event.get("_name")) in target["event_names"]
        ]
        for event in matching_events:
            selected.append({"regatta": regatta, "event": event})
        if len(selected) >= 6:
            break
    return selected[:6], url


def event_results(event_id):
    include = (
        "crews.country,crews.sailors.crewRole,"
        "races.raceResults.crew.country,races.raceResults.crew.sailors,"
        "races.raceResults.crewCompetingStatus,races.status"
    )
    payload, url = request_json(f"/event/{event_id}", {"include": include})
    return payload.get("data") or {}, url


def event_url(regatta):
    slug = slugify(regatta.get("name", "")).lower()
    return f"https://sailing.org/regatta/{slug}?ref={regatta.get('worldSailingId')}"


def build_rows(event):
    races = sorted(event.get("races", []), key=lambda r: int(r.get("number") or 999))
    crews = sorted(event.get("crews", []), key=rank_key)
    rows = []
    for crew in crews:
        race_map = {}
        for race in races:
            found = None
            for rr in race.get("raceResults", []):
                if (rr.get("crew") or {}).get("id") == crew.get("id"):
                    found = rr
                    break
            race_map[race.get("name") or f"R{race.get('number')}"] = race_output(found)
        country = crew.get("country") or {}
        rows.append(
            {
                "rank": crew.get("position") or "",
                "country": country.get("countryCode") or "",
                "country_name": country.get("name") or "",
                "crew": crew_name(crew),
                "world_sailing_ids": sailor_ids(crew),
                "sail_number": crew.get("sailNumber") or "",
                "total_points": crew.get("totalPoints") if crew.get("totalPoints") is not None else "",
                "net_points": crew.get("points") if crew.get("points") is not None else "",
                **race_map,
            }
        )
    return rows, [race.get("name") or f"R{race.get('number')}" for race in races]


def write_csv(path, rows, race_columns):
    base_fields = [
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


def md_table(rows, headers):
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(clean_text(row.get(h, "")) for h in headers) + " |")
    return "\n".join(out)


def write_markdown(target, extracted):
    lines = [
        f"# {target['label']} - World Championships Overall Results",
        "",
        "Fonte primaria: World Sailing API / pagina Results > Overall Results.",
        "Criterio: ultimi 6 mondiali passati, non cancellati, con livello World Championships.",
        "Uso: quadro mondiale completo in CSV; in questa nota sintesi, podio e focus Italia.",
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
                md_table(podium, ["rank", "country", "crew", "net_points", "total_points"]) if podium else "Nessun podio disponibile.",
                "",
                "#### Italiani",
                "",
                md_table(italy, ["rank", "crew", "sail_number", "net_points", "total_points"]) if italy else "Nessun equipaggio italiano trovato nella classifica.",
                "",
            ]
        )
    (CLASS_DIR / f"{target['slug']}.md").write_text("\n".join(lines), encoding="utf-8")


def read_cached_event(raw_path):
    cached = json.loads(raw_path.read_text(encoding="utf-8"))
    return cached["event"], cached["meta"]


def main():
    CLASS_DIR.mkdir(parents=True, exist_ok=True)
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    registry = []
    failures = []
    for target in TARGETS:
        selected, query_url = selected_regattas(target)
        extracted = []
        print(f"{target['label']}: {len(selected)} events", flush=True)
        for item in selected:
            regatta = item["regatta"]
            event = item["event"]
            venue = regatta.get("venue") or {}
            country = venue.get("country") or {}
            venue_text = ", ".join(x for x in [venue.get("name"), country.get("name")] if x)
            source = event_url(regatta)
            meta = {
                "event_label": target["label"],
                "regatta_name": clean_text(regatta.get("name")),
                "world_sailing_id": clean_text(regatta.get("worldSailingId")),
                "start_date": clean_text(regatta.get("startDate"))[:10],
                "end_date": clean_text(regatta.get("endDate"))[:10],
                "year": clean_text(regatta.get("startDate"))[:4],
                "venue": venue_text,
                "source_url": source,
                "event_api_url": "",
                "regatta_query_url": query_url,
                "event_id": event["id"],
            }
            csv_name = f"{target['slug']}__{meta['year']}__{slugify(meta['regatta_name'])}.csv"
            raw_name = f"{target['slug']}__{meta['year']}__{slugify(meta['regatta_name'])}.json"
            raw_path = RAW_DIR / raw_name
            if raw_path.exists():
                details, cached_meta = read_cached_event(raw_path)
                meta.update(cached_meta)
                print("  cache", meta["year"], meta["regatta_name"], flush=True)
            else:
                try:
                    details, event_api_url = event_results(event["id"])
                except Exception as exc:
                    failure = {
                        **meta,
                        "error": str(exc),
                        "event_name": clean_text(event.get("_name")),
                    }
                    failures.append(failure)
                    print("  ERROR", meta["year"], meta["regatta_name"], failure["event_name"], exc, flush=True)
                    continue
                meta["event_api_url"] = event_api_url
            rows, race_columns = build_rows(details)
            enriched = [{**meta, **row} for row in rows]
            write_csv(CSV_DIR / csv_name, enriched, race_columns)
            (RAW_DIR / raw_name).write_text(json.dumps({"meta": meta, "event": details}, ensure_ascii=False, indent=2), encoding="utf-8")
            extracted.append({"meta": meta, "rows": rows, "csv_name": csv_name, "raw_name": raw_name})
            registry.append({**meta, "csv": csv_name, "raw_json": raw_name, "classified_crews": len(rows)})
            print(" ", meta["year"], meta["regatta_name"], len(rows), "crews", flush=True)
        write_markdown(target, extracted)
    write_csv(OUT / "01-Registro-Mondiali-Olimpici.csv", registry, [])
    (OUT / "01-Registro-Mondiali-Olimpici.md").write_text(registry_markdown(registry), encoding="utf-8")
    if failures:
        (OUT / "03-Errori-Estrazione.md").write_text(failures_markdown(failures), encoding="utf-8")
    print(f"Registry rows: {len(registry)}", flush=True)


def registry_markdown(registry):
    lines = [
        "# Registro mondiali olimpici World Sailing",
        "",
        "Fonte: World Sailing API, livello `World Championships`, risultati `Overall Results`.",
        f"Aggiornato: {TODAY.isoformat()}.",
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


def failures_markdown(failures):
    lines = [
        "# Errori estrazione World Sailing",
        "",
        "Questi eventi sono stati selezionati dai filtri, ma l'API World Sailing non ha restituito il dettaglio `Overall Results`.",
        "",
        "| Evento | Anno | Regata | Classe interna | Errore | Fonte |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in failures:
        lines.append(
            f"| {row['event_label']} | {row['year']} | {row['regatta_name']} | "
            f"{row.get('event_name', '')} | {row['error'].replace('|', '/')} | {row['source_url']} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
