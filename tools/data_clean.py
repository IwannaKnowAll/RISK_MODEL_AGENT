# -*- coding: utf-8 -*-
# tools/data_clean.py — 1.2b 拼表前清洗(项目文档 §4.1.2b)
# 状态:框架 stub,计算逻辑待实现
# 三项职能:clean_rules 特殊值转 np.nan(列名子串匹配,规则可扩展)、
#          date_cols 日期列转 %Y%m%d、month_from 派生 month 列(%Y%m)
# 本步不落 artifact:清洗结果写 cache/{run_id}_x_clean.parquet 与 _y_clean.parquet,供 03 join 读取
from common.artifact import cli_main

STEP = "02b_clean"
TOOL = "tools/data_clean.py"


def clean(cfg, run_id):
    """对 data_X 与 data_Y 执行拼表前清洗:
    1. 按 clean_rules(col_pattern 子串匹配列名 + values 值列表)将特殊值转 np.nan
    2. date_cols 指定日期列统一转 %Y%m%d(如 2024-10-31 → 20241031)
    3. 由 month_from 日期列派生 month 列(%Y%m,如 20241031 → 202410),写入 month_col
    清洗后文件写 cache/,不写 artifacts;返回 (results, summary)。待实现"""
    raise NotImplementedError("data_clean 拼表前清洗待实现")


if __name__ == "__main__":
    cli_main(STEP, TOOL, clean)