#!/usr/bin/python2

import os
import string

import rospy
from std_msgs.msg import String

SIZE_IN_MB = int(os.getenv('SIZE_IN_MB', 1024))  # total size of bag file
MSG_SIZE_IN_MB = 100
MSG_INTERVAL = 5

_1KB_STRING = string.printable*10+string.printable[:24]
_1MB_STRING = _1KB_STRING * 1024
MSG = _1MB_STRING * MSG_SIZE_IN_MB

rospy.init_node('heavy_talker', anonymous=True)
pub = rospy.Publisher('heavy_talker', String, queue_size=1)
rate = rospy.Rate(1.0 / MSG_INTERVAL)

try:
    num = (SIZE_IN_MB // MSG_SIZE_IN_MB) or 1  # must send at least one message
    rospy.loginfo('will publish {} msgs of {}MB each, every {}s'.format(num, MSG_SIZE_IN_MB, MSG_INTERVAL))
    for i in range(1, num+1):
        if rospy.is_shutdown():
            break
        rospy.loginfo('publishing {}/{}...'.format(i, num))
        pub.publish(MSG)
        rospy.loginfo('published')
        rate.sleep()

    rospy.loginfo('msgs sent. just spinning now...')
    rospy.spin()
except rospy.ROSInterruptException:
    pass
