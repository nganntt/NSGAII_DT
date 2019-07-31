import sys
from generate_data import getData
import numpy as np
import simple_scenario
from random import sample
import re
import sys_output
from scipy.spatial import distance
from datetime import datetime
import os


POS_FILE = "position.txt"
POP_FILE = "population.txt"

pos = getData(POS_FILE) 
pop = getData(POP_FILE) 


#['53.35311508178711, -139.84017944335938, 0.20729705691337585,0.8766672611236572, -0.4810631573200226, 0.005705998744815588', #'75.94310760498047, -232.62135314941406, 0.20568031072616577,-0.896364688873291, -0.4433068335056305, -0.0030648468527942896', 33]

#def get_rot_pos(index, pop):
def get_rot_pos(str_scenario):
    """
    This function get position and rotation from population data file.
    
    """
    ####
    print("Scenario gets from population: \n",str_scenario)
    str_scenario = re.sub('[\[\]\']','',str_scenario)
    # str_ind =  pop[index]
    # str_ind = str(str_ind[1:-1])
    #list_items = str_ind.split(',')
    list_items = str_scenario.split(',')
    
    list_items = [item.replace('\'', '') for item in list_items]
    
    # for i in list_items:
        # print ("####element ", i)
    # print (list_items)
    # print ("size",len(list_items) )
    # print ("type",type(list_items) )
    
    
    
    car1_pos = (float(list_items[0]), float(list_items[1]),float(list_items[2]))
    car1_rot = (float(list_items[3]),float( list_items[4]),float(list_items[5]))
    car1     = (car1_pos, car1_rot)
    
    
   
    # for j in range(6,11):
        # print ("item +++++++++  ",list_items[j])
    
    car2_pos = (float(list_items[6]), float(list_items[7]), float(list_items[8]))
    car2_rot = (float(list_items[9]), float(list_items[10]),float(list_items[11]))
    car2     = (car2_pos, car2_rot)
    
    
    # print ("####### item 6", list_items[6])
    speed_car2 = int(list_items[12])
    # print ("car1",car1)
    # print ("car2",car2)
    # print ("speed",speed_car2)

    return (car1, car2, speed_car2)
    
def get_pos (pos):
    list_pos = []
    for i in range(len(pos)):
        string_scenarios = re.sub('[\[\]\']','',pos[i])
        str_items = string_scenarios.split(',')
        list_pos.append( float(str_items[0]))
        

    return list_pos
    
    
    
    #postion is file data of position 
def find_pos_2cars(car1, car2, pos):
    """
    This function identify which one is car1 and the other is cars
    We need to rearrange the posion of the car becase car1 must be leading car
    and car2 hit car1 with particular speed. Speed of car1 is a constant
    """
    print ("Position and rotation of car 1\n", car1)
    print ("Position and rotation of car 2\n", car2)
    idx_car1 = -1
    idx_car2 = -1
    pos_x = get_pos(pos)  # take first element x from position tuple(x,y,z)
    for i in range(len(pos)):
        tem_po = pos_x[i]
        car1_pos = car1[0][0]
        car2_pos = car2[0][0]
        if car1_pos == tem_po:
            idx_car1 = i
            
        if car2_pos == tem_po:
            idx_car2 = i
           
        if idx_car1 != -1 and idx_car2 != -1:
            break
    
    if idx_car1 > 0 and idx_car2 > 0:
        if idx_car1 < idx_car2:
            # swap postion of two car
            tmp = car1
            car1 = car2
            car2 = tmp
    return (car1,car2)

    
# select number of tc which needs to run it on beamNG
# take population from pop file

def main(beamNGpath,num_tc):
    
    
    
    testcase = []
    num_tc = int(num_tc)
    if num_tc <= len(pop):
        rand_pop = sample (pop, num_tc)
        
    else:
        sys_output.warning("The population there only %s, thus it is possible to run %s testcase " %(len(pop),len(pop)))
        rand_pop = pop
            #call text of beamNG and deport
    for idx, scenario in enumerate(rand_pop):
        sys_output.print_star_end(" RUN TESTCASE %s " %(idx+1))
        (car1,car2,speed_car2) = get_rot_pos(scenario)
        car1, car2 = find_pos_2cars(car1,car2,pos)
        distance_2cars = distance.euclidean(car1[0],car2[0])
        print ("\n  Distance between 2 car: %s, speed: %s " %(distance_2cars,speed_car2))
        crash = simple_scenario.launch(beamNGpath, car1, car2,speed_car2)
        
        if crash:
            sys_output.result ("FAILED TESTCASE "+ str(idx+1)  + "| Scenario: distance: " + str (distance_2cars) \
                           +", speed of second car: "+ str(speed_car2))
        else:
            sys_output.result ("PASSED TESTCASE "+ str(idx+1) + "| Scenario: distance: " + str (distance_2cars) \
                          + ", speed of second car: "  + str(speed_car2))
        testcase.append([car1,car2,speed_car2,distance_2cars,crash])
        
    sys_output.summary(testcase)
    #write the result to file
    now = datetime.now()
    path_dir = os.getcwd() 
    date_time = now.strftime("%m_%d_%Y__%H%M%S")
    file_gen = path_dir +"\store\Result" + date_time +".txt"
    with open(file_gen, 'w') as f:
         f.write(str(testcase))
            

# def main(num_idx):
    # idx = int(num_idx)
    # (car1, car2, speed ) = get_rot_pos(idx )
    # print(car1[0][0])
    # print("index of car",str(find_pos_2cars(car1,car2,pos) ))



   
if __name__ == "__main__":
    
    main(sys.argv[1],sys.argv[2])
   



# a= get_pos (pos)
# for i in range(len(pos)):
    # print ("type" + str(i)+" ", type(a[i]))
    # print("item"+str(i)+ "   ", a[i])
    
    