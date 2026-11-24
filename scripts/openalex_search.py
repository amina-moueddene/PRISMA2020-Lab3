#!/usr/bin/env python3
"""Exécute les versions V1 à V5 de la requête dans OpenAlex (gratuit, sans compte).

Lit search/queries_openalex.json, interroge l'API OpenAlex (titre + résumé,
période 2013-2026), récupère tous les résultats par pagination et écrit :
  exports/<VERSION>/openalex.csv   (doi, title, year, openalex_id)
  search/openalex_run_log.csv      (version, date, nombre de résultats, URL exacte)

Usage (sur ton ordinateur, avec connexion internet) :
  python3 scripts/openalex_search.py --mailto ton.email@exemple.com
  python3 scripts/openalex_search.py --mailto ... --only V4_enrichie V5_test_NOT
  python3 scripts/openalex_search.py --mailto ... --api-key TA_CLE   (si OpenAlex répond 503)
Puis :
  python3 scripts/recall_check.py

--mailto est recommandé par OpenAlex (accès au "polite pool", plus rapide).
Bibliothèque standard uniquement.
"""
import argparse
import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES = ROOT / "search" / "queries_openalex.json"
EXPORTS = ROOT / "exports"
RUNLOG = ROOT / "search" / "openalex_run_log.csv"
API = "https://api.openalex.org/works"


def build_url(query, period, cursor, mailto, api_key=""):
    params = {
        "filter": f"title_and_abstract.search:{query},publication_year:{period}",
        "per-page": "200",
        "cursor": cursor,
        "select": "id,doi,display_name,publication_year",
    }
    if mailto:
        params["mailto"] = mailto
    if api_key:
        params["api_key"] = api_key
    return API + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def get_json(url, retries=6):
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:500]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 30 * (attempt + 1)
                print(f"  OpenAlex indisponible (HTTP {e.code}), nouvel essai dans {wait} s...")
                time.sleep(wait)
                continue
            sys.exit(f"Erreur OpenAlex HTTP {e.code} : {body}")
        except urllib.error.URLError as e:
            if attempt < retries - 1:
                time.sleep(3)
                continue
            sys.exit(f"Connexion impossible à OpenAlex : {e}")


def run(version, query, period, mailto, api_key=""):
    if "," in query:
        sys.exit(f"{version} : la requête contient une virgule, interdite par l'API.")
    cursor, rows, total = "*", [], None
    first_url = build_url(query, period, "*", mailto)
    while cursor:
        data = get_json(build_url(query, period, cursor, mailto, api_key))
        if total is None:
            total = data["meta"]["count"]
        for w in data["results"]:
            rows.append([
                (w.get("doi") or "").replace("https://doi.org/", ""),
                w.get("display_name") or "",
                w.get("publication_year") or "",
                w.get("id") or "",
            ])
        cursor = data["meta"].get("next_cursor")
        if not data["results"]:
            break
        time.sleep(0.2)
    out = EXPORTS / version
    out.mkdir(parents=True, exist_ok=True)
    with (out / "openalex.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["doi", "title", "year", "openalex_id"])
        w.writerows(rows)
    return total, len(rows), first_url.replace(f"mailto={urllib.parse.quote(mailto or '')}", "mailto=…")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mailto", default="", help="adresse e-mail (recommandée par OpenAlex)")
    ap.add_argument("--api-key", default="", help="clé API OpenAlex gratuite (facultative)")
    ap.add_argument("--only", nargs="*", help="versions à exécuter (par défaut : toutes)")
    args = ap.parse_args()

    spec = json.loads(QUERIES.read_text(encoding="utf-8"))
    versions = spec["versions"]
    names = args.only or list(versions)
    new_log = not RUNLOG.exists()
    with RUNLOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["version", "base", "champ", "periode", "date_execution", "nb_resultats_api", "nb_recuperes", "url"])
        for name in names:
            total, got, url = run(name, versions[name], spec["period"], args.mailto, args.api_key)
            w.writerow([name, "OpenAlex", "title_and_abstract", spec["period"], date.today().isoformat(), total, got, url])
            print(f"{name}: {total} résultats ({got} récupérés)")


if __name__ == "__main__":
    main()
