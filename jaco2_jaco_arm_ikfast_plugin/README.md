## 📦 Jaco2_jaco_arm_ikfast_plugin

> A ROS 2 `ament_cmake` package auto-generated using the **MoveIt IKFast Plugin Generator**, providing an optimized IK solver for the `jaco_arm` planning group of the Kinova **JACO2** manipulator.
---

### 🧠 <ins>Purpose

The `jaco2_jaco_arm_ikfast_plugin` package provides an **analytical inverse kinematics (IK)** solution for the **jaco_arm** using **IKFast** (part of OpenRAVE).  
It replaces the default numerical IK solvers with a **faster, deterministic, and more stable** solver — ideal for high-performance planning and real-time applications.

It includes:

- Auto-generated C++ analytical IK solver
- Plugin wrapper to integrate with MoveIt 2
- MoveIt 2 compatible interface configuration
- Setup script for updating the plugin

<br>

### 📁 <ins>Package Structure

```bash
jaco2_jaco_arm_ikfast_plugin
├── include/                                                # C++ header files for IKFast solver
├── src/                                                    # C++ source files for plugin and solver
├── CMakeLists.txt                                          # ROS 2 build instructions
├── jaco2_jaco_arm_moveit_ikfast_plugin_description.xml     # Plugin metadata for MoveIt
├── package.xml                                             # ROS 2 package manifest
├── update_ikfast_plugin.sh                                 # Script to update IKFast plugin files
└── README.md                                               # Documentation (you are here)
```
<br>

### 🔍 <ins>File Descriptions

| *include/* | |
|:---- | :----- |
| [ikfast.h](./include/ikfast.h) | Shared header file for IKFast solver |
|  ***src/***  |
| [ikfast_kinematics_parameters.yaml](./src/ikfast_kinematics_parameters.yaml) |  IkFast kinematics parameters |
| [jaco2_jaco_arm_ikfast_moveit_plugin.cpp](./src/jaco2_jaco_arm_ikfast_moveit_plugin.cpp) | MoveIt plugin wrapping the IKFast solver for MoveIt KinematicsBase |
| [jaco2_jaco_arm_ikfast_solver.cpp](./src/jaco2_jaco_arm_ikfast_solver.cpp) | Auto-generated analytical IK code from OpenRAVE/IKFast |

<br>

### 🖼️ <ins>Launch & Visualization

To integrate the IKFast solver for the **jaco_arm** planning group:
: Use the [`kinematics_ikfast.yaml`](/jaco2_moveit_config/config/kinematics_ikfast.yaml) file inside your MoveIt config:

   - In your [`jaco2_move_group.launch.py`](/jaco2_moveit_config/launch/jaco2_move_group.launch.py),
   - Update the `robot_description_kinematics` parameter to point to `kinematics_ikfast.yaml`.

   Example patch in your launch file:

   ```python
   .robot_description_kinematics(
      file_path=os.path.join(jaco2_moveit_dir,"config","kinematics_ikfast.yaml"))
   ```
<br>

>[!Note] 
> IKFast provides **extremely fast and reliable IK solutions** but is limited to specific arm configurations at the time of plugin generation. If the robot model changes (URDF), regenerate the IKFast plugin using [`update_ikfast_plugin.sh`](update_ikfast_plugin.sh)

<br>

### 📝 <ins>Key Capabilities</ins> 
- Ultra-fast IK computation (real-time capable)
- Deterministic and stable solutions (unlike numerical solvers)
- Fully integrated with MoveIt 2 motion planning pipelines
- Regenerative — can be updated if URDF/joint definitions change
- Compatible with Servo control, Cartesian paths, and constrained planning
- Optimized for the 7-DOF Kinova JACO2 arm

<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 