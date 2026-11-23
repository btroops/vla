# 论文怎么读

> 这个目录解决两个问题：**为什么具身智能必须读论文**，以及**读哪些、按什么顺序读**。
>
> 面向零基础读者。读完本文，你应该能用 10 分钟判断一篇论文"值不值得读"，用 1 小时抓住它的方法骨架，并能说清楚它的实验是否可信。

---

## 1. 为什么具身智能要读论文

如果你只学传统软件工程，官方文档基本够用。具身智能（Embodied AI）不是这样，原因有三条。

**第一，工程文档滞后于领域进展。** 这个领域每几个月出现一次范式更替（例如 2023 年的扩散策略、2024 年的开源 VLA、2025 年的流匹配 VLA）。开源库的 README 往往是在某次范式已经很热之后才补上的，而当时的"最佳实践"通常只存在于论文的实验章节里。你在文档里看到的接口，可能就是论文作者为了发版临时封的。

**第二，这个领域没有教科书级的共识。** 传统机器人学有《Modern Robotics》这样的标准教材；具身智能的策略学习部分，五年前和今天的"标准做法"几乎是两套东西。教科书讲不了的，只在论文里。

**第三，也是最实用的一点：读论文是为了获得"判断力"。** 你会看到大量令人兴奋的演示视频。判断力决定了你能不能问出下面这些问题：

- 这个成功率是在几次试验、几个随机种子下测出来的？
- baseline 是他们自己重训的，还是抄的别人的旧数字？
- 只在仿真里做的，还是上了真机？
- 数据集是不是就是他们自己收的、自己测的？

没有这种判断力，你会反复被 demo 视频误导，也会把时间浪费在复现一个本来就不可复现的结果上。

一句话总结：**工程文档教你"怎么调 API"，论文教你"什么方法在什么条件下真的有效"。**

---

## 2. 三遍读法（three-pass approach）

这个方法来自 S. Keshav 的《How to Read a Paper》，在具身智能论文上尤其适用，因为这类论文的页数和附录都偏长。核心思想是：**先花很小的成本决定要不要投入，再逐层加深。**

### 第一遍：5~10 分钟，判断要不要读

只看这些部分，按顺序：

1. **标题**。
2. **摘要**（abstract）——尤其注意最后两句，作者通常在那里写"我们比 X 好了多少"。
3. **所有图的标题 + 第一张系统图**——具身智能论文的第一张图几乎总是"任务 + 模型结构"，一张图能顶半页正文。
4. **结论**（conclusion）——注意作者自己承认的局限。
5. **实验表格的表头**——只看表头，看他们拿什么指标、跟谁比。

这一遍结束后，你只需要回答一个问题：**"这篇跟我要解决的问题相关吗？"**

- 不相关 → 关掉，不要内疚。90% 的论文在这一步就该被关掉。
- 相关 → 记一行笔记（标题、链接、一句话），然后决定要不要进第二遍。

> 常见错误：把第一遍读成"精读"。第一遍的唯一目的是**筛掉**，不是理解。

### 第二遍：约 1 小时，抓住方法与实验

这一遍**跳过所有数学证明和附录**，专注两件事：

- **方法（method）**：输入是什么、输出是什么、模型有几个模块、损失函数是什么形式（不需要推导）。
- **实验设置（experimental setup）**：任务有哪些、数据从哪来、多少条、跟谁比、用什么指标。

边读边拿一张纸回答下面第 3 节的"6 个问题"。填不出来的格子，就是你还没读懂的地方。

具身智能论文有一个特殊之处：**方法部分通常比实验部分好读**。真正的坑几乎都在实验设置里。所以第二遍至少要把一半时间花在实验章节。

### 第三遍：数小时到数天，为了复现

只有当你**真的要动手复现**时才进第三遍：

- 把公式和代码逐行对齐（打开官方仓库，找 `loss` 和 `train_step`）。
- 抄下所有超参数、预处理细节、控制频率、动作归一化方式。
- 找出论文没写但代码里有的东西——这些往往才是复现成败的关键（例如观测的历史帧数、相机内参归一化、动作的边界裁剪）。
- 记下所有"论文里含糊、代码里明确"的点，这些是写复现报告的黄金素材。

