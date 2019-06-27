import requests
import json
resp = requests.get('https://www.google.pl/search?source=hp&ei=s-AQXeD7H8-JrwTsmpaYBw&q=samoot')
data_r = json.loads(resp.content)
print(data_r)
