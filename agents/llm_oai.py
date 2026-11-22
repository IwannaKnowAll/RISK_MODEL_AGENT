# -*- coding: utf-8 -*-
# agents/llm_oai.py — LLM 适配层:修复 qwen-agent 0.0.34 原生工具协议的消息字段 bug
# 框架把工具结果消息的关联字段写成 id,OpenAI 协议要求 tool_call_id,导致第二轮回传 422
# 仅重写消息转换一步,其余行为与官方 TextChatAtOAI 完全一致
from qwen_agent.llm.base import register_llm
from qwen_agent.llm.oai import TextChatAtOAI


@register_llm("oai_toolfix")
class TextChatAtOAIToolFix(TextChatAtOAI):
    """工具结果消息字段修正:id → tool_call_id,并剥离协议外字段"""

    def convert_messages_to_dicts(self, messages):
        msgs = super().convert_messages_to_dicts(messages)  # 官方转换结果
        fixed = []  # 修正后的消息列表
        for m in msgs:
            if m.get("role") == "tool":
                fixed.append({
                    "role": "tool",
                    "content": m.get("content", ""),
                    "tool_call_id": m.get("id", "1"),  # 框架误写为 id,此处改为协议标准字段
                    "name": m.get("name", ""),
                })
            else:
                fixed.append(m)
        return fixed