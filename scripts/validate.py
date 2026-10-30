#!/usr/bin/env python3
"""数据完整性校验脚本。

用法:
    python3 scripts/validate.py [--strict]

校验项（error 会失败退出）:
  E1  list.yaml 无重复键，字段类型与 status 范围有效，file 指向存在的详情页
  E2  除 index.md 外的所有博主页都被 list.yaml 引用（无孤儿文件）
  E3  字母索引页（docs/X/index.md）实际链接到该字母下所有条目
  E4  list.yaml 不保存 tags（标签仅由页面 frontmatter 维护）
  E5  页面包含「简介」与「相关链接」区块（按标题判断），且有返回导航
  E6  页面内相对链接无死链
  E7  「简介」「相关链接」区块不得为空
  E8  字母索引中的 @handle 必须对应已核验的 x 字段

校验项（warning，仅提示，--strict 时视为 error）:
  W1  条目缺少 region 字段
  W2  页面为占位页（含「网络搜索未找到」等占位表述）
  W3  平台账号被多个条目共用（互相关联的页面除外）
  W4  tags 大小写、空格或同义写法未规范化
  W5  占位表述与 status ≥ 85 矛盾
  W6  字母索引未按用户名排序
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
NUMBER_DIR = "0-9"
SECTIONS = tuple(LETTERS) + (NUMBER_DIR,)
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


def sections(content: str) -> dict[str, str]:
    """Split page body into ``## `` sections, stopping at the footer rule."""
    result: dict[str, str] = {}
    title = None
    buf: list[str] = []
    for line in content.splitlines():
        if line.startswith("## "):
            if title is not None:
                result[title] = "\n".join(buf).strip()
            title = line[3:].strip()
            buf = []
        elif title is not None:
            if line.strip() == "---":
                result[title] = "\n".join(buf).strip()
                title = None
                buf = []
            else:
                buf.append(line)
    if title is not None:
        result[title] = "\n".join(buf).strip()
    return result


def find_section(secs: dict[str, str], keyword: str) -> str | None:
    for title, body in secs.items():
        if keyword in title:
            return body
    return None


