# AGENTS.md: all-things-ros2

This repository is the ROS 2 handbook of the Advanced Telerobotics Research Laboratory (Department of Computer Science, Kent State University): what ROS 2 is, its distributions from Foxy to Lyrical, how to install it natively or with ROSEnv, a command cheatsheet, useful packages, debugging practice, how each lab device connects to ROS 2, and a small tested example workspace. It serves two readers: a new student who has never used ROS, and a coding agent that needs exact, verified commands. It is **not** the lab's onboarding guide (that is `getting-started-atr-lab`), not its coding standard (`dev-guidelines`), not a place for robot code (each robot has its own repository), and not a substitute for the official ROS 2 documentation, which it links everywhere.

## Repo map

| Path | What it is |
|---|---|
| `README.md` | Landing page: header, card grid, distro quick answer, five-minute quick start (native and ROSEnv), repo map, contributing, license, shared footer |
| `AGENTS.md` | This file: map, sources, rules, checks, open items |
| `CLAUDE.md` | One line, `@AGENTS.md`, so Claude Code loads this file |
| `LICENSE` | MIT, 2026, Advanced Telerobotics Research Laboratory contributors |
| `.gitignore` | Colcon outputs (`build/`, `install/`, `log/`), Python caches, ROSEnv local files, bags, editor and OS files |
| `.markdownlint.jsonc` | Shared markdownlint rules for all lab docs repos |
| `.github/workflows/docs.yml` | CI: markdownlint and lychee link check on every push and pull request |
| `.github/assets/header.png`, `social-preview.png` | Banner and social preview (do not regenerate) |
| `.github/assets/icons/` | The nine card icons used in `README.md` (copied from the shared lab icon set) |
| `docs/README.md` | Index of the handbook pages |
| `docs/01-what-is-ros2.md` | Concepts: graph, nodes, topics, services, actions, parameters, launch, interfaces, RMW and DDS, QoS, discovery, tf2, workspaces, colcon, ament, rosdep; glossary |
| `docs/02-distributions.md` | Foxy to Lyrical plus Rolling: dates, end of life, LTS, Tier 1 platforms, status on Sept. 30, 2026; decision guide; migration checklist and known changes |
| `docs/03-install-native.md` | Official apt install (ros2-apt-source) per distro; end-of-life options; shell setup; checks; Raspberry Pi 5; Jetson; macOS; Windows; uninstall |
| `docs/04-install-rosenv.md` | ROSEnv 0.2.0: when to use it, requirements, install, `rosenv.toml` and `rosenv.lock`, commands, several distros, named environments, networking, limitations |
| `docs/05-cheatsheet.md` | `ros2` CLI, colcon, rosdep, package creation, environment variables, per-distro differences table |
| `docs/06-packages-and-nodes.md` | Packages by task with apt names, example commands, docs links and a per-distro binary availability table |
| `docs/07-debugging.md` | Symptom, cause and fix tables; decision flow; tf, time, build, performance, crash and bag guidance; `ros2 doctor` |
| `docs/08-lab-robots.md` | Unitree Go2 Pro, Booster K1, OpenManipulator-X, LeRobot SO-101, Jetson AGX Thor, Raspberry Pi 5, Yahboom ROSMASTER X3: ROS 2 route, distro, lab repos, hardware page links |
| `docs/09-resources.md` | Official docs, REPs, package search, where to ask, stack docs, books and courses, public lab repos |
| `examples/README.md` | How to build, test and run the example natively, in Docker and with ROSEnv; the exact verification commands |
| `examples/hello_ws/rosenv.toml` | ROSEnv manifest for the example (Jazzy, `ros-base`, tasks `talker`, `listener`, `demo`) |
| `examples/hello_ws/src/hello_atr/` | `ament_python` package: `hello_atr/talker.py`, `hello_atr/listener.py`, `launch/hello_atr.launch.py`, `config/talker.yaml`, `test/test_hello_atr.py`, `package.xml`, `setup.py`, `setup.cfg`, `resource/hello_atr` |

## Sources of truth

