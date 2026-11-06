# Install ROS 2 natively

> **Read this when** you are setting up ROS 2 directly on a computer (a lab workstation, a robot's onboard computer, a Raspberry Pi or a Jetson) rather than in a container.

The traditional install puts ROS 2 in `/opt/ros/<distro>` from the official apt repository. It is the right choice for robot computers and for any machine that talks to hardware, because nothing sits between ROS and the USB ports, GPU or network. This page gives the current official method (checked on Sept. 30, 2026) for each supported distribution, what to do about end-of-life ones, and the platform notes for the Raspberry Pi 5, NVIDIA Jetson, macOS and Windows. The one thing to remember: **the Ubuntu version must match the distribution** (see the table below); installing a distro on the wrong Ubuntu is the most common failed install.

## Contents

- [Before you start](#before-you-start)
- [Step 1: add the ROS 2 apt repository (all distros)](#step-1-add-the-ros-2-apt-repository-all-distros)
- [Step 2: install your distribution](#step-2-install-your-distribution)
- [End-of-life distributions: Iron, Galactic, Foxy](#end-of-life-distributions-iron-galactic-foxy)
- [Set up your shell](#set-up-your-shell)
- [Check the install](#check-the-install)
- [Raspberry Pi 5](#raspberry-pi-5)
- [NVIDIA Jetson](#nvidia-jetson)
- [macOS](#macos)
- [Windows](#windows)
- [Uninstall](#uninstall)
- [Related](#related)

## Before you start

- [ ] Decide the distribution ([which should I use?](02-distributions.md#which-distribution-should-i-use)).
- [ ] Install the matching 64-bit Ubuntu LTS:

  | Distribution | Ubuntu | Codename |
  |---|---|---|
  | Lyrical | 26.04 | `resolute` |
  | Kilted, Jazzy | 24.04 | `noble` |
  | Humble (and Iron, end of life) | 22.04 | `jammy` |
  | Galactic, Foxy (end of life) | 20.04 | `focal` |

- [ ] Have `sudo` rights and an internet connection. On a lab machine, ask the lab manager (Marcus Arnett, <marnett5@kent.edu>) before installing system packages.
- [ ] Check what you have: `lsb_release -a` prints your Ubuntu version.

> [!NOTE]
> Want several distros on one machine, or ROS 2 on a machine you do not want to change? Use [ROSEnv](04-install-rosenv.md) or plain Docker instead. You can have more than one distro installed natively, but never source two in the same shell.

## Step 1: add the ROS 2 apt repository (all distros)

These commands are the official method from the [Lyrical](https://docs.ros.org/en/lyrical/Get-Started/Installation/Ubuntu-Install-Debs.html), [Jazzy](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) and [Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html) install pages; they are the same for every distro. Since 2025 the docs install a small package, `ros2-apt-source`, that writes the repository entry and signing key for you and keeps them up to date. It replaces the older steps that downloaded `ros.key` by hand.

```bash
# Ubuntu 22.04, 24.04 or 26.04. Make sure the locale supports UTF-8.
locale                                   # look for UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Enable Ubuntu's Universe repository
sudo apt install software-properties-common
sudo add-apt-repository universe

# Install ros2-apt-source: it adds the ROS 2 repository and its key for your Ubuntu version
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb

# Development tools: colcon, rosdep, vcstool and friends
sudo apt update && sudo apt install ros-dev-tools
```

On Sept. 30, 2026 the latest `ros-apt-source` release was 1.3.0, with packages for Ubuntu 20.04, 22.04, 24.04 and 26.04 ([releases](https://github.com/ros-infrastructure/ros-apt-source/releases)).

> [!WARNING]
> **Ubuntu 24.04 only:** some installs list only the base `noble` suite, which breaks `ros-dev-tools` with dependency conflicts. Run `grep Suites /etc/apt/sources.list.d/ubuntu.sources`; if `noble-updates` or `noble-backports` is missing, change the line to `Suites: noble noble-updates noble-backports`, then run `sudo apt clean && sudo apt update && sudo apt full-upgrade -y` ([Jazzy install page](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)). Ubuntu images for the Raspberry Pi need the same fix.

## Step 2: install your distribution

Always update and upgrade first: ROS packages are built against an up-to-date Ubuntu.

```bash
sudo apt update
sudo apt upgrade
```

Then pick **one** variant: `desktop` (ROS, RViz, demos, tutorials; for computers with a screen) or `ros-base` (communication libraries, message packages and command-line tools, no GUI; for robots).

### Lyrical (Ubuntu 26.04)

```bash
sudo apt install ros-lyrical-desktop      # or: ros-lyrical-ros-base
```

### Jazzy (Ubuntu 24.04)

```bash
sudo apt install ros-jazzy-desktop        # or: ros-jazzy-ros-base
```

### Kilted (Ubuntu 24.04)

```bash
sudo apt install ros-kilted-desktop       # or: ros-kilted-ros-base
```

> [!CAUTION]
> Kilted reaches end of life in December 2026 (REP 2000 says November 2026). Install it only to keep existing Kilted work running; use Jazzy for anything new on Ubuntu 24.04.

### Humble (Ubuntu 22.04)

> [!WARNING]
> The Humble install page warns that, because of early updates in Ubuntu 22.04, the `systemd` and `udev` packages must be updated **before** you install ROS 2. Run `sudo apt upgrade` first and do not skip it ([Humble install page](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)).

```bash
sudo apt install ros-humble-desktop       # or: ros-humble-ros-base
```

Humble reaches end of life in May 2027. If you are starting fresh and nothing forces Humble, install Jazzy instead.

### Rolling

Rolling now targets Ubuntu 26.04 ([Rolling install page](https://docs.ros.org/en/rolling/Get-Started/Installation/Ubuntu-Install-Debs.html)). When we checked, its 26.04 packages were in the `ros2-testing` repository rather than the main one (the official `ros:rolling` Docker image installs `ros2-testing-apt-source`). Use Rolling only if you are developing ROS 2 itself.

### Initialize rosdep (once per machine)

`rosdep` installs the system dependencies your packages declare. Initialize it once after installing any distro:

```bash
sudo rosdep init
rosdep update
```

Do not run `rosdep update` with `sudo`; it prints a warning when run as root.

## End-of-life distributions: Iron, Galactic, Foxy

These distros get no fixes of any kind, and their Ubuntu versions are aging too: Ubuntu 20.04 (Foxy, Galactic) left standard support in May 2025 ([Ubuntu release cycle](https://ubuntu.com/about/release-cycle)). **Do not install them on a lab computer for new work.** When you must run old code, use these options, best first:

| Option | How | What we found on Sept. 30, 2026 |
|---|---|---|
| 1. Docker image (recommended) | `docker run -it --rm ros:iron` (or `ros:galactic`, `ros:foxy`) | Still on Docker Hub for amd64 and arm64, last rebuilt in June 2025 and no longer maintained; `osrf/ros:<distro>-desktop` images with GUI tools exist for amd64 only |
| 2. Frozen apt packages on the matching Ubuntu | Steps 1 and 2 above on Ubuntu 22.04 (Iron) or 20.04 (Foxy, Galactic) | The main ROS apt repository still holds the last builds (Foxy from June 2023, Galactic from December 2022, Iron from November 2024), and `ros2-apt-source` 1.3.0 still ships for `focal`. Nothing guarantees they stay |
| 3. Final snapshot | Point apt at `http://snapshots.ros.org/<distro>/final/ubuntu` as the [snapshot guide](https://docs.ros.org/en/lyrical/Get-Started/Installation/Snapshot-Repository.html) describes | `final` snapshots exist for Foxy, Galactic and Iron. The guide says snapshots are kept at least six months after end of life, so this may disappear |
| 4. Build from source | Follow the old distro's own docs, on its Ubuntu | Always possible but slow; you own every bug |

The old install pages are still online: [Foxy](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html), [Galactic](https://docs.ros.org/en/galactic/Installation/Ubuntu-Install-Debians.html), [Iron](https://docs.ros.org/en/iron/Installation/Ubuntu-Install-Debs.html). They show an older key-download method; Step 1 on this page also works for them.

A realistic Foxy example: Yahboom ships the ROSMASTER X3's ROS 2 software as a Foxy Docker image ([lab robots](08-lab-robots.md#yahboom-rosmaster-x3)). Keep that container for the vendor demos and write new code on a supported distro.

## Set up your shell

Every new terminal must **source** the setup file before `ros2` works. Add it to `~/.bashrc` so it happens automatically:

```bash
# Replace jazzy with your distro. Add only ONE distro to ~/.bashrc.
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
# Optional: pick a domain ID so you do not see other people's robots (0-101 is safe)
echo "export ROS_DOMAIN_ID=[your domain ID]" >> ~/.bashrc
source ~/.bashrc
```

If you use zsh, source `setup.zsh` instead; Lyrical adds `setup.fish` for fish. When you build your own workspace, source its overlay **after** the distro, in each terminal where you run your code: `source ~/hello_ws/install/setup.bash`.

> [!TIP]
> Mixing distros is the classic cause of strange errors. `printenv ROS_DISTRO` shows which one this shell is using, and `printenv | grep -i ros` shows everything ROS has set.

## Check the install

Run the official talker and listener. They need the `desktop` variant, or install them on `ros-base` with `sudo apt install ros-<distro>-demo-nodes-cpp ros-<distro>-demo-nodes-py`.

```bash
# Terminal 1
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

```bash
# Terminal 2
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

You should see `Publishing: 'Hello World: 1'` in the first terminal and `I heard: [Hello World: 1]` in the second. That proves C++ and Python nodes can talk. Then:

```bash
ros2 doctor               # checks the platform, network and middleware; ends with "All <N> checks passed"
ros2 doctor --report      # full report to paste into a help request
```

If the listener hears nothing, go to [debugging: nodes can't see each other](07-debugging.md#nodes-cant-see-each-other).

We ran Steps 1 and 2 (with `ros-base` plus the demo nodes), the talker and listener, `rosdep init` and `rosdep update` in clean `ubuntu:26.04` (Lyrical), `ubuntu:24.04` (Jazzy and Kilted) and `ubuntu:22.04` (Humble) containers on Sept. 30, 2026; see [AGENTS.md](../AGENTS.md#how-to-check-your-work).

## Raspberry Pi 5

The ROS docs give two routes ([ROS 2 on Raspberry Pi](https://docs.ros.org/en/lyrical/Get-Started/Installation/Installing-on-Raspberry-Pi.html)): 64-bit Ubuntu with the normal binary install (arm64 is Tier 1), or Raspberry Pi OS 64-bit with ROS 2 in Docker (Raspberry Pi OS is Debian-based, which is Tier 3).

| Pi 5 operating system | ROS 2 route |
|---|---|
| Ubuntu 24.04 LTS (64-bit) | **Jazzy via apt** (recommended). Ubuntu 24.04 is the first LTS with Raspberry Pi 5 images ([Ubuntu 24.04 release notes](https://documentation.ubuntu.com/release-notes/24.04/)) |
| Ubuntu 26.04 LTS (64-bit) | Lyrical via apt |
| Raspberry Pi OS (64-bit) | Any supported distro in Docker, for example `docker run -it --rm ros:jazzy-ros-core` |
| Ubuntu 22.04 | Not listed for the Pi 5 in [Ubuntu's Raspberry Pi support matrix](https://ubuntu.com/hardware/docs/boards/how-to/ubuntu_supported/raspberry-pi/); run Humble in Docker instead |

Before Step 1 on Ubuntu for the Pi, make sure `/etc/apt/sources.list.d/ubuntu.sources` lists the updates and backports suites (`Suites: noble noble-updates noble-backports` on 24.04); the ROS docs call this out because Ubuntu's Pi images leave them out. Use `ros-<distro>-ros-base` on the Pi and run RViz on your laptop. The lab's hardware page: [Raspberry Pi 5](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/raspberry-pi-5.md).

## NVIDIA Jetson

A Jetson's JetPack version fixes its Ubuntu version, and that fixes which ROS 2 distro installs natively:

| JetPack | Ubuntu base | Modules (from NVIDIA's [JetPack archive](https://developer.nvidia.com/embedded/jetpack-archive)) | Native ROS 2 (Tier 1) |
|---|---|---|---|
| 7.x | 24.04 ([JetPack](https://developer.nvidia.com/embedded/jetpack)) | AGX Thor, T5000, T4000; Orin family from 7.2 | **Jazzy** (Kilted until it ends) |
| 6.x | 22.04 ([JetPack 6.2](https://developer.nvidia.com/embedded/jetpack-sdk-62)) | AGX Orin, Orin NX, Orin Nano | **Humble** |
| 5.1.x | 20.04 ([JetPack 5.1.4](https://developer.nvidia.com/embedded/jetpack-sdk-514)) | Orin and Xavier | Only end-of-life Foxy or Galactic; use a container or a source build for anything newer |
| 4.6.x | 18.04 ([Jetson Linux 32.7.6](https://developer.nvidia.com/embedded/linux-tegra-r3276)) | Original Jetson Nano, TX1, TX2, Xavier | None natively; use a container or a source build |

Install on a Jetson exactly as on Ubuntu (arm64), with `ros-base`. NVIDIA's own accelerated packages, **Isaac ROS**, follow their own schedule: Isaac ROS 4.x targets Jazzy and added Jetson AGX Thor support, and Isaac ROS 5.0 (Sept. 21, 2026) moved to Lyrical on Ubuntu 24.04 through NVIDIA's own apt buildfarm ([Isaac ROS release notes](https://nvidia-isaac-ros.github.io/releases/index.html)). Since Lyrical is only Tier 3 on Ubuntu 24.04 upstream, stay on Jazzy unless you specifically need Isaac ROS 5.0. Lab page: [Jetson AGX Thor](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/hardware/jetson-agx-thor.md).

## macOS

macOS is **Tier 3** for every current distro: the ROS 2 project provides no binaries, only [build-from-source instructions](https://docs.ros.org/en/lyrical/Get-Started/Installation/Alternatives/macOS-Development-Setup.html). Your realistic options, best first:

1. **Work on a lab Ubuntu machine over SSH** (`[lab remote-access instructions]`), or in an Ubuntu virtual machine.
2. **Docker Desktop** with the official images for learning, building and tests. Docker Desktop runs containers in a Linux VM; its optional host networking works at layer 4 and containers cannot bind to the Mac's own interfaces ([Docker docs](https://docs.docker.com/engine/network/drivers/host/)), so do not count on a container discovering a robot on the Wi-Fi. [ROSEnv](04-install-rosenv.md) does not support macOS as a runtime.
3. **RoboStack**, a community project that packages ROS for conda-forge and pixi, lists Humble, Jazzy, Kilted and Lyrical environments for Apple silicon and Intel Macs ([RoboStack getting started](https://robostack.github.io/GettingStarted.html)). It is not an official ROS 2 platform, so expect gaps. The lab's Coffee Buddy repository ([kami-head](https://github.com/ATR-Lab/kami-head)) uses it for macOS development.

## Windows

Windows is Tier 1, but only as a **binary archive** and only for the core packages: Lyrical supports Windows 11, Humble through Kilted Windows 10 ([Lyrical Windows install](https://docs.ros.org/en/lyrical/Get-Started/Installation/Windows-Install-Binary.html)). Most drivers and community packages you will want are not built for Windows. For lab work:

1. **WSL2 with Ubuntu** (Ubuntu 24.04 for Jazzy), then follow this page as if on Ubuntu. On Windows 11 22H2 or later, set `networkingMode=mirrored` in `.wslconfig` for multicast support and LAN access, and allow inbound connections in the Hyper-V firewall ([WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking)). Linux GUI apps such as RViz run through WSLg on Windows 11 or Windows 10 build 19044 and later ([WSL GUI apps](https://learn.microsoft.com/en-us/windows/wsl/tutorials/gui-apps)).
2. Docker Desktop, with the same networking limits as on macOS.
3. The native binary archive, only if your project needs Windows itself.

## Uninstall

From the official install pages:

```bash
# Replace jazzy with your distro
sudo apt remove '~nros-jazzy-*' && sudo apt autoremove
# Optional: remove the repository too
sudo apt remove ros2-apt-source
sudo apt update
sudo apt autoremove
sudo apt upgrade        # picks up packages the ROS repository had shadowed
```

Also delete the `source /opt/ros/<distro>/setup.bash` line from `~/.bashrc`. Your workspaces are untouched; delete their `build/`, `install/` and `log/` folders before rebuilding against another distro.

## Related

- [Distributions and which to choose](02-distributions.md)
- [Install with ROSEnv](04-install-rosenv.md): several distros side by side, no system changes
- [Command cheatsheet](05-cheatsheet.md)
- [Debugging](07-debugging.md)
- Lab: [Docker in the lab tech stack](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/tech-stack/docker.md) and [the full tech stack](https://github.com/ATR-Lab/getting-started-atr-lab/blob/master/tech-stack/README.md)
- Official: [installation troubleshooting](https://docs.ros.org/en/lyrical/Get-Started/Installation/Installation-Troubleshooting.html)

<sub>Last reviewed: Nov. 5, 2026 · Sources checked on that date · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/docs/03-install-native.md)</sub>
