from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'jaco2_moveit_demos'

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
    description='Package for demos of Moveit_Py on Jaco2 arm',
    license='BSD-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           "moveit_py = jaco2_moveit_demos.moveit_interface:main",
           "moveit_planning = jaco2_moveit_demos.moveit_planning:main"
        ],
    },
)
