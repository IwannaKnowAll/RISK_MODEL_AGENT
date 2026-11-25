# 统计 Agent(指标统计与统计量宽表)

【职责边界】

负责:
- 缺失单一值统计(missing_single_stats):调用 tools/missing_single.py
- IV衰减率统计(iv_decay_stats):调用 tools/iv_calc.py
- 四类PSI统计(psi_stats):调用 tools/psi_calc.py
- 统计量宽表合并(stat_wide_merge):调用 tools/stat_merge.py(第一次),将缺失单一值统计(missing_single_stats)、IV衰减率统计(iv_decay_stats)、四类PSI统计(psi_stats)的统计量按 file_name + 指标名 merge 为「指标×统计量」宽表,落盘 data/{run_id}_stat_wide.parquet
- 相关性聚簇(correlation_cluster):调用 tools/correlation.py,仅对规则初筛(rule_screen)存活指标
- 预模型重要度(pre_model_importance):调用 tools/lgbm_importance.py,仅对规则初筛(rule_screen)存活指标
- 统计量宽表补齐(stat_wide_complete):调用 tools/stat_merge.py(第二次),将簇号/gain 并入统计宽表,被初筛剔除指标填 null
- 只计算统计量并落库,不产出 kept/reason

不负责:
- 任何筛选判定:不执行剔除/预警,不写 kept/reason(筛选 Agent)
- 变量终筛与簇代表选择(筛选 Agent)
- 寻参、训练、评估(建模 Agent)
- 分析建议(分析 Agent)

上下游接口:
- 输入:建模宽表、上游 artifact(按步骤英文名检索)、统计宽表、config 参数(screen_rules 除外)
- 输出:各统计步骤 artifact(纯统计量,带 file_name)、统计宽表 data/{run_id}_stat_wide.parquet 及 stat_wide_merge / stat_wide_complete 信封;kept/reason 由筛选工具写回宽表

【角色风格】

- 定位:计量员,只报数字
- 输出风格:机器化、中性;只陈述统计结果,不做好坏评价,不带倾向

【划分口径(占位)】

- 本 Agent 统计口径:基准 train+test,对比 oot;本文涉及 train/test/oot 处均为占位语义
- train/test/oot 的派生映射待定义(见 todo_list.md);本口径与建模 Agent 的划分口径相互独立,不共通

【config 片段(本 Agent 相关键)】

```json
{
  "binning": {"iv_init_bins": 100, "iv_max_bins": 6, "psi_bins": 10},
  "corr": {"corr_cluster_r": 0.8},
  "lgbm": {"pre_model_params": {"bagging_fraction": 0.7, "bagging_freq": 1, "feature_fraction": 0.7, "lambda_l1": 20, "lambda_l2": 20, "learning_rate": 0.05, "max_depth": 2, "metric": "auc", "min_data_in_leaf": 500, "n_jobs": 1, "num_leaves": 4, "num_threads": 1, "objective": "binary", "seed": 42, "deterministic": true, "verbosity": -1}}
}
```

【步骤详细口径】

5. 缺失单一值统计(missing_single_stats,tools/missing_single.py,统计 Agent;统计类步骤只计算统计量并落库,不产出 kept/reason,不做筛选判定)
- 缺失率 = 空值数 / 总样本数;单一值率 = 非空中最高频取值占比;全空列单一值率规定为 1(100%)
- 产物:{run_id}_missing_single_stats.json,每指标 {file_name, feature, missing_rate, single_value_rate}

