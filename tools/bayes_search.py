# -*- coding: utf-8 -*-
# tools/bayes_search.py — 4.1 Optuna 贝叶斯寻参(项目文档 §4.4.1)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "10a_search"
TOOL = "tools/bayes_search.py"


def bayes_search(cfg, run_id):
    """Optuna TPE,固定 sampler seed;n_trials 次;搜索空间取 search.search_space。
    目标函数取 search.objective;|train_auc−oot_auc|>auc_gap_max 判过拟合并惩罚。
    数据 train+test 训练 / oot 评估;特征=09 selected。
    输出 best_params、top_n_trials 候选、study 摘要。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("bayes_search 贝叶斯寻参待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, bayes_search)