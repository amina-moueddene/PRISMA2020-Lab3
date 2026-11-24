# LAB 3 : stratégie de recherche bibliographique reproductible
## Application à ma SLR : ML et télédétection pour les maladies et le stress de l'olivier

> Sujet de la SLR : **détection des maladies et du stress de l'olivier (*Olea europaea* L.) par apprentissage automatique appliqué à des images UAV, aériennes et satellites.**
> Cadre : PRISMA 2020 + PRISMA-S. Bases : Scopus et Web of Science Core Collection. Période : 2013–2026. Recherche exécutée le **15/11/2026**.

> **Code et tests :** les requêtes de ce README sont générées, validées et testées par `src/search_strategy.py` (voir section 16). `python -m unittest discover -s tests -v` lance 25 tests.

Le sujet « Android + vulnérabilités + IA » du lab a trois concepts. Mon sujet en a **quatre** : culture, plateforme/capteur, cible, méthode. Les étapes sont identiques, mais la requête a un bloc de plus.

---

## 1. Introduction et prérequis

- Bases utilisées : Scopus et Web of Science (accès institutionnel).
- Objectif : produire une équation de recherche rigoureuse, testée, ajustée et documentée, qu'un autre chercheur peut rejouer à l'identique.

## 2. Analyse de la question de recherche

Question générale : *quelles plateformes, capteurs, cibles et algorithmes ont été combinés pour détecter les maladies et le stress de l'olivier, et quelle est la fiabilité des preuves ?*

```
Question de recherche
        ↓
4 concepts
        ↓
Mots-clés + synonymes
        ↓
Groupes avec OR
        ↓
Combinaison avec AND
        ↓
Search string (Scopus / WoS)
```

## 3. Identification des concepts principaux

| # | Concept | Ce qu'il couvre |
|---|---|---|
| C1 | **Culture** | L'olivier, l'oliveraie |
| C2 | **Plateforme et capteur** | UAV, avion, satellite, hyperspectral, thermique, etc. |
| C3 | **Cible** | Maladies (Xylella, Verticillium…), stress hydrique, sécheresse |
| C4 | **Méthode** | ML, DL, classifieurs |

Choix de découpe, comme dans le lab : je **n'inclus pas** « détection » dans C3, car certains articles parlent de « mapping », « monitoring », « discrimination » ou « estimation ». Les concepts « validation », « transfert », « leakage » ne sont **pas** dans la requête, car ils relèvent de l'analyse (V0–V5), pas de la recherche.

## 4. Mots-clés et synonymes

| Concept | Mot-clé principal | Synonymes | Acronymes / variantes |
|---|---|---|---|
| C1 Culture | olive | olives, *Olea europaea*, olive grove, olive orchard | (pluriels et troncatures) |
| C2 Plateforme | remote sensing | UAV, UAS, drone, unmanned aerial, airborne, aircraft, satellite, Sentinel, hyperspectral, multispectral, thermal, LiDAR | UAV/UAS, Sentinel-2 |
| C3 Cible | disease | pathogen, Xylella, Verticillium, olive knot, peacock spot, infection, symptom, water stress, drought, water status, stress | *X. fastidiosa*, *V. dahliae* |
| C4 Méthode | machine learning | deep learning, artificial intelligence, neural network, random forest, SVM, XGBoost, gradient boosting, YOLO, transfer learning, discriminant analysis, classification | ML, DL, CNN, SVM, RF |

Pièges évités : un seul mot-clé par concept, l'oubli des acronymes (CNN, SVM, YOLO), l'oubli des noms de pathogènes (certains articles ne disent jamais « disease »).

## 5. Opérateurs booléens

- **OR** dans un groupe (synonymes) : élargit.
- **AND** entre groupes (concepts) : restreint.
- **NOT** : **non utilisé**. Exclure par exemple « iOS » dans le lab est risquable. Ici, exclure « oil » ou « food » ferait perdre des articles pertinents. Les articles hors sujet sont éliminés à la sélection (codes E1–E8).

## 6. Guillemets et expressions exactes

Guillemets doubles sur toute expression multi-mots :
`"Olea europaea"`, `"olive grove*"`, `"remote sensing"`, `"unmanned aerial"`, `"water stress"`, `"machine learning"`, `"deep learning"`, `"neural network*"`, `"random forest"`, `"support vector"`, `"transfer learning"`.

