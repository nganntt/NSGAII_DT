import time
from time import sleep
import sys
import re
import sys_output


from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics


FILE_POS = "position.txt"
FILE_ROT = "rotation.txt"
positions = list()
directions = list()
def collect_data(beamNG_path):

   
    bng = BeamNGpy('localhost', 64256, beamNG_path)
    #bng = BeamNGpy('localhost', 64256, home='D:/BeamNGReasearch/Unlimited_Version/trunk')

    scenario = Scenario('GridMap', 'example')

    # Create an ETK800 with the licence plate 'PYTHON'
    vehicle1 = Vehicle('ego_vehicle', model='etk800', licence='PYTHON',  color='Red')
    #vehicle2 = Vehicle('vehicle', model='etk800', licence='CRASH', color='Blue')

    electrics = Electrics()
    vehicle1.attach_sensor('electrics', electrics)

    pos1 = (-4.270055770874023, -115.30198669433594, 0.20322345197200775)
    rot1 = (0.872300386428833, -0.48885437846183777, 0.01065115723758936)
    scenario.add_vehicle(vehicle1, pos=pos1, rot=rot1)
   
    # Place files defining our scenario for the simulator to read
    scenario.make(bng)

    # Launch BeamNG.research
    bng.open(launch=True)
    #SIZE = 50

    try:
        bng.load_scenario(scenario)
        bng.start_scenario()
        
        #vehicle1.ai_set_speed(10.452066507339481,mode = 'set')
        vehicle1.ai_set_mode('span')
       
         #collect data
        
        print("\n Position and rotation of car \n ")
       # for _ in range(200):
        for _ in range(200):
            time.sleep(0.1)
            vehicle1.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            sensors = bng.poll_sensors(vehicle1)  # Polls the data of all sensors attached to the vehicle
            positions.append(vehicle1.state['pos'])
            directions.append(vehicle1.state['dir'])
            print([vehicle1.state['pos'],vehicle1.state['dir']])
           
        
        #write data into file
        # print ("position :",positions)
        # print ("position :",directions)
        sys_output.print_title("\n     The position and rotation of the car is saved in \"position.txt and \"roation.txt\" \"")
        write_data(FILE_POS,positions)
        write_data(FILE_ROT,directions)
        
        bng.stop_scenario()
        bng.close()
        time.sleep(2)
        
       
    finally:
            bng.close()
    return (positions,directions)

def write_data(name_file,arg):
    file = name_file 
    with open(file, 'w') as f:
        for line in arg:
            strLine = str(line)
            f.write(str(strLine[1:-1]) +"\n")
            
    

    
if __name__ == "__main__":
    if __name__ == "__main__":
        collect_data(sys.argv[1])
        





