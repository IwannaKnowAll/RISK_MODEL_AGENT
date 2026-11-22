# -*- coding: utf-8 -*-
# tools/common/io_utils.py — 数据加载、split/月份校验、run_id 管理(项目文档 §2.3)
# 状态:框架 stub,全部待实现
from datetime import datetime

#============== run_id 管理 ===============

def new_run_id():
    """生成 run_id,格式 YYYYMMDD_HHMMSS(协议 4.4)"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

#============== 数据加载 ===============

def load_table(path):
    """按扩展名加载 CSV/Parquet 为 DataFrame。待实现"""
    raise NotImplementedError("load_table 数据加载待实现")


def load_wide_table(run_id):
    """加载建模宽表 data/{run_id}_joined.parquet(文档 §3.4)。待实现"""
    raise NotImplementedError("load_wide_table 宽表加载待实现")

#============== 数据校验 ===============

def validate_split(df, split_col):
    """校验划分列取值:train/test/oot/年月(文档 §3.3)。待实现"""
    raise NotImplementedError("validate_split 划分列校验待实现")


def validate_month(df, month_col):
    """校验月份列格式 YYYY-MM(文档 §3.3)。待实现"""
    raise NotImplementedError("validate_month 月份列校验待实现")


def validate_target(df, target_col):
    """校验标签取值 0/1,违规抛数据校验失败(文档 §3.5,退出码 4)。待实现"""
    raise NotImplementedError("validate_target 标签校验待实现")