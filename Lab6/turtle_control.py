#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from std_msgs.msg import Bool
import math
import time

class turtle:
    def __init__(self):
        self.is_moving = Bool()
        self.start_2 = time.time()
        rospy.init_node('turtle_control')
        self.pub = rospy.Publisher('/turtle1/cmd_vel',Twist,queue_size=1)
        self.moving_pub = rospy.Publisher('/turtle1/it_moving',Bool,queue_size=1)
        rospy.Subscriber('/turtle1/pose',Pose,self.callback)
        rospy.Subscriber('/turtle1/wish', Point,self.callback_wish)
        self.wish_points = Point()
        rospy.spin()



    def callback(self,msg):
        x = msg.x
        y = msg.y
        self.moving_pub.publish(self.is_moving)
        wish_angle = math.atan2((self.wish_points.y - y),(self.wish_points.x - x))
        err_theta = wish_angle - msg.theta
        if not self.is_moving.data:
            return
        if math.fabs(err_theta) > 1e-3:
            if err_theta > math.pi:
                err_theta = err_theta - 2*math.pi
            elif err_theta < -math.pi:
                err_theta = err_theta + 2*math.pi
            self.publish_msg(0,err_theta*50)
            return
        err_ampl = math.sqrt((self.wish_points.y - y)**2 + (self.wish_points.x - x)**2)
        if math.fabs(err_ampl) > 1e-3:
            self.publish_msg(err_ampl*50,0)
            return
        self.is_moving.data = False

    def callback_wish(self,msg):
        self.wish_points = msg
        self.is_moving.data = True

    def publish_msg(self,x,theta):
        vel_msg = Twist()
        vel_msg.linear.x = x
        vel_msg.angular.z = theta
        self.pub.publish(vel_msg)

if __name__ == '__main__':
    try:
        Carl = turtle()
    except rospy.ROSInterruptException:
        pass
