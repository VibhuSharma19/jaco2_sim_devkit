#!/usr/bin/python3

import rclpy
import rclpy.executors
import rclpy.logging
import curses
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from moveit.planning import MoveItPy
from moveit.core.robot_state import RobotState # type: ignore
from moveit.core.kinematic_constraints import construct_joint_constraint # type: ignore
import rclpy.timer


class MoveitInterface(Node):
    """
    Jaco2 manipulator control using MoveitPy framework

    Motion planning using various avaible methods like:
      * Pre-defined configuration
      * random configuration
      * Joint positions configuration
      * Goal pose configuration
      * Multi-pipeline planning / Single pipeline planning
    """

    def __init__(self):
        """
        Initializes the node with publishers, subsribers and variables.

        Also defines the planning components and also the planning method and configuration
        """
        super().__init__("MoveitInterface")
        self.logger = rclpy.logging.get_logger("MoveitInterface")

        self.logger.info("Welcome to MoveIt Interface for Jaco2 arm")

        self.jaco = MoveItPy()
        self.jaco_arm = self.jaco.get_planning_component("jaco_arm")
        self.jaco_gripper = self.jaco.get_planning_component("jaco_gripper")
        self.logger.info("MoveitPy Instance created")

        self.robot = self.jaco.get_robot_model()
        self.robot_config = RobotState(self.robot)

        # define the planning group and the method
        comp = self.get_component(component_name="Arm")
        self.predefined_configuration(component=comp, config_name="pickup")


    
    def get_component(self, component_name:str):
        """Return MoveitPy objects for user-frinedly component names"""

        if component_name == "Arm":
            return self.jaco_arm
        elif component_name == "Gripper":
            return self.jaco_gripper
        else:
            raise ValueError(f"Unknown component name: {component_name}")


    def predefined_configuration(self, component, config_name):
        """Planning to pre-defined robot state in srdf file"""

        self.logger.info(f"Planning to predefined configuration '{config_name}' for {component}.")
        component.set_start_state_to_current_state()
        component.set_goal_state(configuration_name=str(config_name))  

        self.plan_and_execute(component=component)


    def random_confguration(self, component):
        """Planning to a random robot configuration"""
        
        self.logger.info(f"Planning to random configuration state for {component}.")
        self.robot_config.set_to_random_positions()
        component.set_start_state_to_current_state()
        component.set_goal_state(robot_state=self.robot_config)

        self.plan_and_execute(component=component)


    def goal_pose_configuration(self, component, pose):
        """Planning to end-effector position defined in 3D space"""

        self.pose_goal = PoseStamped()
        self.pose_goal.header.frame_id = "jaco2_link_base"
        self.pose_goal.pose.position.x, self.pose_goal.pose.position.y, self.pose_goal.pose.position.z = pose[:3]
        self.pose_goal.pose.orientation.x, self.pose_goal.pose.orientation.y, self.pose_goal.pose.orientation.z, self.pose_goal.pose.orientation.w = pose[3:]

        self.logger.info("Planning to a defined end-effector pose:" + str(pose))
        component.set_start_state_to_current_state()
        component.set_goal_state(pose_stamped_msg=self.pose_goal, pose_link="jaco2_link_7")

        self.plan_and_execute(component=component)


    def joint_positions_configuration(self, component, joint_position):
        """Planning to individually defined joint positions"""
        self.jaco_arm.set_start_state_to_current_state()

        if component == "self.jaco_gripper":
          self.joint_values = {"jaco2_joint_finger_1": joint_position[0],
                              "jaco2_joint_finger_tip_1": joint_position[1]}
        else:
          self.joint_values = {"jaco2_joint_1": joint_position[0],
                             "jaco2_joint_2": joint_position[1],
                             "jaco2_joint_3": joint_position[2],
                             "jaco2_joint_4": joint_position[3],
                             "jaco2_joint_5": joint_position[4],
                             "jaco2_joint_6": joint_position[5],
                             "jaco2_joint_7": joint_position[6]}

        self.robot_config.joint_positions = self.joint_values
        self.joint_constraint = construct_joint_constraint(
            robot_state=self.robot_config,
            joint_model_group=self.jaco.get_robot_model().get_joint_model_group("arm" if component == "Arm" else "gripper"),)
        
        self.logger.info("Planning to defined joint positions:" + str(joint_position))
        component.set_goal_state(motion_plan_constraints=[self.joint_constraint])

        self.plan_and_execute(component=component)


    def multi_pipeline_planning(self, component, config_name):
        """Planning using multiple pipeline parallely"""

        self.logger.info("Planning to configuration state:" + str(config_name))
        component.set_start_state_to_current_state()
        component.set_goal_state(configuration_name=str(config_name))

        multi_pipeline_params = MoveItPy.PlanningComponent.MultiPipelinePlanRequestParameters(self.jaco, 
                                ["ompl_rrtc", "pilz_lin", "chomp_pipe", "ompl_rrtstar"])
        
        self.logger.info("Planning using MultiPipeLine Planning")
        
        self.plan_and_execute(component=component,multi_plan_parameters=multi_pipeline_params)


    def plan_and_execute(self,component,single_plan_parameters=None,multi_plan_parameters=None):
        """Plan to given configuration and execute the plan"""
        self.logger.info("Planning trajectory")
        if multi_plan_parameters is not None:
                plan_result = component.plan(multi_plan_parameters=multi_plan_parameters)

        elif single_plan_parameters is not None:
                plan_result = component.plan(single_plan_parameters=single_plan_parameters)

        else:
                plan_result = component.plan()

        self.logger.info("Plan result: " +  str(plan_result))

      # execute the plan
        if plan_result:
                self.logger.info("Executing plan")
                robot_trajectory = plan_result.trajectory
                self.jaco.execute(robot_trajectory, controllers=[])
        else:
                self.logger.error("Planning failed")


