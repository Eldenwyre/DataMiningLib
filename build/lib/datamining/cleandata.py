import pandas as pd 
from dateutil import parser
from typing import Any
def dates(df: pd.DataFrame, header: str ="date", f: str ="%m/%d/%Y") -> None:
    '''Updates all dates under the given header, header(str), 
    in the given dataframe, df(pd.DataFrame), 
    into the given format, f(str), (must be dateutil compatible).'''
    #Stores updated/normalized date values
    date_list=[]

    #Alter the date values in new list
    for date in df[header]:
        #Parse date
        d = (parser.parse(date))
        #Convert to new format and update date_list
        date_list.append(d.strftime(f))
        
    #Update Date Values
    df[header]=date_list

    return

def yes_no(df: pd.DataFrame, header: str, positive: Any, negative: Any, unknown: Any = "?"):
    pass