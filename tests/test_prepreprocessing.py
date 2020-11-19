import pytest
import datamining.prepreprocessing as ppp
import pandas as pd

# Num entries per column
DATA_LENGTH = 10

# Data frame used for testing these functions (DATA_LENGTH entries per column)
data = {
    "dates": [
        "01/17/2000",
        "January 17, 2000",
        "Jan 17, 2000",
        "17 Jan 2000",
        "17 January 2000",
        "01-17-2000",
        "January 17th 2000",
        "17-01-2000",
        "17/01/2000",
        "17th January 2000",
    ],
    "typos": ["yes", "y", "yse", "YES", "?", "no", "No", "on", "NO", "?"],
}
df: pd.DataFrame = pd.DataFrame(data=data)
df_copy: pd.DataFrame = pd.DataFrame(data=data)


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
