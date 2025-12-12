"""
탄소 로그 데이터 확인 스크립트
"""
from sqlmodel import Session, create_engine, select, Field, SQLModel
from datetime import date, timedelta, datetime
from typing import Optional
import os

# CarbonLog 모델 정의 (models.py에서 복사)
class CarbonLog(SQLModel, table=True):
    __tablename__ = "carbonlog"

    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(index=True)
    log_date: date = Field(index=True)
    transport_km: float = 0.0
    ac_hours: float = 0.0
    cup_count: int = 0
    total_emission: float = 0.0
    activities_json: Optional[str] = None
    ai_feedback: Optional[str] = None
    points_earned: int = 0
    created_at: Optional[datetime] = None
    source: str = Field(default="carbon_input")

# DB 연결
db_path = os.path.join(os.getcwd(), "reflex.db")
db_url = f"sqlite:///{db_path}"
engine = create_engine(db_url, echo=False)

# 오늘과 30일 전 날짜
today = date.today()
one_month_ago = today - timedelta(days=30)

print(f"오늘 날짜: {today}")
print(f"30일 전: {one_month_ago}")
print("=" * 60)

with Session(engine) as session:
    # 모든 사용자의 최근 30일 데이터 조회
    stmt = select(CarbonLog).where(
        CarbonLog.log_date >= one_month_ago,
        CarbonLog.log_date <= today
    ).order_by(CarbonLog.student_id, CarbonLog.log_date)

    logs = session.exec(stmt).all()

    if not logs:
        print("[WARNING] 최근 30일 이내 데이터가 없습니다!")
    else:
        print(f"[OK] 총 {len(logs)}개의 로그가 있습니다.\n")

        # 사용자별로 그룹화
        user_logs = {}
        for log in logs:
            if log.student_id not in user_logs:
                user_logs[log.student_id] = []
            user_logs[log.student_id].append(log)

        # 사용자별 출력
        for user_id, user_log_list in user_logs.items():
            print(f"\n[사용자: {user_id}]")
            print(f"  - 총 {len(user_log_list)}개의 로그")
            for log in user_log_list:
                print(f"  - {log.log_date}: {log.total_emission:.2f}kg CO2e (source: {log.source})")

print("\n" + "=" * 60)
print("확인 완료!")
