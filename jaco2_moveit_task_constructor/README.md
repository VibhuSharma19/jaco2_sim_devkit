## 📦 Jaco2_moveit_task_constructor

> A ROS 2 `ament_python` package implementing **Pick-and-Place task-level planning** for the Kinova JACO2 manipulator using the **MoveIt Task Constructor (MTC)** framework.

---

### 🧠 <ins>Purpose</ins>

The `jaco2_moveit_task_constructor` package defines task-level planning pipelines using **MoveIt Task Constructor**, allowing you to create modular, stage-based manipulation tasks such as:

- Pick and Place with grasp and retreat strategies
- Cartesian vs. joint-space movement splits
- Pre- and post-grasp pose planning
- Integrated grasp pose sampling

This package is ideal for researchers and developers interested in testing or benchmarking **complex robotic manipulation** logic in simulation.

<br>

### 📁 <ins>Package Structure</ins>

```bash
jaco2_moveit_task_constructor
├── config/                            # RViz configuration files
├── jaco2_moveit_task_constructor/     # Python scripts for task-level planning
├── launch/                            # ROS 2 launch files for MTC pipeline
├── resource/                          # ROS 2 Python package resource index
├── test/                              # Automated testing scripts for compliance
├── LICENSE                            # License declaration
├── package.xml                        # ROS 2 package manifest
├── setup.py                           # Entry point for ament_python
├── setup.cfg                          # Build config
└── README.md                          # Documentation
```
<br>

### 🔍 <ins>File Descriptions</ins> 

| *config/* | |
|:---- | :----- |
| [mtc.rviz](./config/mtc.rviz) | RViz2 layout for visualizing MTC stages, TF frames, and trajectory previews |
| ***jaco2_moveit_task_constructor/*** |
| [pickplace.py](./jaco2_moveit_task_constructor/pickplace.py) | Full pick-and-place pipeline with grasp sampling, approach/lift, and retreat stages |
| [planner.py](./jaco2_moveit_task_constructor/planner.py) | Generic MTC task interface with configurable Cartesian or joint-space planning |
| [scene_publisher](./jaco2_moveit_task_constructor/scene_publisher.py) | Planning scene publisher for MTC |
|  ***launch/***  |
| [move_group.launch.py](./launch/move_group.launch.py) | Starts Move Group and RViz2 for task planning |
| [run.launch.py](./launch/run.launch.py) | Executes task planning demo scripts using `exe:=<script>` argument |

<br>

### 🖼️ <ins>Launch & Visualization</ins>

- ***Launch MTC demo scripts***
   - Initializes the Move_Group node
   - Visualizes the Moveit Task status and updates in Rviz
   - Executes the demo scripts using `exe` launch parameter

> [!Important]
> Launch Gazebo simulation and controllers before using the below cmd

<br/>

```bash
# Terminal 1: Launch Move Group and RViz2
ros2 launch jaco2_moveit_task_constructor move_group.launch.py
```
```bash
# Terminal 2: Run your desired task script
ros2 launch jaco2_moveit_task_constructor run.launch.py exe:=planner
```
<br>

> [!Note]
> Use exe:=planner: Runs Cartesian or joint-space task pipeline      
    ↳ See [planner.py](./jaco2_moveit_task_constructor/planner.py) for implementation details           
> Use exe:=pickplace: Executes a full Pick-Place task using end-effector grasp strategies            
    ↳ See [pickplace.py](./jaco2_moveit_task_constructor/pickplace.py) for detailed task and planner sequence 


:camera: Moveit Task Constructor Pick-Place Simulation:

![MTC Pick-Place Simulation](/jaco2_media/images/mtc_pickplace.png)

<br>

### 📝 <ins>Key Capabilities</ins>  
- Advanced task planning using MoveIt Task Constructor (MTC)  
- Modular stage-based manipulation pipeline (approach → grasp → lift → place)  
- Pick-and-place task with grasp pose sampling and filtering  
- Fully customizable task stages via Python  
- Preconfigured RViz layout for MTC stage monitoring
- Separate scene publisher script for modular setups

<br>

### 👤 <ins>Maintainer</ins>

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)        
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 