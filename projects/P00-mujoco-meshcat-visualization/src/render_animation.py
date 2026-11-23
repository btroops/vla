import mujoco
from PIL import Image

xml = """
<mujoco>
  <worldbody>
    <light pos="0 0 2" dir="0 0 -1"/>
    <geom name="floor" type="plane" size="2 2 0.1" rgba="0.8 0.8 0.8 1"/>
    <body name="ball" pos="0 0 1">
      <freejoint/>
      <geom type="sphere" size="0.1" rgba="1 0 0 1"/>
    </body>
  </worldbody>
</mujoco>
"""

model = mujoco.MjModel.from_xml_string(xml)
data = mujoco.MjData(model)
renderer = mujoco.Renderer(model, height=240, width=320)

frames = []
for step in range(200):
    mujoco.mj_step(model, data)
    if step % 2 == 0:  # 每 2 步取一帧，降低 gif 体积
        renderer.update_scene(data)
        frames.append(Image.fromarray(renderer.render()))
renderer.close()

out = "assets/images/w1-ball-falling.gif"
frames[0].save(
    out,
    save_all=True,
    append_images=frames[1:],
    duration=40,   # 每帧 40ms，约 25fps
    loop=0,
)
print(f"saved {len(frames)} frames -> {out}")
