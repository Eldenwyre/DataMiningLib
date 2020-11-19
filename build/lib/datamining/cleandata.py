import pandas as pd
from dateutil import parser
from difflib import SequenceMatcher, get_close_matches
from typing import Any, List


def dates(
    df: pd.DataFrame,
    header: str = "date",
    f: str = "%m/%d/%Y",
    missing_values: str = "?",
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
        if ignore_missing and date == missing_values:
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


def typos(
    df: pd.DataFrame,
    header: str,
    correct_values: List[str],
    missing_values: str = "?",
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
        elif ignore_missing and v == missing_values:
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
