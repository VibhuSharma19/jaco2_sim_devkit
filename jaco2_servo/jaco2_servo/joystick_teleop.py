#!/usr/bin/python3

import rclpy, threading
from rclpy.node import Node
from sensor_msgs.msg import Joy
from control_msgs.msg import JointJog
from geometry_msgs.msg import TwistStamped
from std_srvs.srv import Trigger
from moveit_msgs.srv import ServoCommandType
from dataclasses import dataclass

@dataclass
class Xbox360Axes:
    """
     Dataclass to capture Axes of the joy msg
    """
    LEFT_STICK_X: int = 0
    LEFT_STICK_Y: int = 1
    RIGHT_STICK_X: int = 3
    RIGHT_STICK_Y: int = 4
    LT: int = 2  # Left Trigger
    RT: int = 5  # Right Trigger
    DPAD_X: int = 6
    DPAD_Y: int = 7

@dataclass
class Xbox360Buttons:
    """
     Dataclass to capture Buttons of the joy msg
    """
    A: int = 0
    B: int = 1
    X: int = 2
    Y: int = 3
    LB: int = 4
    RB: int = 5
    SELECT: int = 6
    START: int = 7
    MODE: int = 8
    LEFT_THUMB: int = 9
    RIGHT_THUMB: int = 10

class Xbox360Teleop(Node):
    """
    Xbox360Teleop: Class for controlling the movement pf the Jaco2 manipulator with 
    Microsoft Xbox360 type gamepad.
    """

    def __init__(self):
        """
        Initializes publishers, subscriber and server clients and variables for control and commanding
        """
        super().__init__('xbox360_teleop')
        self.declare_parameter('frame_id', 'world')
        self.frame_id = self.get_parameter('frame_id').value
        
        self.joint_pub = self.create_publisher(JointJog, '/servo_node/delta_joint_cmds', 10)
        self.twist_pub = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds', 10)
        self.servo_node_start_client = self.create_client(Trigger, "/servo_node/start_servo")
        self.servo_node_stop_client = self.create_client(Trigger, "/servo_node/stop_servo")
        self.switch_command_client = self.create_client(ServoCommandType, '/servo_node/switch_command_type')
        
        self.joy_sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        
        self.current_mode = '' # Modes: 'joint_jog', 'twist'
        self.teleop_active = False
        

    def joy_callback(self, msg: Joy):
        """
        Commands the servo node for required motion with the received joy msg from the gamepad

        Args:
            msg (Joy): msg from the joystick controller
        """
        if msg.buttons[Xbox360Buttons.START]:
            self.toggle_teleop()
        
        if msg.buttons[Xbox360Buttons.MODE]:
            self.switch_command_mode()
        
        if self.teleop_active:
            if self.current_mode == 'joint_jog':
                self.publish_joint_jog(msg)
            else:
                self.publish_twist(msg)
    

    def publish_joint_jog(self, msg: Joy):
        """
        Control the movement of individual Jaco2 arm joints using the buttons of the gamepad

        Args:
            msg (Joy): gamepad joy msg
        """
        joint_jog = JointJog()
        joint_jog.header.stamp = self.get_clock().now().to_msg()
        joint_jog.joint_names = ["jaco2_joint_1", "jaco2_joint_2", "jaco2_joint_3", "jaco2_joint_4", "jaco2_joint_5", "jaco2_joint_6", "jaco2_joint_7"]
        joint_jog.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        for i in range(7):
            if msg.buttons[i]:
                joint_jog.velocities[i] = -0.5 if msg.buttons[Xbox360Buttons.LEFT_THUMB] else 0.5
        
        self.joint_pub.publish(joint_jog)
    

    def publish_twist(self, msg: Joy):
        """
        Controls the motion of the end-effector of the Jaco2 arm with the axes controllers of the gamepad

        Args:
            msg (Joy): gamepad joy msg
        """
        twist = TwistStamped()
        twist.header.stamp = self.get_clock().now().to_msg()
        twist.header.frame_id = self.frame_id

        twist.twist.linear.z = msg.axes[Xbox360Axes.RIGHT_STICK_Y]
        twist.twist.linear.y = msg.axes[Xbox360Axes.RIGHT_STICK_X]

        lin_x_right = -0.5 * (msg.axes[Xbox360Axes.RT])
        lin_x_left = 0.5 * (msg.axes[Xbox360Axes.LT])
        twist.twist.linear.x = lin_x_right + lin_x_left

        twist.twist.angular.y = msg.axes[Xbox360Axes.LEFT_STICK_Y]
        twist.twist.angular.x = msg.axes[Xbox360Axes.LEFT_STICK_X]
        
        twist.twist.angular.z = msg.axes[Xbox360Axes.DPAD_X]

        self.twist_pub.publish(twist)
    

    def toggle_teleop(self):
        """
        Toggles between stopping and starting of the teleop operation using 'START' button of gamepad
        """

        if self.teleop_active:
            self.get_logger().info("Stopping teleop")
            try:
                self.servo_node_stop_client.wait_for_service(5.0)
                self.servo_node_stop_client.call_async(Trigger.Request())
                self.teleop_thread.join()
            except Exception as e:
                print(e)

        else:
            self.get_logger().info("Starting teleop")
            try:
                self.servo_node_start_client.wait_for_service(5.0)
                self.servo_node_start_client.call_async(Trigger.Request())
            except Exception as e:
                print(e)
        
        self.teleop_active = not self.teleop_active
    

    def switch_command_mode(self):
        """
        Switches between the Joint and Twist control modes for the Jaco2 arm using 'MODE' button from gamepad
        """
        req = ServoCommandType.Request()

        if self.current_mode == "" or self.current_mode == "twist":
            req.command_type = ServoCommandType.Request.JOINT_JOG
            self.get_logger().info("Switching command type to JointJog")
            self.req_mode = "joint_jog"
        elif self.current_mode == "joint_jog":
            req.command_type = ServoCommandType.Request.TWIST
            self.get_logger().info("Switching command type to Twist")
            self.req_mode = "twist"
        else:
            self.get_logger().warn("Incorrect mode of command")
            return 

        future = self.switch_command_client.call_async(req)
        future.add_done_callback(self.update_mode)

    def update_mode(self, future):
        try:
            response = future.result()
            if response.success:
                self.current_mode = self.req_mode 
                self.get_logger().info(f"Switched to {self.current_mode} mode")
            else:
                self.get_logger().warn("Failed to switch modes")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = Xbox360Teleop()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
