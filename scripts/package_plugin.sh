#!/usr/bin/env bash
# (Tùy chọn) Đóng gói agent/skill/lệnh/hook của dự án thành một plugin Claude Code để dùng lại ở repo khác.
# Dự án này KHÔNG cần plugin: thư mục .claude/ đã đủ. Dùng: scripts/package_plugin.sh → dist/vnsoc-plugin
# Nạp thử: claude --plugin-dir dist/vnsoc-plugin
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist/vnsoc-plugin"
rm -rf "$OUT" && mkdir -p "$OUT/.claude-plugin" "$OUT/hooks"
cp -r "$ROOT/.claude/agents" "$ROOT/.claude/skills" "$ROOT/.claude/commands" "$OUT/"
cp "$ROOT"/.claude/hooks/*.py "$OUT/hooks/"
cat > "$OUT/.claude-plugin/plugin.json" <<JSON
{
  "name": "vnsoc-audit",
  "description": "Agents, skills, commands and guard hooks for auditing LLM answers against Vietnamese MoH guidelines",
  "version": "0.1.0",
  "author": {"name": "Binh Minh"}
}
JSON
# Hook của plugin trỏ tới thư mục plugin; state vẫn nằm ở dự án đang mở ($CLAUDE_PROJECT_DIR).
python3 - "$ROOT/.claude/settings.json" "$OUT/hooks/hooks.json" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
hooks = json.loads(json.dumps(s["hooks"]).replace("$CLAUDE_PROJECT_DIR/.claude/hooks", "${CLAUDE_PLUGIN_ROOT}/hooks"))
json.dump({"hooks": hooks}, open(sys.argv[2], "w"), indent=1)
PY
echo "OK: $OUT"