### 三遍读法的进度记录

本站的笔记模板里有三个 checkbox，对应这三遍。**允许一篇论文永远停在第一遍**，这是正常状态，不是失败。

---

## 3. 一篇具身智能论文必须回答的 6 个问题

不管论文多长多花哨，读完第二遍你必须能填满这张表。填不满，说明你还没读懂，而不是论文写得不好。

| # | 问题 | 为什么必须问 | 常见含糊点 |
| --- | --- | --- | --- |
| 1 | 任务（task）是什么 | 决定这篇论文的适用范围 | "manipulation"太笼统，要问清是抓取、放置、装配还是可变形物体操作 |
| 2 | 观测（observation）是什么 | 决定你能不能在自己的机器人上复现 | 是 RGB、RGB-D、点云，还是只有本体感知（proprioception）？有没有语言指令？ |
| 3 | 动作空间（action space）怎么定义 | 这一条最容易被忽略，也最容易导致复现失败 | 是关节位置、关节速度、末端位姿增量（delta pose），还是目标位姿？绝对量还是增量？归一化到 [-1, 1] 了吗？ |
| 4 | 数据集多大、从哪来 | 决定结论的可信度与迁移性 | 多少条轨迹（episode）、多少小时、几个机器人、几个场景、人写的语言标注还是模板生成 |
| 5 | 评测协议（evaluation protocol）是什么 | 决定数字能不能横向比较 | 几次试验、几个随机种子、初始状态怎么采样、成功判据是人工判还是自动判 |
| 6 | 失败案例（failure case）是什么 | 决定你是否该相信这个方法的边界 | 论文里有没有 failure analysis？失败集中在哪类物体、哪种光照、哪个阶段？ |

> 提示：第 3 个问题（动作空间）是具身智能与普通深度学习最大的差别。同样叫"策略网络"，输出关节位置和输出末端位姿增量，是两个完全不同的系统，不能直接比较成功率。

---

## 4. 读 VLA／策略类论文时的额外检查项

通用大模型（LLM）论文的评测相对标准化。具身智能的评测**极不标准化**，所以读 VLA（Vision-Language-Action，视觉—语言—动作模型）和策略学习类论文时，除了上面 6 问，再加查下面 5 条。

| 检查项 | 要看什么 | 为什么重要 |
| --- | --- | --- |
| 是否真机评测 | 实验章节有没有真实机器人；还是只有仿真 | 仿真成功率与真机成功率经常差一个数量级，真机数据是最贵、最有信息量的证据 |
| 评测次数与随机种子 | 写明"每组 N 次试验、M 个随机种子"了吗；N 是否 ≥ 10 | 只测 3~5 次的成功率，置信区间宽到几乎没有意义；换种子就翻盘的结论不可信 |
| baseline 是否被公平重训 | baseline 是在**同一份数据、同样算力**下重训的，还是直接引用原论文数字 | 引用旧数字是最常见的不公平比较手法（数据量、训练步数、评测设置全变了） |
| 是否只在自家数据集上比 | 数据集、模型、评测是不是同一个人做的 | 自建数据集 + 自建评测 + 自建 baseline，三项全自建时，结论需要额外证据支撑 |
| 动作表示与推理频率 | 控制频率（Hz）、推理延迟、是否 action chunking | 真机上 3 Hz 的策略和 50 Hz 的策略，能力完全不同；很多"更聪明"的模型只是"更慢" |

补充两条经验：

- **看附录和补充材料**。具身智能论文的正文常常因为篇幅把"每个任务几次试验"塞进附录，而那正是最关键的数字。
- **看视频的播放速度**。视频被加速 4 倍时，"流畅的操作"可能意味着策略只有 5 Hz。这不是造假，但你需要知道。

---

## 5. 分级论文清单

下面 34 篇**全部是真实存在的论文**，最后一列的关键词方便你检索。

