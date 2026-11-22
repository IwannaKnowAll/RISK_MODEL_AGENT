# -*- coding: utf-8 -*-
# main.py — 风控建模 AGENT 入口
# 用法:python main.py --check  框架装配自检(不调 LLM)
#       python main.py          交互模式(需先填写 LLM_CFG)
import argparse
import sys
from pathlib import Path

from qwen_agent.tools.base import TOOL_REGISTRY

from agents.main_agent import build_main_agent, FUNCTION_LIST, WORKFLOW
from tools.common.io_utils import new_run_id

#============== LLM 配置(占位,待用户填写) ===============

LLM_CFG = {
    "model": "",          # 模型名,如 qwen-max
    "model_server": "",   # 兼容 OpenAI 协议的服务地址
    "api_key": "",        # API Key
}

#============== 框架自检 ===============

def check():
    """验证:五个工具 Agent 已注册、10 个工具脚本存在、状态机 13 步完整"""
    missing = [n for n in FUNCTION_LIST if n not in TOOL_REGISTRY]
    assert not missing, f"未注册的工具 Agent:{missing}"
    scripts = [
        "tools/csv_peek.py", "tools/data_join.py", "tools/missing_single.py",
        "tools/iv_calc.py", "tools/psi_calc.py", "tools/correlation.py",
        "tools/lgbm_importance.py", "tools/var_select.py",
        "tools/bayes_search.py", "tools/model_train.py",
    ]
    absent = [s for s in scripts if not Path(s).exists()]
    assert not absent, f"缺失工具脚本:{absent}"
    assert len(WORKFLOW) == 13, "状态机应为 13 步"
    print(f"框架自检通过:工具 Agent {len(FUNCTION_LIST)} 个已注册,工具脚本 {len(scripts)} 个就位,状态机 {len(WORKFLOW)} 步")
    print("决策点:" + ", ".join(s["no"] + " " + s["name"] for s in WORKFLOW if s["decision"]))

#============== 交互模式 ===============

def chat():
    """交互主循环:生成 run_id 告知用户,逐轮对话驱动状态机"""
    assert LLM_CFG["model"] and LLM_CFG["api_key"], "请先在 main.py 填写 LLM_CFG(model/model_server/api_key)"
    bot = build_main_agent(LLM_CFG)
    run_id = new_run_id()
    print(f"本次运行 run_id:{run_id}")
    messages = []
    while True:
        query = input("\n用户> ").strip()
        if query in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": f"[run_id={run_id}] {query}"})
        response = []
        for response in bot.run(messages):
            pass
        messages.extend(response)
        print("\nAGENT>", response[-1]["content"])

#============== 入口 ===============

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="框架装配自检,不调 LLM")
    args = parser.parse_args()
    if args.check:
        check()
        sys.exit(0)
    chat()