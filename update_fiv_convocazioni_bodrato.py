import os
from pathlib import Path

VAULT = Path(os.environ.get(
    "FIV_VAULT_ROOT",
    "/Users/carlodellacasa/Library/CloudStorage/GoogleDrive-c.dellacasa@federvela.it/Il mio Drive/vault obsidian/FIV",
))
ATHLETES = VAULT / "Atleti Squadre Nazionali"
DATA = VAULT / "Dati Strutturati FIV"

SOURCE_LABEL = "email Roberta Bodrato del 2026-07-28 con allegato PDF ufficiale FIV"

convocations = [
    {
        "athlete": "Borio Attilio",
        "file": "Borio Attilio.md",
        "class_hint": "ILCA 7",
        "societa": "Fiamme Oro",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "17-30 agosto 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Enrico Strazzera",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.260; viaggio max EUR 800; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Giacomoni Pietro",
        "file": "Giacomoni Pietro.md",
        "class_hint": "ILCA 7",
        "societa": "SV GdF",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "17-30 agosto 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Enrico Strazzera",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.260; viaggio max EUR 560; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Peroni Dimitri",
        "file": "Peroni Dimitri.md",
        "class_hint": "ILCA 7",
        "societa": "SV GdF",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "17-30 agosto 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Enrico Strazzera",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.260; viaggio max EUR 800; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Chiavarini Lorenzo Brando",
        "file": "Chiavarini Lorenzo Brando.md",
        "class_hint": "ILCA 7",
        "societa": "Fiamme Oro",
        "protocol": "904/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "17-30 agosto 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "-",
        "role": "Atleta",
        "status": "Ufficiale FIV - rettifica",
        "notes": "La mail dichiara che annulla e sostituisce il precedente invio. Rimborso vitto/alloggio max EUR 1.260; viaggio max EUR 800; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Arseni Maria Vittoria",
        "file": "Arseni Maria Vittoria.md",
        "class_hint": "ILCA 6",
        "societa": "SV GdF",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "04-13 settembre 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Francesco Marrai",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 900; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Caracciolo di Brienza Ginevra",
        "file": "Caracciolo di Brienza Ginevra.md",
        "class_hint": "ILCA 6",
        "societa": "Fiamme Oro",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "04-13 settembre 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Francesco Marrai",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Nel PDF indicata come CARACCIOLO Ginevra. Rimborso vitto/alloggio max EUR 900; viaggio max EUR 560; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Benini Floriani Chiara",
        "file": "Benini Floriani Chiara.md",
        "class_hint": "ILCA 6",
        "societa": "SV GdF",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "01-13 settembre 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Francesco Marrai",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.170; viaggio max EUR 800; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Mattivi Emma",
        "file": "Mattivi Emma.md",
        "class_hint": "ILCA 6",
        "societa": "SV GdF",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "01-13 settembre 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Francesco Marrai",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.170; viaggio max EUR 560; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Talluri Matilda",
        "file": "Talluri Matilda.md",
        "class_hint": "ILCA 6",
        "societa": "CN Livorno",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Campionato Mondo Irlanda",
        "period": "01-13 settembre 2026",
        "place": "Dun Laoghaire, Irlanda",
        "tech": "Francesco Marrai",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 1.170; viaggio max EUR 800; tassa iscrizione early se nel primo 50% classifica.",
    },
    {
        "athlete": "Colasanto Carola",
        "file": "Colasanto Carola.md",
        "class_hint": "iQFOiL F",
        "societa": "Luiss SSD",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Allenamento Weymouth",
        "period": "16-21 agosto 2026",
        "place": "Weymouth, GBR - WPNSA",
        "tech": "Andrea Melis",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 540.",
    },
    {
        "athlete": "Falcioni Medea Marisa",
        "file": "Falcioni Medea Marisa.md",
        "class_hint": "iQFOiL F",
        "societa": "SEF Stamura",
        "protocol": "903/2026",
        "doc_date": "2026-07-28",
        "object": "Allenamento Weymouth",
        "period": "16-21 agosto 2026",
        "place": "Weymouth, GBR - WPNSA",
        "tech": "Andrea Melis",
        "role": "Atleta",
        "status": "Ufficiale FIV",
        "notes": "Rimborso vitto/alloggio max EUR 540; viaggio max EUR 800.",
    },
]

