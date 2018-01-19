#!/usr/bin/env python

import math as m

import rospy
# import numpu as np
from geometry_msgs.msg import Pose
from sensor_msgs.msg import JointState

import foo

nodename = 'joints_cmd_publisher'
dR_topic = 'cmd_dR'
joints_topic = '/arm_command'

params = foo.load_params_from_xacro()
l1 = params['l1']
l2 = params['l2']
l3 = params['l3']
l4 = params['l4']
l5 = params['l5']
l6 = params['l6']
# l1 = 0.3
# l2 = 0.5
# l3 = 0.5
# l4 = 0.3
# l5 = 0.3
# l6 = 0.3
l34 = l3 + l4
elbow = 1  # 1 for top elbow, -1 for bottom


class Publisher:
    node = rospy.init_node(nodename)
    cmd_joint_state = JointState()
    cmd_joint_state.name = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    cmd_joint_state.header.seq = 0
    cmd_joint_state.position[0:5] = [0 for x in range(6)]

    Hz = 100
    rate = rospy.Rate(100)

    def __init__(self):

        self.sub = rospy.Subscriber(dR_topic, Pose, self.get_coordinates)
        self.pub = rospy.Publisher(joints_topic, JointState, queue_size=10)

        while not rospy.is_shutdown():
            self.pub.publish(self.cmd_joint_state)
            self.rate.sleep()

    def get_coordinates(self, data):
        """
        :param data:
        :type data: Pose
        :return:
        """
        x = data.position.x
        y = data.position.y
        z = data.position.z
        r = (x ** 2 + y ** 2) ** 0.5
        h = z - l1

        if r == 0:
            t1 = 0;
        else:
            t1 = m.atan2(y / r, x / r)

        d = (r ** 2 + h ** 2) ** 0.5
        if d > l2 + l34 or d < min([abs(i) for i in [l2 - l34, l34 - l2]]):
            return

        inner_close = m.acos((l2 ** 2 + d ** 2 - l34 ** 2) / (2 * l2 * d))
        inner_central = m.acos(-(d ** 2 - l2 ** 2 - l34 ** 2) / (2 * l2 * l34))
        t2 = m.atan2(h, r) + elbow * inner_close
        t3 = -elbow * (m.pi - inner_central)

        x = m.cos(t1) * (l2 * m.cos(t2) + l34 * m.cos(t2 + t3))
        y = m.sin(t1) * (l2 * m.cos(t2) + l34 * m.cos(t2 + t3))
        z = l1 + (l2 * m.sin(t2) + l34 * m.sin(t2 + t3))

        print("angles = [ {}, {}, {} ]".format(round(inner_close * 180 / m.pi, 1), round(inner_central * 180 / m.pi, 1),
                                               round((m.pi - inner_central - inner_close) * 180 / m.pi, 1)))
        print("t1,t2,t3 = [ {}, {}, {} ]".format(round(t1 * 180 / m.pi, 1), round(t2 * 180 / m.pi, 1),
                                                 round(t3 * 180 / m.pi, 1)))
        print("XYZ = [ {}, {}, {} ]".format(round(x, 4), round(y, 4), round(z, 4)))

        self.cmd_joint_state.position[0] = t1
        self.cmd_joint_state.position[1] = t2
        self.cmd_joint_state.position[2] = t3

    def get_coordinates_2(self, data):
        """
        :param data:
        :type data: Pose
        :return:
        """

        x = data.position.x
        y = data.position.y
        z = data.position.z
        r = (x ** 2 + y ** 2) ** 0.5
        h = z - l1

        if r > 0:
            print("r > 0")
            d = (r ** 2 + h ** 2 - l2 ** 2 - l34 ** 2) / (2 * l2 * l34)

            t1 = m.atan2(y / r, x / r)
            t3 = m.atan2(elbow * m.sqrt(1 - d ** 2), d)
            t2 = m.atan2(h, r) - m.atan2(l34 * m.sin(t3), l2 + l34 * m.cos(3))

            self.cmd_joint_state.position[0] = t1
            self.cmd_joint_state.position[1] = t2
            self.cmd_joint_state.position[2] = t3

        elif r < 0:
            print("r < 0")
            r = -r
            d = (r ** 2 + h ** 2 - l2 ** 2 - l34 ** 2) / (2 * l2 * l34)

            t1 = m.atan2(-y / r, -x / r)
            t3 = m.atan2(elbow * m.sqrt(1 - d ** 2), d)
            t2 = m.atan2(h, r) - m.atan2(l34 * m.sin(t3), l2 + l34 * m.cos(3))

            self.cmd_joint_state.position[0] = t1
            self.cmd_joint_state.position[1] = t2
            self.cmd_joint_state.position[2] = t3

        else:
            d = (r ** 2 + h ** 2 - l2 ** 2 - l34 ** 2) / (2 * l2 * l34)

            t1 = 0
            t3 = m.atan2(elbow * m.sqrt(1 - d ** 2), d)
            t2 = m.atan2(h, r) - m.atan2(l34 * m.sin(t3), l2 + l34 * m.cos(3))

            self.cmd_joint_state.position[0] = t1
            self.cmd_joint_state.position[1] = t2
            self.cmd_joint_state.position[2] = t3

        x = m.cos(t1) * (l2 * m.cos(t2) + l34 * m.cos(t2 + t3))
        y = m.sin(t1) * (l2 * m.cos(t2) + l34 * m.cos(t2 + t3))
        z = l1 + (l2 * m.sin(t2) + l34 * m.sin(t2 + t3))

        print("XYZ = [ {}, {}, {} ]".format(round(x, 4), round(y, 4), round(z, 4)))


if __name__ == '__main__':
    try:
        Publisher()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
