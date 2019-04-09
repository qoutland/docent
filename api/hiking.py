import requests, json

data = requests.get('https://www.hikingproject.com/data/get-trails?lat=39.5296&lon=-119.8138&maxResults=50&key=200446744-75b255e6be35c19e68574645f0e16570').json()
with open('hikes.json', 'w') as f:
    json.dump(data, f)