technicians = [
    {"name": "Enrico Strazzera", "object": "Campionato Mondo Irlanda", "period": "17-30 agosto 2026", "athletes": "Borio, Giacomoni, Peroni"},
    {"name": "Francesco Marrai", "object": "Campionato Mondo Irlanda", "period": "01/04-13 settembre 2026", "athletes": "Arseni, Caracciolo, Benini Floriani, Mattivi, Talluri"},
    {"name": "Andrea Melis", "object": "Allenamento Weymouth", "period": "16-21 agosto 2026", "athletes": "Colasanto, Falcioni"},
]

def wiki(name):
    return f"[[Atleti Squadre Nazionali/{name}|{name}]]"

def table_row(c):
    return (
        f"| {c['doc_date']} | {c['protocol']} | {c['object']} | {c['period']} | "
        f"{c['place']} | {wiki(c['athlete'])} | {c['class_hint']} | {c['societa']} | "
        f"{c['tech']} | {c['status']} | {c['notes']} |"
    )

def athlete_section(c):
    return f"""<!-- FIV_OFFICIAL_CONVOCATIONS_START -->
## Convocazioni ufficiali FIV

> Fonte: {SOURCE_LABEL}. Dato considerato **ufficiale FIV** perche' estratto dal PDF di convocazione firmato dal Segretario Generale.

| Data documento | Protocollo | Oggetto | Periodo | Luogo | Tecnico federale | Stato | Collegamento |
|---|---|---|---|---|---|---|---|
| {c['doc_date']} | {c['protocol']} | {c['object']} | {c['period']} | {c['place']} | {c['tech']} | {c['status']} | [[Dati Strutturati FIV/Convocazioni-Ufficiali-da-Email|registro convocazioni]] |

Nota operativa: {c['notes']}
<!-- FIV_OFFICIAL_CONVOCATIONS_END -->
"""

def replace_between(text, start, end, replacement):
    if start in text and end in text:
        before = text.split(start, 1)[0]
        after = text.split(end, 1)[1]
        return before.rstrip() + "\n\n" + replacement.rstrip() + "\n" + after
    return text.rstrip() + "\n\n" + replacement.rstrip() + "\n"

def ensure_falcioni(path):
    if path.exists():
        return
    path.write_text("""# Falcioni Medea Marisa

> Scheda creata il 2026-07-29 da convocazione ufficiale FIV inviata da Roberta Bodrato il 2026-07-28. Da completare con anagrafica/tesseramento, classe primaria confermata, risultati e fonti sportive.

## Anagrafica FIV

Stato dato: **parziale da convocazione ufficiale**.
Fonte: PDF di convocazione FIV prot. 903/2026, Genova 28 luglio 2026.

- Cognome: Falcioni
- Nome: Medea Marisa
- Societa' indicata nel PDF: SEF Stamura
- Stato scheda: Da completare con elenco anagrafico/tesseramento

## Dati anagrafici e sportivi

- **Classe/i probabili**: iQFOiL F
- **Circolo/gruppo sportivo indicato nel PDF**: SEF Stamura

## Collegamenti

- Storico risultati di classe: [[iQFOiL]] (in [[comunicati stampa sportivi/Storico Risultati per Classe]])
- Registro convocazioni: [[Dati Strutturati FIV/Convocazioni-Ufficiali-da-Email]]
""", encoding="utf-8")

def update_athlete_files():
    for c in convocations:
        path = ATHLETES / c["file"]
        if c["athlete"] == "Falcioni Medea Marisa":
            ensure_falcioni(path)
        if not path.exists():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        text = replace_between(text, "<!-- FIV_OFFICIAL_CONVOCATIONS_START -->", "<!-- FIV_OFFICIAL_CONVOCATIONS_END -->", athlete_section(c))
        path.write_text(text, encoding="utf-8")

