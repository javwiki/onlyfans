#!/usr/bin/env python3
"""数据完整性校验脚本。

用法:
    python3 scripts/validate.py [--strict]

校验项（error 会失败退出）:
  E1  list.yaml 无重复键，字段类型与 status 范围有效，file 指向存在的详情页
  E2  除 index.md 外的所有博主页都被 list.yaml 引用（无孤儿文件）
  E3  字母索引页（docs/X/index.md）实际链接到该字母下所有条目
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
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs")
LIST_YAML = os.path.join(SRC, "0_meta", "list.yaml")
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PLACEHOLDER_MARKS = ("网络搜索未找到", "未找到关于", "未找到其他公开信息")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently overwriting entries."""


def construct_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError:
            raise yaml.constructor.ConstructorError(
                None, None, "映射键必须是可哈希值", key_node.start_mark
            )
        if duplicate:
            raise yaml.constructor.ConstructorError(
                None, None, f"重复键: {key}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def load_data() -> dict:
    try:
        with open(LIST_YAML, encoding="utf-8") as f:
            data = yaml.load(f, Loader=UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as e:
        err(f"E1 {LIST_YAML} 读取或解析失败: {e}")
        return {}
    if not isinstance(data, dict) or not data:
        err("E1 list.yaml 必须是非空映射")
        return {}
    return data


def relative_targets(content: str, source: str, include_images: bool = True) -> list[tuple[str, str]]:
    """Resolve local inline Markdown links, ignoring URL queries and fragments."""
    targets = []
    prefix = "" if include_images else r"(?<!!)"
    pattern = prefix + r"\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)"
    for match in re.finditer(pattern, content):
        link = match.group(1).strip("<>")
        url = urlsplit(link)
        if url.scheme or url.netloc or not url.path:
            continue
        target = os.path.realpath(os.path.join(os.path.dirname(source), unquote(url.path)))
        targets.append((link, target))
    return targets


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="将 warning 视为 error")
    args = parser.parse_args()

    errors.clear()
    warnings.clear()
    data = load_data()

    # ---- E1: schema 与详情文件 ----
    pages = {}
    for key, v in data.items():
        if not isinstance(key, str) or not key.strip():
            err(f"E1 条目键必须是非空字符串: {key!r}")
        if not isinstance(v, dict):
            err(f"E1 条目 {key}: 必须是映射")
            continue
        if "name" not in v:
            err(f"E1 条目 {key}: 缺少 name 字段")
        for field in ("name", "region", "x"):
            if field in v and (not isinstance(v[field], str) or not v[field].strip()):
                err(f"E1 条目 {key}: {field} 必须是非空字符串")
        status = v.get("status")
        if type(status) is not int or not 0 <= status <= 100:
            err(f"E1 条目 {key}: status 必须是 0–100 的整数")
        f = v.get("file")
        if not isinstance(f, str) or not re.fullmatch(r"docs/[A-Z]/[^/]+\.md", f) or os.path.basename(f) == "index.md":
            err(f"E1 条目 {key}: file 必须指向 docs/A–Z 下的 Markdown 详情页")
            continue
        if not os.path.isfile(os.path.join(ROOT, f)):
            err(f"E1 条目 {key}: file 指向不存在的文件 {f}")
            continue
        pages[key] = v

    # ---- E2: 无孤儿博主页 ----
    refs = set(os.path.normpath(v["file"]) for v in pages.values())
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
        content = Path(idx).read_text(encoding="utf-8")
        targets = {target for _, target in relative_targets(content, idx, include_images=False)}
        for key, v in pages.items():
            f = v["file"]
            if not f.startswith(f"docs/{d}/"):
                continue
            if f == f"docs/{d}/index.md":
                continue
            if os.path.realpath(os.path.join(ROOT, f)) not in targets:
                err(f"E3 索引页 {idx} 未链接到条目 {key}: {f}")

    # ---- E4: list.yaml 保持简短，tags 仅存于页面 frontmatter ----
    for key, v in data.items():
        if isinstance(v, dict) and "tags" in v:
            err(f"E4 条目 {key}: list.yaml 不应包含 tags，请移至页面 frontmatter")

    # ---- E5/E6: 页面级检查 ----
    w_region = []
    w_placeholder = []
    for key, v in pages.items():
        f = os.path.join(ROOT, v["file"])
        content = Path(f).read_text(encoding="utf-8")
        # E5: 区块完整性
        if "简介" not in content:
            err(f"E5 {v['file']}: 缺少「简介」区块")
        if "相关链接" not in content and "链接" not in content:
            err(f"E5 {v['file']}: 缺少「相关链接」区块")
        if "返回" not in content or "首页" not in content:
            err(f"E5 {v['file']}: 缺少返回导航")
        # E6: 相对链接死链
        for link, target in relative_targets(content, f):
            if not os.path.exists(target):
                err(f"E6 {v['file']}: 死链 {link}")
        # W1: region
        if not v.get("region"):
            w_region.append(key)
        # W2: 占位
        if any(mark in content for mark in PLACEHOLDER_MARKS):
            w_placeholder.append(v["file"])

    if w_region:
        warn(f"W1 缺少 region 字段的条目: {len(w_region)} 个")
    if w_placeholder:
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
