import requests
import json

# URL
url = 'http://localhost:1234/api'

# Open Local Validation Data JSON type
with open('validation.json') as json_file:
    data = json.load(json_file)

r = requests.post(url,json=data)

print(r.json())