import os  

from random import choice, shuffle, randint, randrange
from scipy.spatial import distance

def FileCheck(fn):
    try:
      if (os.path.isfile(fn)):  
        return 1
    except IOError:
      print ("Error: File does not appear to exist.")
      return 0

      
#get roation or position from file into a list
def getData(fileName):
    list = []
    if (FileCheck(fileName)):
        with open(fileName) as f:
            for line in f:
                list.append(line.rstrip())
    return list


def get_pos_rot_from_list(posList, rotList):
    """
    The function will generate a list which contains posistion (a string of x,y,z) 
    and rotation of car (a string of u,v,w)
    strings (x,y,z) of position. Strings (u,v,w) of rotation
    car state = (x,y,z,u,v,w)    """
    car_state = []
    minLen = min(len(posList),len(rotList))
    for i in range(minLen):
        #state = posList[i] +','+ rotList[i]
        state = str(posList[i]) +','+ str(rotList[i])
        car_state.append(state)
    return car_state
    
 
     
def get_pos_rot_secondCar(car1_list,index_car1):
    """ The function will get a list of position and roation of a car from data file. 
        We need to consider location of car2, Car2 should be heading car. 
        So geting the location of car2, start from particular position of car1 to the end of list"""
    random_index_car2 = -1
    if (index_car1+1 < (len(car1_list)-1)):
        for i in range(5):
             random_index_car2 = randrange(0,len(car1_list)-1)
             if random_index_car2 != -1 and random_index_car2 != index_car1:
                break
                
    car2 = car1_list[random_index_car2]
    return  car2
     

def distance_two_Car(str_pos1, str_pos2):
    
    pos1 = str_pos1.split(',',3)
    pos2 = str_pos2.split(',',3)
    return distance.euclidean([float(i) for i in pos1[:3]], [float(j) for j in pos2[:3]])

