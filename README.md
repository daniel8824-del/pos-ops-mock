# pos-ops-mock

POS 운영팀 AI 자동화 강의 실습 키트 (Day 4 · 5).
**전부 로컬 · 외부 API 0건 · 데이터 외부 유출 0건.**

## 구성

```
pos-ops-mock/
├─ data/                    시뮬레이션 데이터
│   ├─ stores.csv             전국 10 매장
│   ├─ products.csv           아모레 30 SKU
│   ├─ transactions.csv       3일 ~24K 거래
│   ├─ incidents.csv          과거 운영 티켓 50건
│   └─ tickets.jsonl          새 티켓 (create_ticket 결과)
│
├─ scripts/                 운영 자동화 스크립트 3종
│   ├─ generate_data.py       4 csv 생성기 (결정론적)
│   ├─ get_logs.py            최근 거래 조회
│   ├─ detect_anomaly.py      이상 케이스 집계
│   └─ create_ticket.py       운영 티켓 생성 (jsonl append)
│
├─ mcp_server/              stdio MCP 서버
│   └─ server.py              3 tool exposing scripts above
│
├─ skills/                  Claude Code / Copilot CLI 스킬 .md 2개
│   ├─ anomaly-triage/SKILL.md     탐지 → 진단 → 티켓 5단계
│   └─ morning-report/SKILL.md     매일 아침 운영 요약
│
├─ hooks/                   훅 자동화 (강의 시연 항목)
│   ├─ hooks.json             PostToolUse + UserPromptSubmit
│   ├─ notify_on_anomaly.py    이상 임계 초과 시 알림
│   └─ inject_ontology_context.py  운영 키워드 감지 시 컨텍스트 주입
│
├─ ontology/                yucrates 온톨로지 seed
│   └─ pos-ops-domain.yaml    9 node + 5 edge · 학습자 port reference
│
├─ manuals/                 운영 매뉴얼 (QMD ingest 대상)
│   └─ pos-runbook.md         §1~§9 · 결제·단말·재고·환불·네트워크
│
└─ dashboard/               단순 HTML 대시보드
    └─ index.html             Chart.js · KPI 4 + 차트 3 + 티켓 표
```

## Quickstart (강사 환경)

```bash
# 1. venv + 의존성
python3 -m venv .venv
.venv/bin/pip install mcp

# 2. 데이터 생성 (1회)
python3 scripts/generate_data.py

# 3. 단독 동작 검증
python3 scripts/detect_anomaly.py --window 120
python3 scripts/get_logs.py --status POS_DOWN --limit 5

# 4. 대시보드
xdg-open dashboard/index.html

# 5. QMD ingest (운영 매뉴얼)
qmd collection add pos-manuals ./manuals
qmd update
qmd query "POS 단말 다운 해결" -c pos-manuals
```

## 학습자 환경 — Claude Code / Copilot CLI mcp.json

```json
{
  "mcpServers": {
    "pos-ops": {
      "command": "python3",
      "args": ["/path/to/pos-ops-mock/mcp_server/server.py"]
    }
  }
}
```

## 학습자 한 줄 시연

```
"최근 1시간 이상 거래 있어? 있으면 1순위 이슈만 매뉴얼 보고
 답변 초안 + 티켓 만들어줘"
```

→ MCP detect_anomaly → 매뉴얼 검색 (QMD) → 유사 사례 (ontology) →
   create_ticket → notify_on_anomaly hook 발동 → 알림.

## 5축 정합 (PDF 제안서)

| 축 | 위치 | PDF 차시 |
|---|---|---|
| MCP 개발 + Copilot 연결 | mcp_server/ + skills/ | 13차시 |
| Hook 자동화 (가드레일) | hooks/ | 14·8차시 |
| 멀티에이전트 (별도) | — | 15차시 |
| yucrates 온톨로지 | ontology/ | 16-A |
| 문서 청킹·보관 (QMD) | manuals/ + Day 3 QMD 재사용 | 16-B |
| 운영 대시보드 | dashboard/ | 16-C·17차시 |

## 데이터 출처 (정직 명시)

- 매장 좌표: 공개 도시 좌표 (실제 매장 아님, 도시 대표 좌표)
- SKU: 아모레퍼시픽 공식 자사몰 공개 카탈로그
- 거래 패턴: 통계청 소매판매동향 + 자체 시뮬레이션
- **실제 아모레퍼시픽 운영 raw 데이터 아님** (기업 내부)

## 한 줄 메시지

**"본인 노트가 100~5만 파일 사이라면 QMD를 1차로,**
**보강이 필요할 때만 GBrain·Graphify·yucrates를 얹는다 — 전부 로컬, 0원."**
