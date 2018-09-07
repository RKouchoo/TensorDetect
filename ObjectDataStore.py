'''
A class which is used to store information about an object before it is converted to JSON and then sent to the robot. 
'''

class store:
    def __init__(self, obejctType, objectX, objectY, objectDistance):
        self.OBJECT_TYPE = obejctType
        self.OBJECT_X = objectX
        self.OBJECT_Y = objectY
        self.OBJECT_DISTANCE_FROM_ROBOT = objectDistance


# a class that has the numeric values of obejcts which can be detected by tensorflow
class objectType:
    FRC_POWER_UP_POWER_CUBE = 1
    FRC_STRONGHOLD_BOULDER = 2
    FRC_STEAMWORKS_FUEL = 3