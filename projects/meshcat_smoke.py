import time

import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf

# 启动 meshcat 服务器（会打印一个 URL，并用默认浏览器打开）
vis = meshcat.Visualizer()

# 画一个红球（放大到 0.2 更容易看到）
vis["ball"].set_object(
    g.Sphere(0.2),
    g.MeshLambertMaterial(color=0xFF0000),
)

# 无限循环：球从高处落到地面，循环往复，直到你 Ctrl+C 停止
i = 0
try:
    while True:
        phase = (i % 100) / 100.0      # 0 -> 1 循环
        z = 1.0 - 0.9 * phase          # 高度从 1.0 降到 0.1
        vis["ball"].set_transform(
            tf.translation_matrix([0, 0, z])
        )
        i += 1
        time.sleep(0.02)
except KeyboardInterrupt:
    print("\nstopped.")
