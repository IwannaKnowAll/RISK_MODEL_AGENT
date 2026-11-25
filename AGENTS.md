# AGENTS.md — 风控建模 AGENT 指令文件

【文件定位】

本项目基于 Qwen-Agent 构建。本文件为风控建模 AGENT 项目的项目级约束,约束所有 Agent、工具与产物协议;各 Agent 角色定位与职责边界见 AGENT/ 目录。

【设计原则】

- 编排、计算、分析分离:主 Agent 只做流程性事务;数值计算由子 Agent 调用 tools/ 执行;数据分析与最终报告由分析 Agent 负责
- 计算与编排分离:模型不参与计算,不造轮子;缺工具即提示用户
- 全程可追溯:每一步产物落库,任意步骤可独立重跑、可审计
- Human in the loop:决策点情形以主 Agent 职责文档与 WORKFLOW 标注为准,必须向用户确认;决策点交互位置待统一规定(见 todo_list.md)
- 版本安全:迭代前检查 + 高危重构备份;main 历史一个迭代一条提交,里程碑打 tag

1. 执行架构(Qwen-Agent)

- 1.1 主 Agent(建模调度器)为 Assistant;五个工具 Agent 为 FunctionAgent,以 function 形式注册供主 Agent 调用
- 1.2 工具 Agent 分工:见项目文档「工具 Agent 分工」

- 各 Agent 的职责边界与角色风格详见 AGENT/ 目录
- 1.3 调用链:主 Agent → 工具 Agent → 「python tools/<tool>.py」,数值计算只发生在 tools/ 脚本内;主 Agent 职责边界见 AGENT/main_agent.md「职责边界」
- 1.4 失败重试:见 AGENT/main_agent.md「职责边界」

2. 命名事实源(步骤与产物唯一标识,不可违反)

- 2.1 每个步骤/产物有专属中文名 + 英文名,全流程唯一,注册表见下表;流程顺序事实源为项目文档「WORKFLOW」,全流程 = 执行 WORKFLOW 中的所有步骤
- 2.2 代码、文件名、信封 step 字段、上游依赖检索一律用英文名;回答用户 query 时用「中文名(英文名)」
- 2.3 artifact 命名「{run_id}_<英文名>.json」,禁止编号;步骤指代用名称检索,禁止「NN/第N步/编号最大」类表述
- 2.4 分析文件「{run_id}_analysis_<步骤英文名>.json」,不入 WORKFLOW、不作任何步骤的上游依赖

  | 中文名 | 英文名 | 执行 Agent | 产物形态 |
  |---|---|---|---|
  | 数据窥探 | data_peek | 预处理 | artifact |
  | 列角色推断 | column_role_infer | 预处理(用户确认) | artifact |
  | 拼表前清洗 | pre_join_clean | 预处理 | 不产 artifact,cache/{run_id}_x_clean.parquet、_y_clean.parquet,摘要随宽表连接落库 |
  | 宽表连接 | data_join | 预处理 | artifact + data/{run_id}_joined.parquet |
  | 缺失单一值统计 | missing_single_stats | 统计 | artifact |
  | IV衰减率统计 | iv_decay_stats | 统计 | artifact |
  | PSI统计 | psi_stats | 统计 | artifact |
  | 统计量宽表合并 | stat_wide_merge | 统计 | artifact + data/{run_id}_stat_wide.parquet |
  | 规则初筛 | rule_screen | 筛选 | 不新增 artifact:kept/reason 写回宽表 parquet,瀑布表写入 stat_wide_merge 信封 |
  | 相关性聚簇 | correlation_cluster | 统计 | artifact(仅初筛存活指标) |
  | 预模型重要度 | pre_model_importance | 统计 | artifact(仅初筛存活指标) |
  | 统计量宽表补齐 | stat_wide_complete | 统计 | artifact:簇号/gain 并入宽表,被初筛剔除指标填 null |
  | 指标终筛 | var_select | 筛选(用户确认) | artifact |
  | 贝叶斯寻参 | bayes_search | 建模 | artifact |
  | 超参挑选 | hyperparam_choose | 建模(用户确认) | artifact |
  | 正式建模评估 | model_train_eval | 建模 | artifact |
  | 模型保存 | model_save | 建模 | artifact + models/{run_id}_model.txt |
  | 最终报告 | final_report | 分析 | artifact(占位:schema 细节待定义,见 todo_list.md) |

3. 绝对不可违反的规则

- 3.1 所有涉及数学计算的工作流，只有通过调用tools/下的函数产生的结果才是合法的，禁止模型通过推理产生结论
- 3.2 禁止模型在计算过程中自行构建轮子。缺工具或缺依赖时,停止并提示用户,不得现场编写替代计算代码
- 3.3 事实源中要求落库的中间过程必须以 JSON 格式持久化落库到 artifacts/
- 3.4 代码迭代前必须通过迭代前检查;高危重构前必须完成 Git 备份(见「Git 版本管理规则」),检查或备份失败不得改码
- 3.5 阈值、筛选规则、列名、分箱参数一律从 config/default_config.json 读取,不得硬编码
- 3.6 每一步完成后先落库、再解读、再进入下一步
- 3.7 所有测试工作必须在沙箱中进行,不得直接在主分支上操作
4. 工具调用协议

