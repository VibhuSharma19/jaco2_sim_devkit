## 📦 Jaco2_utils

> A ROS 2 `ament_python` package containing utility scripts and helper modules for enhancing the simulation, visualization, and development experience with the **Kinova JACO2** robotic manipulator.
---

### 🧠 <ins>Purpose</ins>

The `jaco2_utils` package provides a set of practical and research-oriented tools to support the development, testing, and study of the JACO2 robot. It includes:

- Workspace visualization tools  
- Orientation conversion utilities  
- Handy Python modules for importing into analysis or control scripts  

Whether you're debugging, prototyping, or preparing a presentation — this package is your go-to toolbox. 🧰

<br>

### 📁 <ins>Package Structure</ins> 

```bash
jaco2_utils
├── jaco2_utils/                  # Python scripts for workspace & conversion utilities
├── resource/                     # ROS 2 Python package resource index
├── test/                         # Automated testing scripts for compliance
├── LICENSE                       # License declaration
├── package.xml                   # ROS 2 package manifest
├── setup.py                      # Entry point for ament_python
├── setup.cfg                     # Build config
└── README.md                     # Documentation
```
<br>

### 🔍 <ins>File Descriptions</ins> 

| *jaco2_utils/* | |
|:---- | :----- |
| [conversions.py](./jaco2_utils/conversions.py) | Class-based utility to convert between Quaternion, Euler angles, Axis-Angle, Rotation matrices |
| [workspace.py](./jaco2_utils/workspace.py) | Plots and analyzes the 3D reachable workspace of the JACO2 arm using FK sampling |

<br>

### 🖼️ <ins>Launch & Visualization</ins>

- ***Workspace Visualization***

    - Plots 3D end-effector reachability
    - Custom FK sampling granularity
    - Useful for understanding manipulability and planning limits

```bash
ros2 run jaco2_utils jaco2_workspace
```

📷	Jaco2 workspace:
<div align="center">

![Jaco2_workspace](/jaco2_media/images/Workspace.png)
</div>


- ***Orientation Conversions***
    - Conversion between:
        * Quaternion ↔ Euler angles
        * Euler angles ↔ Axis-Angle
        * Quaternion ↔ Axis-Angle
        * Quaternion → Matrix
        * Euler angles → Matrix

    - Importable in any external Python project
```python
from jaco2_utils.conversions import Conversions

# Example:
q = [0, 0, 0.707, 0.707]
print(Conversions.quaternion_to_euler(q))

# Output:
# [0.0, 0.0, 1.570494235572534]
```
<br>

### 📝 <ins>Key Capabilities</ins> 

- Robust orientation conversion module for kinematics, planning, and logging

- Workspace plotting to visualize reachable zones of the manipulator

- Easy-to-integrate Python classes for use in demos, notebooks, or research projects

- CLI and API-level access — great for testing or batch analysis

- Built lightweight for scripting, teaching, and toolchain development

<br>

### 👤 <ins>Maintainer</ins>

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)       
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 