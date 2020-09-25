# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as patches

# show design 1

filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - data - design1.csv'
design1 = pd.read_csv(filename, sep =',')

plist = []
xlist = []
ylist = []
zlist = []

# create matrix of plant centres and radii
for index, row in design1.iterrows():

    plist.append(row['plant'])
    x = row['x-centre-first']
    y = row['y-centre-first']
    z = row['x-spacing']
    i = 1

    while i <= row['num-rows']:

        while x <= row['x-centre-last']:
            xlist.append(x)
            ylist.append(y)
            zlist.append(z)
            x += row['x-spacing']

        i +=1
        x = row['x-centre-first']
        y = row['y-centre-first'] + row['y-spacing']



# plot using scatterplot
fig, ax = plt.subplots(figsize=(11, 8.5))
fig.suptitle('Design 1 - 450 mm gap')
ax.set_xlim(xmax=6075, xmin=-75)
ax.set_ylim(ymax=3075, ymin=-75) #switch these round to invert the axis
ax.set_yticks(np.arange(0,3100,step=100))

ax.set_ylabel('x axis')
ax.set_xlabel('y axis')

ax.scatter(ylist, xlist, zlist, c = "green", linewidths= 6, alpha=0.5)
rect1 = patches.Rectangle((0,1200),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
ax.add_patch(rect1)
rect2 = patches.Rectangle((0,1800-75),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
ax.add_patch(rect2)
rect3 = patches.Rectangle((-75,-75),6150,3150,linewidth=25,edgecolor='brown',facecolor='none', alpha=0.5)
ax.add_patch(rect3)
fig.show()
fig.savefig("design1.png")



# show design 2

filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - data - design2.csv'
design2 = pd.read_csv(filename, sep =',')

plist = []
xlist = []
ylist = []
zlist = []

# create matrix of plant centres and radii
for index, row in design2.iterrows():

    plist.append(row['plant'])
    x = row['x-centre-first']
    y = row['y-centre-first']
    z = row['x-spacing']
    i = 1

    while i <= row['num-rows']:

        while x <= row['x-centre-last']:
            xlist.append(x)
            ylist.append(y)
            zlist.append(z)
            x += row['x-spacing']

        i +=1
        x = row['x-centre-first']
        y = row['y-centre-first'] + row['y-spacing']



# plot using scatterplot
fig, ax = plt.subplots(figsize=(11, 8.5))
fig.suptitle('Design 2 - 600 mm gap')
ax.set_xlim(xmax=6075, xmin=-75)
ax.set_ylim(ymax=3075, ymin=-75) #switch these round to invert the axis
ax.set_yticks(np.arange(0,3100,step=100))

ax.set_ylabel('x axis')
ax.set_xlabel('y axis')


# use the scatter function

ax.scatter(ylist, xlist, zlist, c = "green", linewidths= 6, alpha=0.5)
rect1 = patches.Rectangle((0,1200-75),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
ax.add_patch(rect1)
rect2 = patches.Rectangle((0,1800),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
ax.add_patch(rect2)
rect3 = patches.Rectangle((-75,-75),6150,3150,linewidth=25,edgecolor='brown',facecolor='none', alpha=0.5)
ax.add_patch(rect3)
fig.show()
fig.savefig("design2.png")
