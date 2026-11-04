from glob import glob

from setuptools import find_packages, setup

package_name = 'hello_atr'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # Lets ROS 2 tools find the package.
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Installs the launch and parameter files so `ros2 launch` can find them.
        ('share/' + package_name + '/launch', glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Advanced Telerobotics Research Laboratory contributors',
    maintainer_email='atrlab.kent@gmail.com',
    description='A small ROS 2 publisher and subscriber for learning.',
    license='MIT',
    extras_require={'test': ['pytest']},
    entry_points={
        'console_scripts': [
            'talker = hello_atr.talker:main',
            'listener = hello_atr.listener:main',
        ],
    },
)
