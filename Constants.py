###########
'''
CONSTANTS:
The class that stores all of the constants for the application
'''
##########

'''
The vision constants which are used on the robot
'''
class vision:

    CAMERA_WIDTH = 240
    CAMERA_HEIGHT = 320


'''
The class that stores the network constants
'''
class net:

    ROBOT_IP = "10.31.32.1"
    ROBOT_CONNECT_PORT = "5802"


class machine:
    MACHINE_CONCURRENT_TENSORFLOW_THREADS = 8


class tensor:
    MINIMUM_SCORE_THRESHOLD = 0.84
    NUM_CLASSES = 1  # Only one class which has been trained (power cube)
