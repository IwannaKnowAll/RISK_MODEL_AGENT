# -*- coding: utf-8 -*-
# tools/model_train.py — 4.3 正式建模与评估(项目文档 §4.4.3)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "11_train"
TOOL = "tools/model_train.py"


def model_train(cfg, run_id):
    """用 10b chosen_params 在 train+test 训练,保存 models/{run_id}_model.txt。
    评估:train/test/oot 各自 AUC/KS;oot 等频 eval_bins 箱 bad rate 表;
    模型分数口径 PSI(train+test vs oot)。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("model_train 正式建模待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, model_train)