Sans guillemets, `remote sensing` chercherait *remote* AND *sensing* séparément, d'où des faux positifs.

## 7. Troncatures et jokers

| Troncature | Capture | Risque de bruit |
|---|---|---|
| `"olive grove*"`, `"olive orchard*"` | grove / groves, orchard / orchards | faible |
| `uav*`, `drone*`, `satellite*`, `sentinel*` | uav / uavs, drone / drones… | faible |
| `disease*`, `pathogen*`, `infect*`, `symptom*` | pluriels, infection / infected / infectious | moyen |
| `"neural network*"` | neural network / networks | faible |
| `classif*` | classification, classifier, classified | **élevé** (très générique) |

Avertissement : `classif*` et `stress` sont les deux termes les plus bruyants. Ils sont acceptables ici car les blocs C1, C2 et C3 sont très spécifiques et filtrent le bruit.

## 8. Construction des groupes de concepts

**Groupe 1 : Culture**
```
(olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*")
```

**Groupe 2 : Plateforme et capteur**
```
(uav* OR uas OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing"
 OR satellite* OR sentinel* OR hyperspectral OR multispectral OR thermal OR lidar)
```

**Groupe 3 : Cible**
```
(disease* OR pathogen* OR xylella OR verticillium OR "olive knot" OR "peacock spot"
 OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress)
```

**Groupe 4 : Méthode**
```
("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*"
 OR cnn OR "random forest" OR "support vector" OR svm OR xgboost OR "gradient boosting"
 OR yolo OR "transfer learning" OR "discriminant analysis" OR classif*)
```

Les parenthèses forment chaque groupe en une « entité » logique. Sans elles, AND prendrait la priorité sur OR et fausserait la requête.

## 9. Combinaison avec AND : requête large

```
G1 AND G2 AND G3 AND G4
```

C'est la requête **large**, exécutée telle quelle (Section 13).

## 10. Test de la requête

| Base | Champ | Résultats |
|---|---|---|
| Scopus | TITLE-ABS-KEY | **118** |
| Web of Science Core Collection | Topic (TS) | **97** |
| **Total brut** | | **215** |
| Doublons supprimés | DOI (70) + titre normalisé (2) | **72** |
| **Records uniques** | | **143** (71 dans les deux bases, 46 Scopus seul, 26 WoS seul) |

Évaluation de la pertinence :
- Sur 143 records, **90** ont été exclus au titre/abstract, **53** recherchés en texte intégral, **15** introuvables, **38** évalués, **15** exclus, **22 études incluses** (23 rapports).
- Principaux motifs de bruit : autre culture ou hors sujet (E2, n = 36), pas de cible maladie/stress (E3, 17), livre ou chapitre (E7, 14), pas de capteur aérien/satellite (E4, 12), revue (E6, 11).

**Adaptation du critère du lab.** Le lab propose un taux de pertinence > 50 %. Une SLR vise l'**exhaustivité**, pas la précision. Ici : 22 / 143 ≈ **15 %** d'inclusion finale, ce qui est normal pour une SLR. Le critère de qualité de la requête est plutôt de savoir si elle retrouve des études connues, et si les rares études manquantes sont dues à un terme absent.

## 11. Ajustement : requêtes intermédiaire et restrictive

Versions de comparaison (à **exécuter et compléter** dans le tableau de la Section 12). Dans le code, le filtre d'années 2013–2026 (`PUBYEAR` pour Scopus, `PY` pour WoS) est ajouté à toutes les versions, comme à la requête large :

**Intermédiaire** : réduit les synonymes de C2 et C4.
```
TITLE-ABS-KEY(olive OR "Olea europaea")
AND TITLE-ABS-KEY(uav* OR drone* OR airborne OR satellite* OR "remote sensing" OR hyperspectral OR multispectral OR thermal)
AND TITLE-ABS-KEY(disease* OR xylella OR verticillium OR "water stress" OR drought)
AND TITLE-ABS-KEY("machine learning" OR "deep learning" OR "neural network*" OR "random forest" OR svm OR cnn)
```

**Restrictive** : termes les plus spécifiques seulement.
```
TITLE-ABS-KEY("Olea europaea" OR "olive grove*")
AND TITLE-ABS-KEY(uav* OR airborne OR satellite*)
AND TITLE-ABS-KEY(xylella OR verticillium OR "water stress")
AND TITLE-ABS-KEY("machine learning" OR "deep learning")
```

