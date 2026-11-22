# -*- coding: utf-8 -*-
# main.py — 风控建模 AGENT 入口
# 用法:python main.py --check  框架装配自检(不调 LLM)
#       python main.py          交互模式(需环境变量 DEEPSEEK_API_KEY)
import argparse
import os
import sys
from pathlib import Path

from qwen_agent.tools.base import TOOL_REGISTRY

from agents.main_agent import build_main_agent, FUNCTION_LIST, WORKFLOW
from tools.common.io_utils import new_run_id

# ============== LLM 配置 ===============

LLM_config = {  # LLM 连接配置:模型名/服务地址/API Key,供主 Agent 装配使用
    "model": "deepseek-flash",                           # 模型名,如 qwen-max
    "model_server": "https://api.deepseek.com",          # 兼容 OpenAI 协议的服务地址
    "api_key": os.environ.get("DEEPSEEK_API_KEY", ""),   # API Key,读 Mac 环境变量,禁止明文写入代码
    "generate_cfg": {"use_raw_api": True},               # 走 OpenAI 原生 tools 协议,避免 DeepSeek DSML 文本模板不被识别
}

#============== 框架自检 ===============

def check():
    """验证:五个工具 Agent 已注册、10 个工具脚本存在、状态机 13 步完整"""
    missing = [n for n in FUNCTION_LIST if n not in TOOL_REGISTRY]  # 应注册但未注册的工具 Agent 名单
    assert not missing, f"未注册的工具 Agent:{missing}"
    scripts = [  # 应存在的 10 个工具脚本路径清单
        "tools/csv_peek.py", "tools/data_join.py", "tools/missing_single.py",
        "tools/iv_calc.py", "tools/psi_calc.py", "tools/correlation.py",
        "tools/lgbm_importance.py", "tools/var_select.py",
        "tools/bayes_search.py", "tools/model_train.py",
    ]
    absent = [s for s in scripts if not Path(s).exists()]  # 实际缺失的工具脚本名单
    assert not absent, f"缺失工具脚本:{absent}"
    assert len(WORKFLOW) == 13, "状态机应为 13 步"
    print(f"框架自检通过:工具 Agent {len(FUNCTION_LIST)} 个已注册,工具脚本 {len(scripts)} 个就位,状态机 {len(WORKFLOW)} 步")
    print("决策点:" + ", ".join(s["no"] + " " + s["name"] for s in WORKFLOW if s["decision"]))

#============== 交互模式 ===============

def chat():
    """交互主循环:生成 run_id 告知用户,逐轮对话驱动状态机"""
    assert LLM_config["model"] and LLM_config["api_key"], "请先设置环境变量 DEEPSEEK_API_KEY(已写入 ~/.zshrc,重开终端生效)"
    bot = build_main_agent(LLM_config)  # 主 Agent 实例(建模调度器)
    run_id = new_run_id()  # 本次全流程唯一 ID,artifacts 落库按它归组
    print(f"本次运行 run_id:{run_id}")
    messages = []  # 对话历史,逐轮累积用户与 AGENT 消息
    while True:
        query = input("\n用户> ").strip()  # 本轮用户输入
        if query in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": f"[run_id={run_id}] {query}"})
        response = []  # 本轮 AGENT 返回的消息列表(含工具调用中间步骤)
        for response in bot.run(messages):
            pass
        messages.extend(response)
        print("\nAGENT>", response[-1]["content"])

#============== 入口 ===============

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # 命令行参数解析器
    parser.add_argument("--check", action="store_true", help="框架装配自检,不调 LLM")
    args = parser.parse_args()  # 解析后的命令行参数
    if args.check:
        check()
        sys.exit(0)
    chat()