"""把 MuJoCo 仿真的几何体实时同步到 meshcat，在浏览器里交互式观察物理仿真。

用法:
    .venv/bin/python projects/mujoco_meshcat_bridge.py
    终端会打印一个 URL（如 http://127.0.0.1:7000/static/），用浏览器打开。

验证内容:
    - MuJoCo 的 mj_step 驱动真实物理（铰链摆 + 阻尼）
    - 每帧读取 data.geom_xpos / geom_xmat，转换后同步到 meshcat
    - 浏览器里可鼠标拖拽旋转、滚轮缩放

关键坑（详见 notes/2026-11-23-wsl2-mujoco可视化方案.md）:
    - WSL2 下 mujoco.viewer 开窗会崩，所以走 meshcat 浏览器方案
    - geom_xmat 初始化时全零，必须先 mj_step 一次
    - MuJoCo 是 z-up，Three.js 是 y-up，需要坐标变换
    - Three.js 的 Cylinder 默认沿 y 轴，MuJoCo 的 capsule 沿 z 轴，需要额外旋转
    - meshcat 默认相机就是好视角，不要手动设
"""

import time

import mujoco
import numpy as np
import meshcat
import meshcat.geometry as g

# ---------------------------------------------------------------------------
# 1. 加载 MuJoCo 场景
# ---------------------------------------------------------------------------
# 用摆而不是落体：落体 0.5 秒就落地停住，打开浏览器时已经不动了。
# 摆有铰链 + 阻尼 + 初始角速度，随时打开都在摆动，才能验证位姿确实在同步。
xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 3" dir="0 0 -1"/>
    <!-- plane 只参与 MuJoCo 物理（摆不会掉穿地面），但不渲染；
         地面用 meshcat 自带的网格，省掉坐标变换的麻烦 -->
    <geom name="floor" type="plane" size="5 5 0.1" rgba="0.8 0.8 0.8 1"/>
    <body name="pendulum_arm" pos="0 0 2">
      <joint name="hinge" type="hinge" axis="0 1 0" damping="0.05"/>
      <geom name="arm" type="capsule" fromto="0 0 0 0 0 -1" size="0.04" rgba="0.2 0.4 0.9 1"/>
      <body name="bob" pos="0 0 -1">
        <geom name="bob_geom" type="sphere" size="0.15" rgba="1 0.1 0.1 1"/>
      </body>
    </body>
  </worldbody>
</mujoco>
"""
model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
# 给铰链一个初始角速度，否则摆从竖直静止开始不会动
data.qvel[0] = 1.0

# ---------------------------------------------------------------------------
# 2. 启动 meshcat
# ---------------------------------------------------------------------------
# 不设相机：meshcat 默认相机是斜上方俯视，视角已经很好。
# 手动设相机要抵消浏览器端 OrbitControls 的管理，容易把视角搞差（详见笔记）。
vis = meshcat.Visualizer()

# ---------------------------------------------------------------------------
# 3. 坐标系转换
# ---------------------------------------------------------------------------
# MuJoCo 用 z-up，Three.js（meshcat 底层）用 y-up。
# 这个矩阵把 MuJoCo 的 z 轴映射到 Three.js 的 y 轴。
ZUP_TO_YUP = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, -1, 0, 0],
    [0, 0, 0, 1],
], dtype=float)

# meshcat 的 Cylinder 默认沿 y 轴，MuJoCo 的 capsule 沿 z 轴。
# 右乘这个矩阵（局部坐标系旋转）把几何体的轴向对齐。
# 球是旋转对称的，乘不乘都一样，所以可以统一应用到所有 geom。
R_FIX = np.array([
    [1, 0, 0, 0],
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
], dtype=float)


def rgba_to_hex(rgba):
    """MuJoCo 的 geom_rgba 是 0-1 浮点，meshcat 材质要 0xRRGGBB 整数。"""
    r, g_, b = rgba[:3]
    return (int(r * 255) << 16) | (int(g_ * 255) << 8) | int(b * 255)


def geom_to_meshcat_geometry(geom_type, size):
    """按 MuJoCo 的 geom 类型返回对应的 meshcat 几何体。

    MuJoCo 的 size 是半长，Three.js 的 Box/Cylinder 要全长，所以乘 2。
    返回 None 表示暂不支持的类型（如 mesh / ellipsoid）。
    """
    if geom_type == mujoco.mjtGeom.mjGEOM_SPHERE:
        return g.Sphere(size[0])
    if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
        return g.Box([2 * size[0], 2 * size[1], 2 * size[2]])
    if geom_type == mujoco.mjtGeom.mjGEOM_CAPSULE:
        return g.Cylinder(height=2 * size[1] + 2 * size[0], radius=size[0])
    if geom_type == mujoco.mjtGeom.mjGEOM_CYLINDER:
        return g.Cylinder(height=2 * size[1], radius=size[0])
    return None


# ---------------------------------------------------------------------------
# 4. 初始化：为每个 geom 建一个 meshcat 对象
# ---------------------------------------------------------------------------
geom_nodes = {}
# 必须先 step 一次：MjData 刚创建时 geom_xmat / geom_xpos 全是 0
mujoco.mj_step(model, data)

for i in range(model.ngeom):
    geom = model.geom(i)
    name = geom.name if geom.name else f"geom{i}"

    # 跳过无限大平面，地面用 meshcat 自带的网格代替
    if model.geom_type[i] == mujoco.mjtGeom.mjGEOM_PLANE:
        continue

    geometry = geom_to_meshcat_geometry(model.geom_type[i], model.geom_size[i])
    if geometry is None:
        print(f"skip geom {i} ({name}): unsupported type {model.geom_type[i]}")
        continue

    material = g.MeshLambertMaterial(color=rgba_to_hex(model.geom_rgba[i]))
    node = vis[name]
    node.set_object(geometry, material)
    geom_nodes[i] = node
    print(f"geom {i}: {name}, type={model.geom_type[i]} -> {type(geometry).__name__}")

# ---------------------------------------------------------------------------
# 5. 每帧同步位姿
# ---------------------------------------------------------------------------
print("Opening meshcat. Look for the URL in the terminal.")
try:
    while True:
        mujoco.mj_step(model, data)  # 真实物理推进
        for i, node in geom_nodes.items():
            # geom_xmat 是 9 元素，reshape 成 3x3 旋转矩阵，拼进 4x4 齐次矩阵
            T_mujoco = np.eye(4)
            T_mujoco[:3, :3] = data.geom_xmat[i].reshape(3, 3)
            T_mujoco[:3, 3] = data.geom_xpos[i]

            # 先转到 Three.js 坐标系，再修正几何体轴向。
            # 统一应用保证摆杆和球不会错位。
            T_three = ZUP_TO_YUP @ T_mujoco @ R_FIX
            node.set_transform(T_three)
        time.sleep(0.01)  # ~100Hz，够流畅且不给 zmq 太大压力
except KeyboardInterrupt:
    print("\nstopped.")
