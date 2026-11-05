# Rollout then Recycle 精读：把真实失败轨迹变成可用的后训练数据

## 基本信息

原文：Praveen Selvaraj、Lorenzo Uttini、Ville Kuosmanen，Rollout then Recycle: 3,718 Labelled Real-Robot Episodes from Benchmarking 7 Policies on 12 Tasks。首次提交 2026-11-02；本次按 arXiv:2611.03168v1 整理。笔记整理和最近更新日期均为 2026-11-05。已阅读短报告全文及官方数据卡相关字段，未下载完整视频、未训练模型。

[论文全文入口](https://arxiv.org/abs/2611.03168)与[固定版本 PDF](https://arxiv.org/pdf/2611.03168v1)。这是新数据发布说明，不是新的 RL 算法，也不是原 ArmnetBench 排行榜的一次等价重测。

## 一句话总结

这项工作的价值在于公开真实策略失败及其来源标签；真正的复用难点不在数据下载，而在终止语义、长度泄漏和跨相机划分是否正确。

## 数据方法与相对变化

[正文 §2–3、表 1](https://arxiv.org/abs/2611.03168)报告 600 条示范和 3,118 条策略 rollout，后者有 2,288 条失败。七种策略在每任务同一批 50 条示范上训练或微调，再在 SO-101 平台执行；一名操作者给出成功、次优、失败标签。相比只发布成功示范，这提供了实际执行分布中的失败覆盖，但并不包含同状态专家纠正动作，不能直接称为 DAgger 数据。

## 开放内容与字段

官方开放 [单臂 LeRobot 数据](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_so101)、[双臂数据](https://huggingface.co/datasets/armnet/armnetbench_v01_lerobot_bimanual_so101)和 [Robometer 格式](https://huggingface.co/datasets/armnet/armnetbench_v01_robometer)。单臂/双臂分别为 6/12 维关节与夹爪位置，三相机、20 fps。数据包含结果标签、策略类别与 checkpoint 来源；这是数据和基座 checkpoint 的开放，不代表专用后训练算法已经实现。

## 关键证据与适用边界

§3 将 reward 定义为成功终点的稀疏 1，其余为 0，次优也没有正奖励。报告未证明利用该语料训练后能提升某个策略，故不写性能增益。其可靠价值是数据可访问、字段清晰以及失败比例可核对。

[§5](https://arxiv.org/abs/2611.03168)提示：成功回合按完成时刻裁切，失败由人停止，长度与尾部静止可能泄漏标签；失败的 done 不等于物理终态。相机问题与策略来源相关，模型可能学到设备偏差。Robometer 每回合有三相机行，必须按 episode 而非行划分。部分额外评测未完整标记，不能用该发布精确重建原排行榜。

## TD3 与 RECAP 接入：需要重新定义终止

以下为分析建议。TD3 的目标可写为 `y = r + γ × b × min(Q1′, Q2′)`，其中 b 是允许 bootstrap 的标记。数据中的人工停止应先与任务完成、碰撞终止、日志截断分开；不能不经核验就把所有 next.done 当作 b=0，也不能反过来对所有失败强行 bootstrap。最后一帧之后是否存在有效 next observation，需要读取实际分片后确认。

对 RECAP 风格的价值与优势标签，先做按完整 episode 或采集会话分组的训练/验证划分，再拟合价值模型；不能让同回合多视角进入不同折。结果类别可作为评测分层，但不能把 policy_type 直接当作动作好坏，更不能给失败回合的每一步都贴“坏动作”标签。失败前的接近与抓取可能是正确行为，末端失败不意味着整个前缀无用。

## 可迁移实验与公平评测

可先在公开数据上比较 RGB 成功分类器、去掉尾部的固定时长窗口分类器、加入 proprioception 的分类器。训练预算、输入帧数和采样任务相同，增加 leave-one-policy-out 验证，报告 AUROC、AUPRC、校准误差及各任务假阳性率。若仅靠视频长度的模型也很强，优先修正数据协议，不急着更换网络。

自己的专家、干预与自主 rollout 可以沿用来源和结果双标签，但另存人工接管时间、接管原因、策略版本、传感器时间戳、terminated/truncated。残差 actor 已经输入 ref_chunk 时，新实验应是失败覆盖、bootstrap 语义和采样比例，而不是再次添加已有条件。先在同一机器人、相同行为空间做实验；跨 SO-101 与双臂平台不能把关节动作直接混合监督。

## 面试追问与精读路线

优先读 §2 标签协议、§3 reward/done 字段、§5 限制，再看官方数据卡。值得准备的问题是：为什么失败轨迹不等于负动作示范？为什么随机划分视频行会高估泛化？人工中止如何影响 Bellman target？没有对齐初始条件时，为什么不能从每个策略的失败比例推出架构优劣？这些问题比泛泛讲“失败数据很重要”更能体现数据闭环经验。

## 原始资源与更新记录

- [arXiv:2611.03168v1](https://arxiv.org/abs/2611.03168v1)：采集 §2、开放字段 §3、用途 §4、限制 §5。
- [官方数据集合](https://huggingface.co/collections/armnet/armnetbench-v01)。下载前按具体数据仓库核验许可证和当前 revision。
- 2026-11-05 首次入库；仅核验文字与数据卡，未对视频做完整审计，无独立训练结果。
