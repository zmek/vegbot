import requests
import json

response = requests.request(
    method='POST',
    url='https://my.farm.bot/api/tokens',
    headers={'content-type': 'application/json'},
    json={'user': {'email': 'zella.king@gmail.com', 'password': 'TiefymBVLY8qSEH'}})
TOKEN = response.json()['token']['encoded']

headers = {'Authorization': 'Bearer ' + response.json()['token']['encoded'],
           'content-type': "application/json"}

# get existing points
r = requests.get('https://my.farm.bot/api/points',  headers = headers)

#then to interrogate what comes back:
points = r.json()

# save current data
with open('/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/points.json', 'w') as f:
    json.dump(points, f)

points['id']

# loop to delete existing plants
r = requests.get('https://my.farm.bot/api/points',  headers = headers)
existing_plants = r.json()
for i in range(0,len(existing_plants)):
    id = existing_plants[i]['id']
    r = requests.delete('https://my.farm.bot/api/points/'+str(id), headers=headers)
    print(r)

with open('/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/plantdict.json', 'r') as f:
    plants=f.read()
f.close()

new_plants = json.loads(plants)
for key, values in new_plants.items():
    new_plants[key]['index'] = None

# add plants
for key, values in new_plants.items():
    params = new_plants[key] # remove the index for now
    r = requests.post('https://my.farm.bot/api/points/', headers=headers, json = params)
    print(r)


params = {
    "x": 200,
    "y": 1987.5,
    "name": "rocket",
    "pointer_type": "Plant",
    "plant_stage": "planned",
    "radius": 125
}

r = requests.post('https://my.farm.bot/api/points/', headers = headers, json=params)