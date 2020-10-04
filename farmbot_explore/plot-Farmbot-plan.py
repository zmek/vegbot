# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Circle, Rectangle

# set params
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




def make_chart(design, file_label, title, gap_min, gap_max):

    plist = []
    xlist = []
    ylist = []
    zlist = []

    # create lists of plant centres and radii
    for index, row in design.iterrows():

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

            i += 1
            x = row['x-centre-first']
            y = y + row['y-spacing']



    # initialise plot
    fig = plt.figure(figsize=(11, 7.5))
    ax = fig.add_subplot(aspect = 'equal')
    fig.suptitle(title)
    ax.set_xlim(xmax=6075, xmin=-75)
    ax.set_ylim(ymax=3075, ymin=-75) #switch these round to invert the axis
    ax.set_yticks(np.arange(0,3100,step=200))

    ax.set_ylabel('Farmbot\'s x axis')
    ax.set_xlabel('Farmbot\'s y axis')

    # draw empty bed
    rect1 = Rectangle((0,gap_min),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
    ax.add_patch(rect1)
    rect2 = Rectangle((0,gap_max),6000,75,linewidth=1,edgecolor='brown',facecolor='brown', alpha=0.5)
    ax.add_patch(rect2)
    rect3 = Rectangle((-75,-75),6150,3150,linewidth=25,edgecolor='brown',facecolor='none', alpha=0.5)
    ax.add_patch(rect3)
    ax.text(20, 3000, 'Short plants')
    ax.text(20, -75, 'Tall plants')

    # add plants
    i = 0
    while i < len(ylist):
        dot = Circle((ylist[i], xlist[i]), 15, facecolor='green', edgecolor='green',
                        linewidth=1)
        ax.add_patch(dot)
        circle = Circle((ylist[i], xlist[i]), zlist[i]/2, facecolor='none', edgecolor='green',
                        linewidth=1, alpha=0.5)
        ax.add_patch(circle)
        i +=1

    # add names
    for index, row in design.iterrows():

        i = 1
        x = row['y-centre-first']
        while i <= row['num-rows']:
            if row['x-centre-first'] < 1500:
                y = gap_min/2
            else:
                y = 3000-(gap_max/2)
            ax.text(x+20, y, row['plant'], rotation = 90, fontsize = TINY_SIZE,
                    horizontalalignment='center', verticalalignment='center')
            x = x + row['y-spacing']
            i += 1

    fig.show()
    fig.savefig(file_label+".png")


# load data

filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - data - design1.csv'
design1 = pd.read_csv(filename, sep =',')

filename = '/Users/zellaking/GitHubRepos/vegbot/farmbot_explore/Farmbot bed plan - data - design2.csv'
design2 = pd.read_csv(filename, sep =',')

# make charts
make_chart(design1, "design1", 'Design 1 - 450 mm gap', 1200, 1800-75)
make_chart(design2, "design2", 'Design 2 - 600 mm gap', 1200-75, 1800)
