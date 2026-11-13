# TEMPO v2 精读：用两条 TD3 更新通路控制表征漂移

## 基本信息与一句话总结

Ziheng Liu、Quantao Yang，*TEMPO: Semantic-Action Decoupled RL Post-Training for Vision-Language-Action Models*。2026-08-07 首次提交，2026-11-12 13:39:50 UTC 实质修订，实际阅读 arXiv:2608.07314v2，整理与实质更新 2026-11-13。[固定全文](https://arxiv.org/html/2608.07314v2) · [旧版](https://arxiv.org/html/2608.07314v1) · [版本历史](https://arxiv.org/abs/2608.07314)。

保留视觉语言底座，把语义投影和动作专家当作两个不同的决策问题；后者更新更快，前者不频繁改写低层 critic 看到的状态空间。这里的“频率”是**训练优化频率**，不是 RTC 或控制器的实时频率。

## 机制与已有工作区别

[§III-B–D](https://arxiv.org/html/2608.07314v2#S3.SS2)把 FLOWER 写成 h=VL(o,ℓ)、z=π_s(h)、a=π_a(z)。语义层 TD3 的状态/动作是 h/z，低层 TD3 是 z/机器人动作块 a；每层各有 replay、双 Q、目标网络和优化器，但两组 transition 来自同一次真实环境执行，完成当前指令奖励 +1，其余 0。长链继续运行时，当前指令结束仍截断 Bellman bootstrap，故不是把后一条指令的奖励归给前一条。

两组目标都可概括为 y=r+γ(1−done)·min(Q′₁,Q′₂)，但各自的 Q 输入和下一动作含义不同。动作 critic 在存下的 z 上做回归，更新 actor 时从存下的 h 重算当前 z 并停止对语义层的梯度；低层目标亦使用目标投影。旧 replay 与当前 latent 不同仍会造成分布偏移，stop-gradient 只是阻止梯度串联，不能保证策略迭代收敛。[§III-E](https://arxiv.org/html/2608.07314v2#S3.SS5)用各层 critic 更新数 N 与延迟 actor 间隔 d 定义近似更新量 f=N/d，再比较 ρ=f_a/f_s。论文的 FLOWER-RL 对照用单条 TD3 联合更新投影和动作头；与 X5 已冻结的 RLToken 编码加 TD3 动作残差相比，新增的是**可优化的上游条件接口及其独立 critic**，不是加 ref_chunk，也不是把价值分布变成另一个 TD3 双 Q。

## v2 实质变化、结果与局限

v1 的 FLOWER 主表和两项实机不能与 v2 的结果混读。v2 重报三种子的主表，加入固定输入的 latent 漂移探针、VLA-Adapter-Pro 的结构迁移、以及第三项实机操作。[表 I](https://arxiv.org/html/2608.07314v2#S4.T1)在 CALVIN ABC→D 五指令链上，单环 FLOWER-RL 的五连成率（SR5）78.70±0.70%，TEMPO 81.70±0.40%；平均完成链长 4.52→4.58。该表明确三种子，但未明确逐种子分母，不从小数倒推计数。

[表 V](https://arxiv.org/html/2608.07314v2#S4.T5)固定 108 个输入（3 条探针轨迹）比较归一化后 token 均值的 L2 漂移。1:1 为 0.641、4:1 为 0.409，同一个初态每设置 50 次、最多 360 步的目标任务成功率分别为 33/50、49/50。漂移误差条按轨迹而不是训练种子；更小的漂移与更高成功相关，不能排除更新预算差异或宣称 4:1 普适。这个单任务比较不等同于全 CALVIN 的 SR5；[表 VII](https://arxiv.org/html/2608.07314v2#S4.T7)用 VLA-Adapter-Pro 的 layer-wise K/V 投影作语义接口，三种子 SR5 77.23→79.17%，对照为原模型，不是等预算的该骨干单环 RL。

[§IV-C、图 4](https://arxiv.org/html/2608.07314v2#S4.SS3)使用 Alicia-D 单臂，三任务各 60 条演示；每种子每 checkpoint 20 次二元奖励评估，曲线为三种子均值与标准差。作者报告后段回报较高，不能推出 X5 插接成功率，也不代表语义 head 可以无风险在线学习。只有一个主要仿真基准、两种可拆架构，文中未提供广泛 OOD、安全事件率或等 GPU 时间的频率扫描。以上为作者报告，未独立复现。

## 代码、X5 迁移与面试

论文列出[项目入口](https://anonymous.4open.science/w/tempo-page/)，本次访问返回 404，未核验到可下载的 TEMPO 专用代码、权重或实机数据。先读 §III-D 的存储 z 与重算 z、§III-E 的预算定义、表 V 与表 VII，分清哪些结果仅在固定初态下成立。

分析建议：先保持 z_rl + proprio + ref_chunk、C=10、现有 30Hz RTC 不变，用专家与四轮 DAgger 回放做固定探针集。基线为完全冻结 z_rl；另设小型可训练投影、同频和低频更新组，用同一交互集和匹配的 actor/critic 总更新与算力预算，单独记录每层计数。用冻结与重算表示做诊断，分离“critic 学旧坐标”和“新语义更有效”；报告按接触阶段的 latent 漂移、双 Q 分歧、干预/失败时的价值校准、成功率与旧任务遗忘。先离线和仿真，真机不边探索边放开力、限位和夹爪保护。面试可问：两层为什么都用同一个稀疏奖励？训练中的 latent 漂移与部署时语义缓存陈旧有什么区别？何时继续冻结上游反而更强？
