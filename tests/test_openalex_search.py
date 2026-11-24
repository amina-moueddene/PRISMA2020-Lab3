"""Tests de construction des URL OpenAlex (sans appel réseau)."""
import importlib.util
import json
import unittest
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("openalex_search", ROOT / "scripts" / "openalex_search.py")
oa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oa)


class TestURL(unittest.TestCase):
    def test_url_contient_filtre_periode_et_pagination(self):
        q = json.loads((ROOT / "search" / "queries_openalex.json").read_text(encoding="utf-8"))["versions"]["V3_restrictive"]
        url = oa.build_url(q, "2013-2026", "*", "test@example.org")
        p = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
        self.assertEqual(p["filter"][0], f"title_and_abstract.search:{q},publication_year:2013-2026")
        self.assertEqual(p["per-page"][0], "200")
        self.assertEqual(p["cursor"][0], "*")
        self.assertEqual(p["mailto"][0], "test@example.org")

    def test_cle_api_facultative(self):
        url = oa.build_url("olive", "2013-2026", "*", "", "CLE")
        self.assertIn("api_key=CLE", url)
        self.assertNotIn("mailto", oa.build_url("olive", "2013-2026", "*", ""))


if __name__ == "__main__":
    unittest.main()
