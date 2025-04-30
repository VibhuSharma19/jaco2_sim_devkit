#!/usr/bin/python3

import rclpy
import rclpy.logging
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header


class DepthImageRemap(Node):
   """
   ROS2 node to publish depth_images in corrected frame
   """

   def __init__(self):
        super().__init__('depth_image_remaper')

        # Subscriber and publisher
        self.subscription = self.create_subscription(
            Image,
            '/rgbd_camera/depth_image',
            self.image_callback,
            10)
        
        self.publisher = self.create_publisher(Image, '/rgbd_camera/corrected_depth_image', 10)

   def image_callback(self, msg: Image):
      """
      Callback function that republishes depth image in correct frame

      Args:
          msg: depth image from gazebosim sensor
      """

      new_msg = Image()
      
      new_msg.header = Header()
      new_msg.header.stamp = msg.header.stamp
      new_msg.header.frame_id = "rgbd_camera_frame"

      new_msg.height = msg.height
      new_msg.width = msg.width
      new_msg.encoding = msg.encoding
      new_msg.is_bigendian = msg.is_bigendian
      new_msg.step = msg.step
      new_msg.data = msg.data
      
      self.publisher.publish(new_msg)

def main():
    rclpy.init()
    node = DepthImageRemap()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()