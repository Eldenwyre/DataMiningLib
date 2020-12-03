import pandas as pd
import numpy as np
from typing import Any


def complete_count(df: pd.DataFrame, missing_value: Any = np.nan) -> int:
    """Returns the number of complete rows (no missing values)

    df: Dataframe to use
    missing_value: Value that indicates a missing value (np.nan still checked)"""
    return len(df) - len(df[df.isin([missing_value, np.nan]).any(axis=1)])


def count_complete_col(col: pd.Series, missing_value: Any = np.nan) -> int:
    """Returns the number of complete (nonmissing) entries in a column.

    col: col of dataframe to use method
    missing_value: Value that indicates a missing value (np.nan still checked)"""
    return len(col) - col.isin([missing_value, np.nan]).sum()


def unique_values(col: pd.Series) -> list:
    """Returns a list of the unique values for a column in a pandas dataframe

    col: col of dataframe to use method"""
    return list(col.unique())


def unique_values_count(col: pd.Series) -> int:
    """Returns the count of the unique values for a column in a pandas dataframe

    col: col of dataframe to use method"""
    return len(col.unique())


def data_frame_analysis(df: pd.DataFrame, nominal_cutoff: float = 0.05) -> dict:
    """Performs an analysis of the pandas dataframe and prints data for each column
    IMPORTANT TO NOTE: These are analysis based on parameters for general datasets,
    it is better to use this as a tool rather than as an absolute.

    df: DataFrame to use
    nominal_cutoff: ratio of unique values to total values to determine if value is assumed to be nominal"""
    print("Planned to be implemented, not yet in use. Sorry")
