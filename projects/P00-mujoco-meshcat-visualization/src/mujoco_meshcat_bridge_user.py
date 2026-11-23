import time

import mujoco
import numpy as np
import meshcat
import meshcat.geometry as g

# --- 1. 加载场景 ---
xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 3" dir="0 0 -1"/>
    <!-- 我们不在 meshcat 渲染这个 plane，改用 meshcat 自带的网格地面 -->
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
# 调小初始角速度，让摆动作平缓一点
data.qvel[0] = 1.0

# --- 2. 启动 meshcat 并设置完美的初始视角 ---
vis = meshcat.Visualizer()

# 构造 Look-At 矩阵
eye = np.array([3.0, 2.0, 3.0])   # 相机在 Meshcat (Y-up) 世界中的位置
target = np.array([0.0, 1.0, 0.0]) # 看向摆的中间位置
up = np.array([0.0, 1.0, 0.0])     # 头顶朝上

z = eye - target
z = z / np.linalg.norm(z)
x = np.cross(up, z)
x = x / np.linalg.norm(x)
y = np.cross(z, x)

cam_tf = np.eye(4)
cam_tf[:3, 0] = x
cam_tf[:3, 1] = y
cam_tf[:3, 2] = z
cam_tf[:3, 3] = eye

# 抵消 Meshcat 默认父节点的旋转
R_parent = np.array([
    [1, 0, 0, 0],
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
])
cam = vis["/Cameras/default/rotated/<object>"]
cam.set_transform(np.linalg.inv(R_parent) @ cam_tf)


# --- 3. 坐标系转换 ---
ZUP_TO_YUP = np.array([
    [1, 0, 0, 0],
    [0, 0, 1, 0],
    [0, -1, 0, 0],
    [0, 0, 0, 1],
], dtype=float)

# 修正 Three.js 的圆柱体默认沿 Y 轴，而 MuJoCo 沿 Z 轴的问题
R_FIX = np.array([
    [1, 0, 0, 0],
    [0, 0, -1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
], dtype=float)

def rgba_to_hex(rgba):
    r, g_, b = rgba[:3]
    return (int(r * 255) << 16) | (int(g_ * 255) << 8) | int(b * 255)

def geom_to_meshcat_geometry(geom, geom_type, size):
    if geom_type == mujoco.mjtGeom.mjGEOM_SPHERE:
        return g.Sphere(size[0])
    if geom_type == mujoco.mjtGeom.mjGEOM_BOX:
        return g.Box([2 * size[0], 2 * size[1], 2 * size[2]])
    if geom_type == mujoco.mjtGeom.mjGEOM_CAPSULE:
        return g.Cylinder(height=2 * size[1] + 2 * size[0], radius=size[0])
    if geom_type == mujoco.mjtGeom.mjGEOM_CYLINDER:
        return g.Cylinder(height=2 * size[1], radius=size[0])
    return None

# --- 4. 初始化 ---
geom_nodes = {}
mujoco.mj_step(model, data)

for i in range(model.ngeom):
    geom = model.geom(i)
    name = geom.name if geom.name else f"geom{i}"
    
    # 跳过 MuJoCo 里的无限大平面，用 Meshcat 自带的网格代替
    if model.geom_type[i] == mujoco.mjtGeom.mjGEOM_PLANE:
        continue
        
    geometry = geom_to_meshcat_geometry(geom, model.geom_type[i], model.geom_size[i])
    if geometry is None:
        print(f"skip geom {i} ({name}): unsupported type {model.geom_type[i]}")
        continue
        
    material = g.MeshLambertMaterial(color=rgba_to_hex(model.geom_rgba[i]))
    node = vis[name]
    node.set_object(geometry, material)
    geom_nodes[i] = node

# --- 5. 每帧同步 ---
print("Opening meshcat. Look for the URL in the terminal.")
try:
    while True:
        mujoco.mj_step(model, data)
        for i, node in geom_nodes.items():
            T_mujoco = np.eye(4)
            T_mujoco[:3, :3] = data.geom_xmat[i].reshape(3, 3)
            T_mujoco[:3, 3] = data.geom_xpos[i]
            
            # 统一应用旋转修正，保证各个部件之间不会错位
            T_three = ZUP_TO_YUP @ T_mujoco @ R_FIX
            node.set_transform(T_three)
            
        time.sleep(0.01)
except KeyboardInterrupt:
    print("\nstopped.")