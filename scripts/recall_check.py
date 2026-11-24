#!/usr/bin/env python3
"""Lab 3 - Test des versions de la requête (étapes 10 à 12).

Pour chaque version (V2_intermediaire, V3_restrictive, ...), le script lit les
exports de chaque base (OpenAlex, Lens, Scopus, WoS), les dédoublonne (DOI normalisé puis titre
normalisé, comme dans la SLR) et calcule :
  - le nombre de résultats par base et après dédoublonnage ;
  - le nombre des 23 rapports inclus dans la SLR qui sont retrouvés (rappel) ;
  - la précision = inclus retrouvés / résultats ;
  - la liste des rapports inclus manqués.

Organisation attendue (un fichier par base, nom libre) :
  exports/<VERSION>/openalex.csv  produit par scripts/openalex_search.py
  exports/<VERSION>/lens.csv      export CSV de Lens.org (colonnes DOI, Title)
  exports/<VERSION>/scopus.csv    export CSV de Scopus, si un accès est disponible
  exports/<VERSION>/wos.txt       export WoS "Tab delimited file" (DI, TI)

Usage :  python3 scripts/recall_check.py
Sortie : results/recall_results.csv, results/missed_reports.csv, tableau Markdown à l'écran.
Bibliothèque standard uniquement.
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"
INCLUDED = ROOT / "data" / "included_reports.csv"
RESULTS = ROOT / "results"

csv.field_size_limit(sys.maxsize)
LABELS = {"scopus": "Scopus", "wos": "Web of Science", "openalex": "OpenAlex", "lens": "Lens"}


def norm_doi(d):
    d = (d or "").strip().lower()
    d = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)
    return d


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())


def read_table(path):
    """Renvoie une liste de (doi, titre) depuis un export Scopus ou WoS."""
    raw = path.read_bytes().decode("utf-8-sig", errors="replace")
    first = raw.splitlines()[0] if raw else ""
    delim = "\t" if first.count("\t") > first.count(",") else ","
    rows = list(csv.DictReader(raw.splitlines(), delimiter=delim))
    out = []
    for r in rows:
        r = {(k or "").strip(): v for k, v in r.items()}
        doi = r.get("DOI") or r.get("DI") or r.get("doi") or ""
        title = (r.get("Title") or r.get("TI") or r.get("Article Title")
                 or r.get("title") or r.get("display_name") or "")
        if doi or title:
            out.append((norm_doi(doi), norm_title(title)))
    return out


def dedup(records):
    seen_doi, seen_title, unique = set(), set(), []
    for doi, title in records:
        if doi and doi in seen_doi:
            continue
        if title and title in seen_title:
            continue
        if doi:
            seen_doi.add(doi)
        if title:
            seen_title.add(title)
        unique.append((doi, title))
    return unique


def matches(included, records):
    dois = {d for d, _ in records if d}
    titles = {t for _, t in records if t}
    found, missed = [], []
    for inc in included:
        if inc["doi_n"] in dois or inc["title_n"] in titles:
            found.append(inc)
        else:
            missed.append(inc)
    return found, missed


def main():
    included = list(csv.DictReader(INCLUDED.open(encoding="utf-8")))
    for inc in included:
        inc["doi_n"] = norm_doi(inc["doi"])
        inc["title_n"] = norm_title(inc["title"])
    n_inc = len(included)

    versions = sorted(p for p in EXPORTS.iterdir() if p.is_dir()) if EXPORTS.exists() else []
    if not versions:
        print("Aucun export trouvé dans exports/<VERSION>/. Voir exports/README.md.")
        return

    RESULTS.mkdir(exist_ok=True)
    rows, missed_rows = [], []
    for vdir in versions:
        per_db = {}
        for f in sorted(vdir.iterdir()):
            if f.suffix.lower() in (".csv", ".txt"):
                label = LABELS.get(f.stem.lower(), f.stem)
                per_db[label] = read_table(f)
        if not per_db:
            continue
        for label, recs in per_db.items():
            found, _ = matches(included, recs)
            rows.append([vdir.name, label, len(recs), len(found), n_inc])
        merged = dedup([r for recs in per_db.values() for r in recs])
        found, missed = matches(included, merged)
        label = "Toutes bases (dédoublonné)" if len(per_db) > 1 else f"{next(iter(per_db))} (dédoublonné)"
        rows.append([vdir.name, label, len(merged), len(found), n_inc])
        for m in missed:
            missed_rows.append([vdir.name, m["record"], m["first_author"], m["year"], m["doi"], m["title"]])

    # Enregistrements de chaque version absents de V1 (utile pour V4 : que rapportent les nouveaux termes ?)
    base_dir = EXPORTS / "V1_large"
    if base_dir.exists():
        base = dedup([r for f in sorted(base_dir.iterdir()) if f.suffix.lower() in (".csv", ".txt") for r in read_table(f)])
        bd, bt = {d for d, _ in base if d}, {t for _, t in base if t}
        with (RESULTS / "new_vs_V1.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["version", "doi", "title_normalise"])
            for vdir in versions:
                if vdir.name == "V1_large":
                    continue
                for fpath in sorted(vdir.iterdir()):
                    if fpath.suffix.lower() not in (".csv", ".txt"):
                        continue
                    for d, t in dedup(read_table(fpath)):
                        if not ((d and d in bd) or (t and t in bt)):
                            w.writerow([vdir.name, d, t])
        print("\nEnregistrements absents de V1 : results/new_vs_V1.csv")

    with (RESULTS / "recall_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["version", "base", "nb_resultats", "inclus_retrouves", "nb_inclus_reference", "rappel", "precision"])
        for v, b, n, k, t in rows:
            w.writerow([v, b, n, k, t, f"{k / t:.3f}", f"{(k / n if n else 0):.3f}"])
    with (RESULTS / "missed_reports.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["version", "record", "first_author", "year", "doi", "title"])
        w.writerows(missed_rows)

    print("| Version | Base | Résultats | Inclus retrouvés | Rappel | Précision |")
    print("|---|---|---:|---:|---:|---:|")
    for v, b, n, k, t in rows:
        print(f"| {v} | {b} | {n} | {k}/{t} | {k / t:.0%} | {(k / n if n else 0):.1%} |")
    if missed_rows:
        print("\nRapports inclus manqués :")
        for v, rec, a, y, d, _ in missed_rows:
            print(f"  {v}: #{rec} {a} {y} ({d})")


if __name__ == "__main__":
    main()
