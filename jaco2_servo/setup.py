from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'jaco2_servo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Vibhu Sharma',
    maintainer_email='1999vibhusharma@gmail.com',
    description='Servo (Teleop) control of the Jaco2 arm',
    license='BSD-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           "key_teleop = jaco2_servo.keyboard_teleop:main",
           "cmd_switch = jaco2_servo.servo_cmd_switch:main",
           "joy_teleop = jaco2_servo.joystick_teleop:main",
        ],
    },
)