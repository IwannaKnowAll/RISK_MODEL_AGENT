# -*- coding: utf-8 -*-
# tools/common/metrics.py — IV/WOE/PSI/AUC/KS 公式实现(项目文档 §4)
# 状态:框架 stub,全部待实现

#============== WOE / IV ===============

def woe_iv(bad, good):
    """按箱计算 WOE 与 IV:WOE_i=ln((bad_i/Bad)/(good_i/Good));IV=Σ(bad_i/Bad−good_i/Good)×WOE_i。
    missing 箱并入求和(文档 §4.2a.2)。待实现"""
    raise NotImplementedError("woe_iv 计算待实现")

#============== PSI ===============

def psi(expected, actual):
    """PSI=Σ(a_i/e_i 占比差)×ln(a_i%/e_i%),1e-6 平滑防除零(文档 §4.2a.3)。待实现"""
    raise NotImplementedError("psi 计算待实现")

#============== AUC / KS ===============

def auc(y, score):
    """AUC。待实现"""
    raise NotImplementedError("auc 计算待实现")


def ks(y, score):
    """KS。待实现"""
    raise NotImplementedError("ks 计算待实现")