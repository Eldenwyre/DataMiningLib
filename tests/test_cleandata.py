import pytest
import pandas as pd
from datamining import cleandata


#Num entries per column
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
df_copy: pd.DataFrame = pd.DataFrame(data = data)

def test_dates():
    #Value testing
    assert list(cleandata.dates(df, "dates", f="%m/%d/%Y")) == ["01/17/2000"] * DATA_LENGTH
    assert list(cleandata.dates(df, "dates", f="%m/%Y")) == ["01/2000"] * DATA_LENGTH
    assert list(cleandata.dates(df, "dates", f="HAHA")) == ["HAHA"] * DATA_LENGTH
    #Ensure original is unchanged
    assert df.equals(df_copy)

def test_typos():
    #Value Testing
    assert list(cleandata.typos(df, 'typos',['yes','no'],missing_values='?',ignore_missing=True)) == ['yes','yes','yes','yes','?','no','no','no','no','?']
    assert list(cleandata.typos(df, 'typos',['Y','N'],missing_values='?',ignore_missing=True)) == ['Y','Y','Y','Y','?','N','N','N','N','?']
    #Make sure if missing values aren't ignored, they are replaced
    with pytest.raises(ValueError):
        list(cleandata.typos(df, 'typos',["yes","no"], missing_values='?',ignore_missing=False)).index('?')
    #Ensure original is unchanged
    assert df.equals(df_copy)