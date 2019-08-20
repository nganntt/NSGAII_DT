#!/usr/bin/env/python
# 
# Using the file system load
#
# We now assume we have a file in the same dir as this one called
# test_template.html
#
    
from jinja2 import Environment, FileSystemLoader
import os
import random

# Capture our current directory
#print ("print current file",os.path.abspath(__file__))
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(CURRENT_DIR, 'templates')
TESTCASE_DIR = os.path.join(CURRENT_DIR, 'testcases')

def load_xml_criteria(distance,speed2):
    pos1 = (0,0)
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(TEMP_DIR),
                         trim_blocks=True)
                        
    template = j2_env.get_template('criteriaA.dbc.xml')
    testcase_crit = template.render(pos1x = 0, pos1y = 0, pos2x = 0, pos2y = distance, speedcar2 = speed2)
    return testcase_crit
    
   
def genrate_tcs(num_tc):
    dist = []
    speed = []
    for i in range(num_tc):
        temp_dist = random.randint(10,60)
        dist.append(temp_dist) 
        temp_speed = random.randint(10,80)
        speed.append(temp_speed) 
        
        file_name = TESTCASE_DIR +"\criteria" + str(i) +".xml"
        
        xml_data = load_xml_criteria(temp_dist, temp_speed)
        #print (xml_data)
        with open(file_name, 'w') as f:
            f.write(str(xml_data))  
            
    listTC = list(zip(dist,speed))
    
    
    
    
    return listTC
    
  

 
    

if __name__ == "__main__":

    #generate xml file
    num_tc = 10
    genrate_tcs(num_tc)
    
    
    from AIExchangeService import get_service
    from aiExchangeMessages_pb2 import SimStateResponse, Control, SimulationID, VehicleID, DataRequest
    from keyboard import is_pressed

    service = get_service()

    # Send tests
    for i in range(num_tc):
        sids = service.run_tests("admin", "admin", TESTCASE_DIR + '\criteria' + str(i) +".xml", TEMP_DIR + "\environmentA.dbe.xml")

        # Interact with a simulation
        if not sids:
            exit(1)
        sid = SimulationID()
        sid.sid = sids.sids[0]
        ego_requests = ["egoPosition", "egoSpeed", "egoSteeringAngle", "egoFrontCamera", "egoLidar", "egoLaneDist"]
        non_ego_requests = ["nonEgoPosition", "nonEgoSpeed", "nonEgoSteeringAngle", "nonEgoLeftCamera", "nonEgoLidar",
                            "nonEgoLaneDist"]
        ego_vehicle = Thread(target=_handle_vehicle, args=(sid, "ego", ego_requests))
        ego_vehicle.start()
        non_ego_vehicle = Thread(target=_handle_vehicle, args=(sid, "nonEgo", non_ego_requests))
        non_ego_vehicle.start()
        ego_vehicle.join()
        non_ego_vehicle.join()

    
   