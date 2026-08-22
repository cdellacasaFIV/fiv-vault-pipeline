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

API_BASE = "https://federvela.it/wp-json/wp/v2"
AFTER = "2020-01-01T00:00:00"
TODAY = date.today().isoformat()

OUT = VAULT / "Fonti Ufficiali" / "Federvela News"
ARTICLE_DIR = OUT / "Articoli"
YEAR_INDEX_DIR = OUT / "Indici" / "Per Anno"
THEME_INDEX_DIR = OUT / "Indici" / "Per Tema"


KEYWORDS = {
    "risultati": ["oro", "argento", "bronzo", "podio", "classifica", "posto", "campione", "campionessa", "titolo", "medaglia"],
    "olimpica": ["ilca", "49er", "49erfx", "nacra 17", "iqfoil", "formula kite", "olimpic", "parigi", "tokyo", "los angeles"],
    "giovanile": ["youth", "junior", "under", "u15", "u17", "u19", "giovan", "scuola vela", "scuole di vela", "kinder"],
    "parasailing/inclusione": ["parasailing", "para sailing", "disabil", "inclus", "barriere", "hansa", "venture connect", "vela per tutti"],
    "istituzionale": ["protocollo", "accordo", "coni", "consiglio", "assemblea", "presidente", "sostegno", "sviluppo", "intesa"],
    "zone/circoli": ["zona", "circolo", "yacht club", "club nautico", "lega navale", "meeting provinciale", "territorio"],
    "america's cup/napoli": ["america's cup", "americas cup", "napoli", "caivano", "partenope"],
    "formazione/scuola": ["formazione", "scuola", "istruttori", "didattica", "educamp", "studenti"],
    "media/comunicazione": ["tv", "video", "streaming", "comunicazione", "presentato", "conferenza", "racconta"],
}