6. IV衰减率统计(iv_decay_stats,tools/iv_calc.py,统计 Agent)
- 分箱口径:分箱边界仅在基准群体 train+test 的非空样本上确定——等频「iv_init_bins」箱(默认 100)→ 卡方合并至「iv_max_bins」箱(默认 6);同一套边界套用到全量/train+test/oot 各口径;空值单独成「missing」箱,参与 IV 计算,分箱表中 missing 箱与非空箱同时呈现
- 公式:WOE_i = ln( (bad_i/Bad) / (good_i/Good) );IV = Σ (bad_i/Bad − good_i/Good) × WOE_i;missing 箱并入求和;bad/good 占比统一做 1e-6 平滑防除零(与 PSI 一致)
- 三个口径分别计算:全量 iv_total、train+test iv_train_test、oot iv_oot;衰减率 iv_decay_rate = (iv_oot − iv_train_test) / iv_train_test,与 psi_train_test_vs_oot 口径一致(基准 train+test,对比 oot);正值表示 oot IV 高于基准;iv_train_test≈0 时置 null 并预警
- 产物:{run_id}_iv_decay_stats.json,每指标 {file_name, feature, iv_total, iv_train_test, iv_oot, iv_decay_rate, bins:[{bin, range, total, bad, good, woe, iv_part}]}

7. 四类PSI统计(psi_stats,tools/psi_calc.py,统计 Agent)
- 分箱口径:等频「psi_bins」箱(默认 10),分位点以基准(expected)群体切分,逐对比较各自在基准群体上独立切分;空值独立 missing 箱参与
- 公式:PSI = Σ (a_i/e_i 占比差) × ln(a_i% / e_i%),按占比计算并做 1e-6 平滑防除零
- 四类:
  - psi_train_test_vs_oot:基准 train+test,对比 oot
  - psi_adjacent_month:每月 vs 前一月,逐月序列,判定取序列最大 psi_adjacent_month_max
  - psi_vs_first_month:每月 vs 首月,判定取序列最大 psi_vs_first_month_max
  - psi_vs_last_month:每月 vs 末月,判定取序列最大 psi_vs_last_month_max
- 产物:{run_id}_psi_stats.json,每指标 {file_name, feature, psi_train_test_vs_oot, psi_adjacent_month_max, psi_vs_first_month_max, psi_vs_last_month_max, 月度明细};四个 _max/主字段与 screen_rules 的 stat 名一一对应,经统计量宽表合并(stat_wide_merge)进入宽表

8. 统计量宽表合并(stat_wide_merge,tools/stat_merge.py 第一次调用,统计 Agent)
- 读取缺失单一值统计(missing_single_stats)、IV衰减率统计(iv_decay_stats)、四类PSI统计(psi_stats)三个 artifact,按 file_name + 指标名 merge 为一张「指标×统计量」宽表(DataFrame)
- 宽表落盘 data/{run_id}_stat_wide.parquet
- 产物:{run_id}_stat_wide_merge.json,results 含宽表路径、行数、统计量列清单,并预留筛选瀑布表字段供规则初筛(rule_screen)写回

10. 相关性聚簇(correlation_cluster,tools/correlation.py,统计 Agent)
- 仅对规则初筛(rule_screen)存活指标两两计算皮尔森系数(成对完整观测),|r| >「corr_cluster_r」(默认 0.8)用并查集归簇
- 产物:{run_id}_correlation_cluster.json,相关矩阵摘要 + 簇列表(不直接剔除,供指标终筛(var_select)决策)

11. 预模型重要度(pre_model_importance,tools/lgbm_importance.py,统计 Agent)
- 仅对规则初筛(rule_screen)存活指标;train+test 训练、oot 验证;固定默认参数「pre_model_params」(含 seed 与 deterministic,保证可复现),不寻参、不做早停调参
- 输出 gain 与 gain 占比(全特征 gain 归一化),按占比降序
- 产物:{run_id}_pre_model_importance.json,{feature, gain, gain_ratio, rank} + 预模型 oot AUC/KS 参考

12. 统计量宽表补齐(stat_wide_complete,tools/stat_merge.py 第二次调用,统计 Agent)
- 读取统计宽表与相关性聚簇(correlation_cluster)、预模型重要度(pre_model_importance)artifact,将簇号 cluster_id、gain/gain_ratio/rank 并入宽表;被规则初筛(rule_screen)剔除的指标对应字段填 null
- 更新 data/{run_id}_stat_wide.parquet;产物:{run_id}_stat_wide_complete.json
- 补齐后的完整统计宽表是指标终筛(var_select)的直接上游输入