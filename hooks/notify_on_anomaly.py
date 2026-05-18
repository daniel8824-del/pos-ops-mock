"""PostToolUse hook | detect_anomaly 호출 후 자동 알림.

발동: mcp__pos-ops__detect_anomaly tool 실행 직후
조건: top_issue 가 임계값(threshold.yaml) 초과
액션: Discord webhook 또는 stdout 출력 (강의용은 stdout)

학습자 환경 port:
  - Discord webhook URL 환경변수 DISCORD_WEBHOOK 으로 교체
  - Slack: SLACK_WEBHOOK
  - 이메일: SMTP wrapper
"""

import sys
import json
import os
from pathlib import Path

# stdin으로 hook payload 들어옴 (Claude Code 표준)
try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}

tool_result = payload.get("tool_result", {})
if not isinstance(tool_result, dict):
    sys.exit(0)

top_issue = tool_result.get("top_issue")
anomalies = tool_result.get("anomalies", {})
total = tool_result.get("total", 0)

if not top_issue or not anomalies:
    sys.exit(0)

count = anomalies.get(top_issue, 0)

# 단순 임계: top_issue count가 10 이상이면 알림
if count < 10:
    sys.exit(0)

msg = (
    f"🚨 POS 운영 알림\n"
    f"  TOP ISSUE: {top_issue} ({count}건 / 총 {total}건)\n"
    f"  영향 매장: {', '.join(tool_result.get('by_store', {}).keys())}\n"
    f"  자동 사이클: anomaly-triage skill로 1차 진단 후 티켓 생성 권장"
)

# 강의용 | stdout
print(msg)

# 학습자 환경: Discord webhook
webhook = os.environ.get("DISCORD_WEBHOOK")
if webhook:
    import urllib.request
    data = json.dumps({"content": msg}).encode()
    req = urllib.request.Request(
        webhook, data=data, headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"(webhook 전송 실패: {e})", file=sys.stderr)