- **入门必读**：零基础先读这 4 篇，建立基本词汇。
- **进阶**：读完入门后按方向挑，覆盖抓取、模仿学习、世界模型、足式、灵巧操作。
- **前沿**：VLA 与通用策略主线，变化最快，读的时候注意看年份。

> 清单刻意偏重"方法论文"而非"综述"。综述放在最后，当作地图用，不要当正文读。
>
> 链接一律给 arXiv 摘要页（`arxiv.org/abs/xxxx.xxxxx`），这是最稳定的地址。少数论文没有 arXiv 版本，会明确标注。

### 5.1 入门必读（4 篇）

| 阶段 | 论文 | 一句话读它的理由 | 关键词 |
| --- | --- | --- | --- |
| 入门必读 | *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*（DAgger，Ross 等，AISTATS 2011）<https://arxiv.org/abs/1011.0686> | 理解"为什么单纯模仿会越做越错"（分布偏移，distribution shift）的第一篇，也是所有模仿学习论文都要拿来当 baseline 的东西 | Dataset Aggregation；分布偏移；在线学习 |
| 入门必读 | *A survey of robot learning from demonstration*（Argall 等，Robotics and Autonomous Systems，2009）★无 arXiv 版，按标题在 Google Scholar 检索 | 建立"示教学习"的完整概念框架：示教怎么采、策略怎么表示、怎么泛化，一次把词汇表补齐 | Learning from Demonstration；示教；策略表示 |
| 入门必读 | *Proximal Policy Optimization Algorithms*（PPO，Schulman 等，2017）<https://arxiv.org/abs/1707.06347> | 工程上最常用的 on-policy 算法，具身智能里 80% 的 RL baseline 是它；短、好实现 | PPO；策略梯度；clip 目标 |
| 入门必读 | *Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor*（SAC，Haarnoja 等，ICML 2018）<https://arxiv.org/abs/1801.01290> | 连续控制的样本效率标杆，现在仍是机器人 RL 的首选 off-policy 算法 | SAC；最大熵；off-policy |

### 5.2 进阶（17 篇）

