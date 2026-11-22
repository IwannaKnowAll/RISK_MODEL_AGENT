# -*- coding: utf-8 -*-
# tools/lgbm_importance.py — 2b.2 LGBM 预建模重要度(项目文档 §4.2b.2)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "08_importance"
TOOL = "tools/lgbm_importance.py"


def lgbm_importance(cfg, run_id):
    """train+test 训练、oot 验证;固定 pre_model_params,不寻参、不早停调参。
    输出 {feature, gain, gain_ratio, rank} 按占比降序 + 预模型 oot AUC/KS 参考。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("lgbm_importance 重要度计算待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, lgbm_importance)