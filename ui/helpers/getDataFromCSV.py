# input: string file path to url for a csv
# output: pandas dataframe

import requests
import pandas as pd
from io import StringIO

def getDataFromCSV(fileURL):
    try:
        response = requests.get(fileURL)
        response.raise_for_status()  
        df = pd.read_csv(StringIO(response.text), sep=',')
        return df  
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data: {e}")
        return None  
