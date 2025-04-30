#!/usr/bin/python3

import sys
import select
import termios
import tty
import threading
import rclpy
from rclpy.node import Node
from moveit_msgs.srv import ServoCommandType

class CommandSwitch(Node):
    """
        Node to switch command type of servo control between JointJog and Twist commands.
    """
    def __init__(self):
        super().__init__('command_switch')
        self.srv_client = self.create_client(ServoCommandType, '/servo_node/switch_command_type')

        while not self.srv_client.wait_for_service(5.0):
            self.get_logger().info('Service not available, waiting again...')

        self.running = True
        self.get_logger().info("Servo Command Initialized.")

        # Save original terminal settings
        self.original_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin)  # Set terminal to cbreak mode

        # Start the keyboard listener in a separate thread
        self.keyboard_thread = threading.Thread(target=self.key_loop, daemon=True)
        self.keyboard_thread.start()

    def key_loop(self):
        """ Monitors keyboard input asynchronously using sys.stdin. """
        while self.running:
            if self.is_key_pressed():
                key = sys.stdin.read(1)
                if key == 'j':
                    self.get_logger().info("Switching to JointJog mode")
                    self.cmd_joint_jog()
                elif key == 't':
                    self.get_logger().info("Switching to Twist mode")
                    self.cmd_twist_jog()
                elif key == 'q':
                    self.quit()
                    break  # Stop the loop

    def is_key_pressed(self):
        """ Checks if a key is pressed without blocking. """
        return select.select([sys.stdin], [], [], 0)[0] != []

    def cmd_joint_jog(self):
        """ Calls the ROS2 service to switch to JointJog mode. """
        self.call_service(ServoCommandType.Request.JOINT_JOG)

    def cmd_twist_jog(self):
        """ Calls the ROS2 service to switch to Twist mode. """
        self.call_service(ServoCommandType.Request.TWIST)

    def call_service(self, command_type):
        """ Runs the service call in a separate thread. """
        thread = threading.Thread(target=self._call_service, args=(command_type,))
        thread.start()

    def _call_service(self, command_type):
        req = ServoCommandType.Request()
        req.command_type = command_type
        response = self.srv_client.call(req)
        if response.success:
            self.get_logger().info(f"Switched to input type: {command_type}")
        else:
            self.get_logger().warn(f"Failed to switch input to: {command_type}")

    def quit(self):
        """ Handles shutdown and cleanup. """
        self.get_logger().info("Shutting down KeyboardServo...")
        self.running = False
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)  # Restore terminal settings
        rclpy.shutdown()

def main():
    rclpy.init()
    node = CommandSwitch()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, node.original_settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
