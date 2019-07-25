import os  
from random import choice, shuffle, randint
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
        state = posList[i] +','+ rotList[i]
        car_state.append(state)
    return car_state
    
    
        
#select postion and rotation of car1 from car2 state list
# car2 is leading car, car1 hits car2 from the back side 
# def get_pos_rot_secondCar(stateCar1):
    # car2_list = []
    # for i in range(len(stateCar1)-1):
        # substate = stateCar1[i+1:]
        # a = choice(substate)
        # car2_list.append(a)
    # return  car2_list
     
def get_pos_rot_secondCar(car1_list,index_car1):
    """ The function will get a list of position and roation of a car from data file. 
        We need to consider location of car2, Car2 should be heading car. 
        So geting the location of car2, start from particular position of car1 to the end of list"""
    
    if (index_car1+1 < (len(car1_list)-1)):
        random_index_car2 = randint(index_car1+1,len(car1_list)-1)
    else:
        random_index_car2 = 0   # get the first position of car
        
    car2 = car1_list[random_index_car2]
    return  car2
     
# get state of car1, car2 and speed of car1
# the scenarios try to make car 1 hit car 2. Car2 drives with an unchange speed (20km/h)   
#return a list of scenario 
# def get_scenario_State(fileName_postion, fileName_rotation,num_sample):
    # list_state = []
    # pos = getData(fileName_postion)
    # rot = getData(fileName_rotation)
    # minLen = min(len(pos),len(rot))
    # for i in range(minLen):
        # state = pos[i] +','+ rot [i]
        # list_state.append(state)
        
    # car2 = get_pos_rot_secondCar(list_state)
    
    # #speed of car
    # scenario = []
    # for i in range(num_sample):
        # config = []
        # #tuple_state = (list_state[i],car2[i],randint(20,150))
        # # print ("car1: %s"%(list_state[i]))
        # # print ("car2: %s"%(car2[i]))
        # # print ("speed: %s"%(randint(20,150)))
        # config.append(list_state[i])    # X-position and Y-rotation of car1 (X1,X2,X3,Y1,Y2,Y3) 
        # config.append(car2[i])          # V-position and Z-rotation of car2 (V1,V2,V3,Z1,Z2,Z3)
        # config.append(randint(20,150))  # speed of car2 (speed from 20-150)
        
        # scenario.append(config)         # (X1,X2,X3,Y1,Y2,Y3,V1,V2,V3,Z1,Z2,Z3, speed)
    # return scenario


def distance_two_Car(str_pos1, str_pos2):
    pos1 = str_pos1.split(',',3)
    pos2 = str_pos2.split(',',3)
    return distance.euclidean([float(i) for i in pos1[:3]], [float(j) for j in pos2[:3]])



    
# list1 = get_scenario_State ("position_20.txt", "rotation_20.txt",20)
# print("len of car2 %s"% (len(list1)))    
# for i in range(len(list1)): 
    # dist = distance_two_Car(list1[i][0],list1[i][1])
    # #print("dis %s"% dist)
    # l1 = list1[i][0].split(",",3)
    # l2 = list1[i][1].split(",",3)
    # #print("dis %s"% (distance.euclidean([float(i) for i in l1[:3]], [float(j) for j in l2[:3]])))
   
    
    # #print("l1 %s"% (l1[:3]))
    # #print("l2 %s"% (l2[:3]))
    
      
      
      
      
      
  