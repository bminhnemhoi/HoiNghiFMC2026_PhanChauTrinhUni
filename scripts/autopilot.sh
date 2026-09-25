#!/usr/bin/env bash
# Chạy Claude Code không cần ngồi canh: mỗi vòng gọi `claude -p "/next"`; hook Stop giữ Claude làm
# liên tục trong một vòng. Dừng khi: có state/PAUSE, hết việc Claude làm được, hoặc đủ số vòng.
# Dùng:  scripts/autopilot.sh [số_vòng=20] [max_turns_mỗi_vòng=150]
# CHỈ NGƯỜI DÙNG chạy script này ở terminal (hook chặn Claude tự gọi nó).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
ROUNDS="${1:-20}"; TURNS="${2:-150}"
mkdir -p logs/autopilot
scripts/vs autopilot on >/dev/null
for i in $(seq 1 "$ROUNDS"); do
  if [ -f state/PAUSE ]; then echo "PAUSE → dừng"; break; fi
  NEXT="$(scripts/vs next --id-only 2>/dev/null || true)"
  if [ -z "$NEXT" ] || [ "$NEXT" = "NONE" ]; then echo "Không còn việc Claude làm được ngay → dừng"; break; fi
  TS="$(date +%Y%m%d-%H%M%S)"
  echo "[$TS] vòng $i: $NEXT"
  claude -p "/next" --permission-mode acceptEdits --max-turns "$TURNS" --output-format json \
    > "logs/autopilot/$TS.json" 2> "logs/autopilot/$TS.err"
  code=$?
  if command -v jq >/dev/null; then
    jq -r '"  kết quả: \(.subtype // "?") · lượt: \(.num_turns // "?") · chi phí phiên: \(.total_cost_usd // "?") USD"' \
      "logs/autopilot/$TS.json" 2>/dev/null || true
  fi
  if [ $code -ne 0 ]; then echo "claude thoát mã $code (xem logs/autopilot/$TS.err) → dừng"; break; fi
  sleep 5
done
scripts/vs digest
echo "Việc chờ bạn: state/HUMAN_TODO.md"
