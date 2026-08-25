#!/usr/bin/env python3
import os
import re
import unicodedata
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


VAULT = Path(os.environ.get(
    "FIV_VAULT_ROOT",
    "/Users/carlodellacasa/Library/CloudStorage/GoogleDrive-c.dellacasa@federvela.it/"
    "Il mio Drive/vault obsidian/FIV",
))

API_BASE = "https://sportvela.net/wp-json/wp/v2"
AFTER = "2020-01-01T00:00:00"
TODAY = date.today().isoformat()

OUT = VAULT / "Fonti Esterne" / "SportVela News"
ARTICLE_DIR = OUT / "Articoli"
YEAR_INDEX_DIR = OUT / "Indici" / "Per Anno"
THEME_INDEX_DIR = OUT / "Indici" / "Per Tema"


KEYWORDS = {
    "risultati": ["oro", "argento", "bronzo", "podio", "classifica", "posto", "campione", "campionessa", "titolo", "medaglia"],
    "olimpica": ["ilca", "49er", "49erfx", "nacra 17", "iqfoil", "formula kite", "olimpic", "mission paris"],
    "giovanile": ["youth", "junior", "under", "u15", "u17", "u19", "giovan", "scuola vela", "scuole di vela"],
    "para/inclusione": ["para", "disabil", "inclus", "barriere", "hansa", "venture connect", "vela per tutti"],
    "zone/circoli": ["yacht club", "circolo", "club nautico", "zona", "scuole di vela", "meeting provinciale"],
    "america's cup/napoli": ["america's cup", "americas cup", "napoli", "caivano", "partenope"],
    "media/storytelling": ["libro", "racconta", "storie", "presentazione", "evento", "festival"],
}

CLASS_PATTERNS = [
    "49erFX", "49er", "Nacra 17", "Nacra 15", "ILCA 7", "ILCA 6", "ILCA 4",
    "IQFOiL", "iQFOiL", "Formula Kite", "Techno 293", "420", "470", "Waszp",
    "RS21", "Dinghy 12", "Vaurien", "J70", "Slalom X", "Foiling Week", "Hansa",
    "Para Sailing", "WingFoil", "Wing Foil",
]

MONTHS = {
    "01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile",
    "05": "Maggio", "06": "Giugno", "07": "Luglio", "08": "Agosto",
    "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre",
}


def slugify(value):
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.replace("&", "and")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")
    return value[:110] or "sportvela-news"


