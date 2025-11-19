# Configuration du dataset

Ce document explique comment préparer ton dataset pour qu’il puisse être utilisé avec le moteur `GenericRecommender`.

Le moteur attend un **dataset tabulaire** (Pandas DataFrame ou CSV) avec au minimum trois colonnes logiques :

- source : l’entité qui reçoit les recommandations (par exemple : `user`, `patient`, `student`).
- cible : l’élément recommandé (par exemple : `item`, `resource`, `drug`, `course`).
- feedback : un signal numérique qui décrit la qualité de l’interaction (par exemple : `rating`, `click`, `success`).

Ce sont des *rôles*, pas des noms de colonnes imposés : tu peux utiliser n’importe quels noms de colonnes dans ton CSV/DataFrame, tant que tu indiques au moteur quelle colonne joue quel rôle.

---

## Schéma minimal requis

Ton dataset doit contenir au moins :

- Une colonne qui identifie la **source** (par exemple : `user_id`, `patient_id`, `student_id`).
- Une colonne qui identifie la **cible** (par exemple : `item_id`, `drug_id`, `course_id`).
- Une colonne qui contient le **feedback** (par exemple : `rating`, `score`, `clicked`, `success`).

La colonne de feedback doit être numérique (entier ou flottant) ou convertible en valeur numérique.  
Si ce n’est pas le cas, le moteur lèvera une erreur de validation pendant l’appel à `fit()`.

---

## Exemple de dataset

Exemple de petit dataset de recommandation de films :

| user_id | movie_id | rating |
|--------|----------|--------|
| 1      | 10       | 4.0    |
| 1      | 12       | 5.0    |
| 2      | 10       | 3.0    |

Dans ce cas, les rôles sont :

- colonne source : `user_id`
- colonne cible : `movie_id`
- colonne feedback : `rating`

---

## Configurer le moteur

Pour brancher ce dataset sur le moteur, tu passes les noms de colonnes au constructeur :

```
from generic_recommender import GenericRecommender

engine = GenericRecommender(
    source_col="user_id",
    target_col="movie_id",
    feedback_col="rating",
)

engine.fit(df)
```

Ici :

- `df` est un `pandas.DataFrame` qui contient au minimum les colonnes `user_id`, `movie_id` et `rating`.
- Le moteur va vérifier que ces colonnes existent et qu’elles sont utilisables pour l’entraînement.
- En interne, il construit des mappings d’IDs vers indices entiers pour les sources et les cibles.

---

## Comportement de validation

Quand tu appelles `fit(df)` :

1. Le moteur vérifie que les trois colonnes configurées sont présentes dans `df`.
2. Il vérifie que la colonne de feedback est numérique ou peut être convertie proprement.
3. Si quelque chose ne va pas, il lève une erreur explicite, par exemple :

```
MissingColumnError: expected column 'user_id' in dataframe columns ['uid', 'movie_id', 'rating']
```

Cette validation précoce permet de détecter les problèmes de schéma avant l’entraînement du modèle de recommandation.

---

## Conventions de nommage recommandées

Tu peux choisir les noms que tu veux, mais les conventions suivantes sont lisibles et fréquentes :

- `user_id`, `customer_id`, `patient_id`, `student_id` pour les sources.
- `item_id`, `product_id`, `drug_id`, `course_id` pour les cibles.
- `rating`, `score`, `label`, `clicked`, `success` pour le feedback.

## Erreurs

Le moteur vérifie ton dataframe avant l’entraînement.  
Si les colonnes configurées sont absentes ou incohérentes, il lève des erreurs claires et explicites.

### MissingColumnError

Cette erreur est levée lorsqu’une ou plusieurs des colonnes configurées (`source_col`, `target_col`, `feedback_col`) ne sont pas présentes dans le dataframe.

Exemple :

```
MissingColumnError: Missing columns: ['user_id']. Available columns: ['uid', 'movie_id', 'rating']
```

Comment corriger :

- Vérifie l’orthographe de tes noms de colonnes.
- Assure‑toi que le dataframe passé à `fit()` contient bien ces colonnes.
- Adapte le constructeur si les noms réels sont différents, par exemple :

```
engine = GenericRecommender(
    source_col="uid",
    target_col="movie_id",
    feedback_col="rating",
)
```

### Configuration invalide

Si tu configures par erreur le même nom pour plusieurs rôles (par exemple la même colonne pour `source_col` et `target_col`), le moteur lève une `ValueError`.

Exemple :

```
ValueError: Configured columns must be distinct, got source_col='user_id', target_col='user_id', feedback_col='rating'
```

Comment corriger :

- Utilise trois colonnes distinctes pour source, cible et feedback.
- Revérifie les paramètres que tu passes à `GenericRecommender(...)`.

Respecter ces conventions facilite la compréhension de tes datasets et de tes exemples par d’autres développeurs.
