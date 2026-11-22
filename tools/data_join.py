# -*- coding: utf-8 -*-
# tools/data_join.py — 1.3 宽表连接(项目文档 §4.1.3、§3.4/3.5)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "03_join"
TOOL = "tools/data_join.py"


def join(cfg, run_id):
    """按 config 关联键连接 data_X 与 data_Y,产出 data/{run_id}_joined.parquet。
    含数据体检:行数、匹配率、target 分布、各 split 样本量、各月样本量、坏率。
    关联键缺失/匹配率异常/重复匹配 → invalid_data(退出码 4)。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("data_join 宽表连接待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, join)