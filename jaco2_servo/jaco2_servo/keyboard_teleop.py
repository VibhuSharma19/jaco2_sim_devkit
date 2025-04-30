#!/usr/bin/python3

import pygame
import rclpy
from rclpy.node import Node
from control_msgs.msg import JointJog
from geometry_msgs.msg import TwistStamped
from moveit_msgs.srv import ServoCommandType
from dataclasses import dataclass
import threading

# Initialize pygame before using it
pygame.init()


@dataclass
class KeyCodes:
    """ Mapping of keys to their respective pygame key constants. """
    KEYCODE_RIGHT = pygame.K_RIGHT
    KEYCODE_LEFT = pygame.K_LEFT
    KEYCODE_UP = pygame.K_UP
    KEYCODE_DOWN = pygame.K_DOWN
    KEYCODE_PERIOD = pygame.K_PERIOD
    KEYCODE_SEMICOLON = pygame.K_SEMICOLON
    KEYCODE_1 = pygame.K_1
    KEYCODE_2 = pygame.K_2
    KEYCODE_3 = pygame.K_3
    KEYCODE_4 = pygame.K_4
    KEYCODE_5 = pygame.K_5
    KEYCODE_6 = pygame.K_6
    KEYCODE_7 = pygame.K_7
    KEYCODE_Q = pygame.K_q
    KEYCODE_R = pygame.K_r
    KEYCODE_J = pygame.K_j
    KEYCODE_T = pygame.K_t
    KEYCODE_W = pygame.K_w
    KEYCODE_E = pygame.K_e
    KEYCODE_X = pygame.K_x