def write_registry():
    rows = "\n".join(table_row(c) for c in convocations)
    tech_rows = "\n".join(f"| {t['name']} | {t['object']} | {t['period']} | {t['athletes']} |" for t in technicians)
    content = f"""# Convocazioni ufficiali da email

> Nucleo leggero per gestire le convocazioni ufficiali ricevute via email da Roberta Bodrato. Non archivia il testo integrale delle email: conserva solo dati stabili e verificabili dai PDF allegati.

## Stato fonte

- Fonte: {SOURCE_LABEL}
- Mittente: r.bodrato@federvela.it
- Data invio mail: 2026-07-28
- Attendibilita': **Ufficiale FIV**
- Uso: aggiornare schede atleta, storico convocazioni, pianificazione comunicazione e controlli operativi.
- Nota privacy/performance: non duplicare allegati PDF o corpi email nel vault se non indispensabile.

## Convocazioni atleti

| Data documento | Protocollo | Oggetto | Periodo | Luogo | Atleta | Classe | Societa' PDF | Tecnico federale | Stato | Note operative |
|---|---|---|---|---|---|---|---|---|---|---|
{rows}

## Tecnici federali collegati

| Tecnico | Oggetto | Periodo | Atleti collegati |
|---|---|---|---|
{tech_rows}

## Collegamenti rapidi

- [[Atleti Squadre Nazionali/00-Indice-Atleti|Indice atleti]]
- [[Dati Strutturati FIV/00-Overview|Overview dati strutturati]]
- [[00-Mappa-Vault|Mappa vault]]

## Regola di aggiornamento

- Inserire qui solo convocazioni con PDF ufficiale o fonte FIV equivalente.
- Se una mail contiene una rettifica, tenere come dato attivo il PDF rettificato e indicare in `Stato` che sostituisce il precedente invio.
- Aggiornare sempre anche la scheda atleta collegata, usando la sezione `Convocazioni ufficiali FIV`.
"""
    (DATA / "Convocazioni-Ufficiali-da-Email.md").write_text(content, encoding="utf-8")

def update_link_files():
    overview = DATA / "00-Overview.md"
    text = overview.read_text(encoding="utf-8")
    link = "- [[Dati Strutturati FIV/Convocazioni-Ufficiali-da-Email|Convocazioni ufficiali da email]]"
    if link not in text:
        text = text.replace("## Dataset\n\n", "## Dataset\n\n" + link + "\n")
        overview.write_text(text, encoding="utf-8")

    main_map = VAULT / "00-Mappa-Vault.md"
    text = main_map.read_text(encoding="utf-8")
    map_link = "- [[Dati Strutturati FIV/Convocazioni-Ufficiali-da-Email|Convocazioni ufficiali da email]]"
    if map_link not in text:
        text = text.replace("- [[Dati Strutturati FIV/Atleti-Anagrafica|Atleti-Anagrafica.csv]]\n", "- [[Dati Strutturati FIV/Atleti-Anagrafica|Atleti-Anagrafica.csv]]\n" + map_link + "\n")
        text = text.replace("- In ogni scheda atleta, preferire: `Dati`, `Convocazioni`, `Risultati finali`, `Note`.\n", "- In ogni scheda atleta, preferire: `Dati`, `Convocazioni`, `Risultati finali`, `Note`.\n- Le convocazioni da email entrano nel vault solo se hanno PDF ufficiale o fonte FIV equivalente.\n")
        main_map.write_text(text, encoding="utf-8")

    idx = ATHLETES / "00-Indice-Atleti.md"
    text = idx.read_text(encoding="utf-8")
    block = """## Schede create da convocazioni ufficiali

| Atleta | Fonte | Stato |
|---|---|---|
| [[Falcioni Medea Marisa]] | Convocazione ufficiale FIV prot. 903/2026 del 2026-07-28 | Scheda parziale da completare con anagrafica |

"""
    if "## Schede create da convocazioni ufficiali" not in text:
        text = text.replace("## Note sul documento fonte\n\n", block + "## Note sul documento fonte\n\n")
        idx.write_text(text, encoding="utf-8")

def main():
    update_athlete_files()
    write_registry()
    update_link_files()

if __name__ == "__main__":
    main()
