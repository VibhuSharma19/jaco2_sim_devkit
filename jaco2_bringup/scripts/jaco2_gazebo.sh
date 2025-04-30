#!/bin/bash

gnome-terminal  -- ros2 launch jaco2_description gazebo.launch.py &

sleep 10

gnome-terminal  -- ros2 launch jaco2_controller controller.launch.py &

wait
