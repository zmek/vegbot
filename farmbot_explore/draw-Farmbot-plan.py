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
import json

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

BRICK_WIDTH = 75
PATH_WIDTH = 600
PATH_LENGTH = 4500
SPLIT_Y_AT = 3000 - 1200
NARROW_BIT_WIDTH = (3000 - PATH_WIDTH)/2

LETTERS = [chr(i) for i in range(ord('a'), ord('z') + 1)]


# bed dictionary
beddict = {
    "frontL": {
        "xmin": BRICK_WIDTH,
        "xmax": 6000 - PATH_LENGTH,
        "ymin": SPLIT_Y_AT,
        "ymax": 3000 - BRICK_WIDTH,
    },
    "frontR": {
        "xmin": 6000 - PATH_LENGTH,
        "xmax": 6000 - BRICK_WIDTH,
        "ymin": 3000 - NARROW_BIT_WIDTH + BRICK_WIDTH,
        "ymax": 3000 - BRICK_WIDTH
    },
    "backL": {
        "xmin": BRICK_WIDTH,
        "xmax": 6000-PATH_LENGTH,
        "ymin": BRICK_WIDTH,
        "ymax": SPLIT_Y_AT
    },
    "backR": {
        "xmin": 6000 - PATH_LENGTH,
        "xmax": 6000 - BRICK_WIDTH,
        "ymin": BRICK_WIDTH,
        "ymax": NARROW_BIT_WIDTH - BRICK_WIDTH

    },
    "wholeL": {
        "xmin": BRICK_WIDTH,
        "xmax": 6000 - PATH_LENGTH,
        "ymin": BRICK_WIDTH,
        "ymax": 3000 - BRICK_WIDTH,

    },
}

wooddict = {
    "wallB": {
        "xy": (0, 0), "width": 6000, "height": BRICK_WIDTH
    },
    "wallF": {
        "xy": (0, 3000-BRICK_WIDTH), "width": 6000, "height": BRICK_WIDTH
    },
    "wallL": {
        "xy": (0, 0), "width": BRICK_WIDTH, "height": 3000
    },
    "wallR1": {
        "xy": (6000 - BRICK_WIDTH, 0), "width": BRICK_WIDTH, "height": NARROW_BIT_WIDTH
    },
    "wallR2": {
        "xy": (6000 - BRICK_WIDTH, 3000 - NARROW_BIT_WIDTH),
        "width": BRICK_WIDTH,
        "height": NARROW_BIT_WIDTH
    },
    "wallPathB": {
        "xy": (6000 - PATH_LENGTH, NARROW_BIT_WIDTH-BRICK_WIDTH),
        "width": PATH_LENGTH,
        "height": BRICK_WIDTH
    },
    "wallPathF": {
        "xy": (6000 - PATH_LENGTH, 3000-(NARROW_BIT_WIDTH)),
        "width": PATH_LENGTH,
        "height": BRICK_WIDTH}
    ,
    "wallPathL": {
        "xy": (6000 - PATH_LENGTH, NARROW_BIT_WIDTH-BRICK_WIDTH),
        "width": BRICK_WIDTH,
        "height": PATH_WIDTH+2*BRICK_WIDTH
    },
}


# set bed order
bed_order = ["frontL", "frontR", "backL", "backR"]

# arrange plants
filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - data - plants.csv'
plants = pd.read_csv(filename, sep =',')

plants['spacing_y'] = plants['spacing_within']*10
plants['spacing_x'] = plants['spacing_between']*10
plants['tallplant'] = plants['height']>40
plants = plants.sort_values(by=['height'])

plants.reset_index(level=0, inplace=True)
plants = plants.sort_values(by=['tallplant','spacing_x'])

# create plant dictionary
plantdict = dict()
i = 0
current_row = 1
x_start = beddict[bed_order[i]]["xmin"]