class PygameDisplay():
    """
    Display the instructions to use the keyboard teleoperation
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 380))
        pygame.display.set_caption("Keyboard Control")
        self.screen.fill((255, 255, 205))
        pygame.display.update()

        self.heading_font = pygame.font.SysFont("", 24, False, True)
        self.matter_font = pygame.font.SysFont("z003", 20, False, True)

        self.heading_font.set_underline(True)

    def display_text(self):
        """
        Render the display window and instructions to display
        """
        self.heading = "Keyboard Teleop Control"
        self.heading_surface = self.heading_font.render(self.heading, False, (250, 150, 100))
        self.screen.blit(self.heading_surface, (80, 20))
        
        self.matter = [
            "All commands are in the planning frame.",
            "Use arrow keys and the '.' and ';' keys to Cartesian jog.",
            "Use 1|2|3|4|5|6|7 keys to joint jog.",
            "Use 'r' to reverse the direction of jogging.",
            "Use 'w' to send command in planning frame.",
            "Use 'e' to send command in end effector frame.",
            "In command switch node: ",
            "   Use 't' to switch command to twist mode.",
            "   Use 'j' to switch command to joint-jog mode.",
            "Press 'Q' to quit both nodes."]
        
        y_offset = 0  # Tracks vertical spacing
        for line in self.matter:
            self.matter_surface = self.matter_font.render(line, False, (80, 100, 160))
            self.screen.blit(self.matter_surface, (20, 60 + y_offset))
            y_offset += 30


        pygame.display.update()
        pygame.time.Clock().tick(60)


class KeyboardServo(Node):
    """
    ROS2 Node to capture keyboard input using pygame and send servo commands.
    """
    def __init__(self):
        super().__init__('servo_keyboard_input')
        self.joint_pub = self.create_publisher(JointJog, '/servo_node/delta_joint_cmds', 10)
        self.twist_pub = self.create_publisher(TwistStamped, '/servo_node/delta_twist_cmds', 10)
        self.pygame_window = PygameDisplay()
        self.pygame_window.display_text()

        self.running = True
        self.get_logger().info("Keyboard Servo Controller Initialized.")

        self.planning_frame = "world"
        self.command_frame = "world"
        self.ee_frame = "jaco2_end_effector"
        self.joint_vel_cmd = 0.1

        self.pygame_thread = threading.Thread(target=self.key_loop, daemon=True)
        self.pygame_thread.start()

    def key_loop(self):
        """
        Main loop to read keyboard input and publish servo commands.
        """
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    self.process_key(event.key)

    def process_key(self, key: int):
        """
        Processes key inputs and sends initial ROS2 messages.
        """
        if key in (KeyCodes.KEYCODE_LEFT, KeyCodes.KEYCODE_UP, KeyCodes.KEYCODE_DOWN, KeyCodes.KEYCODE_PERIOD, KeyCodes.KEYCODE_RIGHT, KeyCodes.KEYCODE_SEMICOLON):
            self.publish_twist_cmd(key)
        elif key in (KeyCodes.KEYCODE_1, KeyCodes.KEYCODE_2, KeyCodes.KEYCODE_3, KeyCodes.KEYCODE_4, KeyCodes.KEYCODE_5, KeyCodes.KEYCODE_6, KeyCodes.KEYCODE_7):
            self.publish_joint_cmd(key)
        elif key == KeyCodes.KEYCODE_R:
            self.get_logger().info("Reversing the joint motion direction")
            self.joint_vel_cmd *= -1
        elif key == KeyCodes.KEYCODE_W:
            self.get_logger().info(f"Command frame set to: {self.planning_frame}")
            self.command_frame = self.planning_frame
        elif key == KeyCodes.KEYCODE_E:
            self.get_logger().info(f"Command frame set to: {self.ee_frame}")
            self.command_frame = self.ee_frame
        elif key == KeyCodes.KEYCODE_Q:
            self.quit()

    def publish_twist_cmd(self, key: int):
        """
        Publishes TwistStamped messages for Cartesian movements.
        """
        self.twist_msg = TwistStamped()
        self.twist_msg.header.stamp = self.get_clock().now().to_msg()
        self.twist_msg.header.frame_id = self.command_frame

        if key == KeyCodes.KEYCODE_LEFT:
            self.get_logger().info(f"Moving left")
            self.twist_msg.twist.linear.y = - 0.2
        elif key == KeyCodes.KEYCODE_RIGHT:
            self.get_logger().info(f"Moving right")
            self.twist_msg.twist.linear.y =  0.2
        elif key == KeyCodes.KEYCODE_UP:
            self.get_logger().info(f"Moving forward")
            self.twist_msg.twist.linear.x =  0.2
        elif key == KeyCodes.KEYCODE_DOWN:
            self.get_logger().info(f"Moving backward")
            self.twist_msg.twist.linear.x = - 0.2
        elif key == KeyCodes.KEYCODE_PERIOD:
            self.get_logger().info(f"Moving down")
            self.twist_msg.twist.linear.z = - 0.2
        elif key == KeyCodes.KEYCODE_SEMICOLON:
            self.get_logger().info(f"Moving upward")
            self.twist_msg.twist.linear.z =  0.2

        self.twist_pub.publish(self.twist_msg)

    def publish_joint_cmd(self, key: int):
        """
        Publishes JointJog messages for joint movements.
        """
        self.joint_msg = JointJog()
        self.joint_msg.header.stamp = self.get_clock().now().to_msg()
        self.joint_msg.joint_names = ["jaco2_joint_1", "jaco2_joint_2", "jaco2_joint_3", "jaco2_joint_4", "jaco2_joint_5", "jaco2_joint_6", "jaco2_joint_7"]
        self.joint_msg.velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        if key == KeyCodes.KEYCODE_1:
            self.get_logger().info(f"Moving joint 1")
            self.joint_msg.velocities[0] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_2:
            self.get_logger().info(f"Moving joint 2")
            self.joint_msg.velocities[1] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_3:
            self.get_logger().info(f"Moving joint 3")
            self.joint_msg.velocities[2] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_4:
            self.get_logger().info(f"Moving joint 4")
            self.joint_msg.velocities[3] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_5:
            self.get_logger().info(f"Moving joint 5")
            self.joint_msg.velocities[4] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_6:
            self.get_logger().info(f"Moving joint 6")
            self.joint_msg.velocities[5] = self.joint_vel_cmd
        elif key == KeyCodes.KEYCODE_7:
            self.get_logger().info(f"Moving joint 7")
            self.joint_msg.velocities[6] = self.joint_vel_cmd

        self.joint_pub.publish(self.joint_msg)

    def quit(self):
        """
        Handles shutdown and cleanup.
        """
        self.get_logger().info("Shutting down KeyboardServo...")
        self.running = False
        pygame.quit()
        rclpy.shutdown()

def main():
    rclpy.init()
    node = KeyboardServo()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(node)

    try:
     node.key_loop()
     executor.spin()
    except KeyboardInterrupt:
      pass
    finally:
      node.destroy_node()
      rclpy.shutdown()

if __name__ == '__main__':
    main()