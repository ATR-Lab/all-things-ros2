# External resources

> **Read this when** this handbook does not answer your question and you need the official reference, a place to ask, or something longer to learn from.

These are the sources the lab trusts for ROS 2, each checked on Sept. 30, 2026. Start with the official documentation for your distribution and search before you ask. Prefer a primary source (docs, REPs, a package's own README) over a blog post or a video. The one thing to remember: **make sure a page matches your distribution**; the docs site has a version selector, and advice for ROS 1 or an old ROS 2 release is a common source of confusion.

## Contents

- [Official documentation](#official-documentation)
- [Standards and design](#standards-and-design)
- [Finding packages](#finding-packages)
- [Asking questions and community](#asking-questions-and-community)
- [Stack documentation](#stack-documentation)
- [Courses, books and tutorials](#courses-books-and-tutorials)
- [Lab repositories](#lab-repositories)
- [Related](#related)

## Official documentation

| Resource | Use it for |
|---|---|
| [ROS 2 docs: Lyrical](https://docs.ros.org/en/lyrical/), [Jazzy](https://docs.ros.org/en/jazzy/), [Humble](https://docs.ros.org/en/humble/) | Installation, concepts, tutorials and how-to guides for each distribution. Lyrical's docs use a new layout (for example `Get-Started/Installation/...`), so older links may not map one to one |
| [Distributions](https://docs.ros.org/en/lyrical/Releases.html) | Release and end-of-life dates, release notes and "changes since" lists |
| [Tutorials](https://docs.ros.org/en/jazzy/Tutorials.html) | The official beginner-to-advanced learning path (CLI tools, client libraries, launch, tf2, URDF) |
| [Concepts](https://docs.ros.org/en/jazzy/Concepts.html) | Short explanations of nodes, topics, QoS, discovery, executors and more |
| [Installation troubleshooting](https://docs.ros.org/en/lyrical/Get-Started/Installation/Installation-Troubleshooting.html) | Known install problems |
| [ROS 2 source on GitHub](https://github.com/ros2) | Core repositories, issues and changelogs |

## Standards and design

| Resource | Use it for |
|---|---|
| [REP index](https://reps.openrobotics.org/) | ROS Enhancement Proposals: the conventions the ecosystem follows |
| [REP 2000](https://reps.openrobotics.org/rep-2000/) | Release schedule and target platforms per distribution (it had not added Lyrical when we checked) |
| [REP 103](https://reps.openrobotics.org/rep-0103/), [REP 105](https://reps.openrobotics.org/rep-0105/) | Units, axis directions and standard frame names (`map`, `odom`, `base_link`) |
| [REP 2004](https://reps.openrobotics.org/rep-2004/) | Package quality levels |
| [ROS 2 design](https://design.ros2.org/) | Why ROS 2 works the way it does, for example [clock and time](https://design.ros2.org/articles/clock_and_time.html) |

## Finding packages

| Resource | Use it for |
|---|---|
| [ROS Index](https://index.ros.org/) | Search packages by name and see which distros they are released for |
| [rosdistro](https://github.com/ros/rosdistro) | The authoritative list of released packages and their versions (`<distro>/distribution.yaml`) and the rosdep rules |
| [snapshots.ros.org](http://snapshots.ros.org/) | Frozen copies of the apt repository, including final snapshots of end-of-life distros |

## Asking questions and community

| Where | When |
|---|---|
| The lab's `[Slack channel]` | First, for anything about lab robots, machines or projects |
| [Robotics Stack Exchange](https://robotics.stackexchange.com/) | Technical questions; tag them `ros2` and your distro. It replaced ROS Answers, which is now a [read-only archive](https://answers.ros.org/) |
| [ROS Discourse](https://discourse.openrobotics.org/) | Announcements, new package releases, working groups and longer discussions |
| A package's GitHub issues | Bugs in that package, after checking existing issues |
| [ROSCon](https://roscon.ros.org/) | The annual ROS developers conference; past talks are linked from each year's site |

Before posting, read [asking for help](07-debugging.md#asking-for-help) and include your distro, OS and the exact error.

## Stack documentation

The big frameworks keep their own docs; pick the page for your distro.

| Project | Docs |
|---|---|
| Nav2 (navigation) | [docs.nav2.org](https://docs.nav2.org/), [tutorials](https://docs.nav2.org/jazzy/tutorials/index.html) |
| MoveIt 2 (manipulation) | [moveit.picknik.ai](https://moveit.picknik.ai/main/index.html), [tutorials](https://moveit.picknik.ai/main/doc/tutorials/tutorials.html) |
| ros2_control | [control.ros.org](https://control.ros.org/jazzy/index.html), [demos](https://control.ros.org/jazzy/doc/ros2_control_demos/doc/index.html) |
| Gazebo | [gazebosim.org docs](https://gazebosim.org/docs/latest/), [tutorials](https://gazebosim.org/docs/latest/tutorials/), [ROS 2 integration](https://gazebosim.org/docs/latest/ros2_integration/) |
| NVIDIA Isaac ROS and Isaac Sim | [Isaac ROS](https://nvidia-isaac-ros.github.io/), [Isaac Sim ROS installation](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/install_ros.html) |
| micro-ROS | [micro.vulcanexus.org](https://micro.vulcanexus.org/) |
| Foxglove | [docs.foxglove.dev](https://docs.foxglove.dev/docs/getting-started/frameworks/ros2) |
| ROSEnv | [README and user guide](https://github.com/MarcoDotIO/rosenv) |

## Courses, books and tutorials

- **Official ROS 2 tutorials** ([Jazzy](https://docs.ros.org/en/jazzy/Tutorials.html)). Start here. Work through "Beginner: CLI tools" and "Beginner: client libraries" in order; they use turtlesim and need only a laptop.
- **ROS-Industrial training** ([industrial-training-master.readthedocs.io](https://industrial-training-master.readthedocs.io/en/humble/)). A free, structured course with ROS 2 sessions on workspaces, nodes, URDF, tf and MoveIt; the current version is written for Humble, so adjust package names for newer distros.
- **Francisco Martín Rico, *A Concise Introduction to Robot Programming with ROS 2*, 2nd edition** (Chapman & Hall/CRC, 2025; [publisher page](https://www.routledge.com/A-Concise-Introduction-to-Robot-Programming-with-ROS-2/Rico/p/book/9781032851488), [code](https://github.com/fmrico/book_ros2)). A textbook written by a Nav2 contributor that covers the computation graph, a simulated robot, behavior trees and Nav2. Ask the lab manager (Marcus Arnett, <marnett5@kent.edu>) whether the lab or the library has a copy.
- **Stack tutorials**: [Nav2](https://docs.nav2.org/jazzy/tutorials/index.html), [MoveIt 2](https://moveit.picknik.ai/main/doc/tutorials/tutorials.html) and [Gazebo](https://gazebosim.org/docs/latest/tutorials/), each maintained by the project.

> [!TIP]
> A tutorial written for ROS 1 (commands like `rosrun`, `roslaunch`, `catkin_make`) will not work in ROS 2. The ROS 2 equivalents are `ros2 run`, `ros2 launch` and `colcon build`.

## Lab repositories

Public ATR-Lab repositories that use or document ROS 2:

| Repository | What it is |
|---|---|
| [getting-started-atr-lab](https://github.com/ATR-Lab/getting-started-atr-lab) | Onboarding: accounts, tools, the [tech stack](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/tech-stack/README.md) and a page per lab device |
| [dev-guidelines](https://github.com/ATR-Lab/dev-guidelines) | Coding conventions, including [ROS 2 packages](https://github.com/ATR-Lab/dev-guidelines/blob/master/docs/ros2-packages.md) |
| [go2_ws](https://github.com/ATR-Lab/go2_ws) | Unitree Go2 workspace built on the community Go2 ROS 2 SDK (Humble) |
| [yahboom_r2l_ros2](https://github.com/ATR-Lab/yahboom_r2l_ros2) | ROS 2 port of the Yahboom R2L platform from ROS 1 Noetic (Foxy or Humble) |
| [robo_mower_ws](https://github.com/ATR-Lab/robo_mower_ws) | Robot mower: motor control, lidar, SLAM and camera on a Raspberry Pi (Jazzy) |
| [kami-head](https://github.com/ATR-Lab/kami-head) | Coffee Buddy, a service robot with a ROS 2 architecture; its README shows a Humble badge and lists Ubuntu 24.04 and macOS (RoboStack) |
| [TeleBot-4R](https://github.com/ATR-Lab/TeleBot-4R) | ROS 2 software for TeleBot-4R, the lab's telepresence robot (2023 to 2024) |
| [expressive-motion](https://github.com/ATR-Lab/expressive-motion) | Video-to-motion pipeline for the Booster K1 (not a ROS package) |

## Related

- [What is ROS 2](01-what-is-ros2.md) and the [docs index](README.md)
- [Lab robots](08-lab-robots.md)
- Lab: [about the lab](https://github.com/ATR-Lab/about)

<sub>Last reviewed: Nov. 5, 2026 · Sources checked on that date · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/docs/09-resources.md)</sub>
