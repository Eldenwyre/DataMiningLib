import pandas as pd


def unique_values(df: pd.DataFrame, header: str) -> list:
    """Returns a list of the unique values for a column in a pandas dataframe

    df: DataFrame to use
    header: Name of column in dataframe to use"""
    return list(df[header].unique())


def unique_values_count(df: pd.DataFrame, header: str) -> int:
    """Returns the count of the unique values for a column in a pandas dataframe

    df: DataFrame to use
    header: Name of column in dataframe to use"""
    return len(df[header].unique())


def data_frame_analysis(df: pd.DataFrame, nominal_cutoff: float = 0.05) -> dict:
    """Performs an analysis of the pandas dataframe and prints data for each column
    IMPORTANT TO NOTE: These are analysis based on parameters for general datasets,
    it is better to use this as a tool rather than as an absolute.

    df: DataFrame to use
    nominal_cutoff: ratio of unique values to total values to determine if value is assumed to be nominal"""
    print("Planned to be implemented, not yet in use. Sorry")
