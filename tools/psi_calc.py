# -*- coding: utf-8 -*-
# tools/psi_calc.py — 2a.3 四类 PSI(项目文档 §4.2a.3)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "06_psi"
TOOL = "tools/psi_calc.py"


def psi_calc(cfg, run_id):
    """等频 psi_bins 箱,分位点以基准群体切分;空值独立 missing 箱;1e-6 平滑。
    四类:psi_train_test_vs_oot、psi_adjacent_month(取 max)、
    psi_vs_first_month(取 max)、psi_vs_last_month(取 max)。
    每指标四类 PSI 值 + 月度明细;kept/reason 由阶段三a 写回。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("psi_calc PSI 计算待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, psi_calc)