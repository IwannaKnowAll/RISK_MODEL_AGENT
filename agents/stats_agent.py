# -*- coding: utf-8 -*-
# agents/stats_agent.py — 统计 Agent(阶段二a/二b 指标统计,职责见 AGENT/stats_agent.md)
# 只计算统计量并落库,不做筛选判定;CLI 接线真实,工具计算在 tools/ stub
import json

from qwen_agent.tools.base import BaseTool, register_tool

from agents.tool_runner import run_tool

#============== 步骤与脚本映射 ===============

SCRIPTS = {
    "missing_single": "tools/missing_single.py",   # 2a.1 产物 04
    "iv": "tools/iv_calc.py",                      # 2a.2 产物 05
    "psi": "tools/psi_calc.py",                    # 2a.3 产物 06
    "corr": "tools/correlation.py",                # 2b.1 产物 07
    "importance": "tools/lgbm_importance.py",      # 2b.2 产物 08
}

#============== function 注册 ===============

@register_tool("stats_agent")
class StatsAgent(BaseTool):
    description = "统计 Agent:阶段二a/二b 指标统计,只计算不判定。step=missing_single(04)/iv(05)/psi(06)/corr(07)/importance(08)"
    parameters = {
        "type": "object",
        "properties": {
            "step": {"type": "string", "enum": list(SCRIPTS), "description": "执行步骤"},
            "run_id": {"type": "string", "description": "本次运行 ID,格式 YYYYMMDD_HHMMSS"},
            "config": {"type": "string", "description": "配置文件路径,默认 config/default_config.json"},
        },
        "required": ["step", "run_id"],
    }

    def call(self, params, **kwargs):
        p = json.loads(params) if isinstance(params, str) else params
        return run_tool(SCRIPTS[p["step"]], p["run_id"], p.get("config", "config/default_config.json"))