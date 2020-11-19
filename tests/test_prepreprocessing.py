import pytest
import datamining.prepreprocessing as ppp
import pandas as pd
from data_for_tests import DATA_LENGTH, data  # Data for tests


# Build dataframes
df: pd.DataFrame = pd.DataFrame(data=data)
df_copy: pd.DataFrame = pd.DataFrame(data=data)


def test_complete_count():
    #Value testing
    assert ppp.complete_count(df) == 3
    assert ppp.complete_count(df,missing_value="?") == 2
    #Ensure original is unchanged
    assert df.equals(df_copy)


def test_unique_values():
    # Value testing
    assert ppp.unique_values(df, "dates") == list(df["dates"].unique())
    assert ppp.unique_values(df, "typos") == list(df["typos"].unique())
    # Ensure original is unchanged
    assert df.equals(df_copy)


def test_unique_values_count():
    # Value testing
    assert ppp.unique_values_count(df, "dates") == DATA_LENGTH
    assert ppp.unique_values_count(df, "typos") == 9
    # Ensure original is unchanged
    assert df.equals(df_copy)


def test_data_frame_analysis():
    assert True
