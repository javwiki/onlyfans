#!/usr/bin/env python3
"""数据完整性校验脚本。

用法:
    python3 scripts/validate.py [--strict]

校验项（error 会失败退出）:
  E1  list.yaml 可解析，且每条目 file 字段指向存在的文件
  E2  除 index.md 外的所有博主页都被 list.yaml 引用（无孤儿文件）
  E3  字母索引页（src/X/index.md）列出了该字母下所有条目
  E4  list.yaml 不保存 tags（标签仅由页面 frontmatter 维护）
  E5  页面包含「简介」与「相关链接」区块，且有返回导航
  E6  页面内相对链接无死链

校验项（warning，仅提示，--strict 时视为 error）:
  W1  条目缺少 region 字段
  W2  页面为占位页（含「网络搜索未找到」等占位表述）
"""
import argparse
import os
import re
import sys
import glob
from collections import Counter

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
LIST_YAML = os.path.join(SRC, "_meta", "list.yaml")
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PLACEHOLDER_MARKS = ("网络搜索未找到", "未找到关于", "未找到其他公开信息")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def load_data() -> dict:
    if not os.path.exists(LIST_YAML):
        err(f"E1 缺少 {LIST_YAML}")
        return {}
    with open(LIST_YAML, encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            err(f"E1 {LIST_YAML} 解析失败: {e}")
            return {}
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="将 warning 视为 error")
    args = parser.parse_args()

    data = load_data()
    if not data:
        return 1

    # ---- E1: file 字段存在 ----
    missing_files = []
    for key, v in data.items():
        f = v.get("file", "")
        if not f:
            missing_files.append((key, "缺 file 字段"))
        elif not os.path.exists(os.path.join(ROOT, f)):
            missing_files.append((key, f))
    for key, f in missing_files:
        err(f"E1 条目 {key}: file 指向不存在的文件 {f}")
    if len(missing_files) > 0:
        return 1

    # ---- E2: 无孤儿博主页 ----
    refs = set(os.path.normpath(v["file"]) for v in data.values())
    all_pages = set()
    for d in LETTERS:
        for f in glob.glob(os.path.join(SRC, d, "*.md")):
            if os.path.basename(f) == "index.md":
                continue
            all_pages.add(os.path.normpath(os.path.relpath(f, ROOT)))
    for orphan in sorted(all_pages - refs):
        err(f"E2 孤儿页面未被 list.yaml 引用: {orphan}")

    # ---- E3: 字母索引页完整性 ----
    for d in LETTERS:
        idx = os.path.join(SRC, d, "index.md")
        if not os.path.exists(idx):
            err(f"E3 缺少索引页 {idx}")
            continue
        content = open(idx, encoding="utf-8").read()
        for key, v in data.items():
            f = v.get("file", "")
            if not f.startswith(f"src/{d}/"):
                continue
            if f == f"src/{d}/index.md":
                continue
            if key not in content and v.get("name", "") not in content:
                err(f"E3 索引页 {idx} 未列出条目 {key}")

    # ---- E4: list.yaml 保持简短，tags 仅存于页面 frontmatter ----
    for key, v in data.items():
        if "tags" in v:
            err(f"E4 条目 {key}: list.yaml 不应包含 tags，请移至页面 frontmatter")

    # ---- E5/E6: 页面级检查 ----
    w_region = []
    w_placeholder = []
    for key, v in data.items():
        f = os.path.join(ROOT, v["file"])
        content = open(f, encoding="utf-8").read()
        # E5: 区块完整性
        if "简介" not in content:
            err(f"E5 {v['file']}: 缺少「简介」区块")
        if "相关链接" not in content and "链接" not in content:
            err(f"E5 {v['file']}: 缺少「相关链接」区块")
        if "返回" not in content or "首页" not in content:
            err(f"E5 {v['file']}: 缺少返回导航")
        # E6: 相对链接死链
        for m in re.finditer(r"\]\(([^)]+)\)", content):
            link = m.group(1)
            if link.startswith(("http", "#", "mailto")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(f), link))
            if not os.path.exists(target):
                err(f"E6 {v['file']}: 死链 {link}")
        # W1: region
        if not v.get("region"):
            w_region.append(key)
        # W2: 占位
        if any(mark in content for mark in PLACEHOLDER_MARKS):
            w_placeholder.append(v["file"])

    warn(f"W1 缺少 region 字段的条目: {len(w_region)} 个")
    warn(f"W2 占位页（未搜索到信息）: {len(w_placeholder)} 个")

    # ---- 输出 ----
    for w in warnings:
        print(f"[WARN ] {w}")
    for e in errors:
        print(f"[ERROR] {e}")

    fail = bool(errors)
    if not fail and args.strict and warnings:
        print(f"[STRICT] {len(warnings)} 条 warning 视为 error")
        fail = True

    total = len(data)
    print(f"\n共 {total} 个条目: errors={len(errors)}, warnings={len(warnings)}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
