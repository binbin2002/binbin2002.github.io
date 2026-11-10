# MATE 精读：异步融合前，先对齐时间和动作参考系

## 基本信息与版本变化

原文 *MATE: Asynchronous Multi-Rate Diffusion Policy Composition*，Zihao He、Hongjie Fang、Shirun Tang、Cewu Lu、Hao-Shu Fang。首次提交 2026-07-19 13:48:52 UTC；读取 arXiv:2607.17257v2，更新时间 2026-11-06 04:40:03 UTC；整理及实质修订日期 2026-11-10。属于近期版本更新补读，不是本周首发。已读 v2 正文、方法/实验附录及 v1 对应方法和实验，结果为作者报告，未复现。

[v2 全文](https://arxiv.org/html/2607.17257v2)、[PDF](https://arxiv.org/pdf/2607.17257v2)、[v1](https://arxiv.org/html/2607.17257v1)、[版本历史](https://arxiv.org/abs/2607.17257)、[项目页](https://lag-fusion.github.io/)是原始资源。v1 主要讲 LAG-Fusion 的视觉—力融合；v2 将论述推广到兼容动作空间的多策略，并在 §IV-C 新增全局 3D 与腕部 2D 视觉组合任务及表 II。参考系 rebasing 在 v1 已存在，不能当作 v2 新发明。摘要页仍残留 LAG-Fusion 名称，本笔记按实际读取的 v2 正文使用 MATE。

## 核心问题与方法

慢视觉提供全局目标，快力策略提供接触纠正，但各自在不同机器人姿态和时刻生成相对动作。直接平均会把“旧末端系下的向前”与“当前末端系下的向前”混成错误方向。MATE 的重点不是把两条线程开起来，而是先选择预测时间重叠段、对齐动作参考系，再融合去噪 guidance。

[§III-B、式 4–8](https://arxiv.org/html/2607.17257v2#S3.SS2)以 `T_new←old=T_new⁻¹T_old` 得到仿射映射 `a'=Aa+b`。动作是相对平移、按列堆叠的 6D 旋转、夹爪；A 由旋转块及夹爪恒等块组成，b 只含平移。对 DDPM/DDIM 的三类变量，变换不同：

```
clean action: a' = A a + b
noisy sample: a_k' = A a_k + sqrt(alpha_bar_k) b
predicted noise: epsilon_k' = A epsilon_k
```

不能给预测噪声也加平移。正交 A 保持各向同性高斯协方差；若直接在非等比归一化后的空间操作，需重新推导，不能把米和归一化单位混用。Euler/轴角也不能直接套用按列 6D 的线性变换。

[§III-C](https://arxiv.org/html/2607.17257v2#S3.SS3)把每个可用分支的重叠 guidance 变换到共同 frame，非负权重归一化融合，再映回原全时域填入 DDIM 更新。需要兼容动作和 diffusion 参数化，不是任意黑盒动作策略都可即插即用。附录 VI-C 的视觉权重沿选定 horizon 从 0.8 降到 0.2，是 horizon-index 手工日程，不是已经学出的延迟可靠度。

与你的 RTC 的区别在于，本文研究多条独立策略的去噪组合与坐标一致性，不是动作块前缀约束。与 TD3 残差也不同：这里混合噪声预测，不是将确定性残差加到 ref_chunk。作者明确把 flow-matching 扩展列为未来工作，所以不能直接宣称适用于现有 π0.5 管线。

## 实验、消融和新增证据

[§IV、表 I 与附录 VII](https://arxiv.org/html/2607.17257v2#S4)用 Flexiv Rizon4、FT03S 力矩传感器，每任务 50 条示范、同一预采样初态集每策略 20 次试验。视觉/力策略推理率为 5/25Hz；实际动作采样 50Hz，力输入默认 100Hz，三者不能混称。大部分模型在 RTX 5090，TA-VLA 在远程四张 A100，时延比较存在系统条件差异。

Flip 表 I 得分 MATE 60.0%、同步组合 25.0%、不 rebase 的相对动作组 47.5%；Flip 指标给部分翻转半分，不是严格二元 SR。Polish Curve 为分级擦除 score，MATE 55.00%、同步 25.00%、不 rebase 37.50%，同样不能写成完整任务成功率。绝对动作组表现差还因为 force-only 分支没有 proprio、无法确定全局末端位置，不能据此证明绝对动作表示普遍劣于相对动作。

v2 新增 PnP [§IV-C、表 II](https://arxiv.org/html/2607.17257v2#S4.SS3)以 2Hz 全局点云策略和 5Hz 腕部 RGB 策略处理高箱遮挡，MATE Reach/Pick/Place 为 100/90/85%，同步组合为 90/80/75%；每方法 20 次意味着 Place 只多两次成功，小样本不支持稳健普适结论。频率消融固定视觉、改变力推理率，支持快反馈有用，但平均约 40ms 推理不等于满足端到端 P99 截止期。

附录 VII-B 独立 force 实验从接触前姿态开始，五种对象、每频率配置每对象十次；不能将该阶段的高成功率当完整 Flip 性能。视觉指导与接触反馈失衡、遮挡和低频反应仍会失败。对动态场景、噪声力传感和更复杂手部的泛化未充分验证。

## 开源状态与精读路线

截至整理日项目页明确标注 code coming soon，本次未核验到官方训练代码或 checkpoint 可下载，不标完整开源。优先读式 8 的噪声变换、§III-C 的 temporal selection、表 I 的 no-rebase 对照、附录 VI-C 的权重日程，以及 v2 新增 §IV-C。未来实现开放后，先查时间戳、归一化、6D 按列约定、缓存更新及重叠耗尽回退。

## X5 与 Hi-Nav 迁移实验

以下为分析建议。先不增加力策略，在 X5 离线日志构造两次 query 姿态，用已知刚体变换验证 clean/noisy/noise 的往返误差，固定同噪声检查去噪坐标等价性。保持 H=30、D=5–6、blend=4 及现有 `z_rl+proprio+ref_chunk`、C=10，不把已有参考输入当作创新。当前 flow 模型只能先借鉴 clean-action 时间/坐标审计；要融合 flow velocity，需独立推导其插值及场变换并测试，不能复制 DDPM 式 8。

若后续有可靠力传感和兼容 diffusion 分支，再做等数据、等 GPU 预算的同步组合、异步不对齐、仅时间对齐、时间+参考系对齐四组。固定注入时延分布，记录 SR、接触力峰值、过冲、P99 数据年龄及耗尽率；无力传感时不拿 proprio 伪装成真实接触力。限速限力、软物体任务与人工急停先行。

Hi-Nav 更直接的启发是让旧语义航点携带地图 frame、query pose 和时间戳；定位跳变时失效，而不是仅按消息到达顺序更新。这是工程分析建议，不是 MATE 已验证 VLN-CE。面试可问：为什么 clean/noisy/noise 要用三种变换？时间对齐为何不能代替坐标对齐？平均 25Hz 与可靠 25Hz 有何差别？策略兼容性至少需要哪些契约？

2026-11-10 首次入库，记录 v2 新增视觉组合实验、计分与小样本边界，未复现。
