#!/usr/bin/python2

import math
import os
import string

import rospy
from std_msgs.msg import String

SIZE_IN_MB = int(os.getenv('SIZE_IN_MB', 1024))

_1KB_STRING = string.printable*10+string.printable[:24]
_1MB_STRING = _1KB_STRING * 1024
NUM_OF_MB = 100

MSG = _1MB_STRING * NUM_OF_MB


rospy.init_node('heavy_talker', anonymous=True)
pub = rospy.Publisher('heavy_talker', String, queue_size=10)
rate = rospy.Rate(1)

try:
    num = int(math.ceil(SIZE_IN_MB / NUM_OF_MB))
    rospy.loginfo('will publish {} msgs of {}MB each'.format(num, NUM_OF_MB))
    rospy.loginfo('total {}MB will be sent'.format(SIZE_IN_MB))
    for _ in range(num+1):
        if rospy.is_shutdown():
            break
        rospy.loginfo('publishing...')
        pub.publish(MSG)
        rospy.loginfo('published')
        rate.sleep()
except rospy.ROSInterruptException:
    pass

