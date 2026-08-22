#!/usr/bin/env python3
import os
import re
from pathlib import Path


VAULT = Path(os.environ.get(
    "FIV_VAULT_ROOT",
    "/Users/carlodellacasa/Library/CloudStorage/GoogleDrive-c.dellacasa@federvela.it/"
    "Il mio Drive/vault obsidian/FIV",
))

CONNECT = VAULT / "Mappe e Collegamenti"

START = "<!-- CONNECTIVE_LAYER_START -->"
END = "<!-- CONNECTIVE_LAYER_END -->"


def rel_no_ext(path):
    return path.relative_to(VAULT).with_suffix("").as_posix()


def count_md(path):
    return len(list(path.rglob("*.md"))) if path.exists() else 0


def insert_block(path, title, body):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    block = f"{START}\n## {title}\n\n{body.rstrip()}\n{END}"
    if START in text and END in text:
        text = re.sub(re.escape(START) + r".*?" + re.escape(END), block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")


def write(path, lines):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def wiki(path, label=None):
    return f"[[{rel_no_ext(path)}|{label or path.stem}]]"


def main():
    CONNECT.mkdir(parents=True, exist_ok=True)

    fed = VAULT / "Fonti Ufficiali" / "Federvela News"
    sportvela = VAULT / "Fonti Esterne" / "SportVela News"
    ws_map = VAULT / "World Sailing - Mappa Atleti e Classifiche.md"
    athletes = VAULT / "Atleti Squadre Nazionali" / "00-Indice-Atleti.md"
    comunicati = VAULT / "comunicati stampa sportivi"
    istituzionale = VAULT / "Istituzionale FIV"
    america = VAULT / "America's Cup Napoli"
    we_sail = VAULT / "WE SAIL TV"

    pages = {
        "hub": CONNECT / "00-Hub-Mappe-e-Collegamenti.md",
        "query": CONNECT / "01-Indice-Consultazione-Rapida.md",
        "source": CONNECT / "02-Gerarchia-Fonti-e-Attendibilita.md",
        "athlete": CONNECT / "03-Ponte-Atleti-Risultati-Fonti.md",
        "themes": CONNECT / "04-Ponte-Temi-Progetti-Fonti.md",
        "events": CONNECT / "05-Ponte-Eventi-Comunicati-Classifiche.md",
        "rules": CONNECT / "06-Regole-Linking-Obsidian.md",
    }

    write(
        pages["hub"],
        [
            "# Hub mappe e collegamenti",
            "",
            "Punto di ingresso allo strato relazionale del vault FIV.",
            "",
            "Obiettivo: collegare macro-cartelle diverse senza duplicare contenuti e senza appesantire Obsidian.",
            "",
            "## Mappe operative",
            "",
            f"- {wiki(pages['query'], 'Indice consultazione rapida')}",
            f"- {wiki(pages['source'], 'Gerarchia fonti e attendibilita')}",
            f"- {wiki(pages['athlete'], 'Ponte atleti, risultati e fonti')}",
            f"- {wiki(pages['themes'], 'Ponte temi, progetti e fonti')}",
            f"- {wiki(pages['events'], 'Ponte eventi, comunicati e classifiche')}",
            f"- {wiki(pages['rules'], 'Regole linking Obsidian')}",
            "",
            "## Entrate principali",
            "",
            f"- {wiki(VAULT / '00-Mappa-Vault.md', 'Mappa vault')}",
            f"- {wiki(athletes, 'Indice atleti')}",
            f"- {wiki(ws_map, 'Mappa World Sailing')}",
            f"- {wiki(fed / '00-Overview.md', 'Federvela News ufficiali')}",
            f"- {wiki(sportvela / '00-Overview.md', 'SportVela contesto editoriale')}",
            f"- {wiki(istituzionale / '00-Overview.md', 'Istituzionale FIV')}",
            f"- {wiki(america / '00-Overview.md', 'Americas Cup Napoli')}",
            f"- {wiki(we_sail / '00-Overview.md', 'WE SAIL TV')}",
            "",
            "## Numeri rapidi",
            "",
            f"- Schede atleta: {count_md(VAULT / 'Atleti Squadre Nazionali') - 1}",
            f"- News ufficiali Federvela: {count_md(fed / 'Articoli')}",
            f"- News esterne SportVela: {count_md(sportvela / 'Articoli')}",
            f"- Note classifica World Sailing: {count_md(VAULT / 'World Sailing Results' / 'Classifiche') + count_md(VAULT / 'World Sailing European Results' / 'Classifiche') + count_md(VAULT / 'World Sailing Major Regattas' / 'Classifiche') + count_md(VAULT / 'World Sailing Youth Para Results' / 'Classifiche')}",
        ],
    )

    write(
        pages["query"],
        [
            "# Indice consultazione rapida",
            "",
            "Usa questa pagina quando sai cosa cerchi ma non sai da quale cartella partire.",
            "",
            "## Se cerchi un atleta",
            "",
            f"- Vai a {wiki(athletes, 'Indice atleti')}.",
            f"- Poi controlla {wiki(ws_map, 'Mappa World Sailing')} per risultati verificati.",
            f"- Per contesto news ufficiale cerca nel {wiki(fed / '01-Registro-Fonti.md', 'Registro Federvela')}.",
            "",
            "## Se cerchi un risultato sportivo",
            "",
            f"- Prima fonte dati: {wiki(ws_map, 'World Sailing - Overall Results')}.",
            f"- Se e' una news FIV: {wiki(fed / 'Indici' / 'Per Tema' / 'risultati.md', 'Federvela risultati')}.",
            f"- Se e' contesto editoriale: {wiki(sportvela / 'Indici' / 'Per Tema' / 'risultati.md', 'SportVela risultati')}.",
            "",
            "## Se cerchi istituzionale, accordi, progetti",
            "",
            f"- Hub: {wiki(istituzionale / '00-Overview.md', 'Istituzionale FIV')}.",
            f"- Fonte primaria: {wiki(fed / 'Indici' / 'Per Tema' / 'istituzionale.md', 'News istituzionali Federvela')}.",
            f"- Contesto esterno: {wiki(sportvela / 'Indici' / 'Per Tema' / 'media-storytelling.md', 'SportVela media/storytelling')}.",
            "",
            "## Se cerchi giovanile",
            "",
            f"- Risultati: {wiki(VAULT / 'World Sailing Youth Para Results' / '02-Indice-Classifiche-Finali.md', 'Youth & Para Results')}.",
            f"- News ufficiali: {wiki(fed / 'Indici' / 'Per Tema' / 'giovanile.md', 'Federvela giovanile')}.",
            f"- Contesto editoriale: {wiki(sportvela / 'Indici' / 'Per Tema' / 'giovanile.md', 'SportVela giovanile')}.",
            f"- Memoria istituzionale: {wiki(istituzionale / '03-Scuola-Giovani-e-Formazione.md', 'Scuola, giovani e formazione')}.",
            "",
            "## Se cerchi parasailing o inclusione",
            "",
            f"- News ufficiali: {wiki(fed / 'Indici' / 'Per Tema' / 'parasailing-inclusione.md', 'Federvela parasailing/inclusione')}.",
            f"- Risultati: {wiki(VAULT / 'World Sailing Youth Para Results' / '02-Indice-Classifiche-Finali.md', 'Youth & Para Results')}.",
            f"- Memoria istituzionale: {wiki(istituzionale / '02-Inclusione-e-Legacy.md', 'Inclusione e legacy')}.",
            "",
            "## Se cerchi America's Cup / Napoli",
            "",
            f"- Hub progetto: {wiki(america / '00-Overview.md', 'Americas Cup Napoli')}.",
            f"- News ufficiali: {wiki(fed / 'Indici' / 'Per Tema' / 'america-s-cup-napoli.md', 'Federvela Americas Cup/Napoli')}.",
            f"- Contesto esterno: {wiki(sportvela / 'Indici' / 'Per Tema' / 'america-s-cup-napoli.md', 'SportVela Americas Cup/Napoli')}.",
            "",
            "## Se devi scrivere una news",
            "",
            f"- Evento: {wiki(VAULT / 'Modelli' / 'Modello-News-Evento.md', 'Modello news evento')}.",
            f"- Istituzionale: {wiki(VAULT / 'Modelli' / 'Modello-News-Istituzionale.md', 'Modello news istituzionale')}.",
            f"- Tono e metodo: {wiki(VAULT / 'profilo professionale' / 'GUIDA-SCRITTURA-FIV.md', 'Guida scrittura FIV')}.",
        ],
    )

    write(
        pages["source"],
        [
            "# Gerarchia fonti e attendibilita",
            "",
            "Serve a decidere quale dato usare quando piu' fonti parlano dello stesso fatto.",
            "",
            "## Priorita fonte",
            "",
            "1. Comunicati ufficiali FIV / Federvela.",
            "2. Classifiche finali ufficiali World Sailing `Overall Results`.",
            "3. Documenti ufficiali allegati o federali.",
            "4. Fonti esterne editoriali come SportVela.",
            "5. Appunti interni o note di lavoro da verificare.",
            "",
            "## Collegamenti",
            "",
            f"- {wiki(fed / '00-Overview.md', 'Federvela News ufficiali')}",
            f"- {wiki(ws_map, 'World Sailing verificato')}",
            f"- {wiki(comunicati / '02-Nucleo-Comunicati-Ufficiali.md', 'Nucleo comunicati ufficiali')}",
            f"- {wiki(sportvela / '00-Overview.md', 'SportVela fonte esterna')}",
            "",
            "## Regola pratica",
            "",
            "- Se una fonte esterna racconta un risultato, usarla come spunto.",
            "- Se Federvela conferma lo stesso fatto, Federvela diventa fonte primaria.",
            "- Se World Sailing fornisce Overall Results, il piazzamento sportivo va verificato li'.",
        ],
    )

    write(
        pages["athlete"],
        [
            "# Ponte atleti, risultati e fonti",
            "",
            "Questa pagina collega le schede atleta con risultati verificati e fonti news.",
            "",
            "## Percorso consigliato",
            "",
            f"- Scheda atleta: {wiki(athletes, 'Indice atleti')}.",
            f"- Risultati verificati: {wiki(ws_map, 'Mappa World Sailing')}.",
            f"- News ufficiali risultato: {wiki(fed / 'Indici' / 'Per Tema' / 'risultati.md', 'Federvela risultati')}.",
            f"- News ufficiali olimpica: {wiki(fed / 'Indici' / 'Per Tema' / 'olimpica.md', 'Federvela olimpica')}.",
            f"- Contesto esterno risultato: {wiki(sportvela / 'Indici' / 'Per Tema' / 'risultati.md', 'SportVela risultati')}.",
            "",
            "## Regola di collegamento",
            "",
            "- La scheda atleta deve contenere solo risultati finali e link alla classifica.",
            "- Le news restano nelle fonti, ma vanno collegate tramite indice tematico o ricerca per nome atleta.",
            "- Quando una news ufficiale cita un atleta gia' schedato, usare il link alla scheda atleta nella nota evento o nel comunicato consolidato.",
        ],
    )

    write(
        pages["themes"],
        [
            "# Ponte temi, progetti e fonti",
            "",
            "Mappa per navigare per filoni, non per cartelle.",
            "",
            "## Alto livello e risultati",
            "",
            f"- {wiki(ws_map, 'World Sailing - risultati verificati')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'risultati.md', 'Federvela risultati')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'olimpica.md', 'Federvela olimpica')}",
            "",
            "## Giovani e scuola",
            "",
            f"- {wiki(istituzionale / '03-Scuola-Giovani-e-Formazione.md', 'Scuola, giovani e formazione')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'giovanile.md', 'Federvela giovanile')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'formazione-scuola.md', 'Federvela formazione/scuola')}",
            f"- {wiki(sportvela / 'Indici' / 'Per Tema' / 'giovanile.md', 'SportVela giovanile')}",
            "",
            "## Inclusione e parasailing",
            "",
            f"- {wiki(istituzionale / '02-Inclusione-e-Legacy.md', 'Inclusione e legacy')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'parasailing-inclusione.md', 'Federvela parasailing/inclusione')}",
            f"- {wiki(VAULT / 'World Sailing Youth Para Results' / '02-Indice-Classifiche-Finali.md', 'Classifiche Youth & Para')}",
            "",
            "## Territori, zone e circoli",
            "",
            f"- {wiki(comunicati / '_Indice-Atleti-Circoli.md', 'Indice atleti/circoli')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'zone-circoli.md', 'Federvela zone/circoli')}",
            f"- {wiki(sportvela / 'Indici' / 'Per Tema' / 'zone-circoli.md', 'SportVela zone/circoli')}",
            "",
            "## Progetti strategici e media",
            "",
            f"- {wiki(america / '00-Overview.md', 'Americas Cup Napoli')}",
            f"- {wiki(we_sail / '00-Overview.md', 'WE SAIL TV')}",
            f"- {wiki(fed / 'Indici' / 'Per Tema' / 'media-comunicazione.md', 'Federvela media/comunicazione')}",
            f"- {wiki(sportvela / 'Indici' / 'Per Tema' / 'media-storytelling.md', 'SportVela media/storytelling')}",
        ],
    )

    write(
        pages["events"],
        [
            "# Ponte eventi, comunicati e classifiche",
            "",
            "Serve per trasformare una news evento in memoria stabile.",
            "",
            "## Flusso corretto",
            "",
            "1. Identifica evento, classe, data e luogo.",
            "2. Cerca comunicato ufficiale o news Federvela.",
            "3. Se ci sono risultati, cerca classifica finale World Sailing o fonte ufficiale evento.",
            "4. Aggiorna scheda atleta solo con risultato finale verificato.",
            "5. Mantieni SportVela come contesto editoriale, non come fonte primaria di classifica.",
            "",
            "## Link operativi",
            "",
            f"- {wiki(comunicati / '00-Indice-Eventi.md', 'Indice eventi comunicati')}",
            f"- {wiki(comunicati / '03-Registro-Comunicati-Ufficiali.md', 'Registro comunicati ufficiali')}",
            f"- {wiki(fed / '01-Registro-Fonti.md', 'Registro Federvela')}",
            f"- {wiki(ws_map, 'World Sailing - classifiche')}",
            f"- {wiki(VAULT / 'Modelli' / 'Modello-News-Evento.md', 'Modello news evento')}",
        ],
    )

    write(
        pages["rules"],
        [
            "# Regole linking Obsidian",
            "",
            "Piu' link aiutano solo se sono coerenti. Link casuali o ripetuti rendono il vault piu' rumoroso.",
            "",
            "## Regola 3-2-1",
            "",
            "- Ogni nota operativa dovrebbe avere almeno 3 link: fonte, hub tematico, oggetto principale.",
            "- Ogni hub dovrebbe rimandare ad almeno 2 indici specializzati.",
            "- Ogni dato critico dovrebbe avere 1 fonte primaria chiaramente indicata.",
            "",
            "## Link da preferire",
            "",
            "- atleta -> scheda atleta",
            "- risultato -> nota classifica o CSV verificato",
            "- news ufficiale -> registro Federvela",
            "- contesto esterno -> registro SportVela",
            "- progetto -> hub progetto",
            "- tema ricorrente -> indice tematico",
            "",
            "## Link da evitare",
            "",
            "- Linkare ogni parola ripetuta.",
            "- Creare hub enormi con centinaia di link diretti.",
            "- Duplicare lo stesso contenuto in piu' cartelle.",
            "- Mescolare fonte ufficiale e fonte esterna senza indicare priorita'.",
        ],
    )

    connective_body = (
        f"- [[{rel_no_ext(pages['hub'])}|Hub mappe e collegamenti]]\n"
        f"- [[{rel_no_ext(pages['query'])}|Indice consultazione rapida]]\n"
        f"- [[{rel_no_ext(pages['source'])}|Gerarchia fonti e attendibilita]]\n"
        f"- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n"
        "\n"
        "Uso: partire da queste mappe quando vuoi attraversare il vault per tema invece che per cartella."
    )
    insert_block(VAULT / "00-Mappa-Vault.md", "Strato relazionale", connective_body)

    rules_body = (
        f"- Regole operative: [[{rel_no_ext(pages['rules'])}|Regole linking Obsidian]].\n"
        "- Non serve linkare tutto: serve linkare bene.\n"
        "- Priorita': fonte primaria, oggetto principale, hub tematico, classifiche verificate.\n"
        "- Per archivi grandi, usare indici annuali/tematici invece di pagine monolitiche."
    )
    insert_block(VAULT / "99-Regole-Memoria.md", "Regola per collegamenti interni", rules_body)

    for target, title, body in [
        (
            fed / "00-Overview.md",
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['source'])}|Gerarchia fonti e attendibilita]]\n- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n- [[{rel_no_ext(pages['events'])}|Ponte eventi, comunicati e classifiche]]",
        ),
        (
            sportvela / "00-Overview.md",
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['source'])}|Gerarchia fonti e attendibilita]]\n- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n- [[{rel_no_ext(fed / '00-Overview.md')}|Federvela fonte primaria]]",
        ),
        (
            athletes,
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['athlete'])}|Ponte atleti, risultati e fonti]]\n- [[{rel_no_ext(ws_map)}|World Sailing - Mappa Atleti e Classifiche]]\n- [[{rel_no_ext(fed / 'Indici' / 'Per Tema' / 'risultati.md')}|News ufficiali risultati]]",
        ),
        (
            istituzionale / "00-Overview.md",
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n- [[{rel_no_ext(fed / 'Indici' / 'Per Tema' / 'istituzionale.md')}|News istituzionali Federvela]]\n- [[{rel_no_ext(pages['source'])}|Gerarchia fonti e attendibilita]]",
        ),
        (
            america / "00-Overview.md",
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n- [[{rel_no_ext(fed / 'Indici' / 'Per Tema' / 'america-s-cup-napoli.md')}|News ufficiali Americas Cup/Napoli]]\n- [[{rel_no_ext(sportvela / 'Indici' / 'Per Tema' / 'america-s-cup-napoli.md')}|Contesto SportVela Americas Cup/Napoli]]",
        ),
        (
            we_sail / "00-Overview.md",
            "Collegamenti trasversali",
            f"- [[{rel_no_ext(pages['themes'])}|Ponte temi, progetti e fonti]]\n- [[{rel_no_ext(fed / 'Indici' / 'Per Tema' / 'media-comunicazione.md')}|News ufficiali media/comunicazione]]\n- [[{rel_no_ext(sportvela / 'Indici' / 'Per Tema' / 'media-storytelling.md')}|Contesto editoriale storytelling]]",
        ),
    ]:
        insert_block(target, title, body)

    print(f"Connective layer written: {CONNECT}")
    print(f"Connector pages: {len(list(CONNECT.glob('*.md')))}")


if __name__ == "__main__":
    main()
