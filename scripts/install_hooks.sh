#!/bin/sh
# 安装口径校验 pre-commit 钩子。
#
# 用法：
#   scripts/install_hooks.sh                 # 装到本仓库
#   scripts/install_hooks.sh ../legal-ai-watch ../compliance-triangle
#                                            # 同时装到其它仓库
#
# 实现：把各仓库的 core.hooksPath 指向本仓库的 .githooks 目录（绝对路径）。
# 这样钩子只有一份、跟着 hub 走版本，其它仓库不需要各自复制一份。
#
# 注意：core.hooksPath 是本地 git 配置，不会随仓库同步——换机器/新克隆要重跑一次。

set -e

HOOKS_DIR=$(cd "$(dirname "$0")/.." && pwd)/.githooks

if [ ! -f "$HOOKS_DIR/pre-commit" ]; then
    echo "找不到钩子：$HOOKS_DIR/pre-commit" >&2
    exit 1
fi
chmod +x "$HOOKS_DIR/pre-commit"

targets="$*"
if [ -z "$targets" ]; then
    targets=$(cd "$HOOKS_DIR/.." && pwd)
fi

for t in $targets; do
    if [ ! -d "$t/.git" ]; then
        echo "跳过（不是 git 仓库）：$t" >&2
        continue
    fi
    (cd "$t" && git config core.hooksPath "$HOOKS_DIR")
    echo "已安装 -> $t"
done

cat <<'TIP'

完成。校验逻辑见 scripts/check_claims.py（R1–R6）。

- 只有 FAIL 会拦提交，WARN 只提醒
- 紧急绕过：git commit --no-verify
- 卸载：git config --unset core.hooksPath
TIP
