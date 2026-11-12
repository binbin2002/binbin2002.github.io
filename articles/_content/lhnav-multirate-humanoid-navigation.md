# LHNav 精读：让目标交接、动作预测与全身控制各跑自己的频率

## 基本信息与一句话总结

Xueyang Wang、Zehong Shen、Dingkun Wei、Huaijin Pi、Changpeng Wang、Xing Zhu、Hujun Bao、Yujun Shen、Xiaowei Zhou，*LHNav: Long-Horizon Humanoid Navigation via Multirate Coordination and Physics-Grounded Action Data*。首次提交 2026-11-09 09:50:53 UTC，实际阅读 arXiv:2611.12136v1，未见后续修订。2026-11-12 整理与实质更新，近七天新作，非今日首发。[固定全文](https://arxiv.org/html/2611.12136v1) · [版本历史](https://arxiv.org/abs/2611.12136) · [项目页与视频](https://robbyant-research.github.io/LHNav/)。

它把长程语言任务切成可验证的目标序列，用异步 VLA 生成 G1 运动 token，让 50Hz 控制器解码；航点不是执行输入，而是训练时给全身动作施加几何监督的接口。

## 研究问题与方法

[§III-A](https://arxiv.org/html/2611.12136v1#S3.SS1)假设场景有候选目的地参考图目录。Brain 维护已完成、当前、待处理三类子任务；规划器可以根据执行反馈更新待处理项。独立 VLM 以最高 1Hz 读当前目标、参考图和时序观测，写入到达结论与证据。关键工程约定是：停下时阻止新推理请求并丢弃在途旧预测；到达已验证、运动计划耗尽且里程计确认根部稳定后，才提交完成并切换目标。它不是“VLM 说到达就马上把下一个动作塞进队列”。

[§III-B、式 1–3](https://arxiv.org/html/2611.12136v1#S3.SS2)在 GR00T N1.7/SONIC 微调接口上，用共享 DiT 同时预测 H=40 的运动 token 与航点。运动 token 每步 64 维按时间索引；航点用局部平面位置、朝向 sin/cos 和到达位按路径距离采样，两者不逐帧对齐。联合 flow-matching 外加 L_sdf=η·log(1+exp(−c_min/η))，其中 c_min 是去噪完成后有效航点经位姿变换、查询场景平面 SDF 的最小值。最小距离防止少数危险点被平均稀释；但它是训练软损失，不能保证执行时每个足步、全身扫掠体积或未知障碍的安全。

VLA 约 8Hz 更新，SONIC 冻结解码器以 50Hz 下发目标，返回 chunk 跳过推理期间已消耗的前缀并直接替换未执行尾段，不做 blending。相比[原版 RTC](https://arxiv.org/abs/2506.07339)把已确定执行的前缀固定、再 inpaint 后续动作，这里主要靠索引对齐和异步交接；不能把两者的连续性机制或频率对照视为同一实验。相比本文的 waypoint-only 臂，执行端输入的是动作 token，而不是把每次航点预测转成朝向该点的固定速度指令（[表 V](https://arxiv.org/html/2611.12136v1#S5.T5)）。

[§IV](https://arxiv.org/html/2611.12136v1#S4)先在 InteriorGS 的可走平面与可移动障碍中规划 A* 路线，ARDY 生成 50Hz 运动，P-SONIC 用未来骨盆位置偏差和最近机体速度作特权输入，以 PPO 微调编码器、保留量化器与解码器。MuJoCo 执行后筛掉跌倒轨迹，再从实际执行状态渲染视觉并生成动作与航点标签。强化学习用于跟踪教师，不是在 G1 上在线训练部署 VLA；学生无需读未来参考骨盆轨迹。

## 关键实验、消融与局限

[表 I、V、VI](https://arxiv.org/html/2611.12136v1#S5.T1)为 InteriorGS 的 20 个未见场景、522 个相同起终点回合。LHNav 单目标 SR₀.₅（末端距目标 0.5m 内且未跌倒）52.3%，同数据适配 OmniNav 为 36.0%、DualVLN 18.6%。这些基线共享 SONIC，但航点执行采用 0.6m/s、按初段方向给速度，不能外推为任何 ROS 局部规划器都不如 token。联合预测有/无几何项的 SR₀.₅ 为 52.3%/47.3%，路径位于可通行区外的比例 CR 为 8.6%/14.4%；CR 不是实机碰撞事件率。[表 VII](https://arxiv.org/html/2611.12136v1#S5.T7)固定控制 50Hz，约 2Hz 与 8Hz 的 SR₀.₅ 仅 51.7% 对 52.3%，前者 jerk 更低（53.0 对 75.6 m/s³），后者越界比例更低且零跌倒。不能从均值就定一个通用 VLA 频率。

[表 II](https://arxiv.org/html/2611.12136v1#S5.T2)在来自训练场景子集的 45 个、至少三站的任务上，异步 34/45，同步 33/45；成功任务平均 82.1 对 97.8 秒，但各自成功的任务集合不同，不能当全任务配对延迟。去掉到达验证及相关重试/转向恢复后 25/45；该对照不能单独归因给验证器。[表 III](https://arxiv.org/html/2611.12136v1#S5.T3)的 G1 家庭五个单目标各 5/5，三站任务 4/5，涉及场景专用单目标训练和参考图目录。长程“零样本”指没见过多站指令，不表示未见场景或未见单目标技能。移动后推玩具是定性案例，不是完成搬运、烹饪或家务成功率。以上均为作者报告，未独立复现。

## 开放程度与精读路线

[作者仓库](https://github.com/robbyant-research/LHNav)可读，但核验时 main 根目录仅有站点和媒体资产，README 只列标题；未见 LHNav 训练、推理、数据引擎实现或权重。上游 [SONIC/GR00T WBC 工作流](https://nvlabs.github.io/GR00T-WholeBodyControl/tutorials/vla_workflow.html)不是 LHNav 的 checkpoint。优先精读 §III-A 的交接条件、[§III-B](https://arxiv.org/html/2611.12136v1#S3.SS2) 的两种索引与 SDF 梯度，再看表 II、VI、VII 分辨调度、几何监督和频率的作用。

## Hi-Nav 迁移与面试

分析建议：不更换 Hi-Nav 的 ISOM 或 ROS 规划器，先在仿真和日志回放里只替换目标交接协议。对比串行验证、异步但无版本过滤、异步且携带 subgoal_id/地图版本/观测时间戳并等待动作停稳三臂；在同路线、同动作及 VLM 调用预算下重放同一延迟分布和乱序到达事件。记录过期航点实际被执行率、错误阶段推进、SR/SPL、全过程 P95（失败计入超时）、急停和人工接管。异步无过滤仅用于回放；真机默认拒绝旧目标并保留限速、避障、失联停机，不把 SDF 训练项当安全认证。

面试可问：如何让迟到的“已到达”不能提交到新的子任务？时间索引的运动 token 为什么不与距离采样的航点对齐？同步和异步只差一例成功时怎么验证吞吐收益？为什么动作模型更高频会更贴路，却可能让 jerk 变大？
