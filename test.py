import json

import pandas as pd

# with open('a.json') as json_file:
#     jsonData = json.load(json_file)
#     data = pd.DataFrame()
#     a = []
#
#
#     for x in jsonData['historical']:
#         a.append(x['close'])
#
#
#     data['AAPL'] = a
#
#
#     print(data)

with open('gsc.json') as json_file:
    jsonData = json.load(json_file)
    data = pd.DataFrame()
    a = []


    for x in jsonData['historical']:
        a.append(x['close'])


    data['GSC'] = a


    print(data)