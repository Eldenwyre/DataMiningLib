import numpy as np
import pandas as pd
from dateutil import parser
from difflib import SequenceMatcher, get_close_matches
from typing import Any, List, Dict


def dates(
    df: pd.DataFrame,
    header: str = "date",
    f: str = "%m/%d/%Y",
    missing_values: str = np.nan,
    ignore_missing: bool = True,
) -> list:
    """Returns a list of the dates under a column in a pandas dataframe in a uniform format (default is mm/dd/yyyy)

    df: DataFrame to use
    header: Name of column in dataframe to use
    f: Format to apply to the dates (using strftime's formating)
    missing_values:"""
    # Stores updated/normalized date values
    date_list = []

    # Alter the date values in new list
    for date in df[header]:
        if ignore_missing and date in [missing_values, np.nan]:
            date_list.append(date)
        # Parse date
        d = parser.parse(date)
        # Convert to new format and update date_list
        date_list.append(d.strftime(f))

    # Return Date Values
    return date_list


def fix_nan(df: pd.DataFrame, replace_with: Any = "?") -> pd.DataFrame:
    """Returns a copy of the df the all nan (empty) values in the dataframe being replaced with the given value

    df: DataFrame to use
    replace_with: Value(s) to replace nan with"""
    return df.fillna(value=replace_with)


def remove_sparse_rows(
        All columns being ignored results in the original being returned
        If weights are present, the value compared to minimum_ratio is sum_of_row / sum_of_weights.
        Use negative weights at your own risk (Don't).
    default_weight_value (optional): Default value for missing values in weighted_dict. Defaults to 0"""
    # ?TODO:?Add support for negative values?
    # No Dict
    if weighting_dict is None:
        # Get indices to remove
        indices = df[
            (
                1 - (df.isin([missing_values, np.nan]).sum(axis=1) / len(df.columns))
                < minimum_ratio
            )
        ].index
    # Dict Provided
    else:
        # Build weighting list from dict
        weighted_list = []
        for col in df.columns:
            if col in weighting_dict:
                weighted_list.append(weighting_dict[col])
            else:
                weighted_list.append(default_weighting)
        weight_sum = sum(weighted_list)

        # Check for div by 0
        if weight_sum == 0:
            # All Columns Ignored Return DF
            if all(x == 0 for x in weighted_list):
                return df
            # Despite the warnings, negative and positive weights used, just using num columns
            else:
                weight_sum = len(df.columns)

        # Return get indices to remove
        indices = df[
            (
                1
                - (
                    df.isin([missing_values, np.nan])
                    .multiply(
                        weighted_list, axis="columns", level=None, fill_value=None
                    )
                    .sum(axis=1)
                    / abs(weight_sum)
                )
                < minimum_ratio
            )
        ].index

    return df.drop(indices, inplace=False)


def typos(
    df: pd.DataFrame,
    header: str,
    correct_values: List[str],
    missing_values: str = np.nan,
    ignore_missing: bool = True,
) -> list:
    """Compares each value to the values in correct values and matches it to the nearest value using
    sequence comparison. Returns the altered column as a list. Ignores casing.

    df: DataFrame to use
    header: Name of column in dataframe to use
    correct_values: exhaustive list of strings with correct/valid entries
    missing_values: value used to denote a missing value
    ignore_missing: determines whether a guess should be performed on missing values or not
    """
    cleaned_list = []
    s = SequenceMatcher(None)
    for v in df[header]:
        # v is a correct value, no need to clean
        if v in correct_values:
            cleaned_list.append(v)
        # Check for missing value
        elif ignore_missing and v in [missing_values, np.nan]:
            cleaned_list.append(missing_values)
        # Not a correct value, attempt to find best match in given correctValues
        else:
            # Track best guess and it's ratio
            best_guess = ""
            best_guess_ratio = -0.1
            # Update Seq1
            s.set_seq1(v.lower())
            # Find best guess overall
            for guess in correct_values:
                # Update seq2
                s.set_seq2(guess.lower())
                # Find ratio and compare if its best guess yet
                ratio = s.ratio()
                if ratio > best_guess_ratio:
                    best_guess_ratio = ratio
                    best_guess = guess
            # Append to cleaned list
            cleaned_list.append(best_guess)

    # Return cleaned values
    return cleaned_list
