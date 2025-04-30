#!/usr/bin/python3

import time
import rclpy
from rclpy.logging import get_logger
import rclpy.logging
from rclpy.node import Node
from moveit.planning import MoveItPy
from moveit.core.planning_scene import PlanningScene  # type: ignore
from geometry_msgs.msg import Pose
from moveit_msgs.msg import CollisionObject, ObjectColor
from shape_msgs.msg import SolidPrimitive 

class MoveitPlanning(Node):
    """Class to define the planning scene using collision objects"""

    def __init__(self):
       super().__init__("moveit_planning", enable_rosout=True)

       self.moveitpy = MoveItPy()
       self.jaco_arm = self.moveitpy.get_planning_component("jaco_arm")
       self.planning_scene = self.moveitpy.get_planning_scene_monitor()
       self.logger = get_logger("moveit_planning_scene")

    def collision_msg(self, header_frame:str, id_name:str, solid_object:SolidPrimitive, poses:Pose, operation:str): 
        """
        Create an instance of the moveit_msgs.msg.CollisionObject for adding collision object

        Args:
            header_frame: Name of the header frame ID
            id_name: The id used for command for the collision object
            solid_object: Instance of SolidPrimitive msg defining collision object to add (Box, Cylinder, Sphere, Cone)
            poses: Pose msg instance to define collision object position
            operation: operation to perform with the object (Add, Remove, Move, Append)

        Return:
            An instance of CollisonObject msg for adding to the planning scene
        """
        collision_obj = CollisionObject()

        collision_obj.header.frame_id = header_frame
        collision_obj.id = id_name
        collision_obj.primitives.append(solid_object)
        collision_obj.primitive_poses.append(poses)
        if operation == "add": collision_obj.operation = CollisionObject.ADD
        elif operation == "remove": collision_obj.operation = CollisionObject.REMOVE
        elif operation == "append": collision_obj.operation = CollisionObject.APPEND
        elif operation == "move": collision_obj.operation = CollisionObject.MOVE
        else: print("Undefined operation")

        return collision_obj

    def create_pose(self, positions:list[int]):
        """
        Create a 3D position for collision object

        Args:
            positions (list[int]): 3D position at which the object be placed

        Returns:
            An instance of Pose msg
        """
        pose = Pose()
        pose.position.x = positions[0]; pose.position.y = positions[1]; pose.position.z = positions[2]

        return pose

    def solid_primitive(self, object_type:str, dimensions:list[int]):
        """
        Create a solid primitive for collision object creation

        Args:
            object_type: Type of solid object to create. (Box, Cylinder, Sphere, Cone)
            dimensions: Dimensions of the object as per object_type
                For type BOX, the X, Y, and Z dimensions are required as the length of the corresponding sides of the box; 
                For the SPHERE type, only one component is needed, and it gives the radius of the sphere;
                For the CYLINDER and CONE types, the center line is oriented along the Z axis, hence the CYLINDER_HEIGHT (CONE_HEIGHT) component of dimensions gives the height of the cylinder (cone).
                The CYLINDER_RADIUS (CONE_RADIUS) component of dimensions gives the radius of the base of the cylinder (cone).

        Return:
            An instance of the SolidPrimitive msg 
        """

        solid_object = SolidPrimitive()
        if object_type == "box": solid_object.type = SolidPrimitive.BOX
        elif object_type == "sphere": solid_object.type = SolidPrimitive.SPHERE
        elif object_type == "cylinder": solid_object.type = SolidPrimitive.CYLINDER
        elif object_type == "cone": solid_object.type = SolidPrimitive.CONE
        else: print("Undefined Solid object type")

        solid_object.dimensions = dimensions

        return solid_object
    
    def obj_color(self, obj_id:str, colour:list[int]):
        """
        Defines the colour of the object

        Args:
            obj_id: object id to set colour for.
            colour: an array of colour value (RGBA) definning the colour
        Returns:
            ObjectColour msg instance of the moveit_msgs group
        """
        obj_color = ObjectColor()
        obj_color.id = obj_id
        obj_color.color.r = colour[0]; obj_color.color.g = colour[1]; obj_color.color.b = colour[2]; obj_color.color.a = colour[3]

        return obj_color

    
    def add_collision_object(self, collision_msg:CollisionObject, color:ObjectColor):
        """
        Adds a collison obejct to the planning scene

        Args:
            collision_msg: CollisionObject msg defining the object to add
            color: color of the collision object 
        """
        scene = self.planning_scene.read_write().__enter__()

        scene.apply_collision_object(collision_object_msg=collision_msg, color_msg=color)
        scene.current_state.update()

    def remove_collision_object(self):
        """
        Removes all the collision object from the planning scene
        """
        scene = self.planning_scene.read_write().__enter__()

        scene.remove_all_collision_objects()
        scene.current_state.update()

    def check_collision(self, joint_grp_name:str, target_pose:Pose, tip_name:str):
        """
        Gives the status of collision for the given end-effector position for the joint_group_model

        Args:
            joint_grp_name: Name of te joint_group_model to check collision for.
            target_pose: End-effector position to set as target
            tip_name: name of the end-effector tip link
        """
        scene = self.planning_scene.read_write().__enter__()
        robot_state = scene.current_state

        original_state = robot_state.get_joint_group_positions(joint_model_group_name=joint_grp_name)
        robot_state.set_from_ik(joint_model_group_name=joint_grp_name, geometry_pose=target_pose, tip_name=tip_name)
        robot_state.update()

        collision_state = scene.is_state_colliding(robot_state=robot_state, joint_model_group_name=joint_grp_name,verbose=True)
        self.logger.info(f"The Robot collision status for the given pose is: {collision_state}")

        robot_state.set_joint_group_positions(joint_model_group_name=joint_grp_name, position_values=original_state)
        robot_state.update()

    def scene_update(self):
        """Updates the planning scene"""
        scene = self.planning_scene.read_write().__enter__()
        robot_state = scene.current_state
        robot_state.update()



def main(args=None):
    rclpy.init(args=args)

    moveit_scene = MoveitPlanning()

    box_color = moveit_scene.obj_color(obj_id="box", colour=[0.8, 0.4, 0.8, 1.0])
    box = moveit_scene.solid_primitive(object_type="cylinder", dimensions=[0.15, 0.08])
    box_pose = moveit_scene.create_pose(positions=[0.15, 0.2, 0.4])
    box_setup = moveit_scene.collision_msg(header_frame="world",id_name="cylinder", solid_object=box, poses=box_pose, operation="add")
    moveit_scene.add_collision_object(collision_msg=box_setup, color=box_color)
    moveit_scene.scene_update()

    time.sleep(10.0)

    moveit_scene.remove_collision_object()
    moveit_scene.scene_update()
    time.sleep(10.0)
    
    rclpy.shutdown()

if __name__ == '__main__':
    main()





