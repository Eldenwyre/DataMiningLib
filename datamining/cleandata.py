import pandas as pd 
from dateutil import parser
from difflib import SequenceMatcher
from typing import Any, List

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

def typos(df: pd.DataFrame, header: str, correctValues: List[str]) -> None:
    '''Compares each value to the values in correct values and matches it to the nearest value using 
    sequence comparison. Alters the dataframe, df, column, header, to have only values within correctValues'''
    cleaned_list = []

    for v in df[header]:
        #v is a correct value, no need to clean
        if v in correctValues:
            cleaned_list.append(v)
        #Not a correct value, attempt to find best match in given correctValues
        else:
            #Track best guess and it's ratio
            best_guess = ""
            best_guess_ratio = -0.1
            #Find best guess overall
            for guess in correctValues:
                ratio = SequenceMatcher(None, v, guess).ratio()
                if ratio > best_guess_ratio:
                    best_guess_ratio = ratio
                    best_guess = guess
            #Append to cleaned list
            cleaned_list.append(best_guess)

    #Apply changes
    df[header] = cleaned_list

    return