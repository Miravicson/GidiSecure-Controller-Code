import requests
import sys


api_url = 'http://gidisecure.herokuapp.com/readings/'
local_url = 'http://127.0.0.1:8000/readings/'

data = {

    "gas_sensor": '1',
    "vibration_sensor": "0",
    "time_stamp": "10:23:04",
    "date_stamp": "10/12/2004",
}


resp = requests.post(api_url, data)
# resp = requests.post(local_url, data)
print(resp)

