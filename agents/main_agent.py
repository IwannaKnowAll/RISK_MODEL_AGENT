# -*- coding: utf-8 -*-
# agents/main_agent.py — 主 Agent(建模调度器,职责见 AGENT/main_agent.md)
# 只调度、不计算;装配为真实实现,重试/决策点/报告逻辑 stub
from pathlib import Path

from qwen_agent.agents import Assistant

import agents  # noqa: F401 触发五个工具 Agent 注册
import agents.llm_oai  # noqa: F401 注册 oai_toolfix(工具结果消息字段修正)

ROOT = Path(__file__).resolve().parents[1]

#============== 状态机步骤表(项目文档第 4 节,13 步) ===============

WORKFLOW = [
    {"no": "01",  "name": "peek",           "agent": "preprocess_agent", "step_arg": "peek",           "decision": False},
    {"no": "02",  "name": "column_roles",   "agent": "preprocess_agent", "step_arg": "infer_roles",    "decision": True},
    {"no": "03",  "name": "join",           "agent": "preprocess_agent", "step_arg": "join",           "decision": False},
    {"no": "04",  "name": "missing_single", "agent": "stats_agent",      "step_arg": "missing_single", "decision": False},
    {"no": "05",  "name": "iv",             "agent": "stats_agent",      "step_arg": "iv",             "decision": False},
    {"no": "06",  "name": "psi",            "agent": "stats_agent",      "step_arg": "psi",            "decision": False},
    {"no": "3a",  "name": "initial_screen", "agent": "screen_agent",     "step_arg": "initial_screen", "decision": False},
    {"no": "07",  "name": "corr",           "agent": "stats_agent",      "step_arg": "corr",           "decision": False},
    {"no": "08",  "name": "importance",     "agent": "stats_agent",      "step_arg": "importance",     "decision": False},
    {"no": "09",  "name": "var_select",     "agent": "screen_agent",     "step_arg": "var_select",     "decision": True},
    {"no": "10a", "name": "search",         "agent": "modeling_agent",   "step_arg": "bayes_search",   "decision": False},
    {"no": "10b", "name": "choose_params",  "agent": "modeling_agent",   "step_arg": "choose_params",  "decision": True},
    {"no": "11",  "name": "train",          "agent": "modeling_agent",   "step_arg": "model_train",    "decision": False},
]

FUNCTION_LIST = ["preprocess_agent", "stats_agent", "screen_agent", "modeling_agent", "analysis_agent"]

#============== 主 Agent 装配 ===============

def build_system_message():
    """system prompt = AGENT.MD + 主 Agent 角色文件 + 状态机步骤表"""
    parts = [
        (ROOT / "AGENT.MD").read_text(encoding="utf-8"),
        (ROOT / "AGENT" / "main_agent.md").read_text(encoding="utf-8"),
        "【状态机步骤表】按序推进,decision=True 为决策点必须等用户确认:",
    ]
    for s in WORKFLOW:
        parts.append(f"- {s['no']} {s['name']} → {s['agent']}(step={s['step_arg']})"
                     + ("【决策点】" if s["decision"] else ""))
    return "\n\n".join(parts)


def build_main_agent(llm_cfg):
    """装配主 Agent:Assistant + 五个工具 Agent function"""
    return Assistant(
        llm=llm_cfg,
        function_list=FUNCTION_LIST,
        system_message=build_system_message(),
        name="建模调度器",
        description="风控建模全流程调度:编排、重试、决策点交互、报告汇总,不做数值计算",
    )

#============== 调度逻辑 stub ===============

def retry_tool(step, run_id, max_retries):
    """失败重试(AGENT.MD 1.4):异常退出(非 0 且非 2/3/4)重试至多 max_retries 次;
    业务失败/依赖缺失/数据校验失败不重试,停止等用户。待实现"""
    raise NotImplementedError("失败重试逻辑待实现")


def ask_user_decision(step, run_id):
    """决策点交互:流程启动前、列角色推断后、指标终筛后、超参解读后;
    呈现内容并等用户确认,确认结果落库。待实现"""
    raise NotImplementedError("决策点交互逻辑待实现")


def summarize_report(run_id):
    """报告汇总:汇总各步骤产物与分析 Agent 结论,产出最终报告。待实现"""
    raise NotImplementedError("报告汇总待实现")