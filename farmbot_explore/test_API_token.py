import requests
response = requests.request(
    method='POST',
    url='https://my.farm.bot/api/tokens',
    headers={'content-type': 'application/json'},
    json={'user': {'email': 'zella.king@gmail.com', 'password': 'TiefymBVLY8qSEH'}})
TOKEN = response.json()['token']['encoded']

# this gets a 422 error = the server understands the content type and the syntax is correct
# but it is unable to process to contained instructions
r = requests.post('https://my.farm.bot/api/points/', params=
     {
        "id": "",
        "created_at": "2020-10-17T15:55:10.449Z",
        "updated_at": "2020-10-17T15:55:10.449Z",
        "device_id": 7928,
        "name": "Butternut Squash",
        "pointer_type": "Plant",
        "meta": {
            "gridId": "1db26ad2-eb60-4cfe-9c84-3f1ebcadd1bf"
        },
        "x": 5000,
        "y": 1000,
        "z": 0,
        "openfarm_slug": "butternut-squash",
        "plant_stage": "planted",
        "planted_at": "2020-10-17T15:55:10.449Z",
        "radius": 25.0
    }
                  )


r = requests.post('https://my.farm.bot/api/points/', params=
     {
        "name": "Butternut Squash",
        "pointer_type": "Plant",
        "x": 5555,
        "y": 1555,
        "z": 0,
        "openfarm_slug": "butternut-squash",
        "plant_stage": "planted",
         "planted_at": "\"2020-10-08T16:08:00.825+00:00\"",
         "radius": 25.0
    }
                  )

# trying a put
r = requests.put('https://my.farm.bot/api/device/325',  data = {
  "name": "Carrot Overlord"
})



# from https://software.farm.bot/v4/Additional-Information/farmware-dev.html
headers = {'Authorization': 'Bearer ' + response.json()['token']['encoded'],
           'content-type': "application/json"}


# trying a get - this got a 200 = success
r = requests.get('https://my.farm.bot/api/points',  headers = headers)

#then to interrogate what comes back:
points = r.json()


with open('/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/points.json', 'w') as f:
    json.dump(points, f)

points['id']

params = {
	'device_id': 7928,
	"x": 23,
	"y": 45,
	"name": "Salad",
	"pointer_type": "Plant",
	"openfarm_slug": "mung-bean",
	"planted_at": "\"2020-10-08T16:08:00.825+00:00\"",
	"plant_stage": "sprouted"
}


weed = {
  "x": 23,
  "y": 45,
  "pointer_type": "Weed"
}

r = requests.post('https://my.farm.bot/api/points/', headers = headers, json=weed)




# delete a weed
DELETE /api/points/332787
r = requests.delete('https://my.farm.bot/api/points/332787', headers = headers)
r = requests.get('https://my.farm.bot/api/points',  headers = headers)

#then to interrogate what comes back:
len(r.json())
points = r.json()

# loop to delete existing plants
for i in range(0,len(points)):
    id = points[i-1]['id']
    r = requests.delete('https://my.farm.bot/api/points'+id, headers=headers)

# trying a put
r = requests.put('https://my.farm.bot/api/device/325',  data = {
  "name": "Carrot Overlord"
})


bad_r = requests.get('https://httpbin.org/status/422')
bad_r.status_code

bad_r.raise_for_status()


from requests.auth import HTTPBasicAuth