for index, row in plants.iterrows():
    num = 1
    innerdict = {}

    innerdict['name'] = row['plant'] # changed innerdict['plant'] to 'innerdict['name']
    innerdict['index'] = str(row['index']+1)
    innerdict['radius'] = row['spacing_y']/2
    innerdict['pointer_type'] = 'Plant'

    # prepare y dimension
    y_span = beddict[bed_order[i]]["ymax"] - beddict[bed_order[i]]["ymin"]
    num_in_row = y_span//row['spacing_y'] # quotient
    y_margin = (y_span - (num_in_row * row['spacing_y']))/2

    # prepare x dimension
    x_margin = row['spacing_x']/2
    if x_start + row['spacing_x'] > beddict[bed_order[i]]["xmax"]:
        i +=1
        y_span = beddict[bed_order[i]]["ymax"] - beddict[bed_order[i]]["ymin"]
        x_start = beddict[bed_order[i]]["xmin"]

    while current_row <= row['num_rows']:

        # first plant in row
        innerdict['x'] = x_start + x_margin
        innerdict['y'] = beddict[bed_order[i]]["ymin"] + y_margin + row['spacing_y']/2

        while innerdict['y'] < beddict[bed_order[i]]["ymin"] + y_span:
            # write plant details
            plantdict[row['plant'] + str(num)] = innerdict

            # increment
            innerdict = copy.deepcopy(innerdict)
            innerdict['y'] += row['spacing_y']
            num += 1

        current_row +=1
        x_start += row['spacing_x']

        if x_start + row['spacing_x'] > beddict[bed_order[i]]["xmax"]:

            if  bed_order[i] == 'frontL':
                # include any unused x dimension to frontR
                beddict['frontR']["xmin"] = beddict['frontR']["xmin"] - (beddict[bed_order[i]]["xmax"]-x_start)
            if  bed_order[i] == 'backL':
                # include any unused x dimension to backR
                beddict['backR']["xmin"] = beddict['backR']["xmin"] - (beddict[bed_order[i]]["xmax"]-x_start)
            i += 1
            y_span = beddict[bed_order[i]]["ymax"] - beddict[bed_order[i]]["ymin"]
            x_start = beddict[bed_order[i]]["xmin"]

    current_row = 1

# write plantDict to json
#j = json.dumps(plantdict, indent=4)

with open('/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/plantdict.json', 'w') as f:
    json.dump(plantdict, f)
f.close()


# initialise plot
fig = plt.figure(figsize=(11, 7.5), dpi=300)
ax = fig.add_subplot(aspect = 'equal')
fig.suptitle('Proposed Farmbot layout')
ax.set_xlim(xmax=6000, xmin=0)
ax.set_ylim(ymax=0, ymin=3000) #switch these round to invert the axis
ax.set_yticks(np.arange(0,3000,step=200))

ax.set_ylabel('Farmbot\'s y axis')
ax.set_xlabel('Farmbot\'s x axis')

# Show the minor grid lines with very faint and almost transparent grey lines
ax.grid(b=True, which='major', color='#999999', linestyle='-', alpha=0.2)

# draw bed structure
for key, values in wooddict.items():
    rect = Rectangle(wooddict[key]['xy'], wooddict[key]['width'], wooddict[key]['height'],
                     linewidth=1, edgecolor='brown', facecolor='brown', alpha=0.5)
    ax.add_patch(rect)

# show beds
#for key, values in beddict.items():
#    rect = Rectangle((beddict[key]['xmin'], beddict[key]['ymin']),
#                    beddict[key]["xmax"] - beddict[key]["xmin"],
#                     beddict[key]["ymax"] - beddict[key]["ymin"],
#                     linewidth=1, edgecolor='brown', facecolor='green', alpha=0.5)
#    ax.add_patch(rect)
#    ax.text(beddict[key]['xmin'], beddict[key]['ymin'], key)

#fig.show()

# add plants to plot
# useful stuff on text annotation here: https://jakevdp.github.io/PythonDataScienceHandbook/04.09-text-and-annotation.html

for key, values in plantdict.items():
#    dot = Circle((plantdict[key]['x'], plantdict[key]['y']), 15, facecolor='green', edgecolor='green',
#                    linewidth=1)
#    ax.add_patch(dot)
    circle = Circle((plantdict[key]['x'], plantdict[key]['y']), plantdict[key]['radius'], facecolor='none', edgecolor='green',
                    linewidth=1, alpha=0.5)
    ax.add_patch(circle)
    if plantdict[key]['radius'] > 50:
        ax.text(plantdict[key]['x']-25, plantdict[key]['y']+25, plantdict[key]['index'], fontsize=TINY_SIZE)
    else:
        if key[-1]=='1' and (key[-2] in LETTERS or key[-2] == ' '):
            ax.text(plantdict[key]['x'] + 50, plantdict[key]['y'] + 500, plantdict[key]['index'], fontsize=TINY_SIZE)

fig.show()
fig.savefig("veg_plan3.pdf")

# attempts at adding a key
plt.subplots_adjust(top=500)

# with a subtitle
subtitle_string = ""
for index, row in plants.sort_values(by=['index']).iterrows():
    subtitle_string = subtitle_string + str(row['index']+1) + ":"
    subtitle_string = subtitle_string + str(row['plant']) + " "
ax.text(0, -250, subtitle_string, fontsize=SMALL_SIZE, wrap = True)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)


# with a table
# https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4
table1 = np.array(plants.sort_values(by=['index']).loc[:,['index','plant']])
table1[:,0] +=1 # add one to the index

ax.table(cellText = table1, rowLoc= 'top')

# error handling
try:
    y_span = beddict[bed_order[i]]["ymax"] - beddict[bed_order[i]]["ymin"]
except IndexError:
    print("Finished before end of file")
    exit()






# save dictionary
filename = "plantDict"
fw = open(filename, 'wb')
pickle.dump(plantdict, fw)
fw.close()

