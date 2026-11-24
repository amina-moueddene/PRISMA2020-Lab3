# Exports

Un dossier par version, un fichier par base :

```
exports/
├── V1_large/openalex.csv
├── V2_intermediaire/openalex.csv
├── V3_restrictive/openalex.csv
├── V4_enrichie/openalex.csv
└── V5_test_NOT/openalex.csv
```

Ces fichiers sont créés automatiquement par :

```bash
python3 scripts/openalex_search.py --mailto ton.email@exemple.com
```

Les données OpenAlex sont sous licence CC0 : les exports peuvent être publiés dans le dépôt.

Si un accès à Scopus ou à WoS devient disponible, ajouter `scopus.csv` (export CSV) ou
`wos.txt` (export « Tab delimited file ») dans le même dossier : `scripts/recall_check.py`
les prend en compte et calcule aussi le résultat dédoublonné toutes bases confondues.
