#!/usr/bin/env python
import roslib
import rospy

import tf
import sensor_msgs.msg
l1 = 0.4
l3 = 1.0
l4 = 0.7
br = tf.TransformBroadcaster()

def callback_tf(msg):
    #rospy.logdebug('Callback invoked')
    global br
    #print(msg)
    br.sendTransform( (0, 0, l1/2), 
                     tf.transformations.quaternion_from_euler(0,0,msg.position[0]),
                     rospy.Time.now(),
                     "link1",
                     "world")
    br.sendTransform( (0, 0, l1/2), 
                     tf.transformations.quaternion_from_euler(msg.position[1],0,0),
                     rospy.Time.now(),
                     "link2",
                     "link1")
    br.sendTransform( (0,l3, 0), 
                     tf.transformations.quaternion_from_euler(msg.position[2],0,0),
                     rospy.Time.now(),
                     "link3",
                     "link2")
    #br.sendTransform( (0,l3, 0), 
                     #tf.transformations.quaternion_from_euler(0,msg.position[3],0),
                     #rospy.Time.now(),
                     #"link4",
                     #"link3")
    #br.sendTransform( (0,l4, 0), 
                     #tf.transformations.quaternion_from_euler(-msg.position[4],0,0),
                     #rospy.Time.now(),
                     #"link5",
                     #"link4")
    #br.sendTransform( (0,0, 0), 
                     #tf.transformations.quaternion_from_euler(0,msg.position[5],0),
                     #rospy.Time.now(),
                     #"link6",
                     #"link5")
    #br.sendTransform( (0,0, 0), 
                     #tf.transformations.quaternion_from_euler(0,msg.position[5],0),
                     #rospy.Time.now(),
                     #"link7",
                     #"link6")
    #br.sendTransform( (0, 0.0,0.0), 
                     #tf.transformations.quaternion_from_euler(0,0,0),
                     #rospy.Time.now(),
                     #"end_ball",
                     #"link7")
    
if __name__ == '__main__':
    rospy.init_node('my_robotic_arm_tf_broadcaster')
    #rospy.init_node('ManipuH_tf_broadcaster', log_level = rospy.DEBUG)
    #turtlename = rospy.get_param('~turtle')
    rospy.logwarn('my_robotic_arm_tf_broadcaster started.')
    rospy.Subscriber('/my_robotic_arm/joint_states', sensor_msgs.msg.JointState, callback_tf)
    rospy.spin()
    
        