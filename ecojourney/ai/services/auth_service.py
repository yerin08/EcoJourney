from typing import Optional
import hashlib
from datetime import datetime
from sqlmodel import Session, create_engine, select
import os

from ecojourney.models import User as UserModel
from ecojourney.schemas.user import UserCreate, User


# DB 연결 설정 (Reflex와 동일한 DB 사용)
def _get_engine():
    """SQLModel 엔진 생성 (Reflex DB와 동일)"""
    db_path = os.path.join(os.getcwd(), "reflex.db")
    db_url = f"sqlite:///{db_path}"
    return create_engine(db_url, echo=False)


# ======================================================
# 비밀번호 해싱 (SHA256 - Reflex AuthState와 동일)
# ======================================================
def _hash_password(password: str) -> str:
    """비밀번호를 SHA256으로 해시화 (Reflex와 동일한 방식)"""
    return hashlib.sha256(password.encode()).hexdigest()


# ======================================================
# 회원가입: 비밀번호 해싱 후 user 테이블에 저장
# ======================================================
def create_user(user: UserCreate) -> None:
    """
    새 사용자를 생성합니다.
    Reflex의 user 테이블을 사용하며, SHA256으로 비밀번호를 해싱합니다.
    """
    engine = _get_engine()

    # 비밀번호 해시 생성 (SHA256)
    hashed_password = _hash_password(user.password)

    try:
        with Session(engine) as session:
            new_user = UserModel(
                student_id=user.student_id,
                password=hashed_password,
                college=user.college,
                current_points=0,
                created_at=datetime.now()
            )
            session.add(new_user)
            session.commit()
    except Exception as e:
        # student_id 중복 등의 오류는 상위에서 처리
        error_str = str(e).lower()
        if "unique" in error_str or "duplicate" in error_str or "constraint" in error_str:
            import sqlite3
            raise sqlite3.IntegrityError("이미 존재하는 학번입니다.")
        raise


# ======================================================
# 로그인 검증: ID + 비밀번호만 체크
# ======================================================
def verify_user(student_id: str, password: str) -> bool:
    """
    학번과 비밀번호를 검증합니다.
    단과대(college)는 검증에 사용하지 않고, 로그인 성공 후 별도로 조회합니다.
    """
    engine = _get_engine()

    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.student_id == student_id)
        user = session.exec(statement).first()

        if not user:
            return False

        # 비밀번호 검증 (SHA256)
        hashed_password = _hash_password(password)
        return user.password == hashed_password


# ======================================================
# 유저 정보 조회: DB → User 스키마로 변환
# ======================================================
def get_user(student_id: str) -> Optional[User]:
    """
    학번으로 사용자 정보를 조회합니다.
    """
    engine = _get_engine()

    with Session(engine) as session:
        statement = select(UserModel).where(UserModel.student_id == student_id)
        user = session.exec(statement).first()

        if not user:
            return None

        return User(
            student_id=user.student_id,
            college=user.college,
            current_points=user.current_points,
            created_at=user.created_at,
        )
