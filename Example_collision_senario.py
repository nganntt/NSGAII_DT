import time
from time import sleep
import sys

from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics


def scenario(beamNG_path):
   
    if (beamNG_path == ""):
        beamNG_path = 'D:/BeamNGReasearch/Unlimited_Version/trunk'
    
    bng = BeamNGpy('localhost', 64256, beamNG_path)
    
    
  

    #scenario = Scenario('west_coast_usa', 'example')

    scenario = Scenario('GridMap', 'example')

    # Create an ETK800 with the licence plate 'PYTHON'
    vehicle1 = Vehicle('ego_vehicle', model='etk800', licence='PYTHON',  color='Red')
    vehicle2 = Vehicle('vehicle', model='etk800', licence='CRASH', color='Blue')

    electrics = Electrics()
    vehicle1.attach_sensor('electrics', electrics)


   

    pos2 = (-13.04469108581543, -107.0409164428711, 0.202297180891037)
    pos1 = (-4.270055770874023, -115.30198669433594, 0.20322345197200775)
    rot2 = (0.0009761620895005763, -0.9999936819076538, -0.0034209610894322395)
    rot1 = (0.872300386428833, -0.48885437846183777, 0.01065115723758936)
    scenario.add_vehicle(vehicle1, pos=pos1, rot=rot1)
    scenario.add_vehicle(vehicle2, pos=pos2, rot=rot2)

    scenario.make(bng)

    # Launch BeamNG.research
    bng.open(launch=True)
    SIZE = 500

    try:
        bng.load_scenario(scenario)
        bng.start_scenario()
        
        vehicle1.ai_set_speed(10.452066507339481,mode = 'set')
        vehicle1.ai_set_mode('span')
        vehicle2.ai_set_mode('chase')
         #collect data
        positions = list()
        directions = list()
        wheel_speeds = list()
 
        for _ in range(100):
            time.sleep(0.1)
            vehicle1.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            sensors = bng.poll_sensors(vehicle1)  # Polls the data of all sensors attached to the vehicle
            positions.append(vehicle1.state['pos'])
            directions.append(vehicle1.state['dir'])
            wheel_speeds.append(sensors['electrics']['values']['wheelspeed'])
           

            print('The Final result - position  :')
            print(positions)
            print('The Final result - direction  :')
            print(directions)
            print('The Final result - speed  :')
            print(wheel_speeds)
        
        bng.stop_scenario()
        bng.close()
    finally:
            bng.close()


    

if __name__ == "__main__":
    if __name__ == "__main__":
        scenario(sys.argv[1])
        