CLASS_PATTERNS = [
    "49erFX", "49er", "Nacra 17", "Nacra 15", "ILCA 7", "ILCA 6", "ILCA 4",
    "IQFOiL", "iQFOiL", "Formula Kite", "Kite", "Techno 293", "420", "470",
    "Waszp", "RS21", "Dinghy 12", "Vaurien", "J70", "Slalom X", "Foiling Week",
    "Hansa", "2.4", "Para Sailing", "Parasailing", "WingFoil", "Wing Foil",
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
    return value[:110] or "federvela-news"


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
    response = session.get(f"{API_BASE}{path}", params=params or {}, timeout=45)
    response.raise_for_status()
    return response


def all_categories(session):
    response = request_json(session, "/categories", {"per_page": 100})
    return response.json()


def archive_category_ids(categories):
    ids = []
    names = {}
    for cat in categories:
        names[cat["id"]] = cat["name"]
        if cat["slug"] != "senza-categoria":
            ids.append(cat["id"])
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


def is_test_post(post):
    title = clean_text(post.get("title", {}).get("rendered", ""))
    slug = post.get("slug", "")
    link = post.get("link", "")
    hay = " ".join([title, slug, link]).lower()
    return "ciao-mondo" in hay or "test news nazionale" in hay


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
    return out or ["memoria ufficiale"]


def proper_phrases(text):
    candidates = re.findall(
        r"\b(?:[A-ZÀ-Ú][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)(?:\s+(?:di|del|della|dei|degli|"
        r"da|de|e|[A-ZÀ-Ú][A-Za-zÀ-ÖØ-öø-ÿ'’.-]+)){0,3}",
        text,
    )
    blacklist = {
        "News", "Vela", "FIV", "Federazione", "Italian", "Italiana", "Leggi", "Seguici",
        "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio",
        "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre", "Nazionale",
    }
    cleaned = []
    for item in candidates:
        item = clean_text(item)
        item = item.split(".")[0].strip()
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
        r"\b\d{1,4}(?:[.,]\d+)?\b(?:\s?(?:anni|atleti|equipaggi|bambini|giorni|medaglie|posto|titoli|euro))?",
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
        angle.append("risultato/storico sportivo ufficiale da collegare a classifiche finali quando disponibili")
    if "giovanile" in theme_list:
        angle.append("sviluppo giovanile e vivaio FIV")
    if "parasailing/inclusione" in theme_list:
        angle.append("inclusione, parasailing e valore istituzionale")
    if "istituzionale" in theme_list:
        angle.append("atto, accordo, governance o policy federale")
    if "zone/circoli" in theme_list:
        angle.append("territori, zone e circoli")
    if "olimpica" in theme_list:
        angle.append("classi olimpiche o alto livello")
    if "america's cup/napoli" in theme_list:
        angle.append("legacy America's Cup Napoli e promozione territoriale")
    return [
        f"- Temi operativi: {', '.join(theme_list)}.",
        f"- Angoli memoria: {', '.join(angle) if angle else 'memoria ufficiale FIV generale'}.",
        f"- Classi/discipline citate: {', '.join(classes) if classes else 'non isolate automaticamente'}.",
        f"- Nomi, circoli o luoghi da valutare: {', '.join(names) if names else 'non isolati automaticamente'}.",
        f"- Numeri/date utili: {', '.join(nums) if nums else 'nessun numero isolato automaticamente'}.",
        "- Testo fonte ufficiale disponibile online: usare il link per verifica puntuale, senza duplicare integralmente l'articolo nel vault.",
    ]


def obsidian_links(theme_list):
    links = ["[[Istituzionale FIV/00-Overview|Istituzionale FIV]]"]
    if "risultati" in theme_list or "olimpica" in theme_list:
        links.append("[[World Sailing - Mappa Atleti e Classifiche]]")
    if "giovanile" in theme_list:
        links.append("[[World Sailing Youth Para Results/02-Indice-Classifiche-Finali|Youth & Para Results]]")
    if "america's cup/napoli" in theme_list:
        links.append("[[America's Cup Napoli/00-Overview|America's Cup Napoli]]")
    if "zone/circoli" in theme_list:
        links.append("[[comunicati stampa sportivi/_Indice-Atleti-Circoli|Atleti e circoli]]")
    links.append("[[Modelli/Modello-News-Istituzionale|Modello news istituzionale]]")
    links.append("[[Modelli/Modello-News-Evento|Modello news evento]]")
    return list(dict.fromkeys(links))


def reset_generated_dirs():
    for directory in [ARTICLE_DIR, YEAR_INDEX_DIR, THEME_INDEX_DIR]:
        if directory.exists():
            for path in sorted(directory.rglob("*.md")):
                path.unlink()
        directory.mkdir(parents=True, exist_ok=True)


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
        "Stato fonte: **ufficiale FIV / Federvela**.",
        "Uso nel vault: memoria ufficiale, contesto istituzionale, risultati e traccia editoriale. Per classifiche sportive usare comunque il dato finale quando disponibile.",
        "",
        "## Fonte",
        "",
        f"- Data Federvela: {label}",
        f"- Link: {post.get('link', '')}",
        f"- Categorie: {', '.join(cat_names) or '-'}",
        f"- Archiviato: {TODAY}",
        "",
        "## Perche' tenerla",
        "",
        f"- Filoni: {', '.join(theme_list)}",
        "- Valore: fonte federale primaria per ricostruire decisioni, eventi, risultati, territori, progetti e comunicazione FIV.",
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
        "- Se riguarda risultati: usarla come fonte ufficiale FIV e collegare eventuale classifica finale World Sailing quando presente.",
        "- Se riguarda governance, accordi o progetti: collegarla alla memoria istituzionale.",
        "- Se riguarda zone/circoli: collegarla a territorio, circoli e comunicati sportivi.",
    ]
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "post": post,
        "title": title,
        "date_label": label,
        "year": year,
        "iso_date": iso_date,
        "categories": cat_names,
        "themes": theme_list,
        "note_path": note_path,
    }


