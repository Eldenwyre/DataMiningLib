import numpy as np

# Num entries per column
DATA_LENGTH = 10

# Data for tests in datamining lib
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
    "nan1": [0, 1, 2, np.nan, 4, np.nan, np.nan, 7, 8, np.nan],
    "nan2": [np.nan, 1, np.nan, 3, 4, 5, 6, np.nan, 8, 9],
}