def clean_text(value):
    value = BeautifulSoup(value or "", "html.parser").get_text(" ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def unique(values):
    out = []
    seen = set()
    for value in values:
        value = clean_text(value)
        key = value.lower()
        if value and key not in seen:
            seen.add(key)
            out.append(value)
    return out


def rel_no_ext(path):
    return path.relative_to(VAULT).with_suffix("").as_posix()


def md_escape(value):
    return clean_text(value).replace("|", "/")


def request_json(session, path, params=None):
    response = session.get(f"{API_BASE}{path}", params=params or {}, timeout=40)
    response.raise_for_status()
    return response


def all_categories(session):
    response = request_json(session, "/categories", {"per_page": 100})
    return response.json()


def news_category_ids(categories):
    by_parent = defaultdict(list)
    by_slug = {}
    for cat in categories:
        by_parent[cat.get("parent")].append(cat)
        by_slug[cat.get("slug")] = cat
    root = by_slug.get("news")
    if not root:
        return [], {}
    ids = []
    stack = [root["id"]]
    while stack:
        cat_id = stack.pop()
        ids.append(cat_id)
        stack.extend(child["id"] for child in by_parent.get(cat_id, []))
    names = {cat["id"]: cat["name"] for cat in categories}
    return sorted(set(ids)), names


def fetch_posts(session, category_ids):
    posts = {}
    page = 1
    params = {
        "categories": ",".join(str(i) for i in category_ids),
        "after": AFTER,
        "per_page": 100,
        "page": page,
        "orderby": "date",
        "order": "desc",
        "status": "publish",
    }
    while True:
        params["page"] = page
        response = request_json(session, "/posts", params)
        for post in response.json():
            posts[post["id"]] = post
        total_pages = int(response.headers.get("X-WP-TotalPages", "1"))
        print(f"Fetched posts page {page}/{total_pages}: total unique {len(posts)}")
        if page >= total_pages:
            break
        page += 1
    return sorted(posts.values(), key=lambda p: p.get("date", ""), reverse=True)


def date_label(post):
    raw = post.get("date", "")
    try:
        dt = datetime.fromisoformat(raw)
        return f"{dt.day} {MONTHS[dt.strftime('%m')]} {dt.year}", str(dt.year), dt.date().isoformat()
    except ValueError:
        year = raw[:4] or "Senza anno"
        return raw, year, raw[:10]


def post_text(post):
    title = clean_text(post.get("title", {}).get("rendered", ""))
    excerpt = clean_text(post.get("excerpt", {}).get("rendered", ""))
    content = clean_text(post.get("content", {}).get("rendered", ""))
    return title, excerpt, content


def themes(title, excerpt, content, category_names):
    hay = " ".join([title, excerpt, content, " ".join(category_names)]).lower()
    out = []
    for label, words in KEYWORDS.items():
        if any(word in hay for word in words):
            out.append(label)
    return out or ["contesto vela"]


def useful(title, excerpt, content, category_names):
    hay = " ".join([title, excerpt, content, " ".join(category_names)]).lower()
    needles = [
        "italia", "italian", "fiv", "federvela", "campionato", "europeo", "mondiale",
        "vela olimpica", "vela giovanile", "para", "scuole di vela", "zona", "yacht club",
        "oro", "argento", "bronzo", "podio", "titolo", "classifica", "america's cup", "napoli",
    ]
    return any(n in hay for n in needles)


def proper_phrases(text):
    candidates = re.findall(
        r"\b(?:[A-ZÀ-Ú][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)(?:\s+(?:di|del|della|dei|degli|"
        r"da|de|e|[A-ZÀ-Ú][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)){0,3}",
        text,
    )
    blacklist = {
        "News", "Vela", "SportVela", "Leggi", "Facebook", "Instagram", "YouTube",
        "Luglio", "Giugno", "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio",
        "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre", "Copertina", "Vetrina",
        "Nel", "Nella", "Nelle", "Nello",
    }
    cleaned = []
    for item in candidates:
        item = clean_text(item)
        item = re.split(r"\s+(?:Nel|Nella|Nelle|Nello|L’Italia|L Italia)\b", item)[0].strip()
        item = re.sub(r"\s+(?:e|di|del|della|dei|degli|da|de)$", "", item).strip()
        if len(item) < 4 or item in blacklist:
            continue
        if item.split()[0] in {"Nel", "Nella", "Nelle", "Nello"}:
            continue
        if len(item.split()) > 5:
            continue
        cleaned.append(item)
    return unique(cleaned)[:14]


def numbers_and_dates(text):
    values = re.findall(
        r"\b\d{1,4}(?:[.,]\d+)?\b(?:\s?(?:anni|atleti|equipaggi|bambini|giorni|medaglie|posto|titoli))?",
        text,
        re.I,
    )
    return unique(values)[:10]


def context_factlets(theme_list, title, excerpt, content):
    text = " ".join([title, excerpt, content])
    low = text.lower()
    classes = [name for name in CLASS_PATTERNS if name.lower() in low]
    names = proper_phrases(text)
    nums = numbers_and_dates(text)
    angle = []
    if "risultati" in theme_list:
        angle.append("risultato sportivo da incrociare con fonte ufficiale prima di storicizzare")
    if "giovanile" in theme_list:
        angle.append("sviluppo giovanile e vivaio")
    if "para/inclusione" in theme_list:
        angle.append("inclusione/accessibilita' e valore istituzionale")
    if "zone/circoli" in theme_list:
        angle.append("territori, circoli e zone")
    if "olimpica" in theme_list:
        angle.append("classi olimpiche o percorso alto livello")
    if "america's cup/napoli" in theme_list:
        angle.append("legacy America's Cup Napoli e promozione territoriale")
    return [
        f"- Temi operativi: {', '.join(theme_list)}.",
        f"- Angoli editoriali: {', '.join(angle) if angle else 'contesto generale della vela italiana'}.",
        f"- Classi/discipline citate: {', '.join(classes) if classes else 'non isolate automaticamente'}.",
        f"- Nomi, circoli o luoghi da valutare: {', '.join(names) if names else 'non isolati automaticamente'}.",
        f"- Numeri/date utili da verificare: {', '.join(nums) if nums else 'nessun numero isolato automaticamente'}.",
        "- Sommario fonte presente: usarlo come controllo rapido, senza copiarlo nelle news operative.",
    ]


def obsidian_links(theme_list):
    links = []
    if "risultati" in theme_list or "olimpica" in theme_list:
        links.append("[[World Sailing - Mappa Atleti e Classifiche]]")
    if "giovanile" in theme_list:
        links.append("[[World Sailing Youth Para Results/02-Indice-Classifiche-Finali|Youth & Para Results]]")
    if "para/inclusione" in theme_list:
        links.append("[[Istituzionale FIV/00-Overview|Istituzionale FIV]]")
    if "america's cup/napoli" in theme_list:
        links.append("[[America's Cup Napoli/00-Overview|America's Cup Napoli]]")
    if "zone/circoli" in theme_list:
        links.append("[[comunicati stampa sportivi/_Indice-Atleti-Circoli|Atleti e circoli]]")
    links.append("[[Modelli/Modello-News-Evento|Modello news evento]]")
    return list(dict.fromkeys(links))


def reset_generated_dirs():
    # NOTA (2026-08-23): rimosso il backup locale su _backup/<cartella>-<data> che veniva
    # rifatto ad ogni run: la cronologia git del repository e' gia' il backup reale (ogni
    # commit "Auto-fetch dati esterni" conserva lo stato precedente), quindi copiare tutto
    # in una sottocartella datata ogni notte produceva solo un raddoppio del repository
    # e un delta falso enorme per la pipeline di sync a valle. Non serve piu' ricrearlo.
    for directory in [ARTICLE_DIR, YEAR_INDEX_DIR, THEME_INDEX_DIR]:
        if directory.exists():
            for path in sorted(directory.rglob("*.md")):
                path.unlink()
        directory.mkdir(parents=True, exist_ok=True)
    # Keep legacy material intact; new runs should not destroy any previous archive state.


def article_note(post, cat_names):
    title, excerpt, content = post_text(post)
    label, year, iso_date = date_label(post)
    theme_list = themes(title, excerpt, content, cat_names)
    year_dir = ARTICLE_DIR / year
    year_dir.mkdir(parents=True, exist_ok=True)
    note_path = year_dir / f"{iso_date} - {slugify(title)} - wp{post['id']}.md"
    lines = [
        f"# {title}",
        "",
        "Stato fonte: **fonte esterna SportVela**.",
        "Uso nel vault: contesto editoriale e spunti news; verificare con fonte FIV/World Sailing prima di usare come storico ufficiale risultati.",
        "",
        "## Fonte",
        "",
        f"- Data SportVela: {label}",
        f"- Link: {post.get('link', '')}",
        f"- Categorie: {', '.join(cat_names) or '-'}",
        "",
        "## Perche' tenerla",
        "",
        f"- Filoni: {', '.join(theme_list)}",
        "- Valore: aiuta a ricostruire contesto, narrativa, territori/circoli, risultati o iniziative collegate alla memoria FIV.",
        "",
        "## Sintesi operativa",
        "",
    ]
    lines.extend(context_factlets(theme_list, title, excerpt, content))
    lines += [
        "",
        "## Collegamenti utili",
        "",
    ]
    lines.extend(f"- {link}" for link in obsidian_links(theme_list))
    lines += [
        "",
        "## Uso editoriale",
        "",
        "- Se la notizia riguarda risultati: usarla come spunto e incrociare con comunicato ufficiale/FIV o Overall Results.",
        "- Se la notizia riguarda territori, circoli, inclusione o scuola vela: collegarla alla sezione istituzionale o zona/circolo.",
        "- Non copiare integralmente il testo della fonte: conservare sintesi, fonte e contesto operativo.",
    ]
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "post": post,
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "date_label": label,
        "year": year,
        "iso_date": iso_date,
        "categories": cat_names,
        "themes": theme_list,
        "note_path": note_path,
    }


