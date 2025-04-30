## 📦 Jaco2_gazebo

> A ROS 2 `ament_cmake` package for launching and configuring **GazeboSim environments** to simulate the Kinova JACO2 robotic arm within customized worlds and sensor setups.
---

### 🧠 <ins>Purpose

The `jaco2_gazebo` package defines the **Gazebo simulation environment** for the JACO2 manipulator. It includes:

- Prebuilt **worlds** for object manipulation
- **Object models** for dynamic scenes
- ROS 2 **launch files** for Gazebo simulation
- RViz2 configs for **sensor and camera data**
- Utility scripts for **sensor remapping** and sim-specific tweaks

This package focuses on **world-building**, **sensor uses**, and **environment-level simulation**, rather than controllers or planning logic.
<br>

### 📁 <ins>Package Structure

```bash
jaco2_gazebo
├── config/                     # RViz and ROS-Gazebo bridge configurations
├── launch/                     # Launch files for Gazebo world simulation
├── models/                     # Custom object models for Gazebo
├── scripts/                    # Python tools for sim data manipulation
├── worlds/                     # Gazebo SDF world definitions
├── CMakeLists.txt              # Ament_cmake build script
├── package.xml                 # ROS 2 package manifest
├── LICENSE                     # License declaration
└── README.md                   # You're here 
```
<br>

### 🔍 <ins>File Descriptions

| *config/* | |
|:---- | :----- |
| [gazebo_world.rviz](/jaco2_gazebo/config/gazebo_world.rviz) | RViz2 config for visualizing sensors and world data |
| [gz_ros-bridge.yaml](/jaco2_gazebo/config/gz_ros_bridge.yaml) | Parameters for `ros_gz_bridge` plugins |
|  ***launch/***  |
| [gazebo_world.launch.py](/jaco2_gazebo/launch/gazebo_world.launch.py) | Launches the custom Gazebo world with ROS 2 bridge, sensors and plugins |
| ***models/*** |
| */ | Contains `.sdf` and `.config` files for scene objects (e.g., bookshelf, coke-cans, etc.) |
| ***scripts/*** |
| [depth_image_remap.py](/jaco2_gazebo/scripts/depth_image_remap.py) | Remaps the depth image topic to correct its frame/orientation in RViz or downstream tools |
| ***worlds/*** |
| [empty.sdf](./worlds/empty.sdf) | Gazebo empty world description |
| [pick_place_world.sdf](/jaco2_gazebo/worlds/pick_place_world.sdf) | Gazebo custom world with objects description file |

<br>

### 🖼️ <ins>Launch & Visualization

- ***Launch Gazebo World***
   - Custom world with physical props
   - Robot spawned via jaco2_description
   - Gazebo plugins and sensors
```bash
ros2 launch jaco2_gazebo gazebo_world.launch.py
```   
:camera: Jaco2 in Custom Gazebo World

![Jaco2 in Gazebo World](/jaco2_media/images/gazebo_world.png)

- ***Visualize  Camera data in Rviz2***
   - Visualizes RGB, Depth, PointCloud, and TF frames
   - Linked to Gazebo camera sensors via ROS 2 bridge
```bash
# After launching Gazebo:
cd <path to jaco2_gazebo package>
rviz2 -d ./config/gazebo_world.rviz
```
:camera: Rviz Sensor Display

![Rviz Sensor Display](/jaco2_media/images/rviz_sensor.png)

<br>

### 📝 <ins>Key Capabilities</ins> 
- Drop-in simulation world with manipulable objects
- Supports real-time RGBD, segmentation, and 3D perception
- ROS-Gazebo bridge integration for seamless data streaming
- RViz configuration for debugging sensor placement and robot view
- Depth image remapping utility for consistent perception frames
- Designed for motion planning, manipulation demos, and research scenes

<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 