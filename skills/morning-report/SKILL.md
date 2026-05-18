---
name: morning-report
description: 매일 아침 운영팀에게 어제 하루 매장 운영 상태 요약 보고서 자동 생성. 매장별 KPI (거래 건수·매출·이상 비율) + Top 3 이슈 + 미해결 티켓 목록 + 오늘 주의 매장. Use when 사용자가 "어제 운영 요약", "morning report", "데일리 리포트", "출근 보고서" 요청하거나, SessionStart 시 자동 발동.
---

# Morning Report | 어제 운영 한눈에

## 언제 발동

- 매일 아침 첫 세션 시작 (SessionStart hook 자동)
- 사용자 명시: "어제 어땠어?", "데일리 리포트", "출근 보고"

## 3단계

### 1. 어제 거래 집계 (`detect_anomaly`)

```
detect_anomaly(window_min=1440)   # 24시간
```

### 2. 매장별 KPI 계산

각 매장별:
- 총 거래 건수
- 매출 합계 (KRW)
- 이상 비율 (anomaly / total)
- 최다 이상 종류

### 3. 미해결 티켓 (`incidents.csv` + `tickets.jsonl`)

`status in (open, in_progress)` 필터.

## 출력 포맷

```
☀ Morning Report | 2026-05-14 (어제 운영 요약)
═════════════════════════════════════════════

📊 전국 합계
  거래: 7,840건 · 매출: ₩142,580,000
  이상 비율: 11.3% (정상 88.7%)

🏆 매출 Top 3
  1. 강남역점 (이니스프리)   ₩28,420,000  · 932건
  2. 명동점 (아모레스토어)   ₩21,180,000  · 745건
  3. 홍대점 (에뛰드)         ₩18,640,000  · 812건

⚠ 주의 매장 Top 3 (이상 비율 높음)
  1. 광주 충장로점  18.4%  (POS_DOWN 12건)
  2. 부산 서면점    15.2%  (PAYMENT_FAIL 9건)
  3. 대구 동성로점  13.7%  (STOCK_SHORTAGE 11건)

📋 미해결 티켓 5건
  - OPS-A8F2 (P1) 강남역점 POS_DOWN | 어제 22:14 생성
  - INC-1098 (P2) 명동점 카드 승인 거부 | 3일째 in_progress
  - ...

🎯 오늘 주의
  - 광주 충장로점 단말 점검 (현장 출동 권장)
  - 부산 서면점 카드사 연동 재확인
```

## 학습자 환경 port

- 데이터 source: 학습자 본인 POS 시스템 / DB / 로그 stream
- 출력 채널: Discord/Slack webhook 또는 단순 stdout
- 스케줄: cron `0 8 * * 1-5` (평일 08:00) 또는 SessionStart hook
