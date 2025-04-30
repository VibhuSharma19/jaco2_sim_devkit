# 🤖 Jaco2_sim_devkit

> A ROS 2 `ament_cmake` **meta-package** that aggregates all sub-packages related to the Kinova **JACO2 simulation**, motion planning, and teleoperation stack.

---

### 🧠 <ins>Purpose</ins>

The `jaco2_sim_devkit` meta-package serves as a central entry point for the entire JACO2 simulation project. It allows for collective workspace builds and package dependency resolution by grouping together all related submodules under a unified namespace.

<br>

### 📦 <ins>Included Packages</ins>

- [`jaco2_bringup`](../jaco2_bringup) — Shell scripts for simulation setup   
- [`jaco2_controller`](../jaco2_controller) — ROS 2 controllers and control config   
- [`jaco2_description`](../jaco2_description) — URDF, meshes, and RViz/Gazebo visualization setup  
- [`jaco2_gazebo`](../jaco2_gazebo) — Gazebo world, plugins, and object models  
- [`jaco2_jaco_arm_ikfast_plugin`](../jaco2_jaco_arm_ikfast_plugin) — IKFast solver plugin for jaco_arm
- [`jaco2_media`](../jaco2_media) — Media files for visuals and demonstrations
- [`jaco2_moveit_config`](../jaco2_moveit_config) — MoveIt 2 planning setup  
- [`jaco2_moveit_demos`](../jaco2_moveit_demos) — MoveItPy-based demo scripts  
- [`jaco2_moveit_task_constructor`](../jaco2_moveit_task_constructor) — Task-level planning using MTC  
- [`jaco2_servo`](../jaco2_servo) — Real-time teleoperation using joystick & keyboard  
- [`jaco2_utils`](../jaco2_utils) — Utility tools for workspace analysis and conversions  

<br>

### 📁 <ins>Package Structure</ins>

```bash
jaco2_sim_devkit/
├── CMakeLists.txt          # Required for ament_cmake build
├── package.xml             # Declares meta-package and submodule dependencies
└── README.md               # You are here
```
<br/>

> [!Tip]
> Simply include `jaco2_sim_devkit` in your workspace to bring in all core JACO2 packages under one build.

<br>

<p align="center"> <sub>Meta-package for the JACO2 Simulation & Planning Stack. Built with 🤖 and ❤️ by <a href="https://github.com/VibhuSharma19">Vibhu Sharma</a>.</sub> </p> 