| 阶段 | 论文 | 一句话读它的理由 | 关键词 |
| --- | --- | --- | --- |
| 进阶 | *Continuous control with deep reinforcement learning*（DDPG，Lillicrap 等，2016）<https://arxiv.org/abs/1509.02971> | 确定性策略梯度的开山之作，理解 actor-critic 在连续动作空间怎么工作 | DDPG；确定性策略梯度；actor-critic |
| 进阶 | *Addressing Function Approximation Error in Actor-Critic Methods*（TD3，Fujimoto 等，ICML 2018）<https://arxiv.org/abs/1802.09477> | 讲清 Q 值高估（overestimation）这个几乎所有 RL 项目都会踩的坑，以及双 critic、延迟更新两个补丁 | TD3；Q 值高估；双 critic |
| 进阶 | *QT-Opt: Scalable Deep Reinforcement Learning for Vision-Based Robotic Manipulation*（Kalashnikov 等，CoRL 2018）<https://arxiv.org/abs/1806.10293> | 真机大规模视觉抓取的里程碑：用几十万次真机抓取训练闭环策略，说明"数据规模换能力"这条路走得通（原文摘要报告 58 万次抓取尝试、未见物体 96% 成功率） | QT-Opt；真机大规模；闭环抓取；自监督 |
| 进阶 | *Dex-Net 2.0: Deep Learning to Plan Robust Grasps with Synthetic Point Clouds and Analytic Grasp Metrics*（Mahler 等，RSS 2017）<https://arxiv.org/abs/1703.09312> | 抓取领域的另一条路线：纯合成数据 + 解析抓取质量指标，告诉你"不用真机也能学抓取"的条件 | Dex-Net；合成数据；抓取质量；点云 |
| 进阶 | *Learning Synergies between Pushing and Grasping with Self-supervised Deep Reinforcement Learning*（Zeng 等，IROS 2018）<https://arxiv.org/abs/1803.09956> | 展示"推"与"抓"如何互相成全，是理解非抓取式操作（non-prehensile）与操作原语组合的好例子 | 推动—抓取协同；自监督；Q-learning；杂乱场景 |
| 进阶 | *CLIPort: What and Where Pathways for Robotic Manipulation*（Shridhar 等，CoRL 2021）<https://arxiv.org/abs/2109.12098> | 语言条件操作里最早把"语义理解（what）"和"空间精度（where）"分开建模的工作，双流结构的经典范例 | CLIPort；语言条件；双流；Transporter |
| 进阶 | *Perceiver-Actor: A Multi-Task Transformer for Robotic Manipulation*（PerAct，Shridhar 等，CoRL 2022）<https://arxiv.org/abs/2209.05451> | 把动作空间离散化到 3D 体素（voxel），是理解"6-DoF 动作怎么表示"最清晰的一篇 | PerAct；体素动作；6-DoF；多任务 |
| 进阶 | *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*（Chi 等，RSS 2023）<https://arxiv.org/abs/2303.04137> | 把扩散模型用于动作序列生成，解决了"多模态动作分布"这个模仿学习老大难；近年最重要的策略表示之一 | 扩散策略；动作序列；多模态；receding horizon |
| 进阶 | *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware*（ACT / ALOHA，Zhao 等，RSS 2023）<https://arxiv.org/abs/2304.13705> | ACT（Action Chunking with Transformers）与低成本双臂硬件一起出现，是"用便宜设备做精细操作"的代表（原文摘要：约 10 分钟示教、6 个真机任务） | ACT；动作分块；双臂；低成本遥操作 |
| 进阶 | *MimicGen: A Data Generation System for Scalable Robot Learning using Human Demonstrations*（Mandlekar 等，CoRL 2023）<https://arxiv.org/abs/2310.17596> | 回答"数据不够怎么办"：少量人类示教 + 自动增广成大规模数据集，是数据工程思路的范本 | MimicGen；数据增广；示教；长程任务 |
| 进阶 | *Dream to Control: Learning Behaviors by Latent Imagination*（Dreamer，Hafner 等，ICLR 2020）<https://arxiv.org/abs/1912.01603> | 世界模型（world model）路线的入口：在隐空间里"想象"轨迹来学策略，样本效率极高 | Dreamer；世界模型；隐空间想象 |
| 进阶 | *Mastering Diverse Domains through World Models*（DreamerV3，Hafner 等，2023）<https://arxiv.org/abs/2301.04104> | 同一套超参数跨大量任务稳定工作，是"世界模型能不能工业化"的关键证据 | DreamerV3；鲁棒归一化；通用配置 |
| 进阶 | *Isaac Gym: High Performance GPU-Based Physics Simulation For Robot Learning*（Makoviychuk 等，2021）<https://arxiv.org/abs/2108.10470> | 解释"为什么现在训练 RL 只要几分钟"：物理仿真和策略训练全放 GPU、零 CPU 拷数据；读懂它才能读懂后面所有大规模并行训练的论文 | Isaac Gym；GPU 并行；端到端 GPU 训练 |
| 进阶 | *Learning to Walk in Minutes Using Massively Parallel Deep Reinforcement Learning*（Rudin 等，CoRL 2021）<https://arxiv.org/abs/2109.11978> | 足式 RL 的标杆工程：单卡上千并行环境 + 课程学习，把四足行走训练压缩到分钟级 | 大规模并行；课程学习；legged_gym；ANYmal |
| 进阶 | *Rapid Locomotion via Reinforcement Learning*（Margolis 等，RSS 2022）<https://arxiv.org/abs/2205.02824> | 足式高速运动与 sim2real 的代表：速度课程 + 在线系统辨识，跑得快、转得急、能上草地和冰面 | 高速运动；在线系统辨识；sim2real；Mini Cheetah |
| 进阶 | *Learning agile and dynamic motor skills for legged robots*（Hwangbo 等，Science Robotics 2019）<https://arxiv.org/abs/1901.08652> | 四足 RL 走向真实的早期里程碑（ANYmal），把"仿真训练 + 真机迁移"讲得最清楚的一篇老论文 | ANYmal；致动器网络；sim2real；敏捷运动 |
| 进阶 | *Learning Dexterous In-Hand Manipulation*（OpenAI 等，2018）<https://arxiv.org/abs/1808.00177> | 灵巧手（dexterous hand）手内操作的代表作：纯仿真训练、大量域随机化后迁到真机 Shadow Hand | 灵巧手；手内操作；域随机化；Shadow Hand |

