# -*- coding: utf-8 -*-
# tools/iv_calc.py — 2a.2 IV 与衰减率(项目文档 §4.2a.2)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "05_iv"
TOOL = "tools/iv_calc.py"


def iv_calc(cfg, run_id):
    """分箱:非空等频 iv_init_bins 箱 → 卡方合并至 iv_max_bins 箱;空值单独 missing 箱参与 IV。
    三口径:iv_total、iv_train_test、iv_oot;iv_decay_rate=(iv_total−iv_oot)/iv_total,
    iv_total≈0 时置 null 并预警。每指标含 bins 明细;kept/reason 由阶段三a 写回。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("iv_calc IV 计算待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, iv_calc)