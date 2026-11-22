# -*- coding: utf-8 -*-
# tools/var_select.py — 3b.1 指标终筛(项目文档 §4.3b.1)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "09_var_select"
TOOL = "tools/var_select.py"


def var_select(cfg, run_id):
    """综合 IV、衰减率、PSI、重要度、簇内代表(默认簇内保留 IV 最高者,config 可覆盖)。
    输出保留/剔除全清单与逐条理由;用户确认后写回 config 覆盖项,user_confirmed=true。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("var_select 指标终筛待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, var_select)