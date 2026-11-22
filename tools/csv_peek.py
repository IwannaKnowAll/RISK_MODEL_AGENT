# -*- coding: utf-8 -*-
# tools/csv_peek.py — 1.1 数据窥探(项目文档 §4.1.1)
# 状态:框架 stub,计算逻辑待实现
from common.artifact import cli_main

STEP = "01_peek"
TOOL = "tools/csv_peek.py"


def peek(cfg, run_id):
    """读取全部输入文件(字典、data_X、data_Y)前 peek_rows 行 + 完整列名。
    返回 (results, summary)。待实现"""
    raise NotImplementedError("csv_peek 数据窥探待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, peek)