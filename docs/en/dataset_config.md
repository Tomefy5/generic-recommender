# Dataset configuration

This document explains how to prepare your dataset so that it can be used with the `GenericRecommender` engine.

The engine expects a **tabular dataset** (Pandas DataFrame or CSV) with at least three logical columns:

- source: the entity that receives recommendations (for example: `user`, `patient`, `student`).
- target: the thing being recommended (for example: `item`, `resource`, `drug`, `course`).
- feedback: a numeric signal describing how good the interaction was (for example: `rating`, `click`, `success`).

These are *roles*, not fixed column names: you can use any column names in your CSV/DataFrame, as long as you tell the engine which is which.

---

## Minimum required schema

Your dataset must contain at least:

- One column that identifies the **source** entity (for example: `user_id`, `patient_id`, `student_id`).
- One column that identifies the **target** entity (for example: `item_id`, `drug_id`, `course_id`).
- One column that stores a **feedback** value (for example: `rating`, `score`, `clicked`, `success`).

The feedback column should be numeric (integer or float) or convertible to a numeric value.  
If it is not numeric, the engine will raise a validation error during `fit()`.

---

## Example dataset

Example of a small movie recommendation dataset:

| user_id | movie_id | rating |
|--------|----------|--------|
| 1      | 10       | 4.0    |
| 1      | 12       | 5.0    |
| 2      | 10       | 3.0    |

In this case, the roles are:

- source column: `user_id`
- target column: `movie_id`
- feedback column: `rating`

---

## Configuring the engine

To connect this dataset to the engine, you pass the column names to the constructor:

```
from generic_recommender import GenericRecommender

engine = GenericRecommender(
    source_col="user_id",
    target_col="movie_id",
    feedback_col="rating",
)

engine.fit(df)
```

Here:

- `df` is a `pandas.DataFrame` with at least `user_id`, `movie_id`, and `rating` columns.
- The engine will validate that these columns exist and are suitable for training.
- Internally, it will build index mappings (IDs → integer indices) for sources and targets.

---

## Validation behaviour

When you call `fit(df)`:

1. The engine checks that all three configured columns are present in `df`.
2. It checks that the feedback column is numeric or can be safely converted.
3. If something is wrong, it raises a clear error, for example:

```
MissingColumnError: expected column 'user_id' in dataframe columns ['uid', 'movie_id', 'rating']
```

This early validation helps you detect schema problems before training the recommendation model.

---

## Recommended naming conventions

You can use any names you like, but the following patterns are common and readable:

- `user_id`, `customer_id`, `patient_id`, `student_id` for sources.
- `item_id`, `product_id`, `drug_id`, `course_id` for targets.
- `rating`, `score`, `label`, `clicked`, `success` for feedback.


## Errors

The recommender validates your dataframe before training.  
If the configured columns are missing or inconsistent, it raises clear, explicit errors.

### MissingColumnError

This error is raised when one or more of the configured columns (`source_col`, `target_col`, `feedback_col`) are not present in the dataframe.

Example:

```
MissingColumnError: Missing columns: ['user_id']. Available columns: ['uid', 'movie_id', 'rating']
```

How to fix:

- Check the spelling of your column names.
- Make sure the dataframe you pass to `fit()` actually contains the expected columns.
- Update the constructor if your real column names are different, for example:

```
engine = GenericRecommender(
    source_col="uid",
    target_col="movie_id",
    feedback_col="rating",
)
```

### Invalid configuration

If you accidentally configure the same name for multiple roles (for example, the same column as both `source_col` and `target_col`), the engine raises a `ValueError`.

Example:

```
ValueError: Configured columns must be distinct, got source_col='user_id', target_col='user_id', feedback_col='rating'
```

How to fix:

- Use three distinct columns for source, target and feedback.
- Double‑check the parameters you pass to `GenericRecommender(...)`.

Keeping these conventions makes it easier for other developers to understand your datasets and examples.
