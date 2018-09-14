'''
A class which is used to store/send json requests to the robot
'''

import TensorDetect.DetectedObjectDataStore.objectType

class sendables:

	REQUEST_LED_OFF = True
	REQUEST_LED_ON = True
	
	HAS_CONNECTION = True 

# slightly useless but anyway
class recieveables:

	FRC_POWER_UP_POWER_CUBE = objectType.FRC_POWER_UP_POWER_CUBE
    FRC_STRONGHOLD_BOULDER = objectType.FRC_STRONGHOLD_BOULDER
    FRC_STEAMWORKS_FUEL = objectType.FRC_STEAMWORKS_FUEL

    GOAL_MODE = True
    OBJECT_MODE= True

    HAS_CONNECTION = True