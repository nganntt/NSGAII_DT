
import array
import random
import json
import sys
import traceback
import inspect
import sys_output
from datetime import datetime

import numpy

from math import sqrt
import os

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

from random import choice, shuffle, randint, randrange
from scipy.spatial import distance
import decision_tree
import generate_data
import create_xml_scenario

POS_FILE = "position.txt"
ROT_FILE = "rotation.txt"

def main(num_gen, num_pop):
    #run beamNG to collect data
    
    sys_output.print_star_end("Start the process of generation testcases with NSGAII_DT")
    
    int_num_gent = int(num_gen)
    int_num_pop = int(num_pop)
    # print("\n Collect data from BeamNG.research with Grid Map. This process takes around 1 minute. BeamNG is running. Please wailt.... ")
    
    
    #(pos_beamNG ,rot_beamNG) = data_map.collect_data(beamNG_path)
   
    #run nsga2 algorithms
    #sys_output.print_title("  Finish collect data from BeamNG.research")
    nsga2(int_num_gent,int_num_pop)
    sys_output.print_star_end("End the process of generation testcases from NSGAII_DT")




def print_pop(pop):
        for id, ind in enumerate(pop):
            print("\n "+ str(id) + "   " +str(ind))

        print("\n")

def file_name():
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = "NSGAII.py"
    return filename

    
def write_data(name_file,arg):
    file = name_file 
    with open(file, 'w') as f:
        for line in arg:
            strLine = str(line)
            f.write(str(strLine[1:-1]) +"\n")
            
            
      
            
def gen_pop(num_ind):
    dist = []
    speed = []
    for _ in range(num_ind):
        #temp_dist = random.randint(10, 60) #old setting in beamNG.research
        temp_dist = random.randint(10, 200)
        dist.append(temp_dist)
        temp_speed = random.randint(10, 80)
        speed.append(temp_speed)
    
    dist_speed_list = list(zip(dist, speed))
    pop = []
    for i in range(num_ind):
        ind = (0,0,0,0,dist_speed_list[i][0],0,dist_speed_list[i][1])
        pop.append(ind)
    write_data("population.txt",pop)
    return pop

