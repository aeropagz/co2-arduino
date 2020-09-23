import requests
import os

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "helloworld")
#print(response.json())
path = os.path.dirname(__file__)
print(path)