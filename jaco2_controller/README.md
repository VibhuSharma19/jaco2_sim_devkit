## 📦 Jaco2_controller

> A ROS 2 `ament_python` package for launching and configuring **ROS 2 controllers** for the Kinova JACO2 arm in a Gazebo simulation environment.

---

### 🧠 <ins>Purpose</ins>

The `jaco2_controller` package provides configuration files and launch utilities to set up **ROS 2 Control** for the JACO2 manipulator. It includes controller interfaces, launch files, and a custom **Joint State Publisher GUI (JSP-GUI)** bridge script that allows manual control of the robot in simulation.

This package is built as a **Python-based ROS 2 package** (`ament_python`) for flexible scripting and dynamic controller setups.

Key Use Cases:
- Launching controller manager with appropriate config
- Start and manage hardware interfaces (real or mock)
- Testing manual joint control using JSP-GUI
- Integrating controller layers with higher-level planning stacks
- Launch controllers without Gazebo using mock hardware for fast debugging and lightweight testing environments
<br>

### 📁 <ins>Package Structure

```bash
jaco2_controller
├── config/                     # YAML configurations for controller manager
├── jaco2_controller/           # Python scripts for extended control features
├── launch/                     # Launch files for starting controllers
├── resource/                   # Required for Python ROS 2 packages
├── test/                       # Test scripts and validation (WIP)
├── package.xml                 # ROS 2 package manifest
├── setup.py                    # Python build entry point
├── setup.cfg                   # Build configuration for ament_python
├── LICENSE                     # License file
└── README.md                   # This documentation
```
<br>

### 🔍 <ins>File Descriptions

| *config/* | |
|:---- | :----- |
| [jaco2_controllers.yaml](/jaco2_controller/config/jaco2_controllers.yaml) | Controller manager configuration file for Jaco2 |
|***jaco2_controller/*** |
| [jsp_gui_controller.py](/jaco2_controller/jaco2_controller/jsp_gui_controller.py) | Python script to bridge Joint State Publisher GUI inputs with the JACO2 in simulation |
|  ***launch/***  |
| [controller.launch.py](/jaco2_controller/launch/controller.launch.py) | Launches the controller manager and configured JACO2 controllers |
| [generic_controller.launch.py](./launch/generic_controller.launch.py) | Launches the ROS2 controllers without Gazebo |
| [jsp_gui_control.launch.py](/jaco2_controller/launch/jsp_gui_control.launch.py) | Launches JACO2 in Gazebo with controllers and GUI-based joint control support |

<br>

### 🖼️ <ins>Launch & Visualization

- ***Launch Controllers (without Gazebo)***
   * Useful for testing **MoveIt 2**, **RViz2**, or **Teleop nodes** without the need to load Gazebo

   * Uses the **mock hardware interface** defined in `urdf/jaco2_generic/` to simulate joint states

   * Lightweight for development and controller tuning
```bash
ros2 launch jaco2_controller generic_controller.launch.py #use_camera:=false
```
>[!Tip]
> Use the `use_camera` launch argument for loading camera based model description.       
> Default to `use_camera:=false`


- ***Launch JSP-GUI Control in Gazebo***
   * Launch the JACO2 arm in an empty Gazebo world
   * Start the ROS 2 controller manager
   * Enable control through Joint State Publisher GUI
```bash
ros2 launch jaco2_controller jsp_gui_control.launch.py
```

:camera: JSP-GUI control interface

![JSP-GUI control demo](/jaco2_media/images/jsp_gui_control.png)
 

<br>

### 📝 <ins>Key Capabilities</ins> 
- ROS 2 Control setup for simulation  
- Built-in Joint State Publisher GUI integration  
- Easy-to-launch controller configs with modular launch files  
- Clean YAML configs for controllers and hardware interfaces  
- Compatible with MoveIt, Servo, and manual jogging tools  
- Lightweight Python-based package with quick extendability  

<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 