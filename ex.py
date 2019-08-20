
# https://pypi.org/project/Shapely/
# https://shapely.readthedocs.io/en/latest/



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

def plot_polys(polys):
    for poly in polys:
        if (not getattr(poly, "exterior", None)):
            print("got line?")

        plot_coords(poly.exterior.coords)

        for hole in poly.interiors:
            plot_coords(hole.coords)
            
            
from shapely.geometry import Point, LineString, mapping

import numpy as np
import scipy.interpolate






def create_segment_params(coords,degree, connect_point):
    """
        the function create segment from a list of coords with np.array type
        input is coordinate of points on the line, degree of rotation, and the last point of previous segment
    """
    # print("connect point",connect_point )
    # print ("coordinate input: ", coords)
    
    # make the arc of the road
    f = scipy.interpolate.interp1d(coords[:, 0], coords[:, 1], kind='quadratic')
    
    
    
    fine_x = np.linspace(np.min(coords[:, 0]), np.max(coords[:, 0]), 100)
    fine_y = f(fine_x)

    fine_coords = np.array(list(zip(fine_x, fine_y)))
    fine_line = LineString(fine_coords)
    
    #rotate the road with degree
    rotated_a = affinity.rotate(fine_line, degree)
    
    #convert point to lists
    list_fine_line = list(fine_line.coords)
    list_rot = list(rotated_a.coords)
    
    #print ("list_rot: ", list_rot)
    
    x_off = connect_point[0] - list_rot[0][0] 
    y_off = connect_point[1] - list_rot[0][1]
    
    #print("\n print first %s and secodn fine line %s" %(x_off, y_off))
    
    new_line = affinity.translate(rotated_a,xoff= x_off, yoff= y_off)
    list_translate = list(new_line.coords)
    last_point = list_translate[-1]
    #print ("list coordinate 2 ",list(new_line.coords))
    return new_line, last_point
    
    
    
def create_last_seg ( coords, pre_point):

    print ("previous point",pre_point )
    print ("coords: ",coords )
    x_off = pre_point[0] - coords[0][0]
    y_off = pre_point[1] - coords[0][1]
    
    print("xoff %s yoff %s"%(x_off, y_off ))
    
    line = LineString([coords[0], coords[1]])
   
    new_line = affinity.translate(line,xoff= x_off, yoff= y_off)
    print ("coordinate line 3", list(new_line.coords))
    return new_line
    
    

def recreate_road(coords,deg_second_segment):
    """
    This function create 3 segments of the road.  Each segment consists of 2 points (start, end)
    fist seg, and last_seg is always straight
    The middle_seg is generated from create_segment_params
    The input of this function is np array, fx: coords = np.array([[0, 0], [25, 10], [40, 30], [60, 60], [80, 80], [120, 120]])
    """
    firt_seg = coords[:2, :]
    #mid_seg = coords[2:4, :]
    
    
    mid_seg = coords[1:5, :]
    
    last_seg = coords[4:, :]
    
    l1 = LineString([firt_seg[0], firt_seg[1]])
    
    #plot_polys([l1.buffer(7)])
    
    #adding more points for middle segment
    x = np.linspace(np.min(coords[:, 0]), np.max(coords[:, 0]), 5)
    l2, last_l2 = create_segment_params(mid_seg,deg_second_segment, firt_seg[1])
    
   
    
    l3 = create_last_seg(last_seg,last_l2 )
    
    # plot_coords(l3.coords)
    # plt.show()
    
    
    print("l1 tpye %s, l2 type: %s, l3 %s" %(type(l1),type(l2),type(l3)))
    
    mls = MultiLineString([l1,l2,l3])
    plot_coords([mls.coords])
    #plot_polys([mls.buffer(8)])
    #plt.show()
    
    
    
coords = np.array([[0, 0], [25, 10], [40, 30], [100, 70],[80,120], [190, 120]])
coords1 =  np.array(list(zip (coords[:,0]+10, coords[:,1]+10)))


print ("coords", coords)
print ("coords1", coords1)

recreate_road(coords,30)
recreate_road(coords1,30)
plt.show()
