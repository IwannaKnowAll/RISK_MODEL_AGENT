# -*- coding: utf-8 -*-
# tools/missing_single.py — 2a.1 缺失率 / 单一值率(项目文档 §4.2a.1)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "04_missing_single"
TOOL = "tools/missing_single.py"


def missing_single(cfg, run_id):
    """缺失率=空值数/总样本数;单一值率=非空中最高频取值占比。
    每指标 {missing_rate, single_value_rate, kept, reason};kept/reason 由阶段三a 写回。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("missing_single 缺失率/单一值率待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, missing_single)