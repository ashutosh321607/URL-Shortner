import requests

BASE = "http://10.2.73.238:5000"
API_KEY = "zhgjuc7aw2CSbXZkr1yK2s0AOJEdehrU"
# API_KEY = "rvfvW8OyXnsWqTi1ATMcxEJuCFno6ZRZ"

# response = requests.post(BASE + "/api/register", {
#                          "email": "ashutoshgarg@gmail.com", "full_name": "Ashutosh Garg", "password": "ashutosh"})

# response = requests.post(BASE + "/api/login", {
#                           "email": "ashutoshgarg@gmail.com", "password": "ashutosh"})

response = requests.post(BASE + "/api/shorten", {'api_key': API_KEY,
                        'long_url': "https://google.com", 'time_period': 300})
print(response.json())