- 4.1 统一 CLI 形式:「python tools/<tool>.py --config config/default_config.json --run-id <run_id>」
- 4.2 工具按上游步骤英文名检索已存在 artifact 作为输入依赖,执行次序由项目文档 WORKFLOW 定义;自行写出本步 artifact;宽表连接(data_join)例外,读拼表前清洗(pre_join_clean)后的 cache 文件
- 4.3 工具 stdout 只打印一行 JSON 状态(含 out 路径与 summary),AGENT 解析该行判断成败
- 4.4 退出码:「0=成功」「2=业务失败(已落库)」「3=工具或依赖缺失」「4=数据规范校验失败」

5. 产物落库协议

- 5.1 所有产物平铺在 artifacts/ 下,命名「{run_id}_<步骤英文名>.json」(英文名以「命名事实源」注册表为准),同一 run_id 归为一组
- 5.2 统一信封字段:run_id、step(步骤英文名)、tool、timestamp、params、status、results、summary

```json
{
  "run_id": "20261122_143000",
  "step": "iv_decay_stats",
  "tool": "tools/iv_calc.py",
  "timestamp": "2026-11-22T14:31:02+08:00",
  "params": {"iv_init_bins": 100, "iv_max_bins": 6},
  "status": "success",
  "results": {},
  "summary": {"input_features": 320}
}
```

- step 字段一律用步骤英文名;params 只记录函数入参
- 5.3 status 取值:success / error / tool_missing / invalid_data;非 success 也必须完整落库并含 error 详情:error / tool_missing / invalid_data 时 results 置空、必含 error:{code, message, hint},hint 给出用户可执行的下一步(如安装命令)
- 5.4 run_id 格式「YYYYMMDD_HHMMSS」,每次全流程开始时生成并告知用户

6. 缺工具处理协议

- 6.1 每步执行前检查:工具脚本文件存在 + 依赖 import 可成功(python -c 检查)
- 6.2 任一缺失:落库 status=「tool_missing」,停止流程,向用户输出:缺失项名称、所属步骤、安装命令(如「pip install optuna」)、待用户处理后再继续
- 6.3 严禁现场编写计算逻辑替代缺失工具

7. Git 版本管理规则

- 7.1 初始化(一次性):git init → 用户创建远程仓库并提供地址 → 写入 AGENTS.md 末尾 → git remote add origin <url> → 首次全量 push
- 7.2 分支策略:每个工具/迭代在 feature/<名称> 分支开发,小步提交不限次数,提交信息用 Conventional Commits(feat/fix/docs/refactor/test);测试通过后 squash merge 进 main,一个迭代一条提交
- 7.3 迭代前检查:开始改码前确认工作区干净且已推送(git status);有未提交改动先提交推送再开工
- 7.4 高危备份:高危重构(改分箱算法、指标公式、调用/落库协议等)前,必须依次执行并全部成功:
  - git add -A
  - git commit -m "backup: v{N.n} <本次重构前状态说明>"
  - git tag V{N.n}
  - git push origin main --tags
- 7.5 push 失败:禁止修改任何代码,先解决推送问题
- 7.6 里程碑 tag:可用里程碑打语义化版本(v0.1 框架、v0.2 数据接入可用…),回滚与追溯看 tag
- 7.7 仅文档类修改(不改 tools/、config/、agents/)豁免高危备份,直接 docs 提交
- 7.8 .gitignore:data/、artifacts/、cache/、models/、__pycache__/、*.log、.pytest_cache/、.DS_Store、workspace/

8. 测试方案

- 8.1 分层:
  - L1 工具单元测试(pytest + 金样本):tests/fixtures 存手工核算的小样本与期望值,断言工具输出与金样本一致,容差「1e-6」
    - 金样本示例:20 行 × 2 特征 × 3 非空箱 + 1 missing 箱,WOE/IV 用 Excel 按公式手算;PSI 用两群体 10 箱占比手算
    - 交叉基准:IV/PSI 结果与 toad 库对照;皮尔森与 scipy.stats.pearsonr 对照;AUC/KS 与 sklearn.roc_auc_score 对照
    - 分箱专项:等频边界正确性、卡方合并后箱数 ≤ iv_max_bins、missing 箱不参与合并且始终呈现、常量列/全空列退化处理
    - 边界用例:全缺失列、单一值列、单月数据、oot 为空集、标签全 0
  - L2 流程集成测试:1000 行合成数据(固定 seed,含 6 个月份,按 split_col 切分点可划出 base_data/test_data)端到端执行 WORKFLOW 中的所有步骤,断言应产出的 artifact 全部生成(以命名注册表为准)、信封 schema 合法、上下游特征数单调不增
  - L3 复现性测试:同 run 配置重跑两次,测试场景固定 sampler_seed 与超参数,贝叶斯寻参(bayes_search)best_params 一致;正式建模评估(model_train_eval)输出模型预测逐位一致
- 8.2 数据红线:测试只用合成/脱敏数据,tests/fixtures 纳入 git,真实业务数据禁止入库(.gitignore 排除 data/)。
- 8.3 运行约定:「pytest tests/ -q」为迭代改码后的最低门禁;L1 未过不得进入 L2。

9. 依赖环境

- 9.1 requirements.txt:pandas、numpy、scipy、scikit-learn、lightgbm、optuna、pyarrow、pytest、qwen-agent;测试对照依赖 toad(仅 dev)。
- 9.2 环境检查:每步执行前 AGENT 以「python -c "import <pkg>"」探测,缺失即按本文件「缺工具处理协议」走 tool_missing 提示,不自行安装、不自行实现替代计算。

---
远程仓库地址:「https://github.com/IwannaKnowAll/RISK_MODEL_AGENT.git」
