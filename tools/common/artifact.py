# -*- coding: utf-8 -*-
# tools/common/artifact.py — JSON 信封落库与状态协议(AGENT.MD 第 3/4 节)
# 本协议基建为最小实现:信封写入、单行状态输出、CLI 统一骨架;其余函数待实现
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

#============== 信封落库 ===============

def write_artifact(run_id, step, tool, params, status, results=None, summary=None, error=None, out_dir="artifacts"):
    """写出统一信封 artifact,返回文件路径。step 形如「01_peek」「10a_search」"""
    env = {
        "run_id": run_id,
        "step": step,
        "tool": tool,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "params": params,
        "status": status,
        "results": results if status == "success" else {},
        "summary": summary or {},
    }
    if status != "success":
        env["error"] = error or {"code": 1, "message": "未知错误", "hint": "检查工具日志"}
    out = Path(out_dir) / f"{run_id}_{step}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)


def print_status(out, status, summary):
    """stdout 只打印一行 JSON 状态,供 AGENT 解析(协议 3.3)"""
    print(json.dumps({"out": out, "status": status, "summary": summary}, ensure_ascii=False))


def read_latest(run_id, before_step, out_dir="artifacts"):
    """读取上游编号最大的已存在 artifact(协议 3.2)。待实现"""
    raise NotImplementedError("read_latest 上游产物读取待实现")

#============== CLI 统一骨架 ===============

def cli_main(step, tool, func):
    """工具 CLI 统一入口:解析 --config/--run-id → 执行 func(cfg, run_id) → 落库 + 状态行。
    退出码:0=成功、2=业务失败(已落库)、3=工具或依赖缺失、4=数据规范校验失败(AGENT.MD 3.4)。
    框架期 func 均为 stub,抛 NotImplementedError → 落库 tool_missing 并 exit 3"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    try:
        results, summary = func(cfg, args.run_id)
    except NotImplementedError as e:
        out = write_artifact(args.run_id, step, tool, params={}, status="tool_missing",
                             error={"code": 3, "message": str(e), "hint": "工具待实现,完成该工具后再继续"})
        print_status(out, "tool_missing", {})
        sys.exit(3)
    out = write_artifact(args.run_id, step, tool, params={}, status="success",
                         results=results, summary=summary)
    print_status(out, "success", summary)
    sys.exit(0)