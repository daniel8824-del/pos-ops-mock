"""UserPromptSubmit hook | 사용자 프롬프트에 운영 키워드 감지 시
ontology 컨텍스트 자동 주입.

발동 키워드:
  POS / 결제 / 단말 / 매장 / 재고 / 티켓 / 운영 / 장애 / 이상

액션: 관련 ontology node·edge 요약을 system reminder로 stdout 출력.
       Claude/Copilot이 응답 생성 전에 이 컨텍스트를 본다.
"""

import sys
import json

try:
    payload = json.load(sys.stdin)
except Exception:
    payload = {}

prompt = payload.get("user_message", "") or payload.get("prompt", "")
if not prompt:
    sys.exit(0)

# 운영 키워드 감지
KEYWORDS = ["POS", "pos", "결제", "단말", "매장", "재고", "티켓",
            "운영", "장애", "이상", "환불", "timeout"]

if not any(k in prompt for k in KEYWORDS):
    sys.exit(0)

# 강의용 mock ontology 컨텍스트 (실제 강의에선 yucrates ontology_query 호출)
context = """[POS 운영 ONTOLOGY 컨텍스트 | 자동 주입]

도메인 entity 9:
  Store(매장) · POS_Machine(POS 단말) · Transaction(거래) · Product(SKU)
  Employee(직원) · Customer(고객) · ErrorEvent(에러) · IssueTicket(티켓) · Alert(알림)

관계 5:
  Transaction |executed_at→ POS_Machine
  Transaction |contains→ Product
  ErrorEvent |triggers→ Alert
  Alert |escalates_to→ IssueTicket
  Employee |handles→ IssueTicket

본 작업에 사용 가능한 MCP tool:
  - mcp__pos-ops__get_logs(store, status, limit)
  - mcp__pos-ops__detect_anomaly(window_min, store)
  - mcp__pos-ops__create_ticket(title, body, priority, store, category)

권장 사이클: 탐지 → 진단 (매뉴얼/유사사례) → 티켓 → 알림
"""

print(context)