# NOTA (2026-08-24): i file indice "Per Anno"/"Per Tema" possono superare 1000 righe e
# 250-300KB quando un anno/tema accumula molte news. Un file cosi' grande e' impossibile da
# sincronizzare in sicurezza sul vault Drive tramite l'agente conversazionale della routine
# (il contenuto andrebbe riprodotto per intero in un'unica chiamata, con rischio concreto di
# troncamento). Per restare sempre sotto una soglia sicura, se un indice supera MAX_ROWS_PER_INDEX_FILE
# righe lo spezziamo in piu' file "-parte-N" invece di scriverne uno solo enorme.
MAX_ROWS_PER_INDEX_FILE = 250


def _write_index_shards(path_no_ext, title, subtitle, header_row, row_lines):
    """Scrive uno o piu' file per un indice, spezzando ogni MAX_ROWS_PER_INDEX_FILE righe.
    Ritorna la lista dei Path effettivamente scritti, in ordine di lettura (piu' recente prima)."""
    n = len(row_lines)
    if n <= MAX_ROWS_PER_INDEX_FILE:
        path = path_no_ext.with_suffix(".md")
        lines = [title, "", subtitle, "", header_row[0], header_row[1]] + row_lines
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return [path]

    chunks = [row_lines[i:i + MAX_ROWS_PER_INDEX_FILE] for i in range(0, n, MAX_ROWS_PER_INDEX_FILE)]
    total = len(chunks)
    paths = []
    for idx, chunk in enumerate(chunks, start=1):
        path = path_no_ext.parent / f"{path_no_ext.name}-parte-{idx}.md"
        nav = f"Parte {idx} di {total} (indice spezzato automaticamente oltre {MAX_ROWS_PER_INDEX_FILE} righe per restare sincronizzabile)."
        lines = [title, "", subtitle, "", nav, "", header_row[0], header_row[1]] + chunk
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def write_indices(records, category_ids):
    records = sorted(records, key=lambda r: r["iso_date"], reverse=True)
    registry = [
        "# Registro fonti SportVela",
        "",
        "Stato fonte: **fonte esterna SportVela**.",
        f"Aggiornato: {TODAY}.",
        "",
        "| Data | Titolo | Categorie | Temi | Nota | Fonte |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    by_year = defaultdict(list)
    by_theme = defaultdict(list)
    for rec in records:
        registry.append(
            f"| {rec['date_label']} | {md_escape(rec['title'])} | {md_escape(', '.join(rec['categories']))} | "
            f"{md_escape(', '.join(rec['themes']))} | [[{rel_no_ext(rec['note_path'])}|nota]] | {rec['post'].get('link', '')} |"
        )
        by_year[rec["year"]].append(rec)
        for theme in rec["themes"]:
            by_theme[theme].append(rec)
    (OUT / "01-Registro-Fonti.md").write_text("\n".join(registry) + "\n", encoding="utf-8")

    year_links = []
    for year, rows in sorted(by_year.items(), reverse=True):
        row_lines = [
            f"| {rec['date_label']} | {md_escape(rec['title'])} | {md_escape(', '.join(rec['themes']))} | "
            f"[[{rel_no_ext(rec['note_path'])}|nota]] |"
            for rec in rows
        ]
        paths = _write_index_shards(
            YEAR_INDEX_DIR / f"{year}",
            f"# SportVela News {year}",
            "Indice annuale delle news SportVela archiviate come contesto editoriale.",
            ("| Data | Titolo | Temi | Nota |", "| --- | --- | --- | --- |"),
            row_lines,
        )
        if len(paths) == 1:
            year_links.append(f"- [[{rel_no_ext(paths[0])}|{year}]] ({len(rows)} news)")
        else:
            year_links.append(f"- {year} ({len(rows)} news, spezzato in {len(paths)} parti):")
            for p in paths:
                year_links.append(f"  - [[{rel_no_ext(p)}|{p.stem}]]")

    theme_links = []
    for theme, rows in sorted(by_theme.items()):
        row_lines = [
            f"| {rec['date_label']} | {md_escape(rec['title'])} | {md_escape(', '.join(rec['categories']))} | "
            f"[[{rel_no_ext(rec['note_path'])}|nota]] |"
            for rec in rows
        ]
        paths = _write_index_shards(
            THEME_INDEX_DIR / slugify(theme),
            f"# SportVela - {theme}",
            "Indice tematico per consultare rapidamente news SportVela collegate alla memoria FIV.",
            ("| Data | Titolo | Categorie | Nota |", "| --- | --- | --- | --- |"),
            row_lines,
        )
        if len(paths) == 1:
            theme_links.append(f"- [[{rel_no_ext(paths[0])}|{theme}]] ({len(rows)} news)")
        else:
            theme_links.append(f"- {theme} ({len(rows)} news, spezzato in {len(paths)} parti):")
            for p in paths:
                theme_links.append(f"  - [[{rel_no_ext(p)}|{p.stem}]]")

    dates = [r["iso_date"] for r in records]
    overview = [
        "# SportVela News - contesto editoriale",
        "",
        "Sezione per usare SportVela come fonte esterna di contesto, spunti e memoria editoriale.",
        "",
        "## Regola d'uso",
        "",
        "- Fonte: SportVela, non fonte ufficiale primaria per risultati.",
        "- Usare per ricostruire contesto, angoli narrativi, territori, circoli, classi e temi emergenti.",
        "- Incrociare risultati sportivi con comunicati FIV o World Sailing prima di aggiornarli come storico ufficiale.",
        "",
        "## Link rapidi",
        "",
        "- [[Fonti Esterne/SportVela News/01-Registro-Fonti|Registro fonti]]",
        "- [[Fonti Esterne/SportVela News/02-Mappa-Tematica|Mappa tematica]]",
        "- [[World Sailing - Mappa Atleti e Classifiche]]",
        "- [[Istituzionale FIV/00-Overview]]",
        "- [[comunicati stampa sportivi/_Indice-Atleti-Circoli]]",
        "",
        "## Copertura",
        "",
        f"- Cutoff richiesto: dal 2020 in avanti.",
        f"- Categoria API: News + sottocategorie ({len(category_ids)} categorie).",
        f"- Articoli utili archiviati: {len(records)}",
        f"- Intervallo effettivo trovato: {min(dates) if dates else '-'} - {max(dates) if dates else '-'}",
        "",
        "## Indici per anno",
        "",
    ]
    overview.extend(year_links)
    overview += ["", "## Indici per tema", ""]
    overview.extend(theme_links)
    (OUT / "00-Overview.md").write_text("\n".join(overview) + "\n", encoding="utf-8")

    theme_map = [
        "# SportVela - Mappa tematica",
        "",
        "Mappa mentale leggera: rimanda agli indici tematici invece di caricare centinaia di link in un'unica pagina.",
        "",
        "## Temi",
        "",
    ]
    theme_map.extend(theme_links)
    theme_map += [
        "",
        "## Anni",
        "",
    ]
    theme_map.extend(year_links)
    theme_map += [
        "",
        "## Connessioni operative",
        "",
        "- [[World Sailing - Mappa Atleti e Classifiche]]",
        "- [[World Sailing Youth Para Results/02-Indice-Classifiche-Finali|Youth & Para Results]]",
        "- [[America's Cup Napoli/00-Overview|America's Cup Napoli]]",
        "- [[Istituzionale FIV/00-Overview|Istituzionale FIV]]",
        "- [[comunicati stampa sportivi/_Indice-Atleti-Circoli|Atleti e circoli]]",
    ]
    (OUT / "02-Mappa-Tematica.md").write_text("\n".join(theme_map) + "\n", encoding="utf-8")


def update_vault_map():
    path = VAULT / "00-Mappa-Vault.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Mappa vault FIV\n"
    block = (
        "\n## Fonti esterne e contesto editoriale\n\n"
        "- [[Fonti Esterne/SportVela News/00-Overview|SportVela News - contesto editoriale]]\n"
        "- [[Fonti Esterne/SportVela News/01-Registro-Fonti|Registro fonti SportVela]]\n"
        "- [[Fonti Esterne/SportVela News/02-Mappa-Tematica|Mappa tematica SportVela]]\n"
        "\n"
        "Uso: fonte esterna utile per contesto e spunti. Per risultati/storico ufficiale, incrociare con comunicati FIV o World Sailing.\n"
    )
    marker = "## Fonti esterne e contesto editoriale"
    if marker in text:
        text = re.sub(r"\n## Fonti esterne e contesto editoriale\n.*?(?=\n## |\Z)", block.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def update_rules():
    path = VAULT / "99-Regole-Memoria.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Regole memoria FIV\n"
    block = (
        "\n## Regola per fonti esterne editoriali\n\n"
        "- SportVela e altre testate sono fonti di contesto, non sostituiscono comunicati ufficiali FIV o dati World Sailing.\n"
        "- Conservare titolo, data, link, categorie, sintesi operativa e possibili agganci al vault.\n"
        "- Non copiare integralmente gli articoli: tenere fatti essenziali, parole chiave, filoni e uso futuro.\n"
        "- Se una fonte esterna contiene risultati, marcarli come `da verificare` finche' non sono confermati da comunicato ufficiale o classifica finale.\n"
        "- Le news esterne entrano nella memoria solo se alimentano: atleta, classe, evento, circolo/zona, progetto istituzionale o modello editoriale.\n"
        "- Per archivi estesi usare indici annuali e tematici: evitare hub unici con centinaia di link caricati tutti insieme.\n"
    )
    marker = "## Regola per fonti esterne editoriali"
    if marker in text:
        text = re.sub(r"\n## Regola per fonti esterne editoriali\n.*?(?=\n## |\Z)", block.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "FIV-Obsidian-Archive/1.0"})
    # NOTA (2026-08-25): reset_generated_dirs() veniva chiamato QUI, prima di qualsiasi
    # fetch di rete. Un crash di rete (es. ConnectTimeout verso sportvela.net, successo
    # reale la notte del 25/08) lasciava le cartelle svuotate e MAI ripopolate: lo script
    # usciva con errore ma il workflow committava comunque lo stato "vuoto", cancellando
    # 1371 articoli dal repository. La routine di sync si e' accorta dell'anomalia e non
    # ha toccato Drive, ma il repository e' rimasto rotto finche' non e' stato corretto.
    # Fix: tutte le chiamate di rete (categorie, post) avvengono PRIMA di toccare il
    # filesystem di output; reset_generated_dirs() gira solo se il fetch e' riuscito per
    # intero, quindi un crash di rete ora lascia intatto l'ultimo output valido su disco
    # (git non vedra' alcun diff per questo script, invece di un diff di cancellazione).
    categories = all_categories(session)
    category_ids, category_names = news_category_ids(categories)
    posts = fetch_posts(session, category_ids)
    reset_generated_dirs()
    records = []
    for idx, post in enumerate(posts, 1):
        title, excerpt, content = post_text(post)
        cat_names = unique(category_names.get(cat_id, str(cat_id)) for cat_id in post.get("categories", []))
        if useful(title, excerpt, content, cat_names):
            records.append(article_note(post, cat_names))
        if idx % 100 == 0:
            print(f"Processed posts: {idx}/{len(posts)}; archived {len(records)}")
    write_indices(records, category_ids)
    update_vault_map()
    update_rules()
    print(f"Posts fetched from API: {len(posts)}")
    print(f"Useful articles archived: {len(records)}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
