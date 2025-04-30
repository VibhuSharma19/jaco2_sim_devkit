#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from moveit_msgs.msg import PlanningScene, CollisionObject
from geometry_msgs.msg import Pose
from shape_msgs.msg import SolidPrimitive

class ScenePublisher(Node):
    """
    A class to manage publishing collision objects to the planning scene in a ROS 2 environment.

    This class initializes a ROS 2 node and provides functionality to publish collision objects
    to the `/monitored_planning_scene` topic. It is designed to interact with the MoveIt planning scene
    for robotic motion planning.
    """
    def __init__(self, node_name='scene_publisher'):
        """
        Initializes the ScenePublisher with a ROS 2 node and a publisher for the planning scene.
        """
        super().__init__(node_name)
        self.publisher = self.create_publisher(PlanningScene, '/planning_scene', QoSProfile(depth=10))

    def publish_object(self):
        """
        Publishes a collision object to the planning scene.
        """
        objPose = Pose()
        objPose.position.x = 0.35
        objPose.position.y = 0.38
        objPose.position.z = 0.3
        objPose.orientation.w = 1.0
        objPose.orientation.x = 0.0
        objPose.orientation.y = 0.0
        objPose.orientation.z = 0.0

        objbody = SolidPrimitive()
        objbody.type = SolidPrimitive.CYLINDER
        objbody.dimensions = [0.3, 0.03]

        coll_obj = CollisionObject()
        coll_obj.header.frame_id = "world"
        coll_obj.id = "cylinder"
        coll_obj.primitives.append(objbody)
        coll_obj.primitive_poses.append(objPose)
        coll_obj.operation = CollisionObject.ADD

        scene = PlanningScene()
        scene.is_diff = True
        scene.world.collision_objects.append(coll_obj)
        self.publisher.publish(scene)
        self.get_logger().info(f"Published object '{coll_obj.id}' to the planning scene.")

def main():
    rclpy.init()
    node = ScenePublisher()
    node.publish_object()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
