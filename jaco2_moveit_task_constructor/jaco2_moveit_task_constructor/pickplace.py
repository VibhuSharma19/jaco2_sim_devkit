#!/usr/bin/python3

import rclcpp
from moveit.task_constructor import core, stages
from geometry_msgs.msg import PoseStamped, TwistStamped, Pose
from moveit_msgs.msg import Constraints, OrientationConstraint, CollisionObject, PlanningScene
from rclpy.qos import QoSProfile
from shape_msgs.msg import SolidPrimitive
from jaco2_utils.conversions import Conversions
import math, time

def main():
   rclcpp.init()
   node = rclcpp.Node("mtc_pickplace")

   arm = "jaco_arm"
   eef = "jaco_gripper"

   task = core.Task()
   task.name = "pickplace"
   task.loadRobotModel(node)

   task.add(stages.CurrentState("current_state"))
   task.enableIntrospection()

   pipeline = core.PipelinePlanner(node, "pilz_industrial_motion_planner", "PTP")
   planner = [(arm, pipeline)]
   
   task.add(stages.Connect("connect",planner))

   graspGenerator = stages.GenerateGraspPose()
   graspGenerator.angle_delta = math.pi/4.0
   graspGenerator.pregrasp = "Open"
   graspGenerator.grasp = "Close"
   graspGenerator.object = "cylinder"
   graspGenerator.setMonitoredStage(task["current_state"])
   
   simpleGrasp = stages.SimpleGrasp(graspGenerator, "Grasp")
   ik_frame = PoseStamped()
   ik_frame.header.frame_id = "jaco2_end_effector"
   ik_frame.pose.position.z = 0.07
   quat = Conversions.euler_to_quaternion([math.pi/2, 0, 0])
   ik_frame.pose.orientation.w = quat[3]
   ik_frame.pose.orientation.x = quat[0]
   ik_frame.pose.orientation.y = quat[1]
   ik_frame.pose.orientation.z = quat[2]
   simpleGrasp.setIKFrame(ik_frame)

   pick = stages.Pick(simpleGrasp, "Pick")
   pick.eef = eef
   pick.object = "cylinder"

   approach = TwistStamped()
   approach.header.frame_id = "world"
   approach.twist.linear.z = -1.0
   pick.setApproachMotion(approach, 0.001, 0.1)

   lift = TwistStamped()
   lift.header.frame_id = "jaco2_end_effector"
   lift.twist.linear.z = -1.0
   pick.setLiftMotion(lift, 0.001, 0.1)

   task.add(pick)

   oc = OrientationConstraint()
   oc.parameterization = oc.ROTATION_VECTOR
   oc.header.frame_id = "world"
   oc.link_name = "cylinder"
   oc.orientation.w = 1.0
   oc.absolute_x_axis_tolerance = 0.1
   oc.absolute_y_axis_tolerance = 0.1
   oc.absolute_z_axis_tolerance = math.pi
   oc.weight = 1.0

   constraints = Constraints()
   constraints.name = "object:upright"
   constraints.orientation_constraints.append(oc)

   con = stages.Connect( "con",planner)
   con.path_constraints = constraints
   task.add(con)

   placePose = PoseStamped()
   placePose.header.frame_id = "world"
   placePose.pose.position.x = -0.2
   placePose.pose.position.y = -0.4
   placePose.pose.position.z = 0.15
   placePose.pose.orientation.w = 1.0
   placePose.pose.orientation.x = 0.0
   placePose.pose.orientation.y = 0.0
   placePose.pose.orientation.z = 0.0

   placeGenerator = stages.GeneratePlacePose()
   placeGenerator.setMonitoredStage(task["Pick"])
   placeGenerator.pose = placePose

   simpleUngrasp = stages.SimpleUnGrasp(placeGenerator)

   place = stages.Place(simpleUngrasp, "Place")
   place.eef = eef
   place.eef_frame = "jaco2_end_effector"
   place.object = "cylinder"

   retract = TwistStamped()
   retract.header.frame_id = "world"
   retract.twist.linear.z = 1.0
   place.setRetractMotion(retract, 0.001, 0.01)
   
   placeMotion = TwistStamped()
   placeMotion.header.frame_id = "jaco2_end_effector"
   placeMotion.twist.linear.z = 1.0
   place.setPlaceMotion(placeMotion, 0.001, 0.01)

   task.add(place)

   hme = stages.MoveTo("initialize", core.JointInterpolationPlanner())
   hme.group = arm
   hme.setGoal("Home")

   task.add(hme)

   if task.plan():
      task.publish(task.solutions[0])
      task.execute(task.solutions[0])

   #del pipeline
   #del planner

   time.sleep(50)
   rclcpp.shutdown()
   
if __name__ == "__main__":
   main()
