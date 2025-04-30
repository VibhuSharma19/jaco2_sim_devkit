#!/usr/bin/python3

from math import pi
import time, os
from std_msgs.msg import Header
from geometry_msgs.msg import TwistStamped, Twist, Vector3Stamped, Vector3
from moveit.task_constructor import core, stages
import rclcpp

def main():
    rclcpp.init()
    node = rclcpp.Node("mtc_cartesian")

    # Set planning grp name
    group = "jaco_arm"

    # Initialize cartesian and joint planners
    cartesian_planner = core.CartesianPath()
    joint_planner = core.JointInterpolationPlanner()

    cartesian_planner.jump_threshold = 0.0
    cartesian_planner.min_fraction = 0.05
    cartesian_planner.step_size = 0.05

    #Start task and set current robot state
    task = core.Task()
    task.name = "cartesian"
    task.loadRobotModel(node)
    task.enableIntrospection(enabled=True)

    task.add(stages.CurrentState("current_state"))

    # Move along x-axis using MoveRelative stage
    #move_x = stages.MoveRelative("x", cartesian_planner)
    header = Header(frame_id = "world")
    #move_x.group = group
    #move_x.setDirection(Vector3Stamped(header=header, vector = Vector3(x = 0.35, y = 0.0, z = 0.0)))
    #task.add(move_x)

    move = stages.MoveRelative("rz +45°", joint_planner)
    move.group = group
    move.setDirection(
        TwistStamped(header=header, twist=Twist(angular=Vector3(x=0.0, y=0.0, z=pi/4)))
    )
    task.add(move)

    move_to = stages.MoveTo("ready_pose", cartesian_planner)
    move_to.group = group
    move_to.setGoal("pickup")
    task.add(move_to)

    if task.plan():
        task.publish(task.solutions[0])
        task.execute(task.solutions[0])
    time.sleep(10)
    

if __name__ == "__main__":
    main()