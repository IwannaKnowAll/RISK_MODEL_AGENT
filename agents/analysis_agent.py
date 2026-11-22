# -*- coding: utf-8 -*-
# agents/analysis_agent.py — 分析 Agent(任意阶段,职责见 AGENT/analysis_agent.md)
# 只读 artifacts/ 与宽表,输出分析建议,不做数值计算;结论落库 {run_id}_NN_analysis.json
import json

from qwen_agent.tools.base import BaseTool, register_tool

#============== function 注册 ===============

@register_tool("analysis_agent")
class AnalysisAgent(BaseTool):
    description = "分析 Agent:任意阶段只读 artifacts/ 与宽表,对中间过程与最终结果输出分析建议,不做数值计算,结论落库 analysis 产物"
    parameters = {
        "type": "object",
        "properties": {
            "step": {"type": "string", "description": "待分析的步骤编号,如 05_iv、11_train"},
            "run_id": {"type": "string", "description": "本次运行 ID,格式 YYYYMMDD_HHMMSS"},
        },
        "required": ["step", "run_id"],
    }

    def call(self, params, **kwargs):
        p = json.loads(params) if isinstance(params, str) else params
        return self.analyze(p)

#============== 业务逻辑 stub ===============

    def analyze(self, p):
        """读取指定步骤 artifact 与宽表,输出分析建议并落库
        {run_id}_NN_analysis.json,供报告汇总引用。待实现"""
        raise NotImplementedError("分析建议待实现")