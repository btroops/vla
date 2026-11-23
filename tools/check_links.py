#!/usr/bin/env python3
"""检查仓库内 Markdown 的相对链接是否可解析（只查本仓库文件，不联网）。

规则：
- 跳过 fenced code block（``` 或 ~~~）里的内容——那里面的"链接"只是示例。
- 跳过行内代码 `...` 里的内容。
- 跳过 http/https/mailto 等外链与纯锚点 #xxx。
"""
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__", "site-packages"}
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:", "#")


def iter_md():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def main():
    broken, checked, skipped = [], 0, 0
    files = list(iter_md())

    for path in files:
        rel_dir = os.path.dirname(path)
        in_fence = False
        with open(path, encoding="utf-8") as f:
            for lineno, raw in enumerate(f, 1):
                if FENCE_RE.match(raw):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                line = INLINE_CODE_RE.sub("", raw)
                for text, target in LINK_RE.findall(line):
                    target = target.strip()
                    if target.startswith(SKIP_PREFIX):
                        skipped += 1
                        continue
                    file_part = unquote(target.split("#", 1)[0]).strip()
                    if not file_part:
                        skipped += 1
                        continue
                    checked += 1
                    resolved = os.path.normpath(os.path.join(rel_dir, file_part))
                    if not os.path.exists(resolved):
                        broken.append((os.path.relpath(path, ROOT), lineno, target, text))

    print(f"检查 Markdown: {len(files)} 个 | 仓库内相对链接: {checked} 条 | 跳过(外链/锚点): {skipped} 条")
    if broken:
        print(f"\n❌ 失效链接 {len(broken)} 条:")
        for src, ln, tgt, txt in broken:
            print(f"  {src}:{ln}  ->  {tgt}   [文字: {txt}]")
        return 1
    print("✅ 所有仓库内相对链接均可解析")
    return 0


if __name__ == "__main__":
    sys.exit(main())