Conseil du lab : ne supprimez pas de synonymes sans tester. Vérifiez surtout que les **22 études incluses** sont toujours retrouvées (test de rappel).

## 12. Choix de la requête finale et justification

| Version | Résultats | Pertinence estimée | Commentaire |
|---|---|---|---|
| Large | 215 bruts / 143 uniques | 22 études incluses (≈ 15 %) | Exhaustive, bruit géré à la sélection |
| Intermédiaire | *à tester* | *à tester* | Vérifier combien des 22 études sont retrouvées |
| Restrictive | *à tester* | *à tester* | Risque : perdre les études sur drought / foliar disease |

**Choix : requête large.**
> « La requête large a été retenue car l'objectif est l'exhaustivité d'une revue systématique : elle combine quatre blocs de concepts avec de nombreux synonymes (pathogènes nommés, capteurs, algorithmes) afin de ne pas manquer d'études utilisant des vocabulaires variés. Le bruit résultant (autres cultures, livres, revues) est éliminé de façon transparente par des critères d'éligibilité codés E1–E8. Règle du lab : mieux vaut trop d'articles à filtrer que manquer des articles pertinents. »

## 13. Adaptation aux bases de données

**Scopus** (chaîne exacte exécutée)
```
TITLE-ABS-KEY(olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*")
AND TITLE-ABS-KEY(uav* OR uas OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing" OR satellite* OR sentinel* OR hyperspectral OR multispectral OR thermal OR lidar)
AND TITLE-ABS-KEY(disease* OR pathogen* OR xylella OR verticillium OR "olive knot" OR "peacock spot" OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress)
AND TITLE-ABS-KEY("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*" OR cnn OR "random forest" OR "support vector" OR svm OR xgboost OR "gradient boosting" OR yolo OR "transfer learning" OR "discriminant analysis" OR classif*)
AND PUBYEAR > 2012 AND PUBYEAR < 2027
```

**Web of Science Core Collection** (chaîne exacte exécutée)
```
TS=(olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*")
AND TS=(UAV* OR UAS OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing" OR satellite* OR Sentinel* OR hyperspectral OR multispectral OR thermal OR LiDAR)
AND TS=(disease* OR pathogen* OR Xylella OR Verticillium OR "olive knot" OR "peacock spot" OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress)
AND TS=("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*" OR CNN OR "random forest" OR "support vector" OR SVM OR XGBoost OR "gradient boosting" OR YOLO OR "transfer learning" OR "discriminant analysis" OR classif*)
AND PY=(2013-2026)
```

Différences de syntaxe : Scopus utilise `TITLE-ABS-KEY` et `PUBYEAR`, WoS utilise `TS=` et `PY=`. Pas de filtre de langue ou de type de document dans la base : ils sont appliqués à la sélection (E7, E8).

**Pistes d'extension (non exécutées).** IEEE Xplore et CAB Abstracts n'ont pas été interrogés, ce qui est une limite déjà déclarée. Si vous les ajoutez, la syntaxe de champs doit être adaptée et **testée** avant usage, comme le rappelle le lab.

## 14. Documentation et reproductibilité

