# -*- coding: utf-8 -*-
# agents/screen_agent.py — 筛选 Agent(阶段三a/三b 指标筛选,职责见 AGENT/screen_agent.md)
# 判定一律解析 config screen_rules,禁止写死阈值
import json

from qwen_agent.tools.base import BaseTool, register_tool

from agents.tool_runner import run_tool

#============== function 注册 ===============

@register_tool("screen_agent")
class ScreenAgent(BaseTool):
    description = "筛选 Agent:阶段三a/三b 指标筛选。step=initial_screen 初筛判定(3a,无新增产物,kept/reason 写回 04/05/06);step=var_select 指标终筛(09,需用户确认)"
    parameters = {
        "type": "object",
        "properties": {
            "step": {"type": "string", "enum": ["initial_screen", "var_select"], "description": "执行步骤"},
            "run_id": {"type": "string", "description": "本次运行 ID,格式 YYYYMMDD_HHMMSS"},
            "config": {"type": "string", "description": "配置文件路径,默认 config/default_config.json"},
        },
        "required": ["step", "run_id"],
    }

    def call(self, params, **kwargs):
        p = json.loads(params) if isinstance(params, str) else params
        step, run_id = p["step"], p["run_id"]
        cfg = p.get("config", "config/default_config.json")
        if step == "initial_screen":
            return self.initial_screen(p)
        if step == "var_select":
            return run_tool("tools/var_select.py", run_id, cfg)
        raise ValueError(f"未知步骤:{step}")

#============== 业务逻辑 stub ===============

    def initial_screen(self, p):
        """3a.1 初筛判定(文档 §4.3a.1):按 config screen_rules 对产物 04/05/06
        执行剔除/预警判定,kept/reason 写回对应产物,不新增 artifact。待实现"""
        raise NotImplementedError("初筛判定待实现")