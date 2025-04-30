## 📦 Jaco2_description

> A ROS 2 `ament_cmake` package that defines the robot model, simulation configuration, and visualization setup for the Kinova **JACO2 7-DOF** robotic arm.

---

### 🧠 <ins>Purpose

The `jaco2_description` package provides the full **URDF/Xacro model**, **meshes**, **Gazebo plugins**, and **launch files** to simulate and visualize the Kinova JACO2 robot. It is the foundational description package for the simulation stack and is designed to work with ROS 2 Control, MoveIt 2, and Gazebo.

The model files is taken from the official **Kinova Jaco2** package. Some addition modification is done to add mimic joint feature for gripper fingers. 

It also includes tools to:
- Launch the robot in **RViz 2** or **Gazebo**
- Track the **end-effector pose** in real-time
- Customize world and plugin integration for simulation

<br>

### 📁 <ins>Package Structure

```bash
jaco2_description
├── launch/                       # RViz2 + Gazebo launch files
├── meshes/                       # STL/DAE geometry files for robot links
├── rviz/                         # RViz display configurations
├── scripts/                      # Utility Python scripts for simulation
├── urdf/                         # Robot and plugin Xacro files
│   ├── gazebo/                   # Gazebo plugin-specific URDF/Xacro files
│   └── jaco2_generic/            # GenericSystem ROS2-control files
├── CMakeLists.txt                # ROS 2 ament_cmake build setup
├── package.xml                   # ROS 2 package manifest
├── LICENSE                       # License file
└── README.md                     # You're here 
```
<br>

### 🔍 <ins>File Descriptions

|  *launch/*  | |
| :----- | :------ |
| [display.launch.py](/jaco2_description/launch/display.launch.py) | Loads the JACO2 URDF in RViz2 with Joint State Publisher GUI |
| [gazebo.launch.py](/jaco2_description/launch/gazebo.launch.py) | Launches JACO2 in empty Gazebo world with/without camera sensor |
| ***meshes/*** | 
| [*.STL, *.dae](/jaco2_description/meshes/) | 3D models for visual and collision elements (official Kinova resources) |
| ***rviz/*** |
| [display.rviz](/jaco2_description/rviz/display.rviz) | Pre-configured RViz2 view for JACO2 with fixed TF frame and displays |
| ***scripts/*** |
| [track_end_effector.py](/jaco2_description/scripts/track_end_effector.py) | Publishes and logs the real-time pose of the JACO2 end-effector using TF |
| ***urdf/*** | 
| [gazebo / jaco2_control.xacro](/jaco2_description/urdf/gazebo/jaco2_control.xacro) | ROS 2 control plugin and model configuration for Gazebo |
| [gazebo / jaco2_gazebo.xacro](/jaco2_description/urdf/gazebo/jaco2_gazebo.xacro) | Gazebo plugins description |
| [jaco2_generic/*](./urdf/jaco2_generic) | ROS2-control defined using `mock_components` for launching robot without Gazebo |
| [*.xacro](/jaco2_description/urdf/) | Official Kinova Jaco2 7dof robot description files | 

<br>

### 🖼️ <ins>Launch & Visualization

- ***Launch Rviz visualization with JSP gui tool***
   * Loads the full URDF model

   * Uses Joint State Publisher GUI to manually test joint configurations

   * Great for debugging URDF structure and visual frames
``` bash
ros2 launch jaco2_description display.launch.py
```
:camera: Rviz with JSP-GUI

![Rviz with JSP](/jaco2_media/images/rviz_with_jsp.png)

- ***End-Effector pose tracking***
   * Can be used alongside Gazebo or RViz2

   * Logs the real-time position and orientation of the end-effector (ideal for IK testing or validation)     

```bash
ros2 run jaco2_description track_end_effector.py
```    
:camera: Rviz with EE tracking

![Rviz with EE tracking](/jaco2_media/images/rviz_ee_pose.png)

- ***Launch Gazebo simulation***
   * Spawns the robot in empty Gazebo world
   * TF and joint states published
```bash
ros2 launch jaco2_description gazebo.launch.py #use_camera:=false
```    

>[!Tip]
> Use launch argument `use_camera` to select between robot model with/without camera integration.          
> Default is `use_camera:=false`


<br>

### 📝 <ins>Key Capabilities</ins> 
- Official Kinova URDF/Xacro model adapted for ROS 2  
- Modular architecture (arms, sensors, gazebo plugins, etc.)  
- Compatible with both MoveIt and Gazebo  
- RViz-ready with TF trees and joint states preconfigured  
- End-effector pose tracking tool built in  
- Clean launch files for RViz + TF publishing

<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com       


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 