### 5.3 前沿（13 篇）

| 阶段 | 论文 | 一句话读它的理由 | 关键词 |
| --- | --- | --- | --- |
| 前沿 | *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances*（SayCan，Ahn 等，2022）<https://arxiv.org/abs/2204.01691> | LLM 做高层任务分解、底层技能做可行性约束的经典范式，理解"大模型 + 机器人"最初的正确姿势 | SayCan；LLM 规划；affordance；长程任务 |
| 前沿 | *PaLM-E: An Embodied Multimodal Language Model*（Driess 等，2023）<https://arxiv.org/abs/2303.03378> | 把视觉与机器人状态直接塞进语言模型，是"具身多模态大模型"的早期代表（最大的版本是 562B 参数） | PaLM-E；具身多模态；VLM；正迁移 |
| 前沿 | *A Generalist Agent*（Gato，Reed 等，TMLR 2022）<https://arxiv.org/abs/2205.06175> | "一个模型、一套权重、多种具身"的最激进尝试，读它是为了理解通用智能体（generalist agent）的野心与局限 | Gato；多具身；多模态 token；通用智能体 |
| 前沿 | *RT-1: Robotics Transformer for Real-World Control at Scale*（Brohan 等，2022）<https://arxiv.org/abs/2212.06817> | 机器人 Transformer + 大规模真实数据这条主线的起点，理解"数据规模与模型规模如何共同起作用" | RT-1；Robotics Transformer；真实数据规模 |
| 前沿 | *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*（Brohan 等，2023）<https://arxiv.org/abs/2307.15818> | 正式提出 VLA 这个词：把动作表示成文本 token，复用 VLM 的网页知识；所有后续 VLA 论文的参照点 | RT-2；VLA；动作 token 化；co-fine-tuning |
| 前沿 | *Open X-Embodiment: Robotic Learning Datasets and RT-X Models*（Open X-Embodiment Collaboration，2023）<https://arxiv.org/abs/2310.08864> | 机器人界的"统一数据集"：跨机构、跨机器人本体（embodiment）汇总数据，并证明正迁移存在（22 种机器人、21 家机构） | Open X-Embodiment；跨本体；RT-X；数据集标准化 |
| 前沿 | *Octo: An Open-Source Generalist Robot Policy*（Octo Model Team，RSS 2024）<https://arxiv.org/abs/2405.12213> | 第一个被广泛复用的**开源**通用机器人策略：小、快、易微调，适合当你的第一个可跑起来的通用策略 | Octo；开源；通用策略；微调 |
| 前沿 | *OpenVLA: An Open-Source Vision-Language-Action Model*（Kim 等，CoRL 2024）<https://arxiv.org/abs/2406.09246> | 开源 VLA 的事实标准：7B 参数、公开权重、消费级显卡可 LoRA 微调，是"亲手跑 VLA"的第一选择 | OpenVLA；7B；开源权重；LoRA 微调 |
| 前沿 | *π0: A Vision-Language-Action Flow Model for General Robot Control*（Black 等，RSS 2025）<https://arxiv.org/abs/2410.24164> | 用流匹配（flow matching）生成动作的 VLA，把"动作生成"从离散 token 转向连续生成；配合开源的 OpenPI 代码库 | π0；流匹配；动作专家；跨本体 |
| 前沿 | *GR00T N1: An Open Foundation Model for Generalist Humanoid Robots*（NVIDIA，2025）<https://arxiv.org/abs/2503.14734> | 人形机器人通用基础模型的代表，双系统架构（慢思考 VLM + 快动作扩散）是当前主流设计之一 | GR00T N1；人形机器人；双系统；基础模型 |
| 前沿 | *A Survey of Embodied AI: From Simulators to Research Tasks*（Duan 等，IEEE TETCI 2022）<https://arxiv.org/abs/2103.04918> | 快速建立"具身智能全景图"：有哪些仿真器、有哪几类研究任务；当目录用，不要逐页读 | 具身智能综述；仿真器对比；视觉导航；EQA |
| 前沿 | *A Survey on Vision-Language-Action Models for Embodied AI*（Ma 等，2024，期刊版见 IEEE TNNLS）<https://arxiv.org/abs/2405.14093> | 目前维护得最好的 VLA 综述，配套有一个持续更新的资料仓库，用来追新论文最省力 | VLA 综述；分类体系；数据集与基准 |
| 前沿 | 具身智能 / VLA 的**最新**综述 | 这个方向每季度都有新综述，旧综述的"前沿部分"很快就会过时 | 检索 `embodied AI survey`、`vision-language-action survey`、`robot foundation model survey` |

