# LAB 3 : Stratégie de recherche bibliographique reproductible
**Sujet : ML et télédétection (UAV, aérien, satellite) pour la détection des maladies et du stress de l'olivier**

## 1. Concepts principaux

| Concept | Description |
|---|---|
| C1 Culture | Olivier (*Olea europaea*), oliveraie |
| C2 Plateforme / capteur | UAV, avion, satellite, hyperspectral, multispectral, thermique, LiDAR |
| C3 Cible | Maladies (Xylella, Verticillium, etc.), stress hydrique, sécheresse |
| C4 Méthode | Machine learning, deep learning, classifieurs |

## 2. Mots-clés et synonymes

| Concept | Mot-clé principal | Synonymes | Acronymes / variantes |
|---|---|---|---|
| C1 | olive | olives, "Olea europaea", "olive grove*", "olive orchard*" | pluriels, troncatures |
| C2 | "remote sensing" | uav*, uas, drone*, "unmanned aerial", airborne, aircraft, satellite*, sentinel*, hyperspectral, multispectral, thermal, lidar | UAV, UAS |
| C3 | disease* | pathogen*, xylella, verticillium, "olive knot", "peacock spot", infect*, symptom*, "water stress", drought, "water status", stress | *X. fastidiosa*, *V. dahliae* |
| C4 | "machine learning" | "deep learning", "artificial intelligence", "neural network*", "random forest", "support vector", xgboost, "gradient boosting", yolo, "transfer learning", "discriminant analysis", classif* | ML, DL, CNN, SVM |

## 3. Groupes de concepts (OR dans le groupe)

```
G1 : (olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*")
G2 : (uav* OR uas OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing" OR satellite* OR sentinel* OR hyperspectral OR multispectral OR thermal OR lidar)
G3 : (disease* OR pathogen* OR xylella OR verticillium OR "olive knot" OR "peacock spot" OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress)
G4 : ("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*" OR cnn OR "random forest" OR "support vector" OR svm OR xgboost OR "gradient boosting" OR yolo OR "transfer learning" OR "discriminant analysis" OR classif*)
```

## 4. Trois requêtes (AND entre groupes)

**Requête large** (celle réellement exécutée) : `G1 AND G2 AND G3 AND G4`

**Requête intermédiaire**
```
TITLE-ABS-KEY(olive OR "Olea europaea")
AND TITLE-ABS-KEY(uav* OR drone* OR airborne OR satellite* OR "remote sensing" OR hyperspectral OR multispectral OR thermal)
AND TITLE-ABS-KEY(disease* OR xylella OR verticillium OR "water stress" OR drought)
AND TITLE-ABS-KEY("machine learning" OR "deep learning" OR "neural network*" OR "random forest" OR svm OR cnn)
```

**Requête restrictive**
```
TITLE-ABS-KEY("Olea europaea" OR "olive grove*")
AND TITLE-ABS-KEY(uav* OR airborne OR satellite*)
AND TITLE-ABS-KEY(xylella OR verticillium OR "water stress")
AND TITLE-ABS-KEY("machine learning" OR "deep learning")
```

## 5. Test et choix de la requête finale

| Version | Nombre de résultats | Pertinence | Commentaire |
|---|---|---|---|
| Large | 215 bruts (Scopus 118 + WoS 97), 143 uniques | 22 études incluses (≈ 15 %) | Exhaustive, bruit éliminé par les critères E1–E8 |
| Intermédiaire | ---- | ---- | Vérifier combien des 22 études sont retrouvées |
| Restrictive | ---- | ---- | Risque de perdre les études drought et maladies foliaires |

**Requête finale retenue : la requête large.**

**Justification :** l'objectif d'une revue systématique est l'exhaustivité. La requête large combine quatre blocs avec de nombreux synonymes (noms de pathogènes, capteurs, algorithmes), ce qui évite de manquer des études utilisant un vocabulaire différent. Le bruit (autres cultures, livres, revues) est éliminé de manière transparente à la sélection (codes E1–E8). Il vaut mieux avoir trop d'articles à filtrer que manquer des articles pertinents.

## 6. Adaptation aux bases de données

**Scopus**
```
TITLE-ABS-KEY(olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*") AND TITLE-ABS-KEY(uav* OR uas OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing" OR satellite* OR sentinel* OR hyperspectral OR multispectral OR thermal OR lidar) AND TITLE-ABS-KEY(disease* OR pathogen* OR xylella OR verticillium OR "olive knot" OR "peacock spot" OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress) AND TITLE-ABS-KEY("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*" OR cnn OR "random forest" OR "support vector" OR svm OR xgboost OR "gradient boosting" OR yolo OR "transfer learning" OR "discriminant analysis" OR classif*) AND PUBYEAR > 2012 AND PUBYEAR < 2027
```

**Web of Science**
```
TS=(olive OR olives OR "Olea europaea" OR "olive grove*" OR "olive orchard*") AND TS=(UAV* OR UAS OR drone* OR "unmanned aerial" OR airborne OR aircraft OR "remote sensing" OR satellite* OR Sentinel* OR hyperspectral OR multispectral OR thermal OR LiDAR) AND TS=(disease* OR pathogen* OR Xylella OR Verticillium OR "olive knot" OR "peacock spot" OR infect* OR symptom* OR "water stress" OR drought OR "water status" OR stress) AND TS=("machine learning" OR "deep learning" OR "artificial intelligence" OR "neural network*" OR CNN OR "random forest" OR "support vector" OR SVM OR XGBoost OR "gradient boosting" OR YOLO OR "transfer learning" OR "discriminant analysis" OR classif*) AND PY=(2013-2026)
```

## 7. Documentation de la stratégie

| Élément | Valeur |
|---|---|
| Bases de données | Scopus ; Web of Science Core Collection |
| Date de recherche | 15/11/2026 |
| Requête | Section 6 |
| Champs | TITLE-ABS-KEY (Scopus) ; Topic / TS (WoS) |
| Filtres | Période 2013–2026 ; aucun filtre de langue ni de type de document |
| Nombre de résultats | Scopus 118 ; WoS 97 ; total 215 ; 72 doublons ; 143 uniques |
| Justification | Exhaustivité de la SLR ; bruit géré par les critères d'éligibilité |

## 8. Questions de vérification

1. **Pourquoi OR dans les groupes et AND entre les groupes ?** OR regroupe les synonymes d'un même concept (élargit) ; AND impose que tous les concepts soient présents : olivier, capteur, cible et méthode (restreint).
2. **Impact des guillemets ?** Ils forcent l'expression exacte : `"remote sensing"` n'est pas `remote` AND `sensing`, ce qui réduit les faux positifs.
3. **Pourquoi documenter ?** Pour la reproductibilité, la justification des choix et la conformité PRISMA-S.

## 9. Défis

**Défi 1 : corriger une requête.** `olive AND drone OR "machine learning"` est lue comme `(olive AND drone) OR "machine learning"`, donc elle ramène tout article de ML, même sans olivier. Correction : `(olive OR "Olea europaea") AND (drone* OR uav*) AND ("machine learning" OR "deep learning")`.

**Défi 2 : deux nouveaux synonymes pour le groupe Cible (C3).**
- `"olive quick decline syndrome"` : nom de la maladie liée à *Xylella* en Italie, très spécifique, peu de bruit.
- `"Spilocaea oleagina"` : nom latin de l'agent de l'œil de paon, utile car certains auteurs n'écrivent pas « peacock spot ».

À tester avant adoption : vérifier combien de nouveaux records apparaissent et s'ils sont pertinents.
