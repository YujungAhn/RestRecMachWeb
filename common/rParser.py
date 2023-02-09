import pandas as pd

# 다양한 json to DataFrame 변형 방법
# https://sparkbyexamples.com/pandas/pandas-convert-json-to-dataframe/

def convertJsonToDataframe(jsonData, jsonName):
    # df2 = pd.read_json(jsonData.body, orient='items')
    df2 = pd.json_normalize(jsonData[jsonName])
    print(df2)
