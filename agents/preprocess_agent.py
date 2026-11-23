# -*- coding: utf-8 -*-
# agents/preprocess_agent.py — 预处理 Agent(阶段一 数据接入,职责见 AGENT/preprocess_agent.md)
# 以 function 形式注册供主 Agent 调用;CLI 接线真实,业务逻辑 stub
import json

from qwen_agent.tools.base import BaseTool, register_tool

from agents.tool_runner import run_tool

#============== function 注册 ===============

@register_tool("preprocess_agent")
class PreprocessAgent(BaseTool):
    description = "预处理 Agent:阶段一数据接入。step=peek 数据窥探(01);step=infer_roles 列角色推断(02,需用户确认);step=clean 拼表前清洗(02b,特殊值转nan/日期格式化/派生month,不落artifact);step=join 宽表连接(03)"
    parameters = {
        "type": "object",
        "properties": {
            "step": {"type": "string", "enum": ["peek", "infer_roles", "clean", "join"], "description": "执行步骤"},
            "run_id": {"type": "string", "description": "本次运行 ID,格式 YYYYMMDD_HHMMSS"},
            "config": {"type": "string", "description": "配置文件路径,默认 config/default_config.json"},
        },
        "required": ["step", "run_id"],
    }

    def call(self, params, **kwargs):
        p = json.loads(params) if isinstance(params, str) else params
        step, run_id = p["step"], p["run_id"]
        cfg = p.get("config", "config/default_config.json")
        if step == "peek":
            return run_tool("tools/csv_peek.py", run_id, cfg)
        if step == "infer_roles":
            return self.infer_roles(p)
        if step == "clean":
            return run_tool("tools/data_clean.py", run_id, cfg)
        if step == "join":
            return run_tool("tools/data_join.py", run_id, cfg)
        raise ValueError(f"未知步骤:{step}")

#============== 业务逻辑 stub ===============

    def infer_roles(self, p):
        """1.2 列角色推断(文档 §4.1.2):基于 peek 与字典推断每列角色,
        字典缺失列标「疑似无关列」,呈现推断表,等用户确认后写 config 并落库 02。待实现"""
        raise NotImplementedError("列角色推断待实现")