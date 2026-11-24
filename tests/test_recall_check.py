"""Tests du calcul du rappel et de la précision (étapes 10 à 12), sur des données fictives."""
import csv
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def rows(p):
    return list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8"))))

spec = importlib.util.spec_from_file_location("recall_check", ROOT / "scripts" / "recall_check.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


class TestNormalisation(unittest.TestCase):
    def test_doi(self):
        self.assertEqual(rc.norm_doi("https://doi.org/10.3390/RS70505584"), "10.3390/rs70505584")
        self.assertEqual(rc.norm_doi("http://dx.doi.org/10.1/X"), "10.1/x")
        self.assertEqual(rc.norm_doi(""), "")

    def test_titre(self):
        self.assertEqual(rc.norm_title("Spatio-Temporal Assessment: A Case!"), rc.norm_title("spatio temporal assessment a case"))

    def test_dedoublonnage_doi_puis_titre(self):
        recs = [("10.1/a", "titrea"), ("10.1/a", "autre"), ("", "titreb"), ("10.1/c", "titreb"), ("10.1/d", "titred")]
        self.assertEqual(len(rc.dedup(recs)), 3)


class TestRappel(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        t = Path(self.tmp.name)
        (t / "data").mkdir()
        with (t / "data" / "included_reports.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["record", "first_author", "year", "database", "doi", "title"])
            w.writerow([1, "A", 2020, "x", "10.1/a", "Etude A"])
            w.writerow([2, "B", 2021, "x", "10.1/b", "Etude B"])
            w.writerow([3, "C", 2022, "x", "", "Etude C sans DOI"])
            w.writerow([4, "D", 2023, "x", "10.1/d", "Etude D"])
        for v, rows in {"V1_large": [("10.1/a", "Etude A"), ("10.1/B", "Etude B"), ("", "Etude C sans DOI"), ("10.9/z", "Bruit")],
                        "V3_restrictive": [("10.1/a", "Etude A"), ("10.9/z", "Bruit")]}.items():
            (t / "exports" / v).mkdir(parents=True)
            with (t / "exports" / v / "openalex.csv").open("w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["doi", "title", "year", "openalex_id"])
                for d, ti in rows:
                    w.writerow([d, ti, 2020, "W1"])
        rc.EXPORTS, rc.INCLUDED, rc.RESULTS = t / "exports", t / "data" / "included_reports.csv", t / "results"
        self.t = t

    def tearDown(self):
        self.tmp.cleanup()

    def test_rappel_precision_et_manques(self):
        with redirect_stdout(io.StringIO()):
            rc.main()
        res = {(r["version"], r["base"]): r for r in rows(self.t / "results" / "recall_results.csv")}
        v1 = res[("V1_large", "OpenAlex")]
        self.assertEqual((v1["nb_resultats"], v1["inclus_retrouves"], v1["rappel"], v1["precision"]), ("4", "3", "0.750", "0.750"))
        v3 = res[("V3_restrictive", "OpenAlex")]
        self.assertEqual((v3["inclus_retrouves"], v3["rappel"]), ("1", "0.250"))
        missed = (rows(self.t / "results" / "missed_reports.csv"))
        self.assertEqual(sorted((m["version"], m["record"]) for m in missed),
                         [("V1_large", "4"), ("V3_restrictive", "2"), ("V3_restrictive", "3"), ("V3_restrictive", "4")])
        new = (rows(self.t / "results" / "new_vs_V1.csv"))
        self.assertEqual(new, [])  # V3 ne contient rien de plus que V1


class TestResultatsDuDepot(unittest.TestCase):
    """Vérifie que les résultats publiés correspondent aux exports publiés."""

    def test_resultats_publies(self):
        p = ROOT / "results" / "recall_results.csv"
        if not p.exists():
            self.skipTest("results/ absent")
        res = {(r["version"], r["base"]): r for r in rows(p)}
        self.assertEqual(res[("V1_large", "OpenAlex (dédoublonné)")]["inclus_retrouves"], "20")
        for v in ("V2_intermediaire", "V3_restrictive"):
            self.assertLess(int(res[(v, "OpenAlex (dédoublonné)")]["inclus_retrouves"]),
                            int(res[("V1_large", "OpenAlex (dédoublonné)")]["inclus_retrouves"]))


if __name__ == "__main__":
    unittest.main()
