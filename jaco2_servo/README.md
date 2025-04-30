## 📦 Jaco2_servo

> A ROS 2 `ament_python` package enabling **real-time teleoperation** of the Kinova JACO2 arm using **joint-jog** and **Cartesian servoing**, via both **joystick** and **keyboard** interfaces.

---

### 🧠 <ins>Purpose</ins>

The `jaco2_servo` package provides flexible, low-latency servo control interfaces that make real-time manipulation of the JACO2 arm smooth, intuitive, and powerful. It wraps around the **MoveIt Servo** node to support two input modalities:

- 🕹️ Joystick / Gamepad (e.g. Xbox Controller)  
- ⌨️ Keyboard (with live key detection and frame switching)

You'll be able to:
- Jog joints in real time  
- Control Cartesian position/orientation of the end-effector  
- Dynamically switch between **planning frames**  
- Enable/disable servo commands mid-operation  
- Watch it all update live in Gazebo and Rviz!!      

This package is 🔧 the playground and the proving ground for teleoperation research, fine motor control, and UI/HMI integration with physical robots or simulations.

<br>

### 📁 <ins>Package Structure</ins>

```bash
jaco2_moveit_task_constructor
├── config/                            # Servo node parameters and Rviz config 
├── jaco2_servo/                       # Python interface scripts for control input
├── launch/                            # Launch files for servoing setup
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
| [servo_params.yaml](./config/servo_params.yaml) | Parameters for MoveIt Servo (e.g. command filters, control frame, speed limits) |
| [servo.rviz](./config/servo.rviz) | RViz2 layout for live teleop feedback and TF visualization |
| ***jaco2_servo/*** |
| [joystick_teleop.py](./jaco2_servo/joystick_teleop.py) | Main joystick input handler with joint/cartesian servoing modes, frame toggle, and button mapping |
| [keyboard_teleop.py](./jaco2_servo/keyboard_teleop.py) | Script for teleoperation using keyboard mappings|
| [servo_cmd_switch.py](./jaco2_servo/servo_cmd_switch.py) | Standalone ROS node to switch command types (joint-jog or cartesian) during keyboard-based control |
|  ***launch/***  |
| [joystick_teleop.launch.py](./launch/joystick_teleop.launch.py) | Launch setup and nodes for Joystick controller teleoperation |
| [keyboard_teleop.launch.py](./launch/keyboard_teleop.launch.py) | Launch setup and nodes for keyboard based servoing |

> [!Tip]
> To change default control frame or velocity scaling: Edit [servo_params.yaml](./config/servo_params.yaml)

<br>

### 🖼️ <ins>Launch & Visualization</ins>

> [!Important]
> Launch Gazebo simulation and controllers before using servoing

<br>

- ***Launch Joystick Servoing***
    - Support for Xbox/ Microsoft based gamepad/joystick controllers
    - Joint-Jog and cartesian based teleoperation options
    - Change of planning frame available (`world` or `end-effector`)
    - Start/Stop and Servo_cmd_switch using gamepad    

<br>

```bash
# Update joystick device if needed in launch file (e.g. /dev/input/js0)
ros2 launch jaco2_servo joystick_teleop.launch.py
```
<br>

> [!Note]
> 📸 Joystick Control Layout:    
> 
> ![Joystick layout](/jaco2_media/images/Joystick_layout.png.jpg)

📽️ Joystick Servoing:
<div align="center">

![Joystick Servoing](/jaco2_media/gifs/joystick_servoing.gif)
</div>

- ***Launch Keyboard Servoing***
    - Real-time keystroke listener (no need to press enter)
    - Move joints or Cartesian tool frame
    - Frame switching + command mode switching
    - Minimalist + terminal-based — great for SSH sessions or remote control


```bash
# Terminal 1:
ros2 launch jaco2_servo keyboard_teleop.launch.py
```
```bash
# Terminal 2:
ros2 run jaco2_servo cmd_switch
```
<br>

> [!Note]
> For detail on keys functions, keep eye for the **Instructions** window.

📽️ Keyboard Teleoperation:
<div align="center">

![Keyboard Servoing](/jaco2_media/gifs/keyboard_servoing.gif)
</div>
<br>

### 📝 <ins>Key Capabilities</ins>  

- Real-time teleoperation with MoveIt Servo backend  
- Joystick (gamepad) & keyboard control — both fully supported  
- Live frame switching + command mode toggling  
- No relaunch needed to swap control strategies  
- Includes `servo_cmd_switch.py` for runtime switching  
- RViz2 layout for intuitive control + visual feedback  
- Research-ready & demo-polished 


<br>

### 👤 <ins>Maintainer</ins>

**Vibhu Sharma**

🔗 GitHub: [VibhuSharma19](https://github.com/VibhuSharma19)    
📧 Email: 1999vibhusharma@gmail.com      


<p align="center"> <sub>This is a submodule of the <a href="https://github.com/VibhuSharma19/jaco2_sim_devkit">jaco2_sim_devkit</a> project. Built with 🤖 and ❤️.</sub> </p> 