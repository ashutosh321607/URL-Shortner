import requests
from utils import *

BASE = "http://10.3.44.192:5000"
API_KEY = "lZOoW2laje2JQ04gwQeaV6ET4dqFn70X"
# API_KEY = "rvfvW8OyXnsWqTi1ATMcxEJuCFno6ZRZ"

# response = requests.post(BASE + "/api/register", {
#                          "email": "gorocal651@icesilo.com", "full_name": "Ashutosh Garg", "password": "ashutosh"})
# print(response.json())

# response = requests.post(BASE + "/api/verify", {"email": "gorocal651@icesilo.com", "otp": '635371'})
# response = requests.post(BASE + "/api/login", {
#                           "email": "gorocal651@icesilo.com", "password": "ashutosh"})

# response = requests.post(BASE + "/api/shorten", {'api_key': API_KEY,
#                         'long_url': "https://google.com", 'time_period': 300})
print(response.json())