#class CursesMenu:
#    def __init__(self, moveit_interface):
#        self.moveit_interface = moveit_interface
#
#    def run_menu(self):
#        curses.wrapper(self.main_menu)
#
#    def main_menu(self, stdscr):
#        curses.curs_set(0)
#        stdscr.clear()
#
#        components = ["Arm", "Gripper"]
#        arm_methods = ["Predefined Configuration", "Random Configuration", "Goal Pose", "Joint Positions", "Multi Pipeline Planning"]
#        gripper_methods = ["Predefined Configuration", "Random Configuration", "Joint Positions"]
#
#        component_choice = 0
#
#        while True:
#            stdscr.clear()
#            stdscr.addstr(0, 0, "Select Planning Component (Arrow Keys to Navigate, ENTER to Select):", curses.A_BOLD)
#            for idx, comp in enumerate(components):
#                if idx == component_choice:
#                    stdscr.addstr(idx + 1, 0, f"> {comp}", curses.A_REVERSE)
#                else:
#                    stdscr.addstr(idx + 1, 0, f"  {comp}")
#            stdscr.refresh()
#
#            key = stdscr.getch()
#            if key == curses.KEY_UP and component_choice > 0:
#                component_choice -= 1
#            elif key == curses.KEY_DOWN and component_choice < len(components) - 1:
#                component_choice += 1
#            elif key in [curses.KEY_ENTER, 10, 13]:
#                component_name = components[component_choice]
#                if component_name == "Arm":
#                    self.handle_methods(stdscr, arm_methods, "Arm")
#                elif component_name == "Gripper":
#                    self.handle_methods(stdscr, gripper_methods, "Gripper")
#
#    def handle_methods(self, stdscr, methods, component_name):
#        component = self.moveit_interface.get_component(component_name)
#        method_choice = 0
#
#        while True:
#            stdscr.clear()
#            stdscr.addstr(0, 0, f"Select Planning Method for {component_name}:", curses.A_BOLD)
#            for idx, method in enumerate(methods):
#                if idx == method_choice:
#                    stdscr.addstr(idx + 1, 0, f"> {method}", curses.A_REVERSE)
#                else:
#                    stdscr.addstr(idx + 1, 0, f"  {method}")
#            stdscr.refresh()
#
#            key = stdscr.getch()
#            if key == curses.KEY_UP and method_choice > 0:
#                method_choice -= 1
#            elif key == curses.KEY_DOWN and method_choice < len(methods) - 1:
#                method_choice += 1
#            elif key in [curses.KEY_ENTER, 10, 13]:
#                method_name = methods[method_choice]
#                self.execute_method(stdscr, component, method_name)
#                break
#
#    def execute_method(self, stdscr, component, method_name):
#        if method_name == "Predefined Configuration":
#            self.moveit_interface.predefined_configuration(component, "home")
#        elif method_name == "Random Configuration":
#            self.moveit_interface.random_configuration(component)
#        elif method_name == "Goal Pose":
#            pose = self.get_pose_input(stdscr)
#            self.moveit_interface.goal_pose_configuration(pose, component)
#        elif method_name == "Joint Positions":
#            joint_positions = self.get_joint_positions_input(stdscr)
#            self.moveit_interface.joint_positions_configuration(joint_positions, component)
#        elif method_name == "Multi Pipeline Planning":
#            self.moveit_interface.multi_pipeline_planning(component, "home")
#
#    def get_pose_input(self, stdscr):
#        stdscr.clear()
#        stdscr.addstr(0, 0, "Enter Pose as x,y,z,ox,oy,oz,ow (comma-separated):", curses.A_BOLD)
#        curses.echo()
#        user_input = stdscr.getstr(1, 0).decode()
#        curses.noecho()
#        return list(map(float, user_input.split(",")))
#
#    def get_joint_positions_input(self, stdscr):
#        stdscr.clear()
#        stdscr.addstr(0, 0, "Enter Joint Positions as j1,j2,j3,j4,j5,j6,j7 (comma-separated):", curses.A_BOLD)
#        curses.echo()
#        user_input = stdscr.getstr(1, 0).decode()
#        curses.noecho()
#        return list(map(float, user_input.split(",")))


def main():
   rclpy.init()
   moveit_interface = MoveitInterface()

   try:
     rclpy.spin(moveit_interface)
   except KeyboardInterrupt:
      pass
    #curses_menu = CursesMenu(moveit_interface)
    #curses_menu.run_menu()
   finally:
      moveit_interface.destroy_node()
      rclpy.shutdown()


if __name__ == "__main__":
    main()