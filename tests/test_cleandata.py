import pytest
from datamining import cleandata
import pandas as pd
import numpy as np
from data_for_tests import DATA_LENGTH, data  # Data for tests


# Build dataframes
df: pd.DataFrame = pd.DataFrame(data=data)
df_copy: pd.DataFrame = pd.DataFrame(data=data)


def test_dates():
    # Value testing
    assert (
        list(cleandata.dates(df, "dates", f="%m/%d/%Y")) == ["01/17/2000"] * DATA_LENGTH
    )
    assert list(cleandata.dates(df, "dates", f="%m/%Y")) == ["01/2000"] * DATA_LENGTH
    assert list(cleandata.dates(df, "dates", f="HAHA")) == ["HAHA"] * DATA_LENGTH
    # Ensure original is unchanged
    assert df.equals(df_copy)


def test_fix_nan():
    # Value Testing
    _df2 = cleandata.fix_nan(df, replace_with={"nan1": 3, "nan2": "?"})
    assert list(_df2["nan1"]) == [0, 1, 2, 3, 4, 3, 3, 7, 8, 3]
    assert list(_df2["nan2"]) == ["?", 1, "?", 3, 4, 5, 6, "?", 8, 9]
    _df2 = cleandata.fix_nan(df, replace_with="?")
    assert list(_df2["nan1"]) == [0, 1, 2, "?", 4, "?", "?", 7, 8, "?"]
    assert list(_df2["nan2"]) == ["?", 1, "?", 3, 4, 5, 6, "?", 8, 9]
    # Ensure original is unchanged
    assert df.equals(df_copy)


def test_typos():
    # Value Testing
    assert list(
        cleandata.typos(
            df, "typos", ["yes", "no"], missing_values="?", ignore_missing=True
        )
    ) == ["yes", "yes", "yes", "yes", "?", "no", "no", "no", "no", "?"]
    assert list(
        cleandata.typos(
            df, "typos", ["Y", "N"], missing_values="?", ignore_missing=True
        )
    ) == ["Y", "Y", "Y", "Y", "?", "N", "N", "N", "N", "?"]
    # Make sure if missing values aren't ignored, they are replaced
    with pytest.raises(ValueError):
        list(
            cleandata.typos(
                df, "typos", ["yes", "no"], missing_values="?", ignore_missing=False
            )
        ).index("?")
    # Ensure original is unchanged
    assert df.equals(df_copy)
