# P00 · MuJoCo 仿真在 meshcat 中可视化

- 状态：完成
- 起止：2026-11-23，实际投入约 3 小时
- 关联章节：../../docs/07-仿真环境与工具链.md（环境搭建、渲染排查）

## 目标

在 WSL2 环境下，把真实 MuJoCo 仿真的几何体实时同步到浏览器，能交互式观察物理仿真（而不是只靠离屏渲染出的静态图）。

## 前置

- 环境：WSL2 Ubuntu / Python 3.10 / mujoco 3.17.0 / meshcat 0.3.2 / RTX 4060 Laptop
- 已完成：W1 环境验收（PyTorch CUDA 可用、MuJoCo `render ok`）

## 步骤

1. 验证离屏渲染可用（`render_animation.py` → gif 动画）
2. 验证 meshcat 浏览器可视化可用（`meshcat_smoke.py` → 手写红球）
3. 把 MuJoCo 的 geom 按类型转成 meshcat 对象，每帧同步 `geom_xpos` / `geom_xmat`（`mujoco_meshcat_bridge.py`）
4. 排查并修复坐标变换、相机视角等问题（详见 `notes.md`）

## 验收标准（可量化）

- [x] 浏览器里能看到 Gray 网格地面 + 蓝色摆杆 + 红球
- [x] 摆持续运动（真实 `mj_step` 物理），不是静止截图
- [x] 鼠标拖拽旋转、滚轮缩放可用
- [x] 球和摆杆相对位置正确（没有错位或朝向错误）

## 结果

运行 `src/mujoco_meshcat_bridge.py`，浏览器打开终端打印的 URL。反复调试后的最终配置见 `src/mujoco_meshcat_bridge.py`，踩坑过程见 `notes.md`。

## 结论与反思

- 学到什么：
  - WSL2 下 `mujoco.viewer` 开窗会崩整个 WSL 会话，meshcat 是绕开图形栈的正解
  - meshcat 的位姿同步就是发 msgpack 二进制命令（`set_object` / `set_transform`），浏览器端用 THREE.js 重建场景
  - 坐标约定是最大的坑：z-up→y-up、Cylinder 轴向、尺寸半长→全长，每个都要单独处理
- 卡在哪、怎么解决的：见 `notes.md`（5 个坑）
- 如果重做一次，会怎么改：
  - 一开始就用持续运动的系统（摆）验证，而不是落体（0.5 秒就停，看起来像没同步）
  - 一开始就不设相机，用 meshcat 默认视角
  - 更早读源码（`commands.py` / `zmqserver.py` / `index.js`），能省掉一半猜测
