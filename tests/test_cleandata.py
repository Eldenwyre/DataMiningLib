import pytest
from datamining import cleandata
import pandas as pd
import numpy as np
from data_for_tests import DATA_LENGTH, data  # Data for tests


# Build dataframes
df: pd.DataFrame = pd.DataFrame(data=data)
df_copy: pd.DataFrame = pd.DataFrame(data=data)


def test_bounding():
    test_list = [-10,"-9",0,"string", 1, 2, "3", 4, "5.5", 20, "-1"]
    test_data = pd.Series(test_list)
    # Value testing
    #Test Maintaining Values if no bounds given
    assert (cleandata.bounding(test_data).equals(test_data))
    #Test lower bounds
    assert (list(cleandata.bounding(test_data, lower_bound=1.5, replace_with="R")) == ["R","R","R","string", "R", 2, "3", 4, "5.5", 20, "R"])
    #Test upper bounds
    assert (list(cleandata.bounding(test_data,upper_bound=0,replace_with="R")) == [-10,"-9",0,"string", "R", "R", "R", "R", "R", "R", "-1"])
    #Test upper and lower bounds
    assert (list(cleandata.bounding(test_data,lower_bound=0, upper_bound=5,replace_with="R")) == ["R","R",0,"string", 1, 2, "3", 4, "R", "R", "R"])
    #Test ignoring missing values
    assert (list(cleandata.bounding(test_data, lower_bound=0, upper_bound=5, replace_with="R",missing_values=-10,ignore_missing=True)) == [-10,"R",0,"string", 1, 2, "3", 4, "R", "R", "R"])
    #Ensure original is unchanged
    assert test_data.equals(pd.Series(test_list))


def test_dates():
    # Value testing
    assert (
        list(cleandata.dates(df["dates"], f="%m/%d/%Y")) == ["01/17/2000"] * DATA_LENGTH
    )
    assert list(cleandata.dates(df["dates"], f="%m/%Y")) == ["01/2000"] * DATA_LENGTH
    assert list(cleandata.dates(df["dates"], f="HAHA")) == ["HAHA"] * DATA_LENGTH
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


def test_remove_sparse_rows():
    # Value Testing
    #!(These values may need to be changed when data in data_for_tests is changed)
    _df2 = cleandata.remove_sparse_rows(
        df, 0.1, missing_values="?", weighting_dict=None
    )
    assert _df2.equals(df_copy)
    _df2 = cleandata.remove_sparse_rows(
        df, 0.6, missing_values="?", weighting_dict=None
    )
    assert _df2.equals(df.drop([9], inplace=False))
    _df2 = cleandata.remove_sparse_rows(
        df, 0.8, missing_values="?", weighting_dict=None
    )
    assert _df2.equals(df.drop([0, 2, 3, 4, 5, 6, 7, 9], inplace=False))
    # Value Testing with Dicts
    _df2 = cleandata.remove_sparse_rows(
        df, 0.8, missing_values="?", weighting_dict={}, default_weighting=0
    )
    assert _df2.equals(df)  # All 0 case
    _df2 = cleandata.remove_sparse_rows(
        df,
        0.8,
        missing_values="?",
        weighting_dict={"dates": 1, "typos": 1, "nan1": 1, "nan2": 1},
        default_weighting=0,
    )
    assert _df2.equals(
        cleandata.remove_sparse_rows(df, 0.8, missing_values="?")
    )  # Ensuring Dicts don't change results from default
    _df2 = cleandata.remove_sparse_rows(
        df, 0.8, missing_values="?", weighting_dict={}, default_weighting=1
    )
    assert _df2.equals(
        cleandata.remove_sparse_rows(df, 0.8, missing_values="?")
    )  # Ensuring Dicts don't change results from default
    _df2 = cleandata.remove_sparse_rows(
        df, 0.8, missing_values="?", weighting_dict={}, default_weighting=2
    )
    assert _df2.equals(
        cleandata.remove_sparse_rows(df, 0.8, missing_values="?")
    )  # Ensuring Dicts don't change results from default
    _df2 = cleandata.remove_sparse_rows(
        df,
        0.8,
        missing_values="?",
        weighting_dict={"dates": 2, "typos": 1, "nan1": 1, "nan2": 1},
        default_weighting=0,
    )
    assert _df2.equals(df.drop([9], inplace=False))
    _df2 = cleandata.remove_sparse_rows(
        df,
        0.8,
        missing_values="?",
        weighting_dict={"typos": 1, "nan1": 1, "nan2": 1},
        default_weighting=0,
    )
    assert _df2.equals(df.drop([0, 2, 3, 4, 5, 6, 7, 9], inplace=False))
    _df2 = cleandata.remove_sparse_rows(
        df,
        0.8,
        missing_values="?",
        weighting_dict={"typos": 1, "nan1": 10, "nan2": 1},
        default_weighting=0,
    )
    assert _df2.equals(df.drop([3, 5, 6, 9], inplace=False))
    # TODO:Add tests for negative values if actual support implemented
    # Ensure original is unchanged
    assert df.equals(df_copy)


def test_typos():
    # Value Testing
    assert list(
        cleandata.typos(
            df["typos"], ["yes", "no"], missing_values="?", ignore_missing=True
        )
    ) == ["yes", "yes", "yes", "yes", "?", "no", "no", "no", "no", "?"]
    assert list(
        cleandata.typos(
            df["typos"], ["Y", "N"], missing_values="?", ignore_missing=True
        )
    ) == ["Y", "Y", "Y", "Y", "?", "N", "N", "N", "N", "?"]
    # Make sure if missing values aren't ignored, they are replaced
    with pytest.raises(ValueError):
        list(
            cleandata.typos(
                df["typos"], ["yes", "no"], missing_values="?", ignore_missing=False
            )
        ).index("?")
    # Ensure original is unchanged
    assert df.equals(df_copy)
