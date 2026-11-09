# Useful packages and nodes

> **Read this when** you need a tool for a common job (seeing data, recording it, driving motors, mapping, moving an arm, reading a camera) and want the package name, the install command and one command that proves it works.

These are the packages lab projects reach for first, grouped by task. For each one you get what it does, the apt package name, one example command and the official docs. Apt names follow one pattern: `ros-<distro>-<package name with _ replaced by ->`, so `teleop_twist_keyboard` on Jazzy is `ros-jazzy-teleop-twist-keyboard`. Availability was checked on Sept. 30, 2026 in the [rosdistro index](https://github.com/ros/rosdistro) and in the ROS apt repository's amd64 package lists. The one thing to remember: **check that a package exists for your distro before you plan around it**, especially on Lyrical.

## Contents

- [Availability at a glance](#availability-at-a-glance)
- [Visualization](#visualization)
- [Transforms (tf2)](#transforms-tf2)
- [Recording and replay](#recording-and-replay)
- [Control](#control)
- [Navigation and mapping](#navigation-and-mapping)
- [Manipulation](#manipulation)
- [Perception: cameras and lidars](#perception-cameras-and-lidars)
- [Teleoperation](#teleoperation)
- [Embedded: micro-ROS](#embedded-micro-ros)
- [Simulation bridges](#simulation-bridges)
- [Web and remote access](#web-and-remote-access)
- [Demos](#demos)
- [Availability gaps on Lyrical](#availability-gaps-on-lyrical)
- [Related](#related)

## Availability at a glance

Binary package versions in the main ROS apt repository (amd64) on Sept. 30, 2026. "None" means no binary; you would build from source.

| Package (`ros-<distro>-...`) | Humble | Jazzy | Kilted | Lyrical |
|---|---|---|---|---|
| `rviz2` | 11.2 | 14.1 | 15.0 | 15.2 |
| `rqt-graph` | 1.3 | 1.5 | 1.7 | 1.8 |
| `rqt-tf-tree` | 1.1 | 1.1 | 1.1 | 1.1 |
| `foxglove-bridge` | 3.5 | 3.5 | 3.5 | 3.5 |
| `plotjuggler-ros` | 2.3 | 2.3 | 2.3 | None |
| `tf2-tools` | 0.25 | 0.36 | 0.41 | 0.45 |
| `rosbag2-storage-mcap` | 0.15 | 0.26 | 0.32 | 0.33 |
| `ros2-control`, `ros2-controllers` | 2.54 | 4.48, 4.42 | 5.18, 5.17 | 6.10, 6.9 |
| `navigation2`, `nav2-bringup` | 1.1 | 1.3 | 1.4 | 1.5 |
| `slam-toolbox` | 2.6 | 2.8 | 2.9 | 2.10 |
| `robot-localization` | 3.5 | 3.8 | 3.9 | 3.10 |
| `moveit` | 2.5 | 2.12 | 2.14 | 2.15 |
| `image-pipeline` | 3.0 | 5.0 | 6.0 | 7.1 |
| `cv-bridge` | 3.2 | 4.1 | 4.1 | 4.1 |
| `usb-cam` | 0.8 | 0.8 | 0.8 | None |
| `v4l2-camera` | 0.6 | 0.7 | 0.7 | 0.8 |
| `realsense2-camera` | 4.58 | 4.58 | 4.58 | 4.58 |
| `rplidar-ros` | 2.1 | 2.1 | 2.1 | None |
| `ouster-ros` | 0.15 | 0.15 | 0.15 | None |
| `teleop-twist-keyboard` | 2.4 | 2.4 | 2.4 | 2.4 |
| `joy`, `teleop-twist-joy` | 3.3, 2.4 | 3.3, 2.6 | 3.3, 2.6 | 3.3, 2.6 |
| `ros-gz` | 0.244 | 1.0 | 2.1 | 3.0 |
| `rosbridge-server` | 2.0 | 2.7 | 3.3 | 4.2 |
| `turtlesim`, `demo-nodes-cpp` | Yes | Yes | Yes | Yes |

## Visualization

### RViz 2

The 3D view of your robot's world: robot model, lidar scans, point clouds, camera images, tf frames, maps and paths. Included in the `desktop` install.

- Package: `ros-<distro>-rviz2`
- Try it: `ros2 run rviz2 rviz2` (or just `rviz2`), then **Add** a display such as `TF` or `LaserScan` and set **Fixed Frame** to a frame that exists
- Docs: [RViz user guide](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html)

### rqt tools

rqt is a window that hosts small GUI plugins. The ones you will use most:

| Plugin | Package | Command | Use it to |
|---|---|---|---|
| Node graph | `ros-<distro>-rqt-graph` | `ros2 run rqt_graph rqt_graph` | See which nodes connect to which topics |
| Console | `ros-<distro>-rqt-console` | `ros2 run rqt_console rqt_console` | Filter log messages from every node |
| Image view | `ros-<distro>-rqt-image-view` | `ros2 run rqt_image_view rqt_image_view` | Look at a camera topic |
| TF tree | `ros-<distro>-rqt-tf-tree` | `ros2 run rqt_tf_tree rqt_tf_tree` | See the live frame tree |
| Robot steering | `ros-<distro>-rqt-robot-steering` | `ros2 run rqt_robot_steering rqt_robot_steering` | Drive with sliders (`-p default_stamped:=true` for stamped twists) |
| Plot, reconfigure | `ros-<distro>-rqt-plot`, `ros-<distro>-rqt-reconfigure` | `rqt`, then **Plugins** | Plot numeric fields; edit parameters live |

Install every rqt plugin at once with `sudo apt install 'ros-jazzy-rqt*'`. Docs: [About rqt](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-RQt.html).

### Foxglove

A visualization and debugging app (web and desktop) that connects to a robot through a small bridge node. Useful when you cannot run RViz locally, for example from a Mac.

- Package: `ros-<distro>-foxglove-bridge`
- Try it: `ros2 launch foxglove_bridge foxglove_bridge_launch.xml`, then in the [Foxglove app](https://app.foxglove.dev) choose **Open connection** and `ws://<robot IP>:8765` (8765 is the default port)
- Docs: [Foxglove with ROS 2](https://docs.foxglove.dev/docs/getting-started/frameworks/ros2), [foxglove_bridge source](https://github.com/foxglove/foxglove-sdk)

### PlotJuggler

Fast time-series plotting of live topics and bags.

- Package: `ros-<distro>-plotjuggler-ros` (no Lyrical binary yet)
- Try it: `ros2 run plotjuggler plotjuggler`
- Docs: [plotjuggler-ros-plugins](https://github.com/PlotJuggler/plotjuggler-ros-plugins)

## Transforms (tf2)

`tf2_ros` publishes and looks up transforms; `tf2_tools` draws the tree. Both come with `ros-base`.

| Task | Command |
|---|---|
| Publish a fixed transform (camera 10 cm forward, 30 cm up, turned 90°) | `ros2 run tf2_ros static_transform_publisher --x 0.1 --z 0.3 --yaw 1.57 --frame-id base_link --child-frame-id camera_link` |
| Print one transform | `ros2 run tf2_ros tf2_echo base_link camera_link` |
| Write the whole tree to a PDF | `ros2 run tf2_tools view_frames` |
| See the tree live | `ros2 run rqt_tf_tree rqt_tf_tree` |

We ran the first three in `ros:jazzy`. The old positional form (`static_transform_publisher 0 0 0 0 0 0 parent child`) prints a deprecation warning on Humble through Kilted and fails on Lyrical, so always use the flags. Docs: [tf2 tutorials](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Introduction-To-Tf2.html), [debugging tf2](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Debugging-Tf2-Problems.html).

## Recording and replay

**rosbag2** records topics to disk and plays them back; **MCAP** is its default file format since Iron (a single `.mcap` file that Foxglove and PlotJuggler also open).

- Packages: `ros-<distro>-rosbag2` (in `ros-base`); on Humble add `ros-humble-rosbag2-storage-mcap` for MCAP, since Humble records SQLite by default
- Try it: `ros2 bag record --topics /scan /tf /tf_static` (Jazzy and newer; Humble uses `ros2 bag record /scan /tf /tf_static`), then `ros2 bag info <folder>` and `ros2 bag play <folder>`
- Docs: [recording and playing back data](https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html), [rosbag2](https://github.com/ros2/rosbag2), [MCAP](https://mcap.dev/)

## Control

### ros2_control and ros2_controllers

The standard framework between your algorithms and the motors: a hardware interface plugin talks to the drives, and reusable controllers (differential drive, joint trajectory, gripper) run on top.

- Packages: `ros-<distro>-ros2-control`, `ros-<distro>-ros2-controllers`
- Try it (with a controller manager running): `ros2 control list_controllers`
- Docs: [control.ros.org](https://control.ros.org/jazzy/index.html) (pick your distro in the URL), [getting started](https://control.ros.org/jazzy/doc/getting_started/getting_started.html)
- Note: from Jazzy on, `diff_drive_controller` expects `geometry_msgs/msg/TwistStamped` on `cmd_vel` ([migration notes](https://control.ros.org/jazzy/doc/ros2_controllers/doc/migration.html))

## Navigation and mapping

### Nav2

The navigation stack: localization in a map, path planning, obstacle avoidance and behavior trees, driven by the `NavigateToPose` action.

- Packages: `ros-<distro>-navigation2`, `ros-<distro>-nav2-bringup`
- Try it in simulation (from the Nav2 quickstart; also install `ros-jazzy-nav2-minimal-tb*`): `ros2 launch nav2_bringup tb3_simulation_launch.py headless:=False`
- Docs: [docs.nav2.org](https://docs.nav2.org/), [Jazzy quickstart](https://docs.nav2.org/jazzy/getting_started/quickstart/quickstart/)
- Note: Nav2 releases binaries for released distros only, not Rolling

### slam_toolbox

Builds a 2D map from a lidar while working out where the robot is (SLAM: simultaneous localization and mapping).

- Package: `ros-<distro>-slam-toolbox`
- Try it: `ros2 launch slam_toolbox online_sync_launch.py` (needs `/scan` and tf from `odom` to the lidar)
- Docs: [slam_toolbox README](https://github.com/SteveMacenski/slam_toolbox)

### robot_localization

Fuses wheel odometry, an IMU and GPS into one smooth pose estimate with an extended Kalman filter.

- Package: `ros-<distro>-robot-localization`
- Try it: `ros2 launch robot_localization ekf.launch.py` (edit a copy of its parameter file for your sensors)
- Docs: [repository](https://github.com/cra-ros-pkg/robot_localization) and Nav2's [robot_localization guide](https://docs.nav2.org/rolling/configuration_and_development/first_time_robot_setup_guide/odom/setup_robot_localization/)

## Manipulation

### MoveIt 2

Motion planning for arms: collision-aware paths, inverse kinematics, grasp pipelines and an RViz plugin to drag the arm to a goal.

- Package: `ros-<distro>-moveit`
- Try it: `ros2 launch moveit_setup_assistant setup_assistant.launch.py` to generate a MoveIt config for your arm's URDF
- Docs: [MoveIt 2 docs](https://moveit.picknik.ai/main/index.html) (Jazzy and Rolling) and [Humble docs](https://moveit.picknik.ai/humble/index.html)
- Note: MoveIt's [binary install page](https://moveit.ai/install-moveit2/binary/) lists Humble (Ubuntu 22.04), Jazzy and Kilted (Ubuntu 24.04), and Lyrical and Rolling (Ubuntu 26.04)

## Perception: cameras and lidars

| Package | What it does | apt name | Example | Docs |
|---|---|---|---|---|
| image_pipeline | Rectify, debayer, resize and convert images; stereo processing | `ros-<distro>-image-pipeline` | `ros2 launch image_proc image_proc.launch.py namespace:=my_camera` | [image_proc tutorials](https://docs.ros.org/en/jazzy/p/image_proc/doc/tutorials.html) |
| vision_opencv (cv_bridge) | Convert ROS images to OpenCV and back (a library) | `ros-<distro>-cv-bridge` | `from cv_bridge import CvBridge` in Python | [vision_opencv](https://github.com/ros-perception/vision_opencv) |
| usb_cam | Driver for USB webcams (V4L2) | `ros-<distro>-usb-cam` (no Lyrical binary) | `ros2 run usb_cam usb_cam_node_exe` | [usb_cam](https://github.com/ros-drivers/usb_cam) |
| v4l2_camera | Another USB/V4L2 camera driver | `ros-<distro>-v4l2-camera` | `ros2 run v4l2_camera v4l2_camera_node` | [v4l2_camera](https://gitlab.com/boldhearts/ros2_v4l2_camera) |
| realsense2_camera | Intel RealSense depth cameras | `ros-<distro>-realsense2-camera` | `ros2 launch realsense2_camera rs_launch.py` | [realsense-ros](https://github.com/realsenseai/realsense-ros) |
| rplidar_ros | Slamtec RPLIDAR 2D lidars | `ros-<distro>-rplidar-ros` (no Lyrical binary) | Launch file names differ by version: list them with `ls $(ros2 pkg prefix rplidar_ros)/share/rplidar_ros/launch` | [rplidar_ros](https://github.com/Slamtec/rplidar_ros) |
| sllidar_ros2 | Slamtec's newer driver for recent RPLIDAR models | Source only | `ros2 launch sllidar_ros2 view_sllidar_a1_launch.py` | [sllidar_ros2](https://github.com/Slamtec/sllidar_ros2) |
| velodyne | Velodyne 3D lidars | `ros-<distro>-velodyne` (Lyrical has only the driver and message packages) | Launch files in `velodyne/launch` | [velodyne](https://github.com/ros-drivers/velodyne) |
| ouster-ros | Ouster 3D lidars | `ros-<distro>-ouster-ros` (no Lyrical binary) | `ros2 launch ouster_ros sensor.launch.xml sensor_hostname:=<sensor host name>` | [ouster-ros](https://github.com/ouster-lidar/ouster-ros) |

Hardware drivers need access to the device (`/dev/video*`, `/dev/ttyUSB*`), so run them natively or in a container you started with that device passed in; [ROSEnv](04-install-rosenv.md#limitations) cannot pass devices through yet.

## Teleoperation

Teleoperation means driving the robot yourself, from a keyboard or a gamepad.

| Package | apt name | Command | Notes |
|---|---|---|---|
| teleop_twist_keyboard | `ros-<distro>-teleop-twist-keyboard` | `ros2 run teleop_twist_keyboard teleop_twist_keyboard` | Add `--ros-args -p stamped:=true` for controllers that need `TwistStamped`; remap with `-r cmd_vel:=/your/topic` |
| joy | `ros-<distro>-joy` | `ros2 run joy joy_node` | Reads a gamepad and publishes `/joy` |
| teleop_twist_joy | `ros-<distro>-teleop-twist-joy` | `ros2 launch teleop_twist_joy teleop-launch.py joy_config:='xbox'` | Turns `/joy` into `cmd_vel`; hold the enable button to move; `publish_stamped_twist` parameter for stamped output |

Docs: [teleop_twist_keyboard](https://github.com/ros2/teleop_twist_keyboard), [joy](https://github.com/ros-drivers/joystick_drivers), [teleop_twist_joy](https://github.com/ros2/teleop_twist_joy).

> [!WARNING]
> Before any teleoperation on a real robot: clear the area, start at low speed, and have someone ready at the robot's emergency stop. Follow the lab's safety rules: `[lab robot safety page]`.

## Embedded: micro-ROS

micro-ROS puts ROS 2 on microcontrollers (ESP32, STM32, Teensy and others). The microcontroller talks to a **micro-ROS agent** on a computer over serial, UDP or other transports, and the agent bridges it into the normal ROS 2 graph.

- Packages: the setup tools and the agent are **not** released as apt packages; build them with [`micro_ros_setup`](https://github.com/micro-ROS/micro_ros_setup) (branches for Humble, Jazzy, Kilted, Lyrical and Rolling) or use the Docker image (tags for Humble, Jazzy, Kilted and Rolling; none for Lyrical)
- Try it: `docker run -it --rm --net=host microros/micro-ros-agent:jazzy udp4 --port 8888`
- Docs: the project website moved to [micro.vulcanexus.org](https://micro.vulcanexus.org/) ([first application on Linux](https://micro.vulcanexus.org/docs/tutorials/core/first_application_linux/))

## Simulation bridges

### Gazebo (ros_gz)

`ros_gz` connects ROS 2 to Gazebo (the simulator formerly called Ignition). Each distro pairs with one recommended Gazebo release ([Gazebo and ROS installation](https://gazebosim.org/docs/latest/ros_installation/)):

| ROS 2 | Gazebo | Gazebo end of life ([releases](https://gazebosim.org/docs/latest/releases/)) |
|---|---|---|
| Humble | Fortress | May 2027 |
| Jazzy | Harmonic | May 2029 |
| Kilted | Ionic | December 2026 |
| Lyrical | Jetty | May 2031 |

- Package: `ros-<distro>-ros-gz` (installs the matching Gazebo)
- Try it: `ros2 launch ros_gz_sim gz_sim.launch.py gz_args:=empty.sdf`, and bridge a topic with `ros2 run ros_gz_bridge parameter_bridge /scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan`
- Docs: [ROS 2 integration](https://gazebosim.org/docs/latest/ros2_integration/); lab page: [Gazebo in the tech stack](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/tech-stack/gazebo.md)

Gazebo Classic (Gazebo 11) reached end of life in January 2025; do not start new simulations on it.

### NVIDIA Isaac Sim

A GPU-accelerated simulator with a built-in ROS 2 bridge. Its current docs (Isaac Sim 6.2) recommend **Jazzy on Ubuntu 24.04** and also test Humble on Ubuntu 22.04; other natively installed distros on Ubuntu 22.04 or 24.04 are experimental ([Isaac Sim ROS installation](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html)). Check NVIDIA's [system requirements](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html) before you install. Lab page: [Isaac Sim in the tech stack](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/tech-stack/isaac-sim.md).

## Web and remote access

### rosbridge_suite

Exposes topics, services and parameters as JSON over a WebSocket, so a web page (for example with `roslibjs`) or any language without a ROS client library can join.

- Package: `ros-<distro>-rosbridge-server`
- Try it: `ros2 launch rosbridge_server rosbridge_websocket_launch.xml`, then connect to `ws://<robot IP>:9090` (9090 is the default port in the launch file)
- Docs: [rosbridge_suite](https://github.com/RobotWebTools/rosbridge_suite)

> [!CAUTION]
> rosbridge and foxglove_bridge let anyone who can reach the port read and publish topics, including `cmd_vel`. Run them only on a trusted network, never on a port exposed to the internet.

## Demos

| Package | Command | Use it to |
|---|---|---|
| `demo_nodes_cpp`, `demo_nodes_py` | `ros2 run demo_nodes_cpp talker`, `ros2 run demo_nodes_py listener` | Test an install or a network link |
| `turtlesim` | `ros2 run turtlesim turtlesim_node`, then `ros2 run turtlesim turtle_teleop_key` | Learn topics, services, actions and parameters with a toy robot |

Both come with the `desktop` install. Beginner tutorials built on them: [ROS 2 CLI tutorials](https://docs.ros.org/en/jazzy/Tutorials.html).

## Availability gaps on Lyrical

Lyrical is four months old. On Sept. 30, 2026 these packages had a Lyrical entry in rosdistro but **no Lyrical binary** in the main apt repository for Ubuntu 26.04 (amd64): `usb_cam`, `rplidar_ros`, the `velodyne` metapackage (its driver and message packages exist), `ouster_ros` and `plotjuggler_ros`. The micro-ROS agent Docker image has no Lyrical tag (`micro_ros_setup` has a `lyrical` branch), and Isaac Sim's docs did not list Lyrical. If your project needs any of these, use Jazzy or build the package from source in your workspace. Re-check before deciding: `apt-cache policy ros-lyrical-<package>`.

## Related

- [Command cheatsheet](05-cheatsheet.md)
- [Debugging](07-debugging.md): tools from this page in action
- [Lab robots](08-lab-robots.md): which drivers each lab device uses
- [External resources](09-resources.md)
- Search every released package: [ROS Index](https://index.ros.org/)

<sub>Last reviewed: Nov. 9, 2026 · Sources checked on that date · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/docs/06-packages-and-nodes.md)</sub>
