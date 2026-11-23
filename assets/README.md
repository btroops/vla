# assets/ 素材目录

存放正文引用的图片、示意图、动画帧。

## 约定

```
assets/images/     截图、示意图（png / jpg / svg）
assets/diagrams/   可以放 mermaid 源文件（.mmd）或 drawio 源文件
```

- 文件名用**小写英文 + 连字符**：`se3-chain-composition.png`、`vla-three-paradigms.png`，不要用中文名或空格（跨平台最容易出问题）。
- 引用方式（从 `docs/xx.md` 里）：`![齐次变换链](../assets/images/se3-chain-composition.png)`
- 单张图控制在 500KB 以内；超过就压缩，或用外链。
- 能用 mermaid 画的优先用 mermaid（可编辑、体积为 0），复杂的渲染图再放 png。
- 自制图请标注来源；引用他人的图必须注明出处与许可，**不要直接搬用有版权的图**。
