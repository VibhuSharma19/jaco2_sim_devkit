#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class JSPGUIController(Node):
    """Controller for using the Joint_State_Publisher
     GUI interface for controlling manipulator joints in Gazebo simulation. 
    """    
    
    def __init__(self):
        super().__init__(node_name="JSPGUI_Controller")

        self.arm_pub_ = self.create_publisher(msg_type=JointTrajectory, topic='arm_controller/joint_trajectory', qos_profile=10)
        self.gripper_pub_ = self.create_publisher(msg_type=JointTrajectory, topic='gripper_controller/joint_trajectory', qos_profile=10)
        self.jsp_sub_ = self.create_subscription(msg_type=JointState, topic='joint_commands', callback=self.JSPCallback, qos_profile=10)

        self.get_logger().info(message="Joint_State_Publisher GUI Controller Started")

    def JSPCallback(self, msg:JointState):
        """
        Callback function which commands the joint controllers with the input joint position values

        Args:
            msg : joint position values from the Joint_State_Publisher GUI tool
        """
        
        self.arm_controller = JointTrajectory()
        self.gripper_controller = JointTrajectory()
        self.arm_controller.joint_names = ["jaco2_joint_1", "jaco2_joint_2", "jaco2_joint_3", "jaco2_joint_4", "jaco2_joint_5", "jaco2_joint_6", "jaco2_joint_7" ]
        self.gripper_controller.joint_names = ["jaco2_joint_finger_1", "jaco2_joint_finger_tip_1"]


        self.arm_cmd = JointTrajectoryPoint()
        self.gripper_cmd = JointTrajectoryPoint()

        self.arm_cmd.positions = msg.position[:7]
        self.gripper_cmd.positions = msg.position[7:9]

        self.arm_controller.points.append(self.arm_cmd)
        self.gripper_controller.points.append(self.gripper_cmd)

        self.arm_pub_.publish(self.arm_controller)
        self.gripper_pub_.publish(self.gripper_controller)

def main():

    rclpy.init()

    jsp_controller = JSPGUIController()
    rclpy.spin(jsp_controller)

    jsp_controller.destroy_node()
    rclpy.shutdown()

if __name__== '__main__':
    main()