'''
A class which is used to send data about what and where the current object is to the robot.
'''

import threading
import socket


class Connection():
    def __init__(self, robotIP, robotPort, webTimeout, isRobotPresent):
        # Create a new thread
        threading.Thread.__init__(self)

        self.ROBOT_IP = robotIP
        self.ROBOT_PORT = robotPort
        self.IS_ROBOT_PRESENT = isRobotPresent
        self.WEB_TIMEOUT = webTimeout

        if self.IS_ROBOT_PRESENT:
            self.start()

    # opens a connection to the robot based on the IP
    def openConnectionToRobot(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.WEB_TIMEOUT)

            # establish a connection to the robot.
            s.connect((self.ROBOT_IP, self.ROBOT_PORT))
            self.socket = s
            print("Established a connection to: {}".format(self.ROBOT_IP))

        except Exception as e:
            self.socket = None # we don't have a valid connection so we want to kill it while we can
            print("Failed to establish a connetion to: {}".format(self.ROBOT_IP))
            print(" === BEGIN STACK === ")
            print(e)
            pass


    def sendDataToRobot(self, objectData):
        if not self.socket:
            print("Ignoring send request!")
            return

        try:
            self.socket.send(objectData)
        except Exception as e:
            print("Failed to send data: {} to the IP: {}".format(objectData, self.ROBOT_IP))
            print(" === BEGIN STACK === ")
            print(e)
            pass