def write_indices(records, category_ids):
    records = sorted(records, key=lambda r: r["iso_date"], reverse=True)
    registry = [
        "# Registro fonti Federvela",
        "",
        "Stato fonte: **ufficiale FIV / Federvela**.",
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
        path = YEAR_INDEX_DIR / f"{year}.md"
        year_links.append(f"- [[{rel_no_ext(path)}|{year}]] ({len(rows)} news)")
        lines = [
            f"# Federvela News {year}",
            "",
            "Indice annuale delle news ufficiali Federvela archiviate nel vault.",
            "",
            "| Data | Titolo | Temi | Nota |",
            "| --- | --- | --- | --- |",
        ]
        for rec in rows:
            lines.append(
                f"| {rec['date_label']} | {md_escape(rec['title'])} | {md_escape(', '.join(rec['themes']))} | "
                f"[[{rel_no_ext(rec['note_path'])}|nota]] |"
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    theme_links = []
    for theme, rows in sorted(by_theme.items()):
        path = THEME_INDEX_DIR / f"{slugify(theme)}.md"
        theme_links.append(f"- [[{rel_no_ext(path)}|{theme}]] ({len(rows)} news)")
        lines = [
            f"# Federvela - {theme}",
            "",
            "Indice tematico delle news ufficiali Federvela collegate alla memoria FIV.",
            "",
            "| Data | Titolo | Categorie | Nota |",
            "| --- | --- | --- | --- |",
        ]
        for rec in rows:
            lines.append(
                f"| {rec['date_label']} | {md_escape(rec['title'])} | {md_escape(', '.join(rec['categories']))} | "
                f"[[{rel_no_ext(rec['note_path'])}|nota]] |"
            )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    dates = [r["iso_date"] for r in records]
    overview = [
        "# Federvela News - fonte ufficiale FIV",
        "",
        "Archivio operativo delle news ufficiali pubblicate su federvela.it.",
        "",
        "## Regola d'uso",
        "",
        "- Fonte primaria ufficiale FIV.",
        "- Usare per memoria istituzionale, comunicati, risultati, progetti, zone e circoli.",
        "- Per risultati sportivi, collegare quando possibile la classifica finale verificata World Sailing o documenti ufficiali di evento.",
        "",
        "## Link rapidi",
        "",
        "- [[Fonti Ufficiali/Federvela News/01-Registro-Fonti|Registro fonti]]",
        "- [[Fonti Ufficiali/Federvela News/02-Mappa-Tematica|Mappa tematica]]",
        "- [[Istituzionale FIV/00-Overview]]",
        "- [[World Sailing - Mappa Atleti e Classifiche]]",
        "- [[comunicati stampa sportivi/_Indice-Atleti-Circoli]]",
        "",
        "## Copertura",
        "",
        "- Cutoff richiesto: dal 2020 in avanti.",
        f"- Categoria API: categorie ufficiali Federvela escluse `Senza categoria` ({len(category_ids)} categorie).",
        f"- Articoli archiviati: {len(records)}",
        f"- Intervallo effettivo trovato: {min(dates) if dates else '-'} - {max(dates) if dates else '-'}",
        f"- Data estrazione: {TODAY}",
        "",
        "## Indici per anno",
        "",
    ]
    overview.extend(year_links)
    overview += ["", "## Indici per tema", ""]
    overview.extend(theme_links)
    (OUT / "00-Overview.md").write_text("\n".join(overview) + "\n", encoding="utf-8")

    theme_map = [
        "# Federvela - Mappa tematica news ufficiali",
        "",
        "Mappa leggera degli indici ufficiali Federvela: per consultare velocemente senza aprire centinaia di note insieme.",
        "",
        "## Temi",
        "",
    ]
    theme_map.extend(theme_links)
    theme_map += ["", "## Anni", ""]
    theme_map.extend(year_links)
    theme_map += [
        "",
        "## Connessioni operative",
        "",
        "- [[Istituzionale FIV/00-Overview|Istituzionale FIV]]",
        "- [[World Sailing - Mappa Atleti e Classifiche]]",
        "- [[World Sailing Youth Para Results/02-Indice-Classifiche-Finali|Youth & Para Results]]",
        "- [[America's Cup Napoli/00-Overview|America's Cup Napoli]]",
        "- [[comunicati stampa sportivi/_Indice-Atleti-Circoli|Atleti e circoli]]",
    ]
    (OUT / "02-Mappa-Tematica.md").write_text("\n".join(theme_map) + "\n", encoding="utf-8")


def update_vault_map():
    path = VAULT / "00-Mappa-Vault.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Mappa vault FIV\n"
    block = (
        "\n## Fonti ufficiali Federvela\n\n"
        "- [[Fonti Ufficiali/Federvela News/00-Overview|Federvela News - fonte ufficiale FIV]]\n"
        "- [[Fonti Ufficiali/Federvela News/01-Registro-Fonti|Registro fonti Federvela]]\n"
        "- [[Fonti Ufficiali/Federvela News/02-Mappa-Tematica|Mappa tematica Federvela]]\n"
        "\n"
        "Uso: fonte primaria ufficiale per memoria FIV, comunicati, istituzionale, territori e risultati da collegare a classifiche finali.\n"
    )
    marker = "## Fonti ufficiali Federvela"
    if marker in text:
        text = re.sub(r"\n## Fonti ufficiali Federvela\n.*?(?=\n## |\Z)", block.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def update_rules():
    path = VAULT / "99-Regole-Memoria.md"
    text = path.read_text(encoding="utf-8") if path.exists() else "# Regole memoria FIV\n"
    block = (
        "\n## Regola per fonti ufficiali Federvela\n\n"
        "- Federvela.it e comunicati FIV sono fonti primarie ufficiali per memoria federale.\n"
        "- Conservare titolo, data, link, categorie, sintesi operativa, filoni e collegamenti Obsidian.\n"
        "- Non duplicare integralmente l'articolo: il vault conserva memoria consultabile, non copia del sito.\n"
        "- Se la news contiene risultati, collegare o verificare con classifica finale ufficiale quando disponibile.\n"
        "- Le news ufficiali hanno priorita' rispetto a fonti esterne editoriali quando c'e' conflitto di dato.\n"
        "- Per archivi estesi usare indici annuali e tematici, evitando hub unici troppo pesanti.\n"
    )
    marker = "## Regola per fonti ufficiali Federvela"
    if marker in text:
        text = re.sub(r"\n## Regola per fonti ufficiali Federvela\n.*?(?=\n## |\Z)", block.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def update_institutional_overview():
    path = VAULT / "Istituzionale FIV" / "00-Overview.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    block = (
        "\n## Fonti ufficiali collegate\n\n"
        "- [[Fonti Ufficiali/Federvela News/00-Overview|Federvela News - fonte ufficiale FIV]]\n"
        "- [[Fonti Ufficiali/Federvela News/Indici/Per Tema/istituzionale|News istituzionali Federvela]]\n"
        "- [[Fonti Ufficiali/Federvela News/Indici/Per Tema/parasailing-inclusione|Parasailing e inclusione Federvela]]\n"
        "- [[Fonti Ufficiali/Federvela News/Indici/Per Tema/formazione-scuola|Formazione e scuola Federvela]]\n"
    )
    marker = "## Fonti ufficiali collegate"
    if marker in text:
        text = re.sub(r"\n## Fonti ufficiali collegate\n.*?(?=\n## |\Z)", block.rstrip() + "\n", text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text, encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    reset_generated_dirs()
    session = requests.Session()
    session.headers.update({"User-Agent": "FIV-Obsidian-Archive/1.0"})
    categories = all_categories(session)
    category_ids, category_names = archive_category_ids(categories)
    posts = fetch_posts(session, category_ids)
    records = []
    for idx, post in enumerate(posts, 1):
        if is_test_post(post):
            continue
        cat_names = unique(category_names.get(cat_id, str(cat_id)) for cat_id in post.get("categories", []))
        records.append(article_note(post, cat_names))
        if idx % 100 == 0:
            print(f"Processed posts: {idx}/{len(posts)}")
    write_indices(records, category_ids)
    update_vault_map()
    update_rules()
    update_institutional_overview()
    print(f"Posts fetched from API: {len(posts)}")
    print(f"Official articles archived: {len(records)}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
