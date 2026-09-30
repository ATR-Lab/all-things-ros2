# Examples

> **Read this when** you want a small, working ROS 2 workspace to build, run, test and copy from.

The examples here are small on purpose: each one shows a few ideas you can read in one sitting and reuse in your own packages. Every example is built and tested in the official Docker images before it is merged. The one thing to remember: **copy the pattern, not the names**; rename the package before you build on it.

## hello_ws

A workspace with one Python package, `hello_atr`, that shows the pieces every ROS 2 project uses:

| File | What it shows |
|---|---|
| [`src/hello_atr/hello_atr/talker.py`](hello_ws/src/hello_atr/hello_atr/talker.py) | A publisher on `chatter` with two parameters, `greeting` and `publish_rate_hz`, read on every timer tick so `ros2 param set` takes effect live |
| [`src/hello_atr/hello_atr/listener.py`](hello_ws/src/hello_atr/hello_atr/listener.py) | A subscriber that logs what it hears |
| [`src/hello_atr/launch/hello_atr.launch.py`](hello_ws/src/hello_atr/launch/hello_atr.launch.py) | A launch file that starts both, loads a YAML parameter file and takes a `greeting` launch argument |
| [`src/hello_atr/config/talker.yaml`](hello_ws/src/hello_atr/config/talker.yaml) | A parameter file (`talker: ros__parameters: ...`) |
| [`src/hello_atr/test/test_hello_atr.py`](hello_ws/src/hello_atr/test/test_hello_atr.py) | Three pytest tests: a plain unit test, a parameter check and a talker-to-listener integration test in one process |
| [`src/hello_atr/package.xml`](hello_ws/src/hello_atr/package.xml), [`setup.py`](hello_ws/src/hello_atr/setup.py), [`setup.cfg`](hello_ws/src/hello_atr/setup.cfg) | An `ament_python` package: dependencies, entry points and installed data files |
| [`rosenv.toml`](hello_ws/rosenv.toml) | A [ROSEnv](../docs/04-install-rosenv.md) manifest for the same workspace |

Tested on Sept. 30, 2026 in `ros:humble`, `ros:jazzy`, `ros:kilted` and `ros:lyrical` (linux/arm64): the build succeeds with no warnings, `colcon test` reports three tests and no failures, and the launch file shows the listener hearing the talker.

### Run it natively

On a machine with ROS 2 installed ([install guide](../docs/03-install-native.md)). Replace `jazzy` with your distro.

```bash
cd all-things-ros2/examples/hello_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -y   # installs python3-pytest if missing
colcon build --symlink-install
colcon test --packages-select hello_atr
colcon test-result --verbose                       # expect: 3 tests, 0 errors, 0 failures
source install/setup.bash
ros2 launch hello_atr hello_atr.launch.py greeting:='Hi from the lab'
```

Press Ctrl-C to stop. A Python node may print a `KeyboardInterrupt` traceback during shutdown; that is harmless ([why](../docs/07-debugging.md#crashes-and-hangs)).

Then explore the running graph from a second terminal (source the distro and `install/setup.bash` there too):

```bash
ros2 node list                                  # /listener and /talker
ros2 topic echo /chatter --once
ros2 param set /talker greeting "Changed at runtime"
ros2 param dump /talker
ros2 run hello_atr talker --ros-args -p publish_rate_hz:=5.0 -r __node:=fast_talker
```

### Run it in Docker

Any computer with Docker (the official images are amd64 and arm64):

```bash
cd all-things-ros2/examples/hello_ws
docker run -it --rm -v "$PWD:/hello_ws" -w /hello_ws ros:jazzy bash
# then, inside the container:
apt-get update && rosdep update && rosdep install --from-paths src --ignore-src -y
colcon build --symlink-install && colcon test && colcon test-result --verbose
source install/setup.bash
ros2 launch hello_atr hello_atr.launch.py
```

The build writes `build/`, `install/` and `log/` into the folder you mounted; the repository's `.gitignore` keeps them out of Git.

### Run it with ROSEnv

On a Linux host with [ROSEnv](../docs/04-install-rosenv.md) installed:

```bash
cd all-things-ros2/examples/hello_ws
rosenv lock        # writes rosenv.lock for your machine's architecture
rosenv build
rosenv test
rosenv task demo   # the launch file; Ctrl-C to stop
```

We do not commit a `rosenv.lock` here, because a lock is tied to one CPU architecture.

### Exactly what we ran

The verification commands, run from a scratch copy of `hello_ws` so no build output lands in the repository:

```bash
# For each of humble, jazzy, kilted and lyrical (here: jazzy)
docker run --rm -v "$PWD/hello_ws:/hello_ws" -w /hello_ws ros:jazzy bash -c '
  source /opt/ros/jazzy/setup.bash
  apt-get update -qq
  rosdep update --rosdistro jazzy
  rosdep install --from-paths src --ignore-src -y --rosdistro jazzy
  colcon build --symlink-install
  colcon test --packages-select hello_atr --event-handlers console_direct+
  colcon test-result --verbose
  source install/setup.bash
  ros2 pkg executables hello_atr
  timeout -s INT 6 ros2 launch hello_atr hello_atr.launch.py greeting:="Hi from the lab"
'
```

ROSEnv 0.2.0 ran `rosenv lock`, `rosenv sync --locked`, `rosenv build`, `rosenv test` and the launch file against the same workspace; see [AGENTS.md](../AGENTS.md#how-to-check-your-work) for how.

## Related

- [What is ROS 2](../docs/01-what-is-ros2.md): the concepts this example uses
- [Command cheatsheet](../docs/05-cheatsheet.md)
- Official tutorials this example follows: [writing a simple publisher and subscriber (Python)](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html), [creating launch files](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Creating-Launch-Files.html)
- Lab conventions: [dev-guidelines: ROS 2 packages](https://github.com/ATR-Lab/dev-guidelines/blob/master/docs/ros2-packages.md)

<sub>Last reviewed: Sept. 30, 2026 · [Suggest a change](https://github.com/ATR-Lab/all-things-ros2/edit/main/examples/README.md)</sub>
