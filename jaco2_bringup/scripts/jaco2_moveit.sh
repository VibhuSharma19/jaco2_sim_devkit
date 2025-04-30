#!/bin/bash

gnome-terminal  -- ros2 launch jaco2_controller generic_controller.launch.py &

sleep 5

ros2 launch jaco2_moveit_config jaco2_move_group.launch.py

wait
