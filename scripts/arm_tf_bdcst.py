#!/usr/bin/env python
import rospy
import sensor_msgs.msg
import tf

l1 = 0.4
l3 = 1.0
l4 = 0.7
br = tf.TransformBroadcaster()


def callback_tf(msg):
    # rospy.logdebug('Callback invoked')
    global br
    # print(msg)
    br.sendTransform((0, 0, l1 / 2),
                     tf.transformations.quaternion_from_euler(0, 0, msg.position[0]),
                     rospy.Time.now(),
                     "joint1",
                     "world")
    br.sendTransform((0, 0, l1 / 2),
                     tf.transformations.quaternion_from_euler(msg.position[1], 0, 0),
                     rospy.Time.now(),
                     "joint2",
                     "joint1")


if __name__ == '__main__':
    rospy.init_node('my_robotic_arm_tf_broadcaster')
    # rospy.init_node('ManipuH_tf_broadcaster', log_level = rospy.DEBUG)
    # turtlename = rospy.get_param('~turtle')
    rospy.loginfo('my_robotic_arm_tf_broadcaster started.')
    rospy.Subscriber('/my_robotic_arm/joint_states', sensor_msgs.msg.JointState, callback_tf)
    rospy.spin()
    
        