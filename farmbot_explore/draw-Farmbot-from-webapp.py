# Set up access to Google sheet
# following the advice here:
# https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle
import copy
import pickle
import requests
import json
from datetime import datetime

# set params for plot
TINY_SIZE = 6
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=MEDIUM_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

FARMBOT_MARGIN = 70 # added to brick width to allow for Farmbot's margin
BRICK_WIDTH = 75 + FARMBOT_MARGIN


# bed outer dimensions
WHOLE_BED_Y = 2860 + 150 # external dimension as measured on 22.11.20
WHOLE_BED_X = 5870 + 150 # external dimension as measured on 22.11.20

NARROW_FRONT_Y = 1200 # external dimension
NARROW_BACK_Y = 1208 # external dimension
PATH_Y = WHOLE_BED_Y - NARROW_FRONT_Y - NARROW_BACK_Y # external dimension
PATH_LENGTH = 4588 # external dimension ie from outermost edge of bed on RHS to inside the wall on LHS

LENGTH_Y = 2734  # Farmbot axis as measured by Farmbot on 4.11.21
LENGTH_X = 5473  # Farmbot axis as measured by Farmbot on 4.11.21

SPLIT_Y_AT = LENGTH_Y / 2



wooddict = {
    "wallF": {
        "xy": (-BRICK_WIDTH, -BRICK_WIDTH), "width": WHOLE_BED_X , "height": BRICK_WIDTH
    },
    "wallB": {
        "xy": (-BRICK_WIDTH, WHOLE_BED_Y - 2 * BRICK_WIDTH), "width": WHOLE_BED_X, "height": BRICK_WIDTH
    },
    "wallL": {
        "xy": (-BRICK_WIDTH, -BRICK_WIDTH), "width": BRICK_WIDTH, "height": WHOLE_BED_Y
    },
    "wallRF": {
        "xy": (WHOLE_BED_X - 2 * BRICK_WIDTH, -BRICK_WIDTH),
        "width": BRICK_WIDTH,
        "height": NARROW_FRONT_Y
    },
    "wallRB": {
        "xy": (WHOLE_BED_X - 2 * BRICK_WIDTH, WHOLE_BED_Y - NARROW_BACK_Y - BRICK_WIDTH),
        "width": BRICK_WIDTH,
        "height": NARROW_BACK_Y
    },
    "wallPathF": {
        "xy": (WHOLE_BED_X - PATH_LENGTH - BRICK_WIDTH, NARROW_FRONT_Y - 2 * BRICK_WIDTH),
        "width": PATH_LENGTH,
        "height": BRICK_WIDTH
    },
    "wallPathB": {
        "xy": (WHOLE_BED_X - PATH_LENGTH - BRICK_WIDTH, WHOLE_BED_Y - NARROW_BACK_Y - BRICK_WIDTH),
        "width": PATH_LENGTH,
        "height": BRICK_WIDTH
    },
    "wallPathL": {
        "xy": (WHOLE_BED_X - PATH_LENGTH - BRICK_WIDTH, NARROW_FRONT_Y - 2 * BRICK_WIDTH),
        "width": BRICK_WIDTH,
        "height": PATH_Y + 2 * BRICK_WIDTH
    },
}

strutdict = {
    "front1": { # 1420 was measured from the external dimension of the bed hence subtract brick width
        "xy": (1420 - FARMBOT_MARGIN, 0),
        "width": 3,
        "height": NARROW_FRONT_Y - 2 * BRICK_WIDTH
    },
    "front2": {
        "xy": (2910 - FARMBOT_MARGIN, 0),
        "width": 3,
        "height": NARROW_FRONT_Y  - 2 * BRICK_WIDTH
    },
    "front3": {
        "xy": (4420 - FARMBOT_MARGIN, 0),
        "width": 3,
        "height": NARROW_FRONT_Y  - 2 * BRICK_WIDTH
    },
    "back1": {
        "xy": (1420 - FARMBOT_MARGIN, WHOLE_BED_Y - NARROW_BACK_Y),
        "width": 3,
        "height": NARROW_BACK_Y  - 2 * BRICK_WIDTH
    },
    "back2": {
        "xy": (2910 - FARMBOT_MARGIN, WHOLE_BED_Y - NARROW_BACK_Y),
        "width": 3,
        "height": NARROW_BACK_Y  - 2 * BRICK_WIDTH
    },
    "back3": {
        "xy": (4420 - FARMBOT_MARGIN, WHOLE_BED_Y - NARROW_BACK_Y),
        "width": 3,
        "height": NARROW_BACK_Y  - 2 * BRICK_WIDTH
    },
    "fat" : {
        "xy": (0, 1410 + BRICK_WIDTH),
        "width": WHOLE_BED_X - PATH_LENGTH - BRICK_WIDTH,
        "height": 3
    }
}


# read data

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

plantdict = dict()
plant_counter = dict()

for i in range(0,len(existing_plants)):
    if existing_plants[i]['pointer_type'] == 'Plant':

        innerdict = {}
        innerdict['name'] = existing_plants[i]['name']
        innerdict['radius'] = existing_plants[i]['radius']
        innerdict['x'] = existing_plants[i]['x']
        innerdict['y'] = existing_plants[i]['y']

        # create index for plant number
        if existing_plants[i]['name'] in plant_counter:
            plant_counter[existing_plants[i]['name']] +=1
        else:
            plant_counter[existing_plants[i]['name']] =1

        # concatenate plant name with number
        plantdict[existing_plants[i]['name'] + str(plant_counter[existing_plants[i]['name']])] = innerdict

# initialise plot
fig = plt.figure(figsize=(11, 7.5), dpi=300)
ax = fig.add_subplot(aspect = 'equal')
fig.suptitle('Current Farmbot plants: ' + datetime.today().strftime('%Y-%m-%d'))
ax.set_xlim(xmax= WHOLE_BED_X, xmin=-BRICK_WIDTH)
ax.set_ylim(ymax= WHOLE_BED_Y, ymin=-200)
ax.set_yticks(np.arange(-200, WHOLE_BED_Y, step=200))

ax.set_ylabel('Farmbot\'s y axis')
ax.set_xlabel('Farmbot\'s x axis')

# Show the minor grid lines with very faint and almost transparent grey lines
ax.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.2)

# draw bed structure
for key, values in wooddict.items():
    rect = Rectangle(wooddict[key]['xy'], wooddict[key]['width'], wooddict[key]['height'],
                     linewidth=1, edgecolor='brown', facecolor='brown', alpha=0.5)
    ax.add_patch(rect)


# draw struts
for key, values in strutdict.items():
    rect = Rectangle(strutdict[key]['xy'], strutdict[key]['width'], strutdict[key]['height'],
                     linewidth=1, edgecolor='grey', facecolor='grey', alpha=0.5)
    ax.add_patch(rect)
# add plants to plot
# useful stuff on text annotation here: https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html

for key, values in plantdict.items():
    dot = Circle((plantdict[key]['x'], plantdict[key]['y']), 15, facecolor='green', edgecolor='green',
                    linewidth=1)
    ax.add_patch(dot)
    circle = Circle((plantdict[key]['x'], plantdict[key]['y']), plantdict[key]['radius'], facecolor='none', edgecolor='green',
                    linewidth=1, alpha=0.5)
    ax.add_patch(circle)

fig.show()
fig.savefig("veg_plan6.pdf")






# save dictionary
filename = "plantDict"
fw = open(filename, 'wb')
pickle.dump(plantdict, fw)
fw.close()

