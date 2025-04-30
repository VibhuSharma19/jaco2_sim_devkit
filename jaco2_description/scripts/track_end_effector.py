#!/usr/bin/python3

import rclpy, cv2
from rclpy.node import Node
import numpy as np
import rclpy.time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import TransformStamped
from jaco2_utils.conversions import Conversions
from tf2_ros import TransformException


class TrackEndEffector(Node):
   """
   TrackEndEffector
      A class to publish the position and orientation of the end-effector link with respect to world link
      for the Jaco2 manipulator. The position and angles are than displayed in window and updated continously.    
   """   

   def __init__(self):
      super().__init__('track_ee')

      self.tf_buffer = Buffer()
      self.tf_listener = TransformListener(self.tf_buffer, self)

      self.output_timer = self.create_timer(1.0, self.on_timer)

   def on_timer(self):
      """
      on_timer
         The callback function, called at regular interval to get the latest position and orientation of the end-effector
         wrt world frame.
      """

      self.target_frame = 'jaco2_end_effector'
      self.source_frame = 'world'

      try:
         t = self.tf_buffer.lookup_transform(self.target_frame, self.source_frame, rclpy.time.Time())

         translation = t.transform.translation
         rotation = t.transform.rotation

         quaternion = [rotation.x, rotation.y, rotation.z, rotation.w]
         euler_deg = Conversions.quaternion_to_euler(quaternion, True)
         euler_rad = Conversions.quaternion_to_euler(quaternion)

         self.display(translation, euler_deg)

         self.get_logger().info(f"The position and orientation of Jaco2 end-effector are:")
         self.get_logger().info(f"Translation: [{translation.x: .4f}, {translation.y: .4f}, {translation.z: .4f}]")
         self.get_logger().info(f"Euler angles (degrees): {[f'{angle:.2f}' for angle in euler_deg]}")
         self.get_logger().info(f"Euler angles (radians): {[f'{angle:.2f}' for angle in euler_rad]}")
         self.get_logger().info(f"Quaternion: {[f'{angle:.4f}' for angle in quaternion]}")
         
      except TransformException as ex:
         self.get_logger().info(f'Could not transform {self.target_frame} to {self.source_frame}: {ex}')

   def display(self, translation, euler_deg):
      """
      display
         displays the position and orintation angles of the end-effector in a window using OpenCV.

      Args:
          translation (geometry_msgs.msg.TransformedStamped):  translation part of the recieved tranform msg from the tf_lookup tranform.
          euler_deg (list): orientation of the end-effector in a list as [roll, pitch, yaw]
      """
      
      bg_color = (200, 180, 240)  # (B, G, R) format
      img = np.full((250, 600, 3), bg_color, dtype=np.uint8)

      translation_list = [translation.x, translation.y, translation.z]

      cv2.putText(img, "End-Effector Pose Display", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.9, (0, 0, 255), 2, cv2.LINE_AA)
      cv2.putText(img, "Translation (m)", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.7, (0, 0, 0), 2, cv2.LINE_AA)
      cv2.putText(img, "Euler Angles (deg)", (340, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                  0.7, (0, 0, 0), 2, cv2.LINE_AA)
      
      # Display values in two columns
      labels = ["X", "Y", "Z"]
      angles = ["Roll", "Pitch", "Yaw"]

      for i in range(3):
          # Left column: Translation values
          cv2.putText(img, f"{labels[i]}: {translation_list[i]:.4f}", (50, 140 + i * 40), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
          
          # Right column: Euler angles
          cv2.putText(img, f"{angles[i]}: {euler_deg[i]:.2f}", (340, 140 + i * 40), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
          
      cv2.imshow("Pose Display", img)
      cv2.waitKey(1)


def main():
   rclpy.init()
   node = TrackEndEffector()

   try:
      rclpy.spin(node)
   except KeyboardInterrupt:
      pass
   finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
   main()