def page_tags(content: str) -> list[str] | None:
    match = re.match(r"^---\n(.*?)\n---\n", content, re.S)
    if not match:
        return None
    tag_line = re.search(r"^tags:\s*(.*)$", match.group(1), re.M)
    if not tag_line:
        return None
    return [t.strip() for t in tag_line.group(1).strip().strip("[]").split(",") if t.strip()]


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
        if not isinstance(f, str) or not re.fullmatch(r"docs/(?:[A-Z]|0-9)/[^/]+\.md", f) or os.path.basename(f) == "index.md":
            err(f"E1 条目 {key}: file 必须指向 docs/A–Z 或 docs/0-9 下的 Markdown 详情页")
            continue
        if not os.path.isfile(os.path.join(ROOT, f)):
            err(f"E1 条目 {key}: file 指向不存在的文件 {f}")
            continue
        pages[key] = v

    # ---- E2: 无孤儿博主页 ----
    refs = set(os.path.normpath(v["file"]) for v in pages.values())
    all_pages = set()
    for d in SECTIONS:
        for f in glob.glob(os.path.join(SRC, d, "*.md")):
            if os.path.basename(f) == "index.md":
                continue
            all_pages.add(os.path.normpath(os.path.relpath(f, ROOT)))
    for orphan in sorted(all_pages - refs):
        err(f"E2 孤儿页面未被 list.yaml 引用: {orphan}")

    # ---- E3: 字母索引页完整性 ----
    entry_by_file = {os.path.normpath(v["file"]): (key, v) for key, v in pages.items()}
    index_orders: list[tuple[str, list[str]]] = []
    for d in SECTIONS:
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
        # E8: 索引中的 @handle 必须与已核验的 x 字段一致
        order = []
        for line in content.splitlines():
            match = re.match(r"^(?:- )?\[([^\]]+)\]\(\./([^)#]+\.md)\)", line)
            if not match:
                continue
            label, link = match.group(1), match.group(2)
            target = os.path.normpath(os.path.join(f"docs/{d}", link))
            entry = entry_by_file.get(target)
            if entry is None:
                continue
            name, v = entry
            order.append(name)
            if not label.startswith("@"):
                continue
            handle = label[1:]
            x = v.get("x")
            if not x:
                err(f"E8 {idx}: 条目 {name} 标注 @{handle}，但 list.yaml 没有已核验的 x 字段")
            elif handle.casefold() != x.casefold():
                err(f"E8 {idx}: 条目 {name} 标注 @{handle}，与 x={x} 不一致")
        index_orders.append((idx, order))

    # ---- E4: list.yaml 保持简短，tags 仅存于页面 frontmatter ----
    for key, v in data.items():
        if isinstance(v, dict) and "tags" in v:
            err(f"E4 条目 {key}: list.yaml 不应包含 tags，请移至页面 frontmatter")

    # ---- E5/E6/E7: 页面级检查 ----
    w_region = []
    w_placeholder = []
    w_status = []
    w_tags = []
    accounts: dict[str, set[str]] = {}
    contents: dict[str, str] = {}
    for key, v in pages.items():
        f = os.path.join(ROOT, v["file"])
        content = Path(f).read_text(encoding="utf-8")
        contents[v["file"]] = content
        secs = sections(content)
        intro = find_section(secs, "简介")
        links = find_section(secs, "相关链接")
        # E5: 区块完整性（按标题判断，不能被子串误伤）
        if intro is None:
            err(f"E5 {v['file']}: 缺少「简介」区块")
        elif not intro:
            err(f"E7 {v['file']}: 「简介」区块为空")
        if links is None:
            err(f"E5 {v['file']}: 缺少「相关链接」区块")
        elif not links:
            err(f"E7 {v['file']}: 「相关链接」区块为空")
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
        # W4: tags 规范
        tags = page_tags(content)
        if tags is not None:
            if not tags:
                w_tags.append(f"{v['file']}: tags 为空数组")
            seen = set()
            for tag in tags:
                canonical = (tag.strip().casefold().replace(" ", "-")
                             .replace("adultmodel", "adult-model")
                             .replace("cammodel", "cam-model"))
                if tag != canonical:
                    w_tags.append(f"{v['file']}: 标签 {tag!r} 应写作 {canonical!r}")
                if canonical in seen:
                    w_tags.append(f"{v['file']}: 标签 {canonical!r} 重复")
                seen.add(canonical)
        # W5: 占位表述与高 status 矛盾
        status = v.get("status")
        if (type(status) is int and status >= 85
                and any(mark in content for mark in PLACEHOLDER_MARKS)):
            w_status.append(v["file"])
        # W3: 账号是否被多个条目共用
        if v.get("x"):
            accounts.setdefault(f"x:{v['x'].casefold()}", set()).add(v["file"])
        for match in re.finditer(
            r"https?://(?:www\.)?onlyfans\.com/([A-Za-z0-9_.-]+)", content, re.I
        ):
            accounts.setdefault(f"onlyfans:{match.group(1).casefold()}", set()).add(v["file"])

    if w_region:
        warn(f"W1 缺少 region 字段的条目: {len(w_region)} 个")
    if w_placeholder:
        warn(f"W2 占位页（未搜索到信息）: {len(w_placeholder)} 个")
    for account, files in sorted(accounts.items()):
        if len(files) < 2:
            continue
        # 关联账号页面互相引用时视为有意共用，不再提示
        linked = any(
            any(
                target == os.path.realpath(os.path.join(ROOT, other))
                for _, target in relative_targets(contents[f], f)
                for other in files
                if other != f
            )
            for f in files
        )
        if not linked:
            warn(f"W3 账号 {account} 被多个条目共用: {', '.join(sorted(files))}")
    if w_tags:
        warn(f"W4 tags 需规范化的页面: {len(w_tags)} 个")
    if w_status:
        warn(f"W5 占位表述但 status ≥ 85 的页面: {len(w_status)} 个")
    for idx, order in index_orders:
        seq = [(name.lstrip('_-').casefold(), name) for name in order]
        if seq != sorted(seq):
            warn(f"W6 {idx} 未按用户名排序")

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
