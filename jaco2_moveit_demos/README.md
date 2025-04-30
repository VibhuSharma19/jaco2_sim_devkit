## 📦 Jaco2_moveit_demo

>  A ROS 2 `ament_python` package for **motion planning and execution using MoveItPy** APIs with the Kinova JACO2 robotic arm.

---

### 🧠 <ins>Purpose

The `jaco2_moveit_demos` package demonstrates motion planning and scene setup for JACO2 using the **MoveItPy** interface. It provides:

- Clean Python scripts for planning execution
- Support for adding **custom collision objects** into the planning scene
- RViz2 configuration for visualizing trajectories and scene geometry
- Flexible launch system with argument-controlled script execution

This is the **ROS-native**, scriptable way to test planning pipelines without needing external GUIs or predefined goals.

<br>

### 📁 <ins>Package Structure

```bash
jaco2_moveit_demos
├── config/                        # RViz config and planning parameters for demo
├── jaco2_moveit_demos/            # Python module for MoveItPy interfaces and planning demos
├── launch/                        # Launch file for MoveItPy demo setup
├── resource/                      # ROS 2 Python package resource index
├── test/                          # Placeholder for future unit tests
├── LICENSE                        # License declaration
├── package.xml                    # ROS 2 package manifest
├── setup.py                       # Entry point for ament_python
├── setup.cfg                      # Build config
└── README.md                      # Documentation
```
<br>

### 🔍 <ins>File Descriptions

| *config/* | |
|:---- | :----- |
| [moveitpy_planning_params.yaml](./config/moveitpy_planning_params.yaml) | YAML configuration for motion planning via the MoveItPy API |
| [moveitpy_planning.rviz](./config/moveitpy_planning.rviz) | RViz2 display config with planning panel layout optimized for demos |
| ***jaco2_moveit_demos/*** |
| [moveit_interface.py](./jaco2_moveit_demos/moveit_interface.py) | Class and helper functions that wrap MoveItPy APIs for various planning methods |
| [moveit_planning.py](./jaco2_moveit_demos/moveit_planning.py) | Script for wrapping MoveItPy for setting up planning scene using Collision objects |
|  ***launch/***  |
| [moveit_py.launch.py](./launch/moveit_py.launch.py) |	Launches a selected demo script + RViz, using `exe:=<script>` arg to choose script |


<br>

### 🖼️ <ins>Launch & Visualization</ins>

- ***Launch MoveItPy planning setup***
   - Executes motion planning using MoveItPy API
   - Visualizes motion plan and robot in RViz2
   - RViz panel auto-loads planning config

> [!Note]
> To choose from the various available planning methods and setup planning sequence, refer the [moveit_interface.py](./jaco2_moveit_demos/moveit_interface.py) file.

```bash
# After Gazebo and controllers setup:
ros2 launch jaco2_moveit_demo moveit_py.launch.py exe:=moveit_py
```

:film_projector: MoveItPy Planning Execution:

![MoveItPy Planning](/jaco2_media/gifs/moveitpy_planning.gif)


- ***Launch MoveItPy planning scene setup***
   - Create custom scene with collision objects 
   - Starts the Rviz2 for scene visualization 
> [!Note]
> To define a custom planning scene, use the [moveit_planning.py](./jaco2_moveit_demos/moveit_planning.py) file.

```bash
# After starting Gazebo and controllers:
ros2 launch jaco2_moveit_demo moveit_py.launch.py exe:=moveit_planning
```

:film_projector: MoveItPy Planning Scene Modification:

![MoveItPy Planning Scene](/jaco2_media/gifs/moveitpy_scene.gif)

<br>

### 📝 <ins>Key Capabilities</ins>  
-  Script-based planning interface using `moveit_py`  
- Modular planning scene creation with collision object injection  
- Selectable execution via `exe:=` argument in launch file  
- Designed for reproducible, scriptable testing and prototyping  
- Clean separation of interface and planning scene (`moveit_interface.py` vs `moveit_planning.py`)  
- Extendable to support dynamic goals and custom motions

<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)          
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 