def nsga2(number_gen, num_pop):

    creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", list, fitness=creator.Fitness)

    toolbox = base.Toolbox()

    # POS_FILE = "position.txt"
    # ROT_FILE = "rotation.txt"

    # get position and rotation from data files
    # pos = generate_data.getData(POS_FILE) 
    # rot = generate_data.getData(ROT_FILE)
    #initial_pos_rot = generate_data.get_pos_rot_from_list(pos,rot)
    initial_pos_rot = gen_pop(num_pop)
    now = datetime.now()
    path_dir = os.getcwd()  

    def get_scenario_State():
    
         
        temp_dist = random.randint(10, 200)
        
        temp_speed = random.randint(10, 80)
        
        # car1_list = []

        # minLen = min(len(pos),len(rot))
        # for i in range(minLen):
            # state = pos[i] +','+ rot [i]
            # car1_list.append(state)
        
        # #speed of car
        scenario = []
        # random_index_pos_list = randrange(0,minLen-1)
        # car1 = car1_list[random_index_pos_list]
        # #car2 = car2_list[random_index_pos_list]
        # car2 = generate_data.get_pos_rot_secondCar(car1_list,random_index_pos_list)    
        
        car1 = [0,0,0,0,90,0]  #rotation need to be checked later, 3 last element is rotation
        car2 = [0,temp_dist,0,0,90,0] #rotation need to be checked later, 3 last element is rotation
        scenario.append(car1) 
        scenario.append(car2)    
        scenario.append(temp_speed)    
       
        return scenario


    # evaluation function with two parameter of distance(car1, car2) and speed of car2
    def evaluation_collision(individual):
        
        dist = individual[1][1] 
        print("distance of 2 car",dist )
        speed = individual[2]
        if (dist not in range(10,50)):  
            return 10000, 0        # Ensure distance of two car too far and speed already checked in range(20,100)
        return dist, speed


    def mut_randChoice(individual):
        rand_index = randint(0, len(individual)-1)
        num_car1_state = randint(0, len(initial_pos_rot)-1)
        if rand_index== 0:
            individual[0] = initial_pos_rot[num_car1_state]
        elif rand_index == 1:
            individual[1] = initial_pos_rot[num_car1_state]
        else:
            individual[2] = randint(10,35)
        return individual   
            
    def crossOver(ind1, ind2):
        id = randint(0,2)
        #keep the first element, change the second element (change car2)
        if id == 0 :
            tmp = ind1[1]
            ind1[1] = ind2[1]
            ind2[1] = tmp
        # keep the second element, change the first element (change car 1)
        elif id == 1 :
            tmp = ind1[0]
            ind1[0] = ind2[0]
            ind2[0] = tmp
        # change speed of two individual
        elif id == 2:
            tmp = ind1[2]
            ind1[2] = ind2[2]
            ind2[2] = tmp
        return ind1, ind2 
     
    toolbox.register("attr_float", get_scenario_State )
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluation_collision)
    toolbox.register("mate", crossOver)
    
    toolbox.register("mutate", mut_randChoice)
    toolbox.register("select", tools.selNSGA2)


    NGEN = int(number_gen)  #number of generation
    MU = int(num_pop)       #number of population
    CXPB = 0.9
    print("=========================== START NSGAII ====================================================== ")
    print("Number of Genaration: " , NGEN)
    print("Number of Population: " , MU)
    print("=============================================================================================== ")
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    
    pop = toolbox.population(n=MU)
    print("\n\n\n  Initial population : \n\
        Each Car is a vector 6 dimensions. (x1,y1,z1,e1,u1,v1). position (x,y,z), rotation (e,u,v)\n\
        Each indivudual has 2 car (12 parameters, 6 for each car) and state of scenarios \n\
        (x1,y1,z1,e1,u1,v1,  x2,y2,z2,e2,u2,v2,   state )\n")
    print("-----------------------------------------------------------------------------------------------")
    

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    pop = toolbox.select(pop, len(pop))
    print_pop(pop)
    
    #Intergration DT in select population
    record = stats.compile(pop)
    #logbook.record(gen=0, evals=len(invalid_ind), **record)
    
    # Begin the generational process
    print(str( sys_output.trace_func(str(file_name()), str(sys._getframe().f_code.co_name))))
    for gen in range(1, NGEN+1):
        # Vary the population
        sys_output.print_title("ENTER LOOP OF GENERATION WITH DECISION TREE: Generation  " + str(gen))
        sys_output.print_sub_tit("1. Select individuals from Decision Tree")

        # select population from decision tree( The testcases are run on BuildDrive)
        pop_DT = select_pop_DT(pop)
        print ("\n\n Population is select for generation: ")
        print_pop(pop_DT[1])
        
        pop_DT_new = select_gen_from_pop_DtPop(MU,pop)
        pop = toolbox.select(pop_DT_new, MU)
        sys_output.print_sub_tit("2. Generate offspring ....")
        
        #offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = tools.selRandom(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)
            
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        
        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        sys_output.print_sub_tit("3. Select individuals from offspring and population")
        
        print("\n3. Select individuals from offspring and population \n")
        record = stats.compile(pop)
        #logbook.record(gen=gen, evals=len(invalid_ind), **record)
       
        #save  generation population
        print("Population is generated ")
        print_pop(pop)
        date_time = now.strftime("%m_%d_%Y__%H%M%S")
        file_gen = path_dir +"\store\population_" + date_time +".txt"
        with open(file_gen, 'w') as f:
            f.write(str(pop))
        sys_output.print_sub_tit("Generation %s is save in %s "%(gen,file_gen ))
    
    
    file = "population.txt"
    sys_output.print_sub_tit("Final population is saved in %s "%(path_dir +"\population.txt" ))
    with open(file, 'w') as f:
        for line in pop:
            f.write(str(line)+"\n")
    return pop   


def select_pop_DT(pop):
    """
    the population are select from critical situation by DT
    
    """
    new_pop = []
    #run population on DriveBuild
    data = decision_tree.convert_dataFrame(pop)   
    now = datetime.now()
    date_time = now.strftime("%m_%d_%Y__%H%M%S")
    path_dir = os.getcwd()   
    file_name_cvs = path_dir +"\store\\DT_data" + date_time +".cvs"

    data.to_csv(r'decision_tree_data.cvs')
    print("\n Data to build the tree is save in " , file_name_cvs )
   
    
    print("\nc. Train decision tree and select critical events")
    #get leaf which contains the critical situations
    pop_idx = decision_tree.get_critical_sample_DT(data)
    
    #print("index of decision tree", pop_idx)
    for i in pop_idx:
        new_pop.append(pop[i])
    return pop_idx, new_pop


def select_gen_from_pop_DtPop(num_pop, pop):
    idx, dt_pop = select_pop_DT(pop)
    counter = len(dt_pop)
    print("\n Select_gen_from_pop_DtPop \n ")
    print_pop(pop)
    
    while counter < num_pop:
        new_idx = randint(0,len(pop)-1)
        
        #check whether the element is selected from population or not
        while check_idx(idx,new_idx):
            new_idx = randint(0,len(pop)-1)
        
        idx.append(new_idx)
        dt_pop.append(pop[new_idx])
        counter +=1
    print("\n List idx which is used to select individuals from populaiton: \n", idx)
    return dt_pop
    

def check_idx(list_idx, x):
    found = 0
    for item in list_idx:
        if x == item:
            return 1
    return found
       

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
else:
    main(1, 3)
   

    
  