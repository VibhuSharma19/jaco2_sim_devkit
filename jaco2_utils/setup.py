from setuptools import find_packages, setup

package_name = 'jaco2_utils'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='v',
    maintainer_email='1999vibhusharma@gmail.com',
    description='Utilities used for Jaco2 package',
    license='BSD-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           "jaco2_workspace = jaco2_utils.workspace:main",
        ],
    },
)
