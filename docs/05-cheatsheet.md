# ROS 2 command cheatsheet

> **Read this when** you know what you want to do and need the exact command, or you are an agent that must produce a command that works on a specific distribution.

One page of the commands you use every day: the `ros2` tool, `colcon`, `rosdep`, package creation and the environment variables that control discovery and logging. Every command was checked against the `--help` output of the official Docker images `ros:humble`, `ros:jazzy`, `ros:kilted` and `ros:lyrical` on Sept. 30, 2026, and the ones marked **ran** were executed against a live node in `ros:jazzy`. The one thing to remember: **most commands are the same on every distro, and the differences are listed in [distro differences](#distro-differences).**

In the tables, `<pkg>`, `<node>`, `<topic>` and `<type>` stand for your names. Add `-h` to any command for its full help.

## Contents

- [Run and launch](#run-and-launch)
- [Nodes](#nodes)
- [Topics](#topics)
- [Services](#services)
- [Actions](#actions)
- [Parameters](#parameters)
- [Interfaces and packages](#interfaces-and-packages)
- [Bags (record and replay)](#bags-record-and-replay)
- [Doctor, daemon, components and lifecycle](#doctor-daemon-components-and-lifecycle)
- [colcon](#colcon)
- [rosdep](#rosdep)
- [Create a package](#create-a-package)
- [Environment variables](#environment-variables)
- [Distro differences](#distro-differences)
- [Related](#related)

## Run and launch

| Command | What it does | Checked |
|---|---|---|
| `ros2 run <pkg> <executable>` | Start one node | ran |
| `ros2 run <pkg> <exe> --ros-args -p name:=value` | Start it with a parameter | ran |
| `ros2 run <pkg> <exe> --ros-args -r __node:=new_name -r chatter:=/other` | Rename the node, remap a topic | help |
| `ros2 run <pkg> <exe> --ros-args --params-file params.yaml` | Load parameters from YAML | help |
| `ros2 run <pkg> <exe> --ros-args --log-level debug` | More log output (`debug`, `info`, `warn`, `error`, `fatal`) | ran |
| `ros2 run --prefix 'gdb -ex run --args' <pkg> <exe>` | Run under a debugger ([debugging](07-debugging.md#crashes-and-hangs)) | help |
| `ros2 pkg executables <pkg>` | List what you can `ros2 run` | ran |
| `ros2 launch <pkg> <file.launch.py>` | Start a launch file | ran |
| `ros2 launch <pkg> <file> name:=value` | Pass a launch argument | ran |
| `ros2 launch -s <pkg> <file>` | Show the arguments a launch file accepts | help |
| `ros2 launch --launch-prefix 'xterm -e gdb -ex run --args' <pkg> <file>` | Put a prefix in front of every node | help |

## Nodes

| Command | What it does | Checked |
|---|---|---|
| `ros2 node list` | Every node visible on this domain | ran |
| `ros2 node info /<node>` | Its publishers, subscribers, services and actions | ran |

## Topics

| Command | What it does | Checked |
|---|---|---|
| `ros2 topic list -t` | Topic names with types | ran |
| `ros2 topic echo /<topic>` | Print messages as they arrive | ran |
| `ros2 topic echo /<topic> --once` | Print one message and exit | ran |
| `ros2 topic echo /odom --field pose.pose.position` | Print one field | help |
| `ros2 topic echo --qos-reliability best_effort /<topic>` | Subscribe with a chosen QoS (see [QoS mismatch](07-debugging.md#qos-mismatch-subscriber-receives-nothing)) | ran (`reliable`) |
| `ros2 topic info -v /<topic>` | Publishers, subscribers and their QoS | ran |
| `ros2 topic hz /<topic>` | Measured publish rate | ran |
| `ros2 topic bw /<topic>` | Measured bandwidth | ran |
| `ros2 topic delay /<topic>` | Age of messages, from the header stamp | help |
| `ros2 topic type /<topic>` | Its message type | help |
| `ros2 topic find <type>` | Topics that carry a type | help |
| `ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1}}"` | Publish at 10 Hz until Ctrl-C | help |
| `ros2 topic pub --once -w 0 /chatter std_msgs/msg/String "{data: 'hi'}"` | Publish one message now (`--once` alone waits for a subscriber) | ran |

> [!CAUTION]
> `ros2 topic pub` on `/cmd_vel` moves a real robot. Put it on blocks or in an open space, keep the speed low, and keep the robot's emergency stop in reach before you press Enter.

## Services

| Command | What it does | Checked |
|---|---|---|
| `ros2 service list -t` | Service names with types | ran |
| `ros2 service type /<service>` | Its type | help |
| `ros2 service find <type>` | Services of a type | help |
| `ros2 service call /<service> <type> "{field: value}"` | Call once and print the response | ran |
| `ros2 service info /<service>` | Servers and clients (Jazzy and newer) | help |
| `ros2 service echo /<service>` | Watch requests and responses (Jazzy and newer; only for nodes with service introspection on, which is off by default) | help |

Example that works against any running node, since every node has parameter services:

```bash
ros2 service call /talker/get_parameters rcl_interfaces/srv/GetParameters "{names: ['greeting']}"
```

## Actions

| Command | What it does | Checked |
|---|---|---|
| `ros2 action list -t` | Action names with types | help |
| `ros2 action info /<action>` | Servers and clients | help |
| `ros2 action send_goal /<action> <type> "{...}"` | Send a goal and wait for the result | help |
| `ros2 action send_goal /<action> <type> "{...}" --feedback` | Also print feedback | help |
| `ros2 action type /<action>` | Its type (Jazzy and newer) | help |
| `ros2 action echo /<action>`, `ros2 action find <type>` | Watch an action, find actions by type (Kilted and newer) | help |

## Parameters

| Command | What it does | Checked |
|---|---|---|
| `ros2 param list /<node>` | Parameter names | ran |
| `ros2 param get /<node> <name>` | Current value | ran |
| `ros2 param set /<node> <name> <value>` | Change it now (if the node allows) | ran |
| `ros2 param describe /<node> <name>` | Type, description, limits | help |
| `ros2 param dump /<node> > params.yaml` | Save all values as YAML | ran |
| `ros2 param load /<node> params.yaml` | Apply a saved file to a running node | help |
| `ros2 param delete /<node> <name>` | Undeclare it | help |

`use_sim_time` is a parameter on every node: `ros2 param get /<node> use_sim_time` tells you whether it follows `/clock` ([time problems](07-debugging.md#time-and-use_sim_time)).

## Interfaces and packages

| Command | What it does | Checked |
|---|---|---|
| `ros2 interface show geometry_msgs/msg/Twist` | Field definitions | ran |
| `ros2 interface proto geometry_msgs/msg/Twist` | A YAML template to paste into `pub` or `call` | ran |
| `ros2 interface list`, `ros2 interface package <pkg>` | All types, or one package's types | help |
| `ros2 pkg list` | Every package this shell can see | help |
| `ros2 pkg prefix <pkg>` | Where it is installed (underlay or overlay?) | help |
| `ros2 pkg xml <pkg>` | Its `package.xml` | help |

## Bags (record and replay)

A **bag** is a recording of topics that you can replay later, the best way to share a bug ([debugging](07-debugging.md#record-a-bag-to-reproduce-a-problem)).

| Command | What it does | Checked |
|---|---|---|
| `ros2 bag record -a` | Record all topics (all distros) | help |
| `ros2 bag record --topics /scan /odom /tf /tf_static` | Record chosen topics (Jazzy and newer) | ran |
| `ros2 bag record /scan /odom` | Record chosen topics (Humble; deprecated in Jazzy and Kilted, removed in Lyrical) | help |
| `ros2 bag record -o my_bag -a` | Choose the output folder name | ran |
| `ros2 bag record -s mcap -a` | Choose the storage format (`mcap` or `sqlite3`) | help |
| `ros2 bag info my_bag` | Duration, topics and message counts | ran |
| `ros2 bag play my_bag` | Replay | help |
| `ros2 bag play my_bag -r 0.5 -l --clock` | Half speed, loop, publish `/clock` for sim time | help |
| `ros2 bag convert -i in_bag -o out.yaml` | Rewrite with other settings (the YAML names the output format) | help |

## Doctor, daemon, components and lifecycle

| Command | What it does | Checked |
|---|---|---|
| `ros2 doctor` | Checks platform, network, middleware, topics | ran |
| `ros2 doctor --report` | Full report to paste into a help request | ran |
| `ros2 doctor hello` | Tests whether this host can reach others (run it on two machines) | help |
| `ros2 daemon status`, `ros2 daemon stop` | The background discovery cache; stop it when `ros2` lists look stale | ran (`status`) |
| `ros2 component types` | Composable nodes installed | help |
| `ros2 component list` | Running containers and the components in them | help |
| `ros2 component load /ComponentManager <pkg> <plugin>` | Load a component into a running container | help |
| `ros2 component standalone <pkg> <plugin>` | Run one component in its own container | help |
| `ros2 lifecycle nodes` | Nodes with a managed lifecycle | help |
| `ros2 lifecycle get /<node>` | Current state | help |
| `ros2 lifecycle set /<node> configure` | Trigger a transition (`configure`, `activate`, `deactivate`, `cleanup`, `shutdown`) | help |
| `ros2 lifecycle list /<node>` | Transitions available now | help |

## colcon

Run `colcon` from the **workspace root** (the folder that holds `src/`), after sourcing the distro. Official reference: [colcon tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html).

| Command | What it does | Checked |
|---|---|---|
| `colcon build` | Build every package in `src/` | ran |
| `colcon build --symlink-install` | Link Python files and launch/config files instead of copying, so edits apply without rebuilding | ran |
| `colcon build --packages-select <pkg>` | Build only this package | help |
| `colcon build --packages-up-to <pkg>` | Build it and everything it depends on | help |
| `colcon build --packages-skip <pkg>` | Build all except this | help |
| `colcon build --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo` | Pass CMake options (optimized, with debug symbols) | help |
| `colcon build --parallel-workers 2` | Limit parallel jobs (for a Raspberry Pi or low-memory machine) | help |
| `colcon build --executor sequential` | One package at a time | help |
| `colcon build --event-handlers console_direct+` | Show compiler output live | ran |
| `colcon build --continue-on-error` | Keep building other packages after a failure | help |
| `colcon test` | Run all tests | ran |
| `colcon test --packages-select <pkg> --pytest-args -k name` | One package, filtered pytest | help |
| `colcon test --return-code-on-test-failure` | Exit non-zero on failures (for CI) | help |
| `colcon test-result --verbose` | Show failures from the last `colcon test` | ran |
| `colcon test-result --all` | List every result file | help |

After a successful build, run `source install/setup.bash` in every terminal that uses the workspace. After adding a **new** package or executable, rebuild and source again.

## rosdep

`rosdep` installs the system packages listed in your `package.xml` files. Official reference: [managing dependencies with rosdep](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Rosdep.html).

| Command | What it does | Checked |
|---|---|---|
| `sudo rosdep init` | Once per machine | ran |
| `rosdep update` | Refresh the database (no `sudo`) | ran |
| `rosdep install --from-paths src --ignore-src -y` | Install everything the workspace needs | ran |
| `rosdep install --from-paths src --ignore-src -y --rosdistro jazzy` | The same, naming the distro explicitly (useful in scripts and containers) | ran |
| `rosdep check --from-paths src --ignore-src` | Report what is missing without installing | help |
| `rosdep resolve <key>` | Show the system package a key maps to (`rclpy` becomes `ros-jazzy-rclpy`) | ran |
| `rosdep keys --from-paths src --ignore-src` | List the keys your packages use | help |

## Create a package

Run these inside `src/` of your workspace. `ros2 pkg create` supports `ament_cmake`, `ament_python`, `cmake` and `ament_cargo` build types.

```bash
# Python package with a starter node (Jazzy; also works on Humble, Kilted and Lyrical)
ros2 pkg create --build-type ament_python --license MIT --dependencies rclpy std_msgs --node-name talker my_py_pkg

# C++ package with a starter node
ros2 pkg create --build-type ament_cmake --license MIT --dependencies rclcpp std_msgs --node-name talker my_cpp_pkg
```

Both commands ran in `ros:jazzy`. The Python template includes `test_copyright.py`, `test_flake8.py` and `test_pep257.py`; the C++ template includes `CMakeLists.txt` with `ament_lint_auto` for tests. Then build with `colcon build --packages-select my_py_pkg`. A complete, tested Python package is in [examples/hello_ws](../examples/hello_ws/). Official tutorial: [creating a package](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html). Lab naming and layout rules: [dev-guidelines: ROS 2 packages](https://github.com/ATR-Lab/dev-guidelines/blob/master/docs/ros2-packages.md).

## Environment variables

Set these in the shell before starting nodes (or in `~/.bashrc`). Every node that must talk to another needs the same `ROS_DOMAIN_ID` and compatible discovery settings.

| Variable | Values | Distros | What it does |
|---|---|---|---|
| `ROS_DISTRO` | set by `setup.bash` | All | Which distro this shell sourced. Read it; do not set it |
| `ROS_DOMAIN_ID` | `0` (default) to `101` is safe on Linux | All | Separates ROS networks ([About domain ID](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Domain-ID.html)) |
| `ROS_AUTOMATIC_DISCOVERY_RANGE` | `SUBNET` (default), `LOCALHOST`, `OFF`, `SYSTEM_DEFAULT` | Iron and newer | How far discovery reaches ([improved dynamic discovery](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html)) |
| `ROS_STATIC_PEERS` | `192.168.1.10;robot.local` | Iron and newer | Extra hosts to discover even outside the range |
| `ROS_LOCALHOST_ONLY` | `1` or `0` | Humble (and older); deprecated in Iron and Jazzy; **removed in Kilted** | Keep traffic on this machine. On Jazzy use `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` instead |
| `RMW_IMPLEMENTATION` | `rmw_fastrtps_cpp`, `rmw_cyclonedds_cpp`, `rmw_zenoh_cpp`, `rmw_connextdds` | All (`ros-<distro>-rmw-zenoh-cpp` is packaged for Humble through Lyrical; Tier 1 from Kilted) | Pick the middleware; install its package first (`ros-<distro>-rmw-cyclonedds-cpp`) |
| `RCUTILS_CONSOLE_OUTPUT_FORMAT` | `"[{severity}] [{name}]: {message}"` | All | Log line format; other fields include `{time}` and `{function_name}` |
| `RCUTILS_COLORIZED_OUTPUT` | `1` or `0` | All | Force colors on or off |
| `RCUTILS_LOGGING_USE_STDOUT` | `1` or `0` (default: stderr) | All | Send log output to stdout |
| `RCUTILS_LOGGING_BUFFERED_STREAM` | `1` or `0` | All | Line-buffer the log stream (set `1` if logs appear late) |
| `ROS_LOG_DIR`, `ROS_HOME` | a path | All | Where log files go (default `~/.ros/log`) |

Sources: the [logging concept page](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Logging.html), the [Iron release notes](https://docs.ros.org/en/lyrical/Releases/Release-Iron-Irwini.html) for the discovery variables and the `rcl` [changelog](https://github.com/ros2/rcl/blob/kilted/rcl/CHANGELOG.rst) for the removal ("Removed deprecated localhost_only"). We also read the strings compiled into `librcl` in each image: Humble's knows only `ROS_LOCALHOST_ONLY`, Jazzy's prints `ROS_LOCALHOST_ONLY is deprecated but still honored if it is enabled`, and Kilted's and Lyrical's no longer contain it. The official images set `ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET` (Jazzy, Kilted, Lyrical) and `ROS_LOCALHOST_ONLY=0` (Humble).

```bash
# Keep ROS traffic on this computer (Jazzy, Kilted, Lyrical)
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
# The same on Humble
export ROS_LOCALHOST_ONLY=1
# Talk only to your robot's domain
export ROS_DOMAIN_ID=[robot domain ID]
```

## Distro differences

The commands above work on Humble, Jazzy, Kilted and Lyrical except where this table says otherwise. Verified from each image's `--help` output.

| Feature | Humble | Jazzy | Kilted | Lyrical |
|---|---|---|---|---|
| Default bag format | SQLite 3 (`.db3`); MCAP needs `ros-humble-rosbag2-storage-mcap` | MCAP | MCAP | MCAP |
| `ros2 bag record /a /b` (positional topics) | Yes | Deprecated | Deprecated | Removed |
| `ros2 bag record --topics /a /b` | No | Yes | Yes | Yes |
| Exclude topics by regex when recording | `-x REGEX` | `--exclude-regex` | `--exclude-regex` | `--exclude-regex` |
| `ros2 bag burst` | No | Yes | Yes | Yes |
| `ros2 service info`, `ros2 service echo` | No | Yes | Yes | Yes (`info --verbose` too) |
| `ros2 action type` | No | Yes | Yes | Yes |
| `ros2 action echo`, `ros2 action find` | No | No | Yes | Yes |
| `--stdin` for `topic pub`, `service call`, `action send_goal` | No | Yes | Yes | Yes |
| `ros2 topic hz` on several topics, `--all` | No | No | Yes | Yes |
| `ros2 topic bw` on several topics, `--all` | No | No | No | Yes |
| `ros2 param get <param>` across all nodes; get or set several on one node | No | No | No | Yes |
| Discovery variables | `ROS_LOCALHOST_ONLY` | Both (`ROS_LOCALHOST_ONLY` deprecated) | `ROS_AUTOMATIC_DISCOVERY_RANGE` only | `ROS_AUTOMATIC_DISCOVERY_RANGE` only |
| `static_transform_publisher x y z yaw pitch roll parent child` (old positional form) | Deprecated, warns | Deprecated, warns | Deprecated, warns | Removed; use `--x ... --frame-id ... --child-frame-id` |
| Python version | 3.10 | 3.12 | 3.12 | 3.14 (Ubuntu 26.04) |

> [!TIP]
> Writing a script that must run on several distros? Stick to `ros2 bag record -a`, the flag form of `static_transform_publisher` and `ROS_DOMAIN_ID`, which behave the same everywhere, and branch on `$ROS_DISTRO` for the rest.

## Related

- [What is ROS 2](01-what-is-ros2.md): what nodes, topics, services and actions are
- [Useful packages and nodes](06-packages-and-nodes.md)
- [Debugging](07-debugging.md): symptoms and fixes
- [Example workspace](../examples/hello_ws/): the node these commands were run against
- Official: [ROS 2 CLI tutorials](https://docs.ros.org/en/jazzy/Tutorials.html), [using ros2 param](https://docs.ros.org/en/jazzy/How-To-Guides/Using-ros2-param.html)

<sub>Last reviewed: Sept. 30, 2026 · Sources checked on that date · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/docs/05-cheatsheet.md)</sub>
