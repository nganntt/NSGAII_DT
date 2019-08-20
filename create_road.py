import time
from time import sleep
import sys
import re
import sys_output


from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics



import pdb

import sys
import math
#from sets import Set

# if having trouble installing: https://stackoverflow.com/a/49335954/23630
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

from shapely.ops import polygonize
from shapely.geometry import Polygon
from shapely.geometry import MultiPolygon
from shapely.geometry import MultiLineString
from shapely.geometry import CAP_STYLE, JOIN_STYLE
from shapely.ops import cascaded_union
from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import LinearRing
from shapely.geometry import Point


from shapely import affinity


import numpy as np
import scipy.interpolate








def plot_coords(coords):
    pts = list(coords)
    #print ("pts %s"%pts)
    x,y = zip(*pts)
    #print("x= %s, y = %s"%(x,y))
    plt.plot(x,y)