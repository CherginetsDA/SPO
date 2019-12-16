#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from std_msgs.msg import Bool
import math
import threading
import time

it_moving = False
pub = None

def can_move():
    try:
        time.sleep(0.5)
        while it_moving:
            time.sleep(1e-3)
    except rospy.ROSInterruptException:
        pass


def publish_msg(wish_points):
    global pub
    global it_moving
    can_move()
    point = Point()
    point.x = wish_points[0]
    point.y = wish_points[1]
    pub.publish(point)

def callback(msg):
    global it_moving
    it_moving = msg.data

def pen_control(r,g,b,w,o):
    try:
        rospy.wait_for_service('/turtle1/set_pen')
        pen = rospy.ServiceProxy('/turtle1/set_pen',SetPen)
        pen(r,g,b,w,o)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def send_first_point(wish_points):
    time.sleep(0.5)
    pen_control(0,0,0,0,1)
    publish_msg(wish_points)
    can_move()
    pen_control(200,50,150,2,0)

def send(wish_points):
    send_first_point(wish_points[0])
    for n in range(1,len(wish_points)):
        publish_msg(wish_points[n])

def send_points():
        send([[2,5.5],[2,6],[3,6],[3,5.5],[2,4],[3,4]])
        send([[3.5,6],[3.5,5],[4.5,5],[4.5,6],[4.5,4]])
        send([[5,5.7],[5.3,6],[5.7,6],[6,5.7],[6,5.3],[5.7,5],[6,4.7],[6,4.3],[5.7,4],[5.3,4],[5,4.3]])
        send([[7.5,5],[6.8,5],[6.5,5.3],[6.5,5.7],[6.8,6],[7.2,6],[7.5,5.7],[7.5,4.3],[7.2,4],[6.8,4],[6.5,4.3]])
        send([[8,4.3],[8,4],[9,4],[9,5],[8,5],[8,6],[9,6]])
        send([[10.2,5],[9.8,5],[9.5,5.3],[9.5,5.7],[9.8,6],[10.2,6],[10.5,5.7],[10.5,5.3],[10.2,5],[10.5,4.7],[10.5,4.3],[10.2,4],[9.8,4],[9.5,4.3],[9.5,4.7],[9.8,5]])

if __name__ == '__main__':
    try:
        rospy.init_node('lab6_move')
        pub = rospy.Publisher('/turtle1/wish',Point,queue_size=1)
        rospy.Subscriber('/turtle1/it_moving',Bool,callback)
        thread = threading.Thread(target=send_points)
        thread.start()
        rospy.spin()
        thread.join()
    except rospy.ROSInterruptException:
        pass
