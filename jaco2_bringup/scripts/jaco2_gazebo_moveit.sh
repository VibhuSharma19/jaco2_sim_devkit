#!/bin/bash

gnome-terminal  -- ros2 launch jaco2_description gazebo.launch.py &

sleep 10

gnome-terminal  -- ros2 launch jaco2_controller controller.launch.py &

sleep 5

ros2 launch jaco2_moveit_config jaco2_move_group.launch.py

wait
