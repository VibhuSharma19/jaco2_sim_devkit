## 📦 Jaco2_bringup

> A ROS 2 package that provides easy-to-use shell scripts to launch various simulation and motion planning setups for the Kinova JACO2 robotic arm.

---

### 🧠 <ins>Purpose</ins>

The `jaco2_bringup` package simplifies launching complex multi-node setups by bundling them into clean, reusable **Bash scripts**. These scripts orchestrate Gazebo, MoveIt 2, and controller nodes across **separate terminals**, making it easy to debug, monitor, and manage your simulation environment in real-time.

This is especially helpful for:
- Parallel launching of large systems
- Cleaner debugging with window separation
- Automation of startup sequences
<br>

### 📁 <ins>Package Structure</ins>

```bash
jaco2_bringup
├── scripts/                 # Shell scripts to launch simulation and planning setups
├── package.xml              # ROS 2 package manifest
├── CMakeLists.txt           # Build setup (for ROS 2 ament_cmake build system)
├── License                  # License file
└── README.md                # You are here!
```
<br>

### 🔍 <ins>File Descriptions

| scripts/ | |
|:---- | :----- |
| [jaco2_gazebo.sh](./scripts/jaco2_gazebo.sh) | Launches the Jaco2 arm in empty gazebosim world with controllers |
| [jaco2_gazebo_moveit.sh](./scripts/jaco2_gazebo_moveit.sh) | Launches Gazebosim + Moveit 2 planning framework |
| [jaco2_gazeboworld.sh](./scripts/jaco2_gazeboworld.sh) | Launches jaco2 in custom Gazebo world with environment and sensors|
| [jaco2_gazeboworld_moveit.sh](./scripts/jaco2_gazeboworld_moveit.sh) | Launches custom world + MoveIt 2 + Octomap integration |
| [jaco2_moveit.sh](./scripts/jaco2_moveit.sh) | Launches ROS2 controllers using Mock hardware and Moveit 2 |


>[!Important]
> The default robot model used is without sensor. To use with senosr, use `use_camera` argument in the gazebo launch command in scripts files.

<br>

### 🖼️ <ins>Launch & Visualization

- ***Gazebo(empty world) launch***
```bash
jaco2_gazebo.sh
```
- ***Gazebo (empty world) + Moveit launch***
```bash
jaco2_gazebo_moveit.sh
```

- ***Gazebo (custom world with sensors) launch***
```bash
jaco2_gazeboworld.sh
```
:camera: Gazebo Custom World with Sensors

![Gazebo World](/jaco2_media/images/gazebo_world_with_image.png)

- ***Gazebo (custom world with sensors) + Moveit (with octomap) launch***
```bash
jaco2_gazeboworld_moveit.sh
```

<br>

### 📝 <ins>Key Capabilities
- One-click launch of multi-node simulation setups
- Launches each component in its own terminal for visibility
- Integrates robot, controllers, environment, and planner
- Supports modular combinations (with or without MoveIt, custom world, etc.)
- Easy to extend or modify for new experimental setups
- Perfect for automated testing or rapid simulation bootstrapping
<br>

### 👤 <ins>Maintainer

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com     


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 
