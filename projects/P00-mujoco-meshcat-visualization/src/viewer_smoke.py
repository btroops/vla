import mujoco
import time
from  mujoco import viewer
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

with viewer.launch_passive(model, data) as v:
        while viewer.is_running():
            mujoco.mj_step(model, data)
            v.sync()
            time.sleep(0.01)