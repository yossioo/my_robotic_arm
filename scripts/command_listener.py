#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64

node_name = 'command_listener'
command_topic = '/arm_command'
j1_topic = '/my_robotic_arm/joint1_position/command'
j2_topic = '/my_robotic_arm/joint2_position/command'
j3_topic = '/my_robotic_arm/joint3_position/command'
j4_topic = '/my_robotic_arm/joint4_position/command'
j5_topic = '/my_robotic_arm/joint5_position/command'
j6_topic = '/my_robotic_arm/joint6_position/command'


class Publisher:

    def __init__(self):
        rospy.init_node(node_name)
        hz = 100
        self.rate = rospy.Rate(hz)

        self.sub = rospy.Subscriber(command_topic, JointState, self.send_command)
        self.pub1 = rospy.Publisher(j1_topic, Float64, queue_size=10)
        self.pub2 = rospy.Publisher(j2_topic, Float64, queue_size=10)
        self.pub3 = rospy.Publisher(j3_topic, Float64, queue_size=10)
        self.pub4 = rospy.Publisher(j4_topic, Float64, queue_size=10)
        self.pub5 = rospy.Publisher(j5_topic, Float64, queue_size=10)
        self.pub6 = rospy.Publisher(j6_topic, Float64, queue_size=10)

        rospy.spin()

    def send_command(self, data):
        """

        :param data:
        :type data: JointState
        :return:
        """
        self.pub1.publish(data.position[data.name.index('j1')])
        self.pub2.publish(data.position[data.name.index('j2')])
        self.pub3.publish(data.position[data.name.index('j3')])
        self.pub4.publish(data.position[data.name.index('j4')])
        self.pub5.publish(data.position[data.name.index('j5')])
        self.pub6.publish(data.position[data.name.index('j6')])


if __name__ == '__main__':
    try:
        Publisher()
    except rospy.ROSInterruptException:
        pass
