# MR0 精读：保留被替换动作，让干预形成正负监督

## 基本信息与一句话总结

原文 *Meituan-Robotics-0: A Vision-Language-Action Foundation Model for Desktop Manipulation*，Meituan Robotics Team，Caicheng Wang、Chen Zhao 等。首次提交 2026-11-05 18:55:42 UTC；实际读取 arXiv:2611.08577v3，v2 更新于 2026-11-10，v3 更新于 2026-11-12 16:51:56 UTC。首次整理 2026-11-09，本笔记修订 2026-11-13。已读方法、实验、附录 A–C；以下均为作者报告，未复现训练或真机。

[固定全文](https://arxiv.org/html/2611.08577v3)、[PDF](https://arxiv.org/pdf/2611.08577v3)、[版本历史](https://arxiv.org/abs/2611.08577)、[项目页](https://meituan-robotics.github.io/Meituan-Robotics-0/)、[官方代码](https://github.com/Meituan-Robotics/Meituan-Robotics-0)是原始资源。对现有项目最有价值的不是更大的预训练数字，而是 Rollback 数据协议：将被替换的策略片段也保存为负条件，与人工纠正共同训练 CFG-DAgger；另提供可审计的异步队列算法。

## 问题与训练框架

[§2–3](https://arxiv.org/html/2611.08577v3#S3)使用 Qwen3.5-4B backbone，先用 FAST 离散动作及视觉语言任务共训，再换连续 MMDiT action head，最后执行任务后训练。连续头预测 clean action、转为速度空间损失。论文的 15,060 小时是整理后的机器人数据库存，而历史 [v1 表 3](https://arxiv.org/html/2611.08577v1#S3.T3)的预训练 action pool 约 13.6k 小时；v3 已删去该明细表，不能将历史重采样计数当作新版逐类统计。147M 原始视觉语言样本与重采样后的 effective count 也不是同一口径。

统一动作接口最多 20 维，对应双臂各十维末端位姿与夹爪，单臂等缺失通道用 mask。统一维度不意味着体现动力学一致；不能从大规模预训练结果推断 Joint 与 EE Pose 对某台 X5 的优劣。

## Rollback 与 CFG-DAgger 的具体变化

[§3.2.3、图 6 和附录 C.3](https://arxiv.org/html/2611.08577v3#A3.SS3)由操作者暂停失败附近的动作，选择早先记录的 anchor，返回并提供纠正。被替换分支 τ− 标 I=0，演示及人类纠正 τ+ 标 I=1；两分支共享起点，但无需后续逐帧对齐。场景无法恢复时退回普通 HIL，只贡献正数据。这是采集协议，不能仅用倒播关节轨迹就假设物体、接触和隐藏状态都被恢复。

共享策略用 flow-matching 学正、负和无条件分支。正数据以 0.3 概率丢掉条件训练 unconditional；负数据始终保留负条件。推理从同一初始噪声分别完成正负动作块，再一次性组合：

`a_CFG = a_negative + γ (a_positive − a_negative)`，论文 γ=1.25。

这是完成后的 action-space extrapolation，不是每个去噪步骤的速度 guidance，也不是 DPO。负标签表示被替换的局部段，而非整回合每个动作都失败。原文不重平衡正负类别，排除其他自主片段、重置动作及短于 H=50 的段，因而“保留负数据”不代表全部失败轨迹直接进入动作学习。

[附录 C.2](https://arxiv.org/html/2611.08577v3#A3.SS2)的 RECAP 对照另行训练 201-bin value，以 N=50 的优势和分位阈值给正/基础条件；失败分支用于 value，但被排除出 policy 训练。这个本地实现与 CFG-DAgger 数据选取不同，因此结果不能写成所有 RECAP 实现均不如直接标签。没有 value 训练节省的是一个环节，不代表推理也无额外开销：CFG 仍需正负预测。

## 异步执行：可借鉴队列，不混称 RTC

[§4.1、附录 B 算法 1 与表 6](https://arxiv.org/html/2611.08577v3#A2)解耦控制与预测：30Hz 消耗队列，目标 3Hz 预测，H=50、K_lat=4、短缓冲补齐长度 8。新块到达时丢弃 `d=min(k,K_lat)` 个前导命令；k 是自上次成功更新以来消耗的命令数，而不是直接等于本次请求耗时。重叠区用线性权重从旧块过渡到新块，短旧块重复末命令补齐。

它没有这里已核验方法所述的训练前缀注入或推理 inpainting；不能将线性合并等同于你的 RTC。延迟估计包含网络、预测、后处理及 IK，正文还指出过于频繁更新会反复重启 blend、拖慢响应。完整 overlap 的平滑长度也不等于固定 blend=4。空缓冲并未建立机器人安全制动保证，保持末目标和停止发新目标的硬件语义必须另查。

## 实验与结论边界

[§5.1 表 3](https://arxiv.org/html/2611.08577v3#S5.SS1)在 RoboTwin 2.0 的 50 任务、每任务每 split 100 回合报告 clean 93.2%、randomized 93.9%、均值 93.6%；这是策略适配结果，明确未使用 agent 或 RL 后训练，不能归因于 Rollback。不同基座预训练规模也不是受控单变量消融。

[§5.2、图 11](https://arxiv.org/html/2611.08577v3#S5.SS2)Ethernet insertion 用同演示和 Rollback episodes、同 mid-training 起点比较 HG-DAgger、RECAP、CFG-DAgger，每策略每任务 30 次自主试验。全 Rollback 数据时 CFG-DAgger SR=0.70、PS=0.90，RECAP SR=0.60、PS=0.67。PS 是抓取、交接、插入三个 milestone 的完成比例，不是成功概率。30 次评估差异只有三次成功，不能说已证明跨任务普遍优势。

表 5 中以太网组为 200 demo+450 Rollback episodes；与 π0.5 的主比较另用超过 1,400 episodes，不可把两组数据量混写成同一个实验。字母块和叠衣的指标另有定义。高层事件记忆的跨任务检索与条件恢复只有两个定性部署，不足以声明长程 agent 成功率或 VLN-CE 性能提升；也未看到异步 vs 同步的充分受控成功率/尾延迟消融。

## v3 修订核验：基准重报，不等于发布了新权重

对照 [v2](https://arxiv.org/html/2611.08577v2) 和 [v3 表 4](https://arxiv.org/html/2611.08577v3#S5.T4)：RoboDojo 为 42 个双臂仿真任务，MR0 从旧表的 Score/SR 20.15/14.63 更新为 21.68/15.73，Memory 分组从 29.03/28.33 到 39.52/39.22。旧表写同一 checkpoint 两次完整评测等权平均，新表写三评估种子等权，且展示基线有变化；没有逐种子逐任务结果，不能把这 1.10 个百分点归为模型或算法改进。核验时官方 [模型卡](https://huggingface.co/MeituanRobotics/Meituan-Robotics-0)说明发布 checkpoint 字节未变，不能将表中历史增强策略自动等同于该下载。RoboTwin 93.6% 和 Rollback 的 0.70 SR/0.90 PS 核心结果没有变化；v3 附录 C 更明确地说明了 RECAP 拼完整前缀、CFG-DAgger 只用局部片段，以及 HG-DAgger 保留样本同权。

## 实际开放情况与精读路线

官方仓库可读训练入口 `mr0/training/train_mr0.py`、配置、MMDiT head 和 OpenPI 兼容 server 说明，README 提供模型及 RoboDesk 数据入口。当前目录核验尚不足确认 Rollback 采集器、CFG-DAgger/RECAP 完整训练和上述 agent 均已开放，不能用“官方代码存在”替代逐模块核验。[官方模型卡](https://huggingface.co/MeituanRobotics/Meituan-Robotics-0)列出完整 `checkpoints/model.pt`、配置、归一化统计和 SHA256SUMS，但发布预训练 checkpoint 的 action horizon 为 16，与论文真机后训练的 H=50 不同，不能直接视作同一部署配置。本次读取模型卡，未下载权重或测试硬件。

优先读附录 A 的数据边界、C.2/C.3 的分支与采样差异、B 的计数器和锁，再读图 11。代码先读 [GETTING_STARTED](https://github.com/Meituan-Robotics/Meituan-Robotics-0/blob/opensource/GETTING_STARTED.md) 和 [QwenMMDiT](https://github.com/Meituan-Robotics/Meituan-Robotics-0/blob/opensource/mr0/model/framework/VLM4A/QwenMMDiT.py)，部署前核对坐标、归一化、夹爪开闭方向及 IK。

## 可迁移实验与面试追问

以下是分析建议。对现有 100 专家+220 DAgger 数据先审计是否保存了接管前策略输出、实际执行动作和同步观测；没有可恢复 anchor 的历史记录，不应补造正负配对。新增少量可安全重置的摆放任务，比较普通 HG-DAgger、你现有 RECAP、直接正负条件三组，固定采集人工分钟、回合、训练 FLOPs 与同初始化；另给每组相同推理预算，报告 CFG 额外调用成本。统计 SR、阶段进度、干预分钟、恢复误差和原成功任务退化。

异步实验独立进行：固定策略和 H=30，以现有 RTC D=5–6、blend=4 为基线，只替换队列合并，注入相同延迟轨迹。报告 P95/P99 观测年龄、耗尽率、轨迹抖动、响应距离及任务完成时间，不能同时更换模型。Rollback 只在物体可复位、限速、可急停的任务上使用，不倒放插接、夹持或有蓄能的接触动作。

面试重点：负条件为什么不等于坏状态？同 anchor 是否足以构成偏好对？动作空间 CFG 能否违反关节/力限制？3Hz 更新与 30Hz 控制为何不能称作模型 30Hz？这些问题能串起数据闭环、价值条件化与异步部署。

2026-11-09 首次入库，区分数据库存与训练池、局部 RECAP 变体、代码开放边界及定性 agent 证据。

2026-11-13 按 v3 修订：核对 RoboDojo 评估口径、公开权重说明及附录 C，并更新原链接和表号；保留文章地址。
