import pandas as pd

# 다양한 json to DataFrame 변형 방법
# https://sparkbyexamples.com/pandas/pandas-convert-json-to-dataframe/

def convertJsonToDataframe(jsonData, jsonName):
    df = pd.json_normalize(jsonData[jsonName])
    return df
