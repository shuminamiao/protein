# 扰动预测闭环示范（GEARS/scGen → DLD-1类器官qPCR）

本仓库提供一个**最小可复现**闭环：
1. 用公开单细胞CRISPRi扰动数据训练/微调 GEARS 或 scGen。
2. 在严格基线（ATE/均值/线性）和“未见基因+外部数据”评测下，输出候选基因抑制的方向性预测。
3. 将模型输出映射到 1–2 条 DLD-1 类器官 qPCR 验证面板，完成小规模湿实验闭环。

> 目标：证明平台具备“可预测、可验证、可复用”的能力，而不是追求大规模 Perturb-seq。

## 目录结构

- `configs/experiment.yaml`：实验参数、数据路径、模型与评测开关。
- `scripts/run_pipeline.py`：统一入口（可先 dry-run，再逐步替换为真实训练）。
- `scripts/baselines.py`：ATE/均值/线性基线定义（审稿关键对照）。
- `scripts/qpcr_panel_mapper.py`：将模型输出映射为 qPCR 候选基因面板。
- `data/metadata/qpcr_panel_template.csv`：qPCR 模板（基因、引物、方向预测、通路标签）。
- `notebooks/01_closed_loop_demo.ipynb`：最小演示 notebook（占位，可按实际补充）。
- `environment.yml`：可复现实验环境。

## 核心实验设计（建议按此执行）

### 1) 数据策略

- **训练数据（高优先级）**：Virtual Cell Challenge 相关 CRISPRi 单细胞数据。
- **内部验证**：hold-out genes（训练时完全未见的目标基因）。
- **外部验证**：不同来源公开扰动数据（建议复现 GEARS 论文中常用 Perturb-seq 设置之一）。

### 2) 模型与基线

- 深度模型：`GEARS`、`scGen`（至少二选一，最好都跑）。
- 强制基线：
  - ATE baseline（平均处理效应）
  - Mean baseline（条件均值）
  - Linear baseline（如岭回归/弹性网）

> 论文叙事重点：在你任务定义下，深度模型是否**显著优于**基线；若不显著，也要诚实报告并解释适用边界。

### 3) 指标

建议最低报告：
- 基因表达层面：Pearson/Spearman、MSE。
- 方向性指标：对预先定义 marker 集的上/下调方向准确率。
- 通路层面：基于基因集打分的方向一致性（如 Hallmark / KEGG）。

### 4) 湿实验闭环（DLD-1类器官）

- 选择 1–2 条模型高置信候选扰动（CRISPRi 或 siRNA）。
- 每条候选输出 6–12 个 qPCR marker（含阳性、阴性、housekeeping）。
- 预注册“通过阈值”：例如 marker 方向一致率 ≥ 70%。

## 快速开始

```bash
conda env create -f environment.yml
conda activate perturb-loop
python scripts/run_pipeline.py --config configs/experiment.yaml --dry-run
```

## 可重复性要求（务必执行）

- 固定随机种子（数据划分、训练初始化、采样过程）。
- 记录软件版本、CUDA、GPU 型号。
- 输出统一落盘到 `results/`，并保留 `run_metadata.json`。
- notebook 与脚本同源：关键结果可由 CLI 一键重算。

## 后续可发表最小结果包（MVP）

1. 任务定义 + 数据划分图（含 hold-out genes）。
2. GEARS/scGen vs ATE/均值/线性 的主表格。
3. 外部数据集泛化结果。
4. DLD-1 类器官 qPCR 方向验证（1–2条候选）。
5. 失败案例分析（最能打动审稿人的部分）。
