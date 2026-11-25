# -*- coding: utf-8 -*-
# agents/tool_runner.py — 工具 CLI 调用协议(AGENTS.md 第 3 节)
# 协议接线为真实实现:subprocess 调 CLI → 解析 stdout 单行 JSON → 附退出码返回
import json
import subprocess
import sys

#============== CLI 调用 ===============

def run_tool(script, run_id, config="config/default_config.json"):
    """执行「python tools/<tool>.py --config ... --run-id ...」,返回单行 JSON 字符串。
    退出码语义:0=成功、2=业务失败、3=工具或依赖缺失、4=数据校验失败(协议 3.4)"""
    proc = subprocess.run(
        [sys.executable, script, "--config", config, "--run-id", run_id],
        capture_output=True, text=True,
    )
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    status = json.loads(line)
    status["exit_code"] = proc.returncode
    return json.dumps(status, ensure_ascii=False)