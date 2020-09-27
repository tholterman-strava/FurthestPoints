import csv
from scipy.spatial.distance import pdist
import numpy as np
import matplotlib.pyplot as plt

import math

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))


with open('concap.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    # This list ends up being the coordinates furthest from each other
    max_coords = []
    # This ends up being the max area made up by max_coords
    current_area = 0
    all_points = []
    capital_info = []

    for row in csv_reader:
        #Skip the title line
        if line_count == 0:
            line_count += 1
            continue
        # Just some parsing for the capital CSV File
        capital_name = str(row[0] +  ", " + row[1])
        #After that, I wanted to start the row at the latitude
        row = row[2:]
        # Adding the first 4 points to be the initial max distanced coords
        if line_count < 5 :
            latitude = float(row[0])
            longitude = float(row[1])
            coord = (latitude, longitude)
            max_coords.append(coord)
            #Capital_info just tracks the capital names alongside the max_coords
            capital_info.append(capital_name)
            line_count += 1
            #All points is just cool for plotting
            all_points.append(coord)
            continue

        #To use PolyArea we need a list of latitudes and a list of longitudes
        # So these are basically just the current furthest latitudes, and
        # current furthest longitudes
        rolling_lats = map(lambda coord: coord[0], max_coords)
        rolling_longs = map(lambda coord: coord[1], max_coords)

        #Before we do any adjustments we need to know what area the current
        # max_coords make for.
        current_area = PolyArea(rolling_longs, rolling_lats)
        # Next_areas is going to hold the 4 different areas we get by substituting
        # in the next_coordinate in different spots of max_coords
        next_areas = []
        # Extract the next coordinate we're looking at
        next_coord = (float(row[0]), float(row[1]))
        all_points.append(next_coord)

        # Go through each index of max_coords so 0-->3 and we change
        # the i'th latitude and longitudes to be the latitude and longitude
        # of our next coordinate. Then once we have them changed, we find the
        # area of our temporary lats/longs list. Then we add that to next_areas
        # so we can see which replacement did best.
        for i in range(len(max_coords)):
            temp_lats = list(rolling_lats)
            temp_longs = list(rolling_longs)
            temp_lats[i] = next_coord[0]
            temp_longs[i] = next_coord[1]
            next_areas.append(PolyArea(temp_lats, temp_longs))

        # Now that next_areas[i] holds what the new area would be if we swapped
        # our new coordinate for max_coords[i], we want to know which index gave
        # us the best swap. So that's what index_of_max is.
        index_of_max = next_areas.index(max(next_areas))

        #Then we want to see if the best new area we could make is better than
        # the current max area that we have. If it is, then we make that swap
        # permanently, putting the next_coord in max_coords at the index it
        # made the biggest difference.
        if next_areas[index_of_max] > current_area:
            max_coords[index_of_max] = next_coord
            capital_info[index_of_max] = capital_name

        line_count += 1

    print("Max area found is: " + str(current_area))
    print(max_coords)

    #This is all for plotting purposes but just want to take out the
    # max _coords from all_points so we can plot the all points as red
    # and the max points as blue.
    all_minus = [x for x in all_points if x not in max_coords]
    # we need a list of lats and a list of longs for plotting
    all_lats = map(lambda coord: coord[0], all_minus)
    all_longs = map(lambda coord: coord[1], all_minus)

    # Plot all the points (excluding max_coords) as red
    plt.plot(all_longs, all_lats, 'ro')
    # Plot max points as blue
    plt.plot(rolling_longs, rolling_lats, 'bo')  #

    # Adding text annotation, basically just putting the capital names next to
    # their dots
    for i in range(len(rolling_lats)):
        plt.annotate(capital_info[i], (rolling_longs[i], rolling_lats[i]))

    plt.show()
