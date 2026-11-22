# -*- coding: utf-8 -*-
# tools/correlation.py — 2b.1 皮尔森相关(项目文档 §4.2b.1)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "07_corr"
TOOL = "tools/correlation.py"


def correlation(cfg, run_id):
    """初筛存活指标两两皮尔森(成对完整观测);|r|>corr_cluster_r 并查集归簇。
    输出相关矩阵摘要 + 簇列表,不直接剔除,供 3b.1 决策。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("correlation 相关计算待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, correlation)