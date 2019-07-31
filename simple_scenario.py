import time
from time import sleep
import sys
import re
import sys_output
from scipy.spatial import distance

from beamngpy import BeamNGpy, Scenario, Vehicle
from beamngpy.sensors import Electrics

def launch (beamNGPath, car1, car2, speed_car2):
    crash = False
    dist_2car = 20
    speed_car2 = int(speed_car2)
    bng = BeamNGpy('localhost', 64256, beamNG_path)
    #bng = BeamNGpy('localhost', 64256, home='D:/BeamNGReasearch/Unlimited_Version/trunk')

    scenario = Scenario('GridMap', 'example')

    # Create an ETK800 with the licence plate 'PYTHON'
    vehicle1 = Vehicle('ego_vehicle', model='etk800', licence='PYTHON',  color='Red')
    vehicle2 = Vehicle('vehicle', model='etk800', licence='CRASH', color='Blue')

    electrics1 = Electrics()
    electrics2 = Electrics()
    vehicle1.attach_sensor('electrics1', electrics1)
    vehicle2.attach_sensor('electrics2', electrics2)
    
    #position to try drive then teleport
    #-365.2436828613281, -214.7460479736328, 1.2118444442749023], [0.9762436747550964, 0.20668958127498627, 0.0650215595960617]]
    #[[-362.4477844238281, -214.16226196289062, 1.32931387424469], [0.9824153780937195, 0.1852567195892334, 0.023236412554979324]]
    
    pos2 = ( 25.75335693359375, -127.78406524658203, 0.2072899490594864)
    pos1=  (-88.8136978149414, -261.0204162597656, 0.20253072679042816)
    
    #pos_tel1 = (53.35311508178711, -139.84017944335938, 0.20729705691337585)           #change this
    #pos_tel2 = (75.94310760498047, -232.62135314941406, 0.20568031072616577)            #change this
    pos_tel1 = car1[0]
    pos_tel2 = car2[0]
    
    rot2 = (0.9298766851425171, -0.36776003241539, 0.009040255099534988)
    rot1 = (-0.9998571872711182, 0.016821512952446938, -0.0016229493776336312)
    # rot_tel1= (0.8766672611236572, -0.4810631573200226, 0.005705998744815588)         #change this
    # rot_tel2 = (-0.896364688873291, -0.4433068335056305, -0.0030648468527942896)       #change this
    rot_tel1= car1[1]
    rot_tel2= car2[1]
    
    #initial postion of two car.
    # run 2cars on particular road until they reach particular speed which satisfies the condisiton of the given testcase
    scenario.add_vehicle(vehicle1, pos=pos1, rot=rot1)
    scenario.add_vehicle(vehicle2, pos=pos2, rot=rot2)
    
    scenario.make(bng)

    # Launch BeamNG.research
    bng.open(launch=True)
   

    try:
        bng.load_scenario(scenario)
        bng.start_scenario()
        
        vehicle1.ai_set_speed(10,mode = 'set')
        vehicle1.ai_set_mode('span')
        
        vehicle2.ai_set_speed(speed_car2,mode = 'set')               ##change this param of speed
        vehicle2.ai_set_mode('chase')
        sys_output.print_sub_tit("Initial Position and rotation of car")
        print ("\nInitial  Position and rotation of car1  %s %s  " %(pos1,rot1))
        print ("\nInitial  Position and rotation of car2  %s %s  " %(pos2,rot2))
        sys_output.print_sub_tit("\n when speed of car 1 rearch 10 and speed car 2 reach %s. Two cars are teleport to new locations." %(speed_car2))
        for _ in range(450):
            time.sleep(0.1)
            vehicle1.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            vehicle2.update_vehicle()
            sensors1 = bng.poll_sensors(vehicle1)  # Polls the data of all sensors attached to the vehicle
            sensors2 = bng.poll_sensors(vehicle2)
            
            speed1 = sensors1['electrics1']['values']['wheelspeed']
            speed2 = sensors2['electrics2']['values']['wheelspeed']
            print ("speed of car 1", speed1)
            print ("speed of car 2", speed2)
            #print([vehicle1.state['pos'],vehicle1.state['dir']])
            if speed1 > 9 and speed2 > speed_car2-1:                            #change speed here
                bng.teleport_vehicle(vehicle1,pos_tel1,rot_tel1 )
                bng.teleport_vehicle(vehicle2,pos_tel2,rot_tel2 )
                sys_output.print_sub_tit ("Teleport 2 car to new location")
                print ("\n  Car1 : " + str(pos_tel1) + ", "+ str(rot_tel1) )
                print ("\n  Car2 : " + str(pos_tel2) + ", "+ str(rot_tel2) )
                print ("\n  Distance between two cars: " + str(distance.euclidean(pos_tel1,pos_tel2)))
                break
           
            # if speed > 19:
                # bng.teleport_vehicle(vehicle1,pos_tel,rot_tel )
                # break

        for _ in range(100):
           #pos1 = []
           time.sleep(0.1)
           vehicle1.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
           vehicle2.update_vehicle()
           sensors1 = bng.poll_sensors(vehicle1)  # Polls the data of all sensors attached to the vehicle
           sensors2 = bng.poll_sensors(vehicle2)
            
           speed1 = sensors1['electrics1']['values']['wheelspeed']
           speed2 = sensors2['electrics2']['values']['wheelspeed']
           
           #pos1.append(vehicle1.state['pos'])
           #pos2.append(vehicle2.state['pos'])
           
           dist_2car =  distance.euclidean(vehicle1.state['pos'],vehicle2.state['pos'])
           if dist_2car < 5: #or int(speed2)== 0 :
                crash = True
                print("\n  Failed because distance of two cars are less than 5")
                break
           print ("\n speed1 %s, speed2: %s, distance: %s" %(speed1, speed2, dist_2car))
           if int(speed2)== 0 :
                print("\n  Pass because car2 stoped")
                break
        
        bng.stop_scenario()
        bng.close()
    finally:
            bng.close()
    
    
    return crash
    

 
   
if __name__ == "__main__":
    
    main(sys.argv[1])