"""
퀴즈 진행도 확인 스크립트
"""
from sqlmodel import Session, create_engine, select, Field, SQLModel
from datetime import date, datetime
from typing import Optional
import os

# ChallengeProgress 모델 정의
class ChallengeProgress(SQLModel, table=True):
    __tablename__ = "challengeprogress"

    id: Optional[int] = Field(default=None, primary_key=True)
    challenge_id: int = Field(foreign_key="challenge.id")
    student_id: str = Field(index=True)
    current_value: int = 0
    is_completed: bool = False
    completed_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None

# Challenge 모델 정의
class Challenge(SQLModel, table=True):
    __tablename__ = "challenge"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    type: str
    goal_value: int
    reward_points: int
    is_active: bool = True
    created_at: Optional[datetime] = None

# DB 연결
db_path = os.path.join(os.getcwd(), "reflex.db")
db_url = f"sqlite:///{db_path}"
engine = create_engine(db_url, echo=False)

today = date.today()

print(f"오늘 날짜: {today}")
print("=" * 60)

with Session(engine) as session:
    # 모든 챌린지 조회
    challenges = session.exec(select(Challenge)).all()

    print("\n[모든 챌린지]")
    for ch in challenges:
        print(f"  ID: {ch.id}, 제목: {ch.title}, 타입: {ch.type}")

    # 사용자 20215277의 퀴즈 진행도 조회
    user_id = "20215277"

    print(f"\n[사용자 {user_id}의 챌린지 진행도]")
    stmt = select(ChallengeProgress).where(
        ChallengeProgress.student_id == user_id
    )

    progresses = session.exec(stmt).all()

    if not progresses:
        print("  진행도 없음")
    else:
        for prog in progresses:
            # 챌린지 정보 조회
            ch = session.exec(select(Challenge).where(Challenge.id == prog.challenge_id)).first()
            ch_title = ch.title if ch else "알 수 없음"
            ch_type = ch.type if ch else "알 수 없음"

            last_updated_date = prog.last_updated.date() if prog.last_updated else None

            print(f"\n  챌린지: {ch_title} (타입: {ch_type})")
            print(f"    현재 진행도: {prog.current_value}")
            print(f"    완료 여부: {prog.is_completed}")
            print(f"    마지막 업데이트: {prog.last_updated}")
            print(f"    마지막 업데이트 날짜: {last_updated_date}")
            print(f"    오늘과 같은 날짜?: {last_updated_date == today if last_updated_date else False}")

print("\n" + "=" * 60)
print("확인 완료!")