> 关于最后一行：**不要编造标题**。综述类文献请自己用上面三个检索词去 arXiv 或 Google Scholar 按时间排序，取最近 6 个月的来看。本站不给不确定的篇目。

---

## 6. 按方向查：如果只有 1 小时，读哪一篇

清单按"阶段"排好了，但真实情况往往是你带着一个具体问题来查。下表按研究方向索引同一批论文，并给出**时间只够读一篇时的首选**。

| 方向 | 本文清单里的论文 | 只有 1 小时读这篇 | 理由 |
| --- | --- | --- | --- |
| 机器人与操作基础 | DAgger、Argall 综述 | **Argall 综述**（若已有 RL 背景则读 DAgger） | 综述能在 1 小时内建立完整词汇表；DAgger 更"硬核"，适合已有基础的人 |
| 强化学习应用于机器人 | PPO、SAC、DDPG、TD3、Dreamer、DreamerV3 | **PPO** | 最短、最常用；而且 Dreamer 系列的对比对象通常就是 PPO |
| 抓取与操作 | Dex-Net 2.0、QT-Opt、推动—抓取协同 | **QT-Opt** | 一篇论文同时讲清真机规模、闭环控制、自监督，信息密度最高 |
| 通用策略与模仿学习 | CLIPort、PerAct、Diffusion Policy、ACT、MimicGen、RT-1、Octo、OpenVLA | **Diffusion Policy** | 它是理解"动作表示为什么重要"的分水岭；读完再看 ACT 和 VLA 会顺很多 |
| 世界模型与仿真 | Dreamer、DreamerV3、Isaac Gym、MuJoCo（见下） | **Isaac Gym** | 如果你要动手训练，它决定了你后面所有实验的时间预算 |
| 足式与运动 | Learning to Walk in Minutes、Rapid Locomotion、Hwangbo 2019 | **Learning to Walk in Minutes** | 工程细节最完整、配套代码 `legged_gym` 开源，读完就能上手 |
| 灵巧操作 | Learning Dexterous In-Hand Manipulation | **Learning Dexterous In-Hand Manipulation** | 这个方向 1 小时够读的就这一篇经典，读它足以理解难点在哪 |
| VLA 主线 | RT-1、RT-2、Open X-Embodiment、Octo、OpenVLA、π0、GR00T N1 | **RT-2** | VLA 的定义性论文；先懂它，后面所有 VLA 都是它的变体 |
| 综述 | 具身智能综述、VLA 综述 | **VLA 综述** | 最贴近当前主线，且配套资料仓库可长期复用 |

补充说明两篇不在上表、但同样重要的基础文献：

| 文献 | 说明 |
| --- | --- |
| *MuJoCo: A physics engine for model-based control*（Todorov、Erez、Tassa，IROS 2012）★无 arXiv 版，按标题检索 | MuJoCo 仿真器的原始论文。今天你几乎一定会在 MuJoCo 里做实验，但**不需要**在入门阶段读它；等你要调接触参数、怀疑仿真不真实时再回来看。 |
| 《How to Read a Paper》（S. Keshav，ACM SIGCOMM CCR 2007） | 三遍读法的原始出处，3 页，建议在开始读第一篇论文之前读完。 |

