from dataclasses import dataclass
from typing import Optional

import pandas as pd


class MissingColumnError(ValueError):
    print("")



class GenericRecommender:
    def __init__(self, source_col: str, target_col: str, feedback_col: str) -> None :
        print("")

    def fit(self, df: pd.Dataframe):
        print("")

@dataclass
class DatasetConfig:
    source_col: str
    target_col: str
    feedback_col: str
    dataset_name: Optional[str] = None

    def validate_against_df(self, df: pd.DataFrame) -> None:
        cols = {self.source_col, self.target_col, self.feedback_col}
        if len(cols) != 3:
            raise ValueError(
                f"Configured columns must be distinct, got "
                f"source_col={self.source_col}"
                f"target_col={self.target_col}"
                f"feedback_col={self.feedback_col}"
            )
        missing = [col for col in cols if col not in df.columns]
        if missing:
            dataset_label = f"for dataset '{self.dataset_name}'" if self.dataset_name else ""
            raise MissingColumnError(
                f"Missing columns {dataset_label}: {missing}.\n"
                f"Available {dataset_label}: {list(df.columns)}"
            )
