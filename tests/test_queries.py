"""Tests de cohérence des requêtes (étapes 5 à 9, 11 et 13). Aucun accès réseau."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = json.loads((ROOT / "search" / "queries_openalex.json").read_text(encoding="utf-8"))
Q = SPEC["versions"]


def blocks(query):
    """Découpe une requête en blocs de premier niveau reliés par AND."""
    depth, cur, out = 0, "", []
    i = 0
    while i < len(query):
        c = query[i]
        if c == '"':
            j = query.index('"', i + 1)
            cur += query[i:j + 1]
            i = j + 1
            continue
        depth += c == "("
        depth -= c == ")"
        if depth == 0 and query.startswith(" AND ", i):
            out.append(cur.strip())
            cur, i = "", i + 5
            continue
        cur += c
        i += 1
    out.append(cur.strip())
    return out


def terms(block):
    return {t.strip().strip("()").lower() for t in re.split(r"\s+OR\s+", block.strip("()"))}


class TestQueries(unittest.TestCase):
    def test_versions_presentes(self):
        self.assertEqual(set(Q), {"V1_large", "V2_intermediaire", "V3_restrictive", "V4_enrichie", "V5_test_NOT"})

    def test_parentheses_et_guillemets_equilibres(self):
        for name, q in Q.items():
            with self.subTest(name):
                self.assertEqual(q.count("("), q.count(")"))
                self.assertEqual(q.count('"') % 2, 0)

    def test_pas_de_virgule_pour_openalex(self):
        for name, q in Q.items():
            self.assertNotIn(",", q, name)

    def test_pas_de_troncature_dans_openalex(self):
        for name, q in Q.items():
            self.assertNotIn("*", q, name)

    def test_operateurs_en_majuscules(self):
        for name, q in Q.items():
            self.assertIsNone(re.search(r"\s(and|or|not)\s", q), name)

    def test_quatre_concepts_relies_par_AND(self):
        for name in ("V1_large", "V2_intermediaire", "V3_restrictive", "V4_enrichie"):
            self.assertEqual(len(blocks(Q[name])), 4, name)

    def test_V2_et_V3_plus_etroites_que_V1(self):
        b1 = [terms(b) for b in blocks(Q["V1_large"])]
        for name in ("V2_intermediaire", "V3_restrictive"):
            for k, b in enumerate(blocks(Q[name])):
                self.assertTrue(terms(b) <= b1[k], f"{name}, concept {k + 1}")

    def test_V4_contient_V1(self):
        b1 = [terms(b) for b in blocks(Q["V1_large"])]
        b4 = [terms(b) for b in blocks(Q["V4_enrichie"])]
        for k in range(4):
            self.assertTrue(b1[k] <= b4[k], f"concept {k + 1}")

    def test_V5_est_V1_plus_NOT(self):
        self.assertTrue(Q["V5_test_NOT"].endswith(' NOT "olive oil"'))
        self.assertIn(Q["V1_large"], Q["V5_test_NOT"])

    def test_V1_identique_dans_scopus_et_wos(self):
        sco = (ROOT / "search" / "queries_scopus.txt").read_text(encoding="utf-8")
        wos = (ROOT / "search" / "queries_wos.txt").read_text(encoding="utf-8")
        for txt, field in ((sco, "TITLE-ABS-KEY("), (wos, "TS=(")):
            v1 = txt.split("## V1")[1].split("## V2")[0]
            self.assertEqual(v1.count(field), 4)
            for t in ('"Olea europaea"', '"remote sensing"', '"water stress"', '"machine learning"', "classif*"):
                self.assertIn(t.lower(), v1.lower())


if __name__ == "__main__":
    unittest.main()
