
import array
import random
import json

import numpy

from math import sqrt
import os

from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools


from random import choice, shuffle, randint
from scipy.spatial import distance

import decision_tree

import generate_data

creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Problem definition
#
POS_FILE = "position_20.txt"
ROT_FILE = "rotation_20.txt"

# get position and rotation from data files
pos = generate_data.getData(POS_FILE) 
rot = generate_data.getData(ROT_FILE)
initial_pos_rot = generate_data.get_pos_rot_from_list(pos,rot)




def get_scenario_State():
    car1_list = []
    #pos = generate_data.getData(fileName_postion)
    #rot = generate_data.getData(fileName_rotation)
    minLen = min(len(pos),len(rot))
    for i in range(minLen):
        state = pos[i] +','+ rot [i]
        car1_list.append(state)
    
    #speed of car
    scenario = []
    random_index_pos_list = randint(0,minLen-1)
    car1 = car1_list[random_index_pos_list]
    #car2 = car2_list[random_index_pos_list]
    car2 = generate_data.get_pos_rot_secondCar(car1_list,random_index_pos_list)    
    speed = randint(20,100)
    scenario.append(car1) 
    scenario.append(car2)    
    scenario.append(speed)    
  
    return scenario


# evaluation function with two parameter of distance(car1, car2) and speed of car2
def evaluation_collision(individual):
    dist = generate_data.distance_two_Car(individual[0], individual[1])
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
        individual[2] = randint(20,100)
    return individual   
        
 

toolbox.register("attr_float", get_scenario_State)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluation_collision)
toolbox.register("mate", tools.cxOnePoint)
# toolbox.register("mutate", tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)

#toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mut_randChoice)
toolbox.register("select", tools.selNSGA2)



#example to run indiviudal and population
#['96.72881317138672, -209.87376403808594, 0.20368465781211853,-0.3515154719352722, -0.9361792802810669, -0.0022529030684381723',
# '74.01776123046875, -233.57073974609375, 0.20380012691020966,-0.9138180613517761, -0.40611740946769714, -0.002287991577759385'
#, 38]
     
        
def main(seed=None):

    NGEN = 1
    MU = 100  # don't change this number too low--> error tournament
    CXPB = 0.9

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean, axis=0)
    # stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"
    
    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    #pop = toolbox.select(pop, len(pop))
    #Intergration DT in select population
    pop = select_pop_DT(pop)
    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print(logbook.stream)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
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
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)
    
    file = "population.txt"
    with open(file, 'w') as f:
        for line in pop:
            f.write(str(line)+"\n")
    
    print("Final population hypervolume is %f" % hypervolume(pop, [11.0, 11.0]))
    
    return pop, logbook

    
    

def select_pop_DT(pop):
    """
    the population are select from critical situation by DT
    
    """
    new_pop = []
    data = decision_tree.convert_dataFrame(pop)
    data.to_csv(r'decision_tree_data.cvs')
    
    pop_idx = decision_tree.get_critical_sample_DT(data)
    for i in pop_idx:
        new_pop.append(pop[i])
    
    return new_pop



if __name__ == "__main__":
    
    pop, stats = main()
    #print("population type : ", type(pop))
    #print("population len : ", len(pop))
    for i in pop:
        pass
        #print("individual", i[0],'\n', i[1],'\n',i[2])
    # pop.sort(key=lambda x: x.fitness.values)

    
  