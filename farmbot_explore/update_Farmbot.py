import requests
import json
from datetime import datetime

response = requests.request(
    method='POST',
    url='https://my.farm.bot/api/tokens',
    headers={'content-type': 'application/json'},
    json={'user': {'email': 'zella.king@gmail.com', 'password': 'dU2WLuGBe27NkMZ'}})
TOKEN = response.json()['token']['encoded']

headers = {'Authorization': 'Bearer ' + response.json()['token']['encoded'],
           'content-type': "application/json"}

# get existing points
r = requests.get('https://my.farm.bot/api/points',  headers = headers)
existing_plants = r.json()

file = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/points_' + datetime.today().strftime('%Y-%m-%d %H:%M')
# save current data
with open(file, 'w') as f:
    json.dump(existing_plants, f)

points['id']

# add plants
filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - plants_to_add.csv'
coords = pd.read_csv(filename, sep =',')

# create plant dictionary
plantdict = dict()
plant_counter = dict()

for index, row in coords.iterrows():

    # create index for plant number
    if row['plant'] in plant_counter:
        plant_counter[row['plant']]+=1
    else:
        plant_counter[row['plant']]=1

    innerdict = {}

    innerdict['name'] = row['plant'] # changed innerdict['plant'] to 'innerdict['name']
    innerdict['radius'] = row['spacing_y']/2
    innerdict['pointer_type'] = 'Plant'
    innerdict['x'] = row['start_x']
    innerdict['y'] = row['start_y']

    plantdict[row['plant'] + str(plant_counter[row['plant']])] = innerdict


# write plantDict to json
file = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/plants_to_add_' + datetime.today().strftime('%Y-%m-%d')
with open(file, 'w') as f:
    json.dump(plantdict, f)
f.close()

with open(file, 'r') as f:
    plants=f.read()
f.close()

new_plants = json.loads(plants)
#for key, values in new_plants.items():
#    new_plants[key]['index'] = None

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