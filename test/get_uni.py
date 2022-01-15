import requests
import json

url = "http://universities.hipolabs.com/search"
PARAMS = {"alpha_two_code": "pe"}

r = requests.get(url, params=PARAMS)
data = r.json()

print(json.dumps(data, indent = 2))
print(len(data))