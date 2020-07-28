#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt8

rospy.init_node('tf_tester')
pub0 = rospy.Publisher('traffic_light_0_topic', UInt8, queue_size=10)
pub1 = rospy.Publisher('traffic_light_1_topic', UInt8, queue_size=10)
pub2 = rospy.Publisher('traffic_light_2_topic', UInt8, queue_size=10)

rate = rospy.Rate(1)

def start_talker():
    msg = UInt8()
    counter = 0
    while not rospy.is_shutdown():
        msg.data = counter % 3
        pub0.publish(msg)
        msg.data = (counter % 3 + 1) % 3
        pub1.publish(msg)
        msg.data = (counter % 3 + 2) % 3
        pub2.publish(msg)

        counter += 1
        rate.sleep()

try:
    start_talker()
except (rospy.ROSInterruptException, KeyboardInterrupt):
    rospy.logerr('Exception catched')
