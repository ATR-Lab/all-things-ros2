# Lab robots and ROS 2

> **Read this when** you are about to write ROS 2 code for one of the lab's robots or computers and need to know how it connects to ROS 2, which distribution to use and where the drivers live.

Each device in the lab reaches ROS 2 differently: some have an official vendor driver, some depend on community packages, and one is not ROS-native at all. This page covers the Unitree Go2 Pro, Booster K1, ROBOTIS OpenManipulator-X, LeRobot SO-101, NVIDIA Jetson AGX Thor, Raspberry Pi 5 and Yahboom ROSMASTER X3, from vendor and project sources checked on Sept. 30, 2026. The one thing to remember: **the robot's software decides the distribution**, so check its section before you install anything. Setup, unboxing and checkout steps for each device are on its hardware page in [getting-started-atr-lab](https://github.com/ATR-Lab/getting-started-atr-lab).

## Contents

- [At a glance](#at-a-glance)
- [Unitree Go2 Pro](#unitree-go2-pro)
- [Booster K1](#booster-k1)
- [ROBOTIS OpenManipulator-X](#robotis-openmanipulator-x)
- [LeRobot SO-101](#lerobot-so-101)
- [NVIDIA Jetson AGX Thor](#nvidia-jetson-agx-thor)
- [Raspberry Pi 5](#raspberry-pi-5)
- [Yahboom ROSMASTER X3](#yahboom-rosmaster-x3)
- [Related](#related)

## At a glance

| Device | How it talks to ROS 2 | Distro to use | Lab repo | Hardware page |
|---|---|---|---|---|
| Unitree Go2 **Pro** | Community package over Wi-Fi (WebRTC); the official ROS 2 interface is for the EDU model | Humble | [go2_ws](https://github.com/ATR-Lab/go2_ws) | [unitree-go2](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/unitree-go2.md) |
| Booster K1 | Vendor SDK on Fast DDS, plus a vendor ROS 2 message package | Humble (matches the SDK's Ubuntu 22.04) | [expressive-motion](https://github.com/ATR-Lab/expressive-motion) (not a ROS package) | [booster-k1](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/booster-k1.md) |
| ROBOTIS OpenManipulator-X | Official ROS 2 packages (ros2_control) | Jazzy | None | [openmanipulator-x](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/openmanipulator-x.md) |
| LeRobot SO-101 | Not ROS-native (Python LeRobot); community ROS 2 bridges only | Jazzy if you bridge it (Python 3.12) | None | [lerobot-so-101](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/lerobot-so-101.md) |
| NVIDIA Jetson AGX Thor | A computer: ROS 2 installs natively on JetPack 7 (Ubuntu 24.04) | Jazzy | None | [jetson-agx-thor](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/jetson-agx-thor.md) |
| Raspberry Pi 5 | A computer: native on 64-bit Ubuntu, Docker on Raspberry Pi OS | Jazzy (Ubuntu 24.04) | [robo_mower_ws](https://github.com/ATR-Lab/robo_mower_ws) | [raspberry-pi-5](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/raspberry-pi-5.md) |
| Yahboom ROSMASTER X3 | Vendor images and Docker (Foxy on Nano and Pi 5; Orin images on JetPack 6.2) | Vendor's image; port to Humble or Jazzy for new work | [yahboom_r2l_ros2](https://github.com/ATR-Lab/yahboom_r2l_ros2) (for the R2L model) | [rosmaster-x3](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/rosmaster-x3.md) |

> [!WARNING]
> These are real machines that move fast and can hurt people or break. Before running any ROS 2 code on a robot, follow the lab's robot safety rules (`[lab robot safety page]`), clear the area, start at low speed and keep the emergency stop or remote in reach. Never test new motion code on a robot for the first time without someone watching it.

## Unitree Go2 Pro

A quadruped (four-legged robot, a "robot dog" for general readers) made by Unitree. The lab's unit is the **Pro** model: `[confirm the lab's Go2 model(s) and firmware version]`.

**Official ROS 2 support is for the EDU model, not the Pro.**

- Unitree's developer FAQ says only EDU and higher versions can be developed on, and that "PRO and AIR versions do not open the secondary development interface" ([Unitree developer FAQ](https://support.unitree.com/home/en/developer/FAQ)). The spec table on the [Go2 product page](https://www.unitree.com/go2/) marks secondary development as unavailable for AIR and PRO and full for EDU.
- The official packages are [unitree_sdk2](https://github.com/unitreerobotics/unitree_sdk2) (C++, BSD-3-Clause, built on Cyclone DDS; prebuilt for Ubuntu 20.04) and [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2) (BSD-3-Clause). The `unitree_ros2` README lists tested systems Ubuntu 20.04 with Foxy and Ubuntu 22.04 with Humble ("recommend"), connects over Ethernet and requires Cyclone DDS 0.10.2.

**What Pro owners use instead: community packages that talk to the robot the way Unitree's phone app does, over WebRTC on Wi-Fi.** None of these are made or supported by Unitree.

| Project | What it is | License | Status on Sept. 30, 2026 |
|---|---|---|---|
| [abizovnuralem/go2_ros2_sdk](https://github.com/abizovnuralem/go2_ros2_sdk) | "Unofficial ROS2 SDK support for Unitree GO2 AIR/PRO/EDU": URDF, joint states, IMU, lidar point cloud and laser scan, camera and joystick control, plus examples with slam_toolbox and Nav2, over WebRTC (Wi-Fi) or Cyclone DDS (Ethernet) | BSD-2-Clause | Active (last push July 13, 2026). README tests Ubuntu 22.04 with Iron, Humble and Rolling; CI builds Humble and Jazzy; its Dockerfile starts from `ros:humble-ros-base` |
| [legion1581/unitree_webrtc_connect](https://github.com/legion1581/unitree_webrtc_connect) (formerly `go2_webrtc_connect`) | Python WebRTC driver for Go2 AIR, PRO and EDU; not a ROS package | MIT | Active (v2.2.0, Aug. 17, 2026) |
| [tfoldi/go2-webrtc](https://github.com/tfoldi/go2-webrtc) | Browser UI and Python API over WebRTC; not a ROS package | BSD-2-Clause | Last push January 2026; its README points to legion1581's library for more features |

Caveats from the `go2_ros2_sdk` README:

- Close the Unitree phone app's connection before connecting over WebRTC.
- Robots on **firmware 1.1.15 or newer** need a per-device AES-128 key (the `aes_key` parameter or the `ROBOT_AES_KEY` environment variable); support for this was merged in July 2026.
- On firmware 1.1.7, joint states arrive at about 1 Hz, so the robot model in RViz lags.

**Distro:** Humble on Ubuntu 22.04, matching the community SDK's tested setup and the lab's workspace.

**Lab repo:** [ATR-Lab/go2_ws](https://github.com/ATR-Lab/go2_ws) is the lab's Go2 workspace ("Robot Dog Petting Zoo"): computer vision, human interaction, speech, navigation, dance and teleoperation packages built on a copy of `go2_ros2_sdk` in `src/`. It targets Humble (its `activate_workspace.sh`, dependency script and `src/docker/Dockerfile`, which starts from `ros:humble-ros-base`). Its copy of the SDK predates the upstream `aes_key` change, so it may not connect to a Go2 on firmware 1.1.15 or newer until the copy is updated: `[lab to confirm Go2 firmware and whether go2_ws needs the upstream update]`.

## Booster K1

A small humanoid (a robot shaped roughly like a person) from Booster Robotics. The current [K1 specifications](https://docs.booster.tech/docs/product-manual/k1/getting-started/specifications/) list Geek, Education and Professional variants with different onboard computers: `[confirm the lab's K1 variant]`.

**How it talks to ROS 2: through Booster's SDK, which uses Fast DDS, the same middleware family as ROS 2.**

- [booster_robotics_sdk](https://github.com/BoosterRobotics/booster_robotics_sdk) is the C++ SDK (its README says Apache 2.0; prebuilt for Ubuntu 22.04 on aarch64 and x86_64). A Python SDK is published separately.
- Booster's [SDK overview](https://docs.booster.tech/docs/developer-guide/cpp/sdk-overview/) says the SDK is compatible with ROS 2's DDS communication: "When message types, topic names, and QoS settings match, ROS 2 nodes and Booster Robotics SDK applications can communicate."
- [booster_robotics_sdk_ros2](https://github.com/BoosterRobotics/booster_robotics_sdk_ros2) provides the ROS 2 message and service definitions (`booster_interface`: low-level state and command, motor and IMU state, odometry, RPC services) and examples. It has no license file and does not state a distro.
- Booster's own [robocup_demo](https://github.com/BoosterRobotics/robocup_demo) (Apache-2.0) is "designed for running on Booster K1", supports JetPack 6.2 (Ubuntu 22.04) and installs Humble packages.

**Distro:** Humble on Ubuntu 22.04, which matches the SDK's prebuilt environment and Booster's demo. Booster's C++ quick start also mentions Ubuntu 24.04; we found no official statement of a supported ROS 2 distro, so confirm with Booster before moving the robot's computer to another one.

**Lab repo:** [ATR-Lab/expressive-motion](https://github.com/ATR-Lab/expressive-motion) (MIT) turns a video of a person walking into a K1 reference motion and a training task. It is not a ROS package; its README notes that running on the robot additionally needs Booster's SDK, firmware, ROS 2, networking and safety procedures.

## ROBOTIS OpenManipulator-X

A small arm with four joints plus a gripper (five Dynamixel XM430-W350-T servos, 500 g payload, per the [specification](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/specification/)).

**How it talks to ROS 2: official ROBOTIS packages built on ros2_control.**

- The [OpenManipulator-X quick start](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/quick_start_guide/) has tabs for Jazzy ("ROS 2 Jazzy is supported on Ubuntu 24.04"; Docker recommended, or build from source), Humble (Ubuntu 22.04) and ROS 1 Noetic.
- Source: [ROBOTIS-GIT/open_manipulator](https://github.com/ROBOTIS-GIT/open_manipulator) (Apache-2.0), with `jazzy` and `humble` branches. The `jazzy` branch is under active development (updated Sept. 28, 2026) and is the only distro its CI builds; the `humble` branch was last updated in July 2025.
- Binaries: `ros-jazzy-open-manipulator` (and its bringup, description, GUI, MoveIt config and teleop packages) at version 4.1.3, older than the 5.1.3 source; Humble packages are named `ros-humble-open-manipulator-x-*` at 3.0.4.
- Lower layers: `ros-<distro>-dynamixel-sdk` ([DynamixelSDK](https://github.com/ROBOTIS-GIT/DynamixelSDK)) and `ros-<distro>-dynamixel-hardware-interface` ([dynamixel_hardware_interface](https://github.com/ROBOTIS-GIT/dynamixel_hardware_interface), a ros2_control plugin), both released for Humble and Jazzy.

```bash
# Jazzy, per the ROBOTIS quick start (Docker route)
git clone -b jazzy https://github.com/ROBOTIS-GIT/open_manipulator.git
cd open_manipulator
./docker/container.sh start
./docker/container.sh enter
```

**Distro:** Jazzy on Ubuntu 24.04. The arm connects over USB through a ROBOTIS U2D2 adapter (the container script installs a udev rule for it), and the ROBOTIS Docker setup runs privileged with `/dev` mounted and host networking. Run it natively or in that container, not in [ROSEnv](04-install-rosenv.md#limitations).

## LeRobot SO-101

A low-cost six-motor arm (a leader arm you move by hand and a follower arm that copies it) designed by TheRobotStudio and used with Hugging Face's LeRobot library for learning robot policies from demonstrations.

**It is not ROS-native.**

- [LeRobot](https://github.com/huggingface/lerobot) (Apache-2.0) is a Python and PyTorch library; the [PyPI package](https://pypi.org/project/lerobot/) (0.6.1) requires Python 3.12 or newer.
- The [SO-101 guide](https://huggingface.co/docs/lerobot/so101) sets it up with `pip install -e ".[feetech]"` and the `lerobot-find-port`, `lerobot-setup-motors` and `lerobot-calibrate` commands. The follower uses six Feetech STS3215 servos on a USB serial bus. The guide does not use ROS.
- [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) (Apache-2.0) holds the hardware files and a URDF and MuJoCo model in `Simulation/SO101`, which you can load in RViz or a simulator.

**Community ROS 2 bridges** (not from Hugging Face or TheRobotStudio; check each before relying on it):

| Project | Distro | License | Notes |
|---|---|---|---|
| [nimiCurtis/so101_ros2](https://github.com/nimiCurtis/so101_ros2) | Humble | MIT | LeRobot-to-ROS 2 bridge, teleoperation and dataset recording; last push December 2025 |
| [adoodevv/so101_ros2](https://github.com/adoodevv/so101_ros2) | Jazzy | BSD-3-Clause | Gazebo Harmonic and MoveIt 2; its README says the real-hardware interface is not implemented yet |
| [SeeedJP/lerobot_ros2_so101](https://github.com/SeeedJP/lerobot_ros2_so101) | Humble on JetPack 6.0 | MIT | Last push September 2025 |

**Distro:** use LeRobot directly (in a Python virtual environment) unless you need the arm in a ROS graph. If you do, prefer Jazzy: Ubuntu 24.04's Python 3.12 meets LeRobot's minimum, while Humble's Ubuntu 22.04 ships Python 3.10.

## NVIDIA Jetson AGX Thor

NVIDIA's robotics computer module. It is not a robot but a computer you put on one.

- **JetPack 7** supports Thor and is "built on Linux Kernel 6.8 and Ubuntu 24.04 LTS" ([JetPack](https://developer.nvidia.com/embedded/jetpack)). So ROS 2 **Jazzy** installs natively with the [normal Ubuntu steps](03-install-native.md#step-2-install-your-distribution) (arm64 is Tier 1).
- **Isaac ROS** (NVIDIA's GPU-accelerated ROS 2 packages): 4.0.0 (Oct. 24, 2025) added Jetson AGX Thor and JetPack 7.0 support, and the 4.x releases target Jazzy. Isaac ROS 5.0.0 (Sept. 21, 2026) "migrated to ROS 2 Lyrical Luth" and adds NVIDIA's own apt buildfarm with Lyrical packages for Ubuntu 24.04 ([Isaac ROS release notes](https://nvidia-isaac-ros.github.io/releases/index.html)). Upstream, Lyrical is only Tier 3 on Ubuntu 24.04.

**Distro:** Jazzy. Move to Isaac ROS 5.0 and Lyrical only if you need something in that release, and then use NVIDIA's packages for everything, not a mix. See [Jetson notes](03-install-native.md#nvidia-jetson) for other JetPack versions.

## Raspberry Pi 5

A small single-board computer, often the robot's onboard computer in student builds.

- Ubuntu 24.04 is the first LTS with Raspberry Pi 5 images ([Ubuntu 24.04 release notes](https://documentation.ubuntu.com/release-notes/24.04/)), and Ubuntu's [Raspberry Pi support matrix](https://ubuntu.com/hardware/docs/boards/how-to/ubuntu_supported/raspberry-pi/) lists the Pi 5 for 24.04 and 26.04 but not 22.04.
- ROS 2 on 64-bit Ubuntu uses the normal apt install; on Raspberry Pi OS (Debian, Tier 3) the ROS docs recommend Docker ([ROS 2 on Raspberry Pi](https://docs.ros.org/en/jazzy/How-To-Guides/Installing-on-Raspberry-Pi.html)).

**Distro:** Jazzy on Ubuntu 24.04 (64-bit) with `ros-jazzy-ros-base`; Lyrical on Ubuntu 26.04 also works. Humble only in Docker. Full steps: [install notes](03-install-native.md#raspberry-pi-5).

**Lab repo:** [ATR-Lab/robo_mower_ws](https://github.com/ATR-Lab/robo_mower_ws) (MIT) is the lab's robot mower workspace: a RoboClaw motor controller, Arduino-read encoders, an RPLIDAR with SLAM, a camera and remote control of a Raspberry Pi. Its documentation installs Jazzy, and its `NETWORK_SETUP_GUIDE.md` pairs a Humble PC with a Jazzy Raspberry Pi. The official ROS docs say [nodes are not guaranteed to communicate across distributions](https://docs.ros.org/en/lyrical/Releases.html), so run one distro on both machines for anything beyond simple teleoperation: `[lab to confirm the mower's current distros]`.

## Yahboom ROSMASTER X3

A mecanum-wheel (omnidirectional) educational robot car with a lidar, depth camera and voice module, sold with a Jetson Nano 4GB, Jetson Orin Nano Super, Jetson Orin NX Super or Raspberry Pi 5 as its controller ([Yahboom product page](https://category.yahboom.net/products/rosmaster-x3)).

**How it talks to ROS 2: Yahboom's own system images, Docker images and tutorials.**

- The product page says Yahboom provides ROS 1 and ROS 2 system images and Docker for the X3, "using Humble and Foxy", with tutorials for ROS 1 Melodic, ROS 2 Foxy and Humble. Asked in 2025 about newer distros, Yahboom replied on the same page: "we currently have no plans to upgrade to other versions."
- Tutorials and code: the [ROSMASTER X3 study page](https://www.yahboom.net/study/ROSMASTER-X3) and the [YahboomTechnology/ROSMASTERX3](https://github.com/YahboomTechnology/ROSMASTERX3) repository (PDF tutorials; no license file).
- In those tutorials, ROS 2 on the Jetson Nano and Raspberry Pi 5 runs inside Yahboom's **Foxy** Docker image (`yahboomtechnology/ros-foxy`), and the Orin images are built on JetPack 6.2 (Ubuntu 22.04) without Docker. We did not find an explicit statement of the ROS 2 distro on the Orin images: `[confirm the distro on the lab's X3 image]`.

**Distro:** keep Yahboom's image to run the vendor demos. Foxy reached end of life in June 2023 ([distributions](02-distributions.md)), so write new lab code for Humble or Jazzy and port the drivers you need.

**Lab repo:** [ATR-Lab/yahboom_r2l_ros2](https://github.com/ATR-Lab/yahboom_r2l_ros2) is a "ROS2 Humble port of the Yahboom R2L robot platform, migrated from ROS1 Noetic", with bringup, control, description, messages and a multi-robot racing UI; its README supports Foxy (Ubuntu 20.04) or Humble (Ubuntu 22.04). It is for the Yahboom **R2L**, a different model from the ROSMASTER X3: `[confirm which Yahboom models the lab has]`.

## Related

- [Distributions and which to choose](02-distributions.md)
- [Install natively](03-install-native.md): Raspberry Pi 5 and Jetson notes
- [Useful packages and nodes](06-packages-and-nodes.md): drivers, ros2_control, MoveIt 2
- [Debugging](07-debugging.md): networking to a robot
- Lab: [getting-started-atr-lab hardware pages](https://github.com/ATR-Lab/getting-started-atr-lab), [dev-guidelines: ROS 2 packages](https://github.com/ATR-Lab/dev-guidelines/blob/master/docs/ros2-packages.md)

<sub>Last reviewed: Sept. 30, 2026 · Sources checked on that date · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/docs/08-lab-robots.md)</sub>
