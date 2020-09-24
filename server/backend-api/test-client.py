import requests
import random

BASE = "http://127.0.0.1:5000/co2/Raum2"

def randomData():
    hours = random.randint(0,23)
    min = random.randint(0,59)
    time = str(hours)+":"+str(min)
    value = random.randint(0, 1800)
    return {"time": time, "value": value}


response = requests.post(BASE, data=randomData())
print(response)
