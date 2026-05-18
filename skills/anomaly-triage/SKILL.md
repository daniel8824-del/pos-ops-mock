---
name: anomaly-triage
description: 최근 POS 거래 로그에서 이상을 탐지하고, 1차 진단 + 운영 티켓 자동 생성까지 한 사이클로 처리. Use when 사용자가 "최근 이상 있어?", "POS 문제 확인", "운영 모니터링" 등 운영 상태 점검을 요청하거나, 알림에서 이상 패턴이 감지되었을 때.
---

# Anomaly Triage — POS 운영 1차 자동화

## 언제 발동

- 사용자가 "최근 이상 확인", "POS 문제", "운영 모니터링", "장애 체크" 요청
- 알림(Slack/Discord webhook)에서 이상 키워드 감지
- 정기 스케줄 (매 30분 / 1시간)

## 5단계 사이클

### 1. 탐지 (`detect_anomaly`)

```
detect_anomaly(window_min=60)
```

반환: `{total, anomalies: {POS_DOWN: N, ...}, by_store: {...}, top_issue: ...}`

### 2. 임계값 판정

`threshold.yaml`의 기준 적용:

| Anomaly | 임계 (count / window 60min) | 우선순위 |
|---|---|---|
| POS_DOWN | ≥10 | P1-Critical |
| PAYMENT_FAIL | ≥15 | P2-High |
| TERMINAL_TIMEOUT | ≥15 | P2-High |
| STOCK_SHORTAGE | ≥20 | P3-Medium |
| REFUND | ≥10 (이상 폭주) | P3-Medium |

### 3. 1차 진단 (운영 매뉴얼 검색)

`pos-runbook.md`에서 top_issue 키워드로 해당 섹션 인용. 학습자 환경에선
`qmd query "<top_issue> 해결 절차" -c manuals` 으로 검색.

### 4. 유사 과거 사례 (ontology query)

```
query_ontology("최근 30일간 같은 매장에서 발생한 <top_issue> 사례 + 해결책")
```

→ 과거 ticket 3건 추출 + 평균 해결 시간.

### 5. 티켓 생성 (`create_ticket`)

```
create_ticket(
  title="<top_issue> @ <매장명> — count 폭주",
  body="[탐지 결과 요약]\n[매뉴얼 인용]\n[과거 사례 3건]\n[권장 조치 1순위]",
  priority=<우선순위>,
  store=<영향 매장 ID>,
  category=<auto>,
)
```

## 출력 포맷 (사용자에게 보여줄 형태)

```
🚨 이상 탐지 결과 (최근 60분)
─────────────────────────────
총 거래: 234건 · 이상: 25건 (10.7%)

⚠ TOP ISSUE: POS_DOWN (12건)
  └─ 영향 매장: 강남역점 (7) · 명동점 (3) · 홍대점 (2)

📖 매뉴얼 권장 조치 (pos-runbook §3.2):
  1) POS 단말 power cycle (5초)
  2) 5분 후 미복구 시 본사 IT 010-...
  3) 결제 백업 수단 (모바일 영수증) 안내

📋 유사 과거 사례 (3건):
  - INC-1023 (3주 전, 강남역점): 단말 펌웨어 업데이트로 해결
  - INC-1067 (1주 전, 명동점): 케이블 교체로 해결
  - INC-1102 (어제, 홍대점): 재부팅으로 해결

✅ 티켓 생성: OPS-A8F2 (P1-Critical · ops-team1)
```

## 학습자 환경 port

- `qmd query` → 학습자 본인 매뉴얼 컬렉션 이름으로 교체
- `query_ontology` → 학습자 본인 ontology instance URL로 교체
- `create_ticket` → `gh issue create` 또는 `jira issue create`로 교체