- **Lab facts** (names, people, rooms, contacts, projects, platforms) come only from the ATR Lab design skill's `references/brand-foundation.md` or from the lab lead. Never print anything on its "never print" list.
- **ROS 2 facts** come from primary sources checked on the date shown in each page footer:
  - Release and end-of-life dates: [docs.ros.org distributions page](https://docs.ros.org/en/lyrical/Releases.html) (source: `ros2/ros2_documentation`, `source/Releases.rst`).
  - Platforms and tiers: [REP 2000](https://reps.openrobotics.org/rep-2000/) for Foxy to Kilted; the [Lyrical supported platforms page](https://docs.ros.org/en/lyrical/Releases/lyrical/supported-platforms.html) for Lyrical (REP 2000 had no Lyrical section on Sept. 30, 2026). REP 2000 says Kilted ends November 2026; docs.ros.org says December 2026; the pages state both.
  - Install commands: each distro's Ubuntu install page on docs.ros.org (Lyrical's lives under `Get-Started/Installation/`).
  - Package availability: `packages.ros.org/ros2/ubuntu/dists/<codename>/main/binary-amd64/Packages.gz` and `ros/rosdistro` `<distro>/distribution.yaml`.
  - CLI syntax: `--help` output in the official Docker images listed below.
  - ROSEnv: its README, `docs/guide.md`, `docs/features.md`, `docs/architecture.md` and `rosenv --help` (repo `MarcoDotIO/rosenv`, commit `1cb9104`).
  - Robots: vendor pages and repositories (Unitree, Booster Robotics, ROBOTIS e-Manual, Hugging Face LeRobot, NVIDIA JetPack and Isaac ROS, Ubuntu, Yahboom) and the lab repositories' own files, as linked in `docs/08-lab-robots.md`.
- **Never invent** names, rooms, results, versions, dates, firmware numbers or package availability. If you cannot verify something, say so in the text or use a `[bracketed placeholder]` and add it to Open items.

## Writing rules

- Follow the lab voice: precise, curious, hands-on, welcoming, grounded. Write for a smart first-year student; define jargon on first use.
- Kent State style: sentence case headings; no Oxford comma in a simple series; "and", not "&"; one through nine spelled out, numerals for 10 and up and always for versions and units; dates like "Sept. 30, 2026" and "May 2027"; no emoji; no exclamation marks.
- Word list: **ROS 2** in prose (never "ROS2", except in names, slugs and code), teleoperation, open-source (adjective), real-world (adjective), leader-follower (never master-slave), robots are "it". No hype words (see the check below).
- Page skeleton (all pages except `README.md`, `AGENTS.md`, `CLAUDE.md`): H1, a `> **Read this when** ...` line, two to four sentences with the one thing to remember, `## Contents` when there are five or more sections, sections, `## Related`, then the `<sub>Last reviewed ...</sub>` footer with an edit link.
- Commands: fenced blocks tagged `bash` (or the right language), one command per line, no `$` prompts, a comment where a step is not obvious, and say which OS and distro the command is for. **Only document a command you ran** or whose syntax you confirmed with `--help`; say so when a command needs a GUI or hardware and was not run.
- Distro differences: when a command or variable differs between Humble, Jazzy, Kilted and Lyrical, say which distro does what (see the table in `docs/05-cheatsheet.md`).
- Mermaid diagrams start with the shared theme line (copy it from any diagram in `docs/`). When edges carry labels, add `linkStyle default color:#1B2533` at the end of the diagram so the labels stay readable. Don't set a font in the theme line: a custom `fontFamily` makes node text clip.
- GitHub alerts sparingly; safety goes in `[!WARNING]` or `[!CAUTION]`. Never write robot safety procedures from imagination; point to `[lab robot safety page]`.
- Links: relative inside this repo; full `https://github.com/ATR-Lab/<repo>/blob/<branch>/<path>` across repos (`master` for dev-guidelines, about, getting-started-atr-lab; `main` for this repo and `.github`). Only link public ATR-Lab repositories.
- Update the footer date and this file's Repo map and Open items whenever you change a page.

## How to check your work

Run from the repository root.

```bash
# 1. Brand, facts and Kent State style (exit 0 = no errors)
PYTHONDONTWRITEBYTECODE=1 ~/.claude/skills/atr-lab-design/.venv/bin/python ~/.claude/skills/atr-lab-design/scripts/brand_check.py $(git ls-files --others --cached --exclude-standard '*.md')
# 2. Markdown structure
npx --yes markdownlint-cli2 "**/*.md"
# 3. Hype words and "ROS2" in prose (review each hit; slugs, URLs and code are fine)
grep -rnE -i "cutting-edge|state-of-the-art|revolutionary|groundbreaking|world-class|innovative|novel|leverag|utiliz|seamless|robust|holistic|transformative|pivotal|delve|furthermore|moreover|ROS2" --include='*.md' .
# 4. Links (the same checker CI runs)
docker run --rm -v "$PWD:/input" -w /input lycheeverse/lychee --no-progress --accept 200,206,429 --exclude-path .git '**/*.md'
```

**Example workspace.** Build and test `examples/hello_ws` in every supported distro, from a scratch copy so no `build/`, `install/` or `log/` lands in the repo:

```bash
cp -R examples/hello_ws /tmp/hello_ws_check
for d in humble jazzy kilted lyrical; do
  rm -rf /tmp/hello_ws_check/build /tmp/hello_ws_check/install /tmp/hello_ws_check/log
  docker run --rm -v /tmp/hello_ws_check:/hello_ws -w /hello_ws ros:$d bash -c "
    source /opt/ros/$d/setup.bash && apt-get update -qq &&
    rosdep update --rosdistro $d && rosdep install --from-paths src --ignore-src -y --rosdistro $d &&
    colcon build --symlink-install && colcon test --packages-select hello_atr && colcon test-result --verbose &&
    source install/setup.bash && timeout -s INT 5 ros2 launch hello_atr hello_atr.launch.py"
done
```

Expected: `Summary: 3 tests, 0 errors, 0 failures, 0 skipped` and `I heard: "Hello from the ATR Lab #1"` for each distro.

**CLI verification.** Cheatsheet syntax was checked by capturing `ros2 <verb> -h` and `ros2 <verb> <sub> -h` for every verb in each image, and by running the commands marked "ran" against the example's talker in `ros:jazzy` (see `docs/05-cheatsheet.md`). Discovery (domain IDs, `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`), the QoS-mismatch warning, `ros2 multicast send/receive`, tf2 tools, `use_sim_time` without `/clock` and the rosdep error messages were reproduced with two or more `ros:jazzy` containers on a user-defined Docker network. GUI tools (RViz, rqt, Gazebo, Foxglove) and hardware drivers were not run.

**Official install steps.** Steps 1 and 2 of `docs/03-install-native.md` (with `ros-<distro>-ros-base` plus the demo nodes instead of `desktop`), the talker and listener, `rosdep init`, `rosdep update` and a dry run of the uninstall command (`apt remove -s '~nros-<distro>-*'`) were run as written in clean `ubuntu:26.04` (Lyrical), `ubuntu:24.04` (Jazzy and Kilted) and `ubuntu:22.04` (Humble) containers; all four installed and the listener heard the talker. The README's Route A block was also run in `ubuntu:24.04` (with `ros-base` instead of `desktop`). In these non-interactive tests, sudo was configured to keep `DEBIAN_FRONTEND=noninteractive`; without that, the Humble run stalled at a debconf prompt (a person at a terminal would simply answer it).

**ROSEnv.** ROSEnv 0.2.0 (commit `1cb9104`) was installed into a Python virtual environment and run inside an Alpine `docker:cli` container as a non-root user with the host's Docker socket mounted and the workspace bind-mounted at the same absolute path, then: `rosenv lock` (598 packages, Jazzy, arm64), `rosenv sync --locked`, `rosenv build`, `rosenv test` (three tests passed), `rosenv run -- ... ros2 launch ...`, `rosenv task`, `rosenv env list` and cleanup with `rosenv env remove`. This is not ROSEnv's tested host (Ubuntu 24.04), so it confirms the manifest and workflow only. On macOS, `rosenv distros`, `rosenv task` and `rosenv init --help` work; `rosenv doctor` exits with "This release supports a Linux Docker host".

**Images verified against** (all linux/arm64, pulled Sept. 30, 2026):

| Image | Digest | Ubuntu | `ros-base` | `ros2cli` |
|---|---|---|---|---|
| `ros:humble` | `sha256:1813d3c85d7f96ff7d3012d865204583255740182db5d0065f8f8cd029a83138` | 22.04 | 0.10.0 | 0.18.19 |
| `ros:jazzy` | `sha256:c3706ef0a0aa45413c07803cf433602f543b22e45b4855f6fca955c2d8ecc4e8` | 24.04 | 0.11.0 | 0.32.12 |
| `ros:kilted` | `sha256:8e7b828a8f24416dd29fde258d81ad49c87fb9becc1289cf69c9d28d36fa78f9` | 24.04 | 0.12.0 | 0.38.4 |
| `ros:lyrical` | `sha256:0c19f326a339ed770ef1d4c0646a8b53bdb49dd5ff74b6de41ebdb8ac21e1806` | 26.04 | 0.13.0 | 0.40.8 |

`ros-apt-source` was at 1.3.0. Re-verify all of this at least once a semester and whenever a distribution is released or reaches end of life (next: Kilted in November or December 2026, Humble in May 2027, the next distribution in May 2027).

## Open items

Placeholders the lab must fill. Agents must not fill these by guessing.

| File | Placeholder | Who can fill it |
|---|---|---|
| `docs/01-what-is-ros2.md`, `docs/04-install-rosenv.md`, `docs/07-debugging.md` | `[lab domain ID assignments]` (a list of which robot or group uses which `ROS_DOMAIN_ID`) | Lab manager |
| `docs/03-install-native.md` | `[your domain ID]` (in a `.bashrc` example) | Each member, from the domain ID list |
| `docs/05-cheatsheet.md` | `[robot domain ID]` (in an example) | Each member, from the domain ID list |
| `docs/03-install-native.md`, `docs/09-resources.md` | `[lab manager name]` | Director or lab manager |
| `docs/03-install-native.md` | `[lab remote-access instructions]` (SSH to lab Ubuntu machines) | Lab manager |
| `docs/06-packages-and-nodes.md`, `docs/08-lab-robots.md` | `[lab robot safety page]` | Director or lab manager (likely a page in getting-started-atr-lab) |
| `docs/07-debugging.md` | `[lab shared storage location]` (for large bags) | Lab manager |
| `docs/07-debugging.md`, `docs/09-resources.md` | `[Slack channel]` | Lab manager |
| `docs/08-lab-robots.md` | `[confirm the lab's Go2 model(s) and firmware version]` | Go2 project members |
| `docs/08-lab-robots.md` | `[lab to confirm Go2 firmware and whether go2_ws needs the upstream update]`: `go2_ws` vendors a copy of `go2_ros2_sdk` without the `aes_key` support added upstream in July 2026 for firmware 1.1.15 and newer | Go2 project members |
| `docs/08-lab-robots.md` | `[confirm the lab's K1 variant]` (Geek, Education or Professional) | K1 project members |
| `docs/08-lab-robots.md` | `[lab to confirm the mower's current distros]`: `robo_mower_ws` docs pair a Humble PC with a Jazzy Raspberry Pi | Mower project members |
| `docs/08-lab-robots.md` | `[confirm the distro on the lab's X3 image]` | Whoever maintains the X3 |
| `docs/08-lab-robots.md` | `[confirm which Yahboom models the lab has]`: the brand fact base says "a Yahboom ROS 2 robot"; the lab repo is for the R2L, the handbook covers the ROSMASTER X3 as assigned | Lab manager |
| `docs/08-lab-robots.md` | `[owner and dates for the Lyrical SDK forks]` | Director |

Decided (Nov. 2026, not placeholders): the lab manages ROS 2 with ROSEnv and uses the distribution each robot's SDK was written for; Jazzy stays the recommendation when nothing pins a distro. The lab plans to fork the Go2 and Booster K1 SDKs to support Lyrical before Humble's end of life in May 2027. The lab's ROSMASTER X3 runs a Jetson Nano.

## Related repos

| Repository | Answers the question |
|---|---|
| [about](https://github.com/ATR-Lab/about) | Who is the lab, what does it work on and how do I contact it? |
| [getting-started-atr-lab](https://github.com/ATR-Lab/getting-started-atr-lab) | I just joined: what do I set up, which tools do we use, and how do I use each lab device? |
| [dev-guidelines](https://github.com/ATR-Lab/dev-guidelines) | How do we write, review and ship code, including ROS 2 packages? |
| [all-things-ros2](https://github.com/ATR-Lab/all-things-ros2) | How does ROS 2 work, which version do I use, and how do I install, run and debug it? (this repo) |
| [.github](https://github.com/ATR-Lab/.github) | What does the ATR-Lab GitHub organization profile show, and what are the shared community files? |