---

## 7. 论文笔记的存放约定

**目录与命名**：所有论文笔记都放在本目录（`papers/`）下，文件名格式为：

```
YYYY-会议或arXiv-短标题.md
```

示例：

```text
papers/
├── README.md                                  ← 本文件
├── 论文笔记模板.md                             ← 模板，不要改它，复制它
├── 2011-AISTATS-DAgger.md
├── 2023-RSS-DiffusionPolicy.md
├── 2024-CoRL-OpenVLA.md
└── 2024-arXiv-Octo.md
```

命名规则细节：

- `YYYY` 用论文**首次公开**的年份（通常是 arXiv 首发年，不一定等于会议年）。
- 会议名用官方缩写：`CoRL`、`RSS`、`ICRA`、`IROS`、`ICML`、`NeurIPS`、`ICLR`、`AISTATS`、`CVPR`。
- 只有 arXiv 版（尚未中稿或没有会议）时写 `arXiv`。
- 短标题用驼峰或连字符，不要空格、不要中文标点，方便命令行检索。
- 同一篇论文只建一个文件。会议版和 arXiv 版合并记在一个文件里，在元信息里写清两个链接。

**工作流程**：

1. 复制 [`论文笔记模板.md`](./论文笔记模板.md) 到上面格式的新文件名。
2. 第一遍读完，立刻填"元信息 + 一句话总结"，把三个 checkbox 的第一个勾上。
3. 第二遍读完，填"要解决的问题 / 核心方法 / 实验设置与结果 / 我认为的局限"，勾第二个 checkbox。
4. 第三遍（复现时）才填"可复现性评估"与"关键设计选择与理由"，勾第三个。
5. 任何时候想到的 idea 都直接写进"可延伸的 idea"，哪怕只有一句话。

> 一个反直觉但有效的建议：**先写缺点再写优点**。"我认为的局限"这一栏如果空着，通常说明你还没读到实验章节。

---

## 8. 相关链接

**本仓库内**：

- 论文笔记模板：见 [`./论文笔记模板.md`](./论文笔记模板.md)
- VLA 主线的系统讲解（RT-1 / RT-2 / OpenVLA / Octo / π0、动作表示、评测协议）：见 [`../docs/06-VLA视觉语言动作模型.md`](../docs/06-VLA视觉语言动作模型.md)
- 模仿学习与示教的完整推导（BC、分布偏移、DAgger、动作分块、扩散策略）：见 [`../docs/05-模仿学习与示教.md`](../docs/05-模仿学习与示教.md)
- 强化学习与机器人的基础（MDP、PPO/SAC、奖励设计、sim2real）：见 [`../docs/04-强化学习与机器人.md`](../docs/04-强化学习与机器人.md)
- 常用术语的中英对照：见 [`../docs/10-术语表.md`](../docs/10-术语表.md)
- 教材、课程、仿真器、数据集的汇总：见 [`../resources/资源清单.md`](../resources/资源清单.md)

**外部**：

- arXiv 机器人学分类最新投稿：<https://arxiv.org/list/cs.RO/recent>
- CoRL（Conference on Robot Learning）：<https://www.corl.org/>
- RSS（Robotics: Science and Systems）：<https://roboticsconference.org/>

---

## 附：一页速查

```text
读一篇具身智能论文的动作顺序

1. 标题 + 摘要最后两句 + 第一张图 + 结论         （5 分钟）
   → 不相关？关掉。
2. 方法：输入 / 输出 / 模块 / 损失形式            （20 分钟）
3. 实验：任务 / 数据 / 对手 / 指标                （30 分钟）
   边读边填 6 问：任务、观测、动作空间、
                  数据、评测协议、失败案例
4. 对 VLA / 策略论文再加 5 查：
   真机？试验次数与种子？baseline 重训？
   自建数据集自测？控制频率？
5. 写笔记：先写局限，再写优点。
   三个 checkbox 允许只勾一个。
```
