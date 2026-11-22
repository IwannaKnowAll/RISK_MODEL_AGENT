# -*- coding: utf-8 -*-
# tools/common/binning.py — 等频分箱、卡方合并、missing 箱处理(项目文档 §4.2)
# 状态:框架 stub,全部待实现

#============== 等频分箱 ===============

def equal_freq_bins(x, n_bins):
    """仅非空样本等频分箱,返回分位边界;空值单独 missing 箱。待实现"""
    raise NotImplementedError("equal_freq_bins 等频分箱待实现")


def apply_bins(x, edges):
    """按给定边界分箱(PSI 用基准群体分位点切分),空值归 missing 箱。待实现"""
    raise NotImplementedError("apply_bins 边界应用待实现")

#============== 卡方合并 ===============

def chi_merge(x, y, max_bins):
    """卡方合并至 max_bins 箱;missing 箱不参与合并(文档 §4.2a.2)。待实现"""
    raise NotImplementedError("chi_merge 卡方合并待实现")