| Élément | Valeur |
|---|---|
| Bases | Scopus ; Web of Science Core Collection (toutes éditions de l'abonnement institutionnel) |
| Date de recherche | 15/11/2026 |
| Requête finale | Voir Section 13 (chaînes exactes) |
| Champs | TITLE-ABS-KEY (Scopus) ; Topic / TS (WoS) |
| Filtres | Période 2013–2026 uniquement ; aucun filtre langue, type de document ou domaine |
| Résultats | Scopus 118 ; WoS 97 ; total 215 |
| Déduplication | DOI normalisé (70) puis titre normalisé (2) → 72 supprimés → **143 uniques** |
| Justification | Exhaustivité d'une SLR ; bruit géré par E1–E8 |
| Non recherché | Littérature grise, listes de références des études incluses |
| Export | Titres, abstracts, mots-clés, auteurs, DOI |
| Protocole | Fixé le 15/11/2026 avant le screening ; non enregistré dans un registre public |

Fichiers supplémentaires à conserver : S1 (screening), S2 (texte intégral), S3 (extraction), S4 (qualité), S5 (données codées).

## 15. Vérification : questions et défis

**Q1. Pourquoi OR dans les groupes et AND entre les groupes ?**
OR rassemble les synonymes d'un même concept (élargit). AND impose la présence de tous les concepts (restreint) : olivier ET capteur ET cible ET méthode.

**Q2. Impact des guillemets ?**
Ils forcent l'expression exacte : `"remote sensing"` n'est plus `remote` AND `sensing`, ce qui réduit les faux positifs.

**Q3. Pourquoi documenter ?**
Pour la reproductibilité, la justification méthodologique et la conformité PRISMA-S (date, chaînes exactes, filtres, nombres).

**Défi 1 : corriger une requête**
Requête fautive : `olive AND drone OR "machine learning"`.
AND l'emporte souvent sur OR, donc elle devient `(olive AND drone) OR "machine learning"` : elle ramène tout article de ML, même sans olivier.
Correction : `(olive OR "Olea europaea") AND (drone* OR uav*) AND ("machine learning" OR "deep learning")`.

**Défi 2 : enrichir le groupe 3 (cible) sans trop de bruit**
- `"olive quick decline syndrome"` : nom de la maladie liée à *Xylella* en Italie. Pertinent, peu bruyant.
- `"Spilocaea oleagina"` : agent de l'œil de paon, déjà couvert par « peacock spot » seulement si les auteurs utilisent ce terme. Utile car certains articles emploient le nom latin.
- Autres candidats à tester : `anthracnose`, `"leaf scorch"`, `"Verticillium wilt"`.

À tester comme dans le lab : exécuter la requête enrichie, vérifier combien de **nouveaux** records apparaissent et s'ils sont pertinents.

**Défi 3 : points faibles de ma stratégie (à discuter)**
1. `stress` et `classif*` sont très génériques (bruit élevé).
2. Aucun terme « vision transformer » ni « foundation model » : l'article note qu'aucune étude n'en utilise, mais la requête pourrait les rater. À tester.
3. Seulement deux bases, sans IEEE Xplore ni CAB Abstracts, et sans « snowballing » (référence des études incluses).
4. Recherche non relue par un pair (PRISMA-S item 8, déjà indiqué).

---

## 16. Code et tests

```
src/search_strategy.py          construit, valide et documente les requêtes
queries/                        requêtes générées (Scopus, WoS, générique) et journal de recherche
queries/search_log.csv          base, version, date, champs, filtres, requête, résultats
tests/test_search_strategy.py   25 tests
tests/golden/                   requêtes réellement exécutées le 15/11/2026 (référence des tests)
```

```bash
python src/search_strategy.py                 # régénère queries/
python -m unittest discover -s tests -v       # 25 tests
```

| Étape du lab | Dans le code |
|---|---|
| 3 et 4 : concepts, mots-clés, synonymes | `CONCEPTS` (4 blocs, 44 termes) |
| 5 à 7 : OR, AND, guillemets, troncatures | `group`, termes entre guillemets, `*` |
| 8 et 9 : groupes de concepts et combinaison avec AND | `generic_query`, `queries/generique_large.txt` |
| 10 : test de la requête | `validate_query` (parenthèses, guillemets, NOT interdit, troncature ≥ 3 lettres, 4 blocs), `matches` (évalue AND/OR/guillemets/troncature sur un texte) |
| 11 : requêtes intermédiaire et restrictive | `VARIANTS` (44, 21 et 10 termes) |
| 13 : adaptation aux bases | `scopus_query` (`TITLE-ABS-KEY`, `PUBYEAR`), `wos_query` (`TS=`, `PY=`) |
| 14 : documentation et reproductibilité | `build_log` → `queries/search_log.csv` |

**Ce que les tests vérifient**
- Les chaînes générées pour Scopus et WoS sont **identiques, caractère pour caractère**, à celles exécutées le 15/11/2026 (118 et 97 résultats, total 215).
- Les versions intermédiaire et restrictive sont des sous-ensembles de la requête large et sont plus courtes.
- Le validateur détecte des parenthèses non équilibrées, un guillemet ouvert, un `NOT`, une troncature trop courte et un nombre de blocs incorrect.
- La logique booléenne se comporte comme prévu sur des textes d'exemple : un texte sans concept « méthode » est rejeté (AND), un seul synonyme par bloc suffit (OR), `"remote sensing"` exige des mots adjacents, `drone*` couvre `drones` alors que `drone` seul non.
- Le journal ne contient des résultats que pour les deux requêtes réellement exécutées ; les versions intermédiaire et restrictive sont notées « non exécutée ».
