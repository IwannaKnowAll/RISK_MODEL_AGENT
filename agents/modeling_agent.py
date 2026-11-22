# -*- coding: utf-8 -*-
# agents/modeling_agent.py — 建模 Agent(阶段四 建模,职责见 AGENT/modeling_agent.md)
# CLI 接线真实,寻参/训练计算在 tools/ stub
import json

from qwen_agent.tools.base import BaseTool, register_tool

from agents.tool_runner import run_tool

#============== function 注册 ===============

@register_tool("modeling_agent")
class ModelingAgent(BaseTool):
    description = "建模 Agent:阶段四建模。step=bayes_search 贝叶斯寻参(10a);step=choose_params 呈现候选供用户挑选(10b,需用户确认);step=model_train 正式建模与评估(11)"
    parameters = {
        "type": "object",
        "properties": {
            "step": {"type": "string", "enum": ["bayes_search", "choose_params", "model_train"], "description": "执行步骤"},
            "run_id": {"type": "string", "description": "本次运行 ID,格式 YYYYMMDD_HHMMSS"},
            "config": {"type": "string", "description": "配置文件路径,默认 config/default_config.json"},
        },
        "required": ["step", "run_id"],
    }

    def call(self, params, **kwargs):
        p = json.loads(params) if isinstance(params, str) else params
        step, run_id = p["step"], p["run_id"]
        cfg = p.get("config", "config/default_config.json")
        if step == "bayes_search":
            return run_tool("tools/bayes_search.py", run_id, cfg)
        if step == "choose_params":
            return self.choose_params(p)
        if step == "model_train":
            return run_tool("tools/model_train.py", run_id, cfg)
        raise ValueError(f"未知步骤:{step}")

#============== 业务逻辑 stub ===============

    def choose_params(self, p):
        """4.2 挑选超参数(文档 §4.4.2):呈现 top_n_trials 候选的
        「参数组 × oot AUC × oot KS × train-oot gap」对比表,用户指定后落库 10b。待实现"""
        raise NotImplementedError("超参挑选呈现待实现")