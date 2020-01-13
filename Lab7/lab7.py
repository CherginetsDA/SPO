#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
# from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
from sensor_msgs.msg import LaserScan
import math
import time

class robot:
    def __init__(self):
        self.is_moving = Bool()
        self.start_2 = time.time()
        rospy.init_node('robot_control')
        self.pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
        self.odom = Odometry()
        self.moving_pub = rospy.Publisher('/it_moving',Bool,queue_size=1)
        rospy.Subscriber('/base_scan',LaserScan,self.callback)
        rospy.spin()



    def callback(self,msg):
        rang = msg.ranges
        size = len(rang)
        x = min(rang[-90:]+rang[:90])
        err_left = 0.7 - min(rang[size//2:]);
        if x > 0.7:
            self.publish_msg(1,err_left/abs(err_left))
        else:
            self.publish_msg(0,1)

    def publish_msg(self,x,theta):
        vel_msg = Twist()
        vel_msg.linear.x = x
        vel_msg.angular.z = theta
        self.pub.publish(vel_msg)

if __name__ == '__main__':
    try:
        Carl = robot()
    except rospy.ROSInterruptException:
        pass
