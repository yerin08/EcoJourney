# state.py

import reflex as rx
import httpx
from typing import Dict, List, Any, Optional
from json.decoder import JSONDecodeError

# 💡 백엔드 FastAPI 서버의 주소.
# 로컬 개발 환경에서는 일반적으로 이 주소를 사용합니다.
BASE_URL = "http://localhost:8001"

# 탄소 배출량 데이터를 저장할 딕셔너리 구조 정의
# 필수 필드: category, activity_type, value, unit
CarbonActivity = Dict[str, Any]

class AppState(rx.State):
    """
    EcoJourney 앱의 전역 상태를 관리하는 클래스.
    """
    
    # 1. 화면 흐름 제어 변수
    current_category: str = "transportation" 
    # NOTE: 카테고리 이름은 FastAPI 백엔드의 데이터와 일치해야 합니다.
    CATEGORY_ORDER: List[str] = [
        "교통", "식품", "의류", "쓰레기", "전기", "물" 
    ]
    
    # 2. 카테고리별 사용자 입력값 저장소
    all_activities: List[CarbonActivity] = []
    
    # 카테고리별 입력 임시 저장소 (현재 페이지의 입력값)
    transport_inputs: List[Dict[str, Any]] = [] 
    food_inputs: List[Dict[str, Any]] = []
    clothing_inputs: List[Dict[str, Any]] = []
    electricity_inputs: List[Dict[str, Any]] = []
    water_inputs: List[Dict[str, Any]] = []
    waste_inputs: List[Dict[str, Any]] = []
    
    # UI 및 오류 메시지
    is_loading: bool = False
    error_message: str = ""
    
    # 3. 결과 리포트 데이터
    total_carbon_emission: float = 0.0
    category_breakdown: Dict[str, float] = {}
    is_report_calculated: bool = False
    
    # --- 4. 헬퍼 함수 및 라우팅 로직 ---

    def get_current_input_list(self) -> List[Dict[str, Any]]:
        """현재 카테고리에 해당하는 입력 리스트를 반환합니다."""
        if self.current_category == "교통":
            return self.transport_inputs
        elif self.current_category == "식품":
            return self.food_inputs
        elif self.current_category == "의류":
            return self.clothing_inputs
        elif self.current_category == "전기":
            return self.electricity_inputs
        elif self.current_category == "물":
            return self.water_inputs
        elif self.current_category == "쓰레기":
            return self.waste_inputs
        return []

    def set_current_input_list(self, new_list: List[Dict[str, Any]]):
        """현재 카테고리에 해당하는 입력 리스트를 설정합니다."""
        if self.current_category == "교통":
            self.transport_inputs = new_list
        elif self.current_category == "식품":
            self.food_inputs = new_list
        elif self.current_category == "의류":
            self.clothing_inputs = new_list
        # ... (나머지 카테고리도 필요하다면 구현)
        
    def _get_category_path(self, category: str) -> str:
        """카테고리 이름을 URL 경로로 변환합니다."""
        # 예: '교통' -> 'transportation' (URL에서 영문 사용 가정)
        mapping = {
            "교통": "transportation", "식품": "food", "의류": "clothing",
            "쓰레기": "waste", "전기": "electricity", "물": "water"
        }
        return mapping.get(category, category)

    # --- 5. 핵심 라우팅 및 액션 함수 ---

    def go_to_intro(self):
        """홈 화면에서 소개 화면으로 이동"""
        return rx.redirect("/intro")
    
    def next_category(self):
        """
        다음 카테고리 페이지 또는 리포트 페이지로 이동합니다.
        """
        self.error_message = "" # 오류 메시지 초기화
        
        try:
            current_index = self.CATEGORY_ORDER.index(self.current_category)
            
            if current_index < len(self.CATEGORY_ORDER) - 1:
                # 다음 카테고리로 이동
                next_category_name = self.CATEGORY_ORDER[current_index + 1]
                self.current_category = next_category_name
                next_path = self._get_category_path(next_category_name)
                return rx.redirect(f"/input/{next_path}")
            else:
                # 마지막 카테고리 후 리포트 페이지로 이동
                self.current_category = "report"
                return self.calculate_report()
                
        except ValueError:
            # 현재 카테고리가 목록에 없는 경우 (오류 방지)
            return rx.redirect("/intro")
    
    def back_category(self):
        """이전 카테고리 입력 페이지로 돌아갑니다."""
        self.error_message = "" # 오류 메시지 초기화
        
        try:
            current_index = self.CATEGORY_ORDER.index(self.current_category)
            
            if current_index > 0:
                # 이전 카테고리로 이동
                prev_category_name = self.CATEGORY_ORDER[current_index - 1]
                self.current_category = prev_category_name
                prev_path = self._get_category_path(prev_category_name)
                return rx.redirect(f"/input/{prev_path}")
            else:
                # 첫 카테고리에서는 소개 페이지로 이동
                self.current_category = ""
                return rx.redirect("/intro")
                
        except ValueError:
            # 오류 방지
            return rx.redirect("/intro")
            
    # --- 6. API 호출 및 데이터 저장 로직 ---
    
    async def _calculate_emission_for_activity(self, activity: CarbonActivity) -> Optional[float]:
        """FastAPI 서버에 활동 데이터를 전송하고 탄소 배출량을 받아옵니다."""
        
        # FastAPI의 CarbonActivity 모델에 맞게 데이터 준비
        payload = {
            "category": activity.get("category"),
            "activity_type": activity.get("activity_type"),
            "value": activity.get("value"),
            "unit": activity.get("unit"),
            "sub_category": activity.get("sub_category", None)
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{BASE_URL}/calculate", 
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("carbon_emission_kg")
                
            except httpx.RequestError as e:
                self.error_message = f"API 연결 오류: 서버가 실행 중인지 확인하세요. ({e})"
                return None
            except JSONDecodeError:
                self.error_message = f"API 응답 형식 오류: {response.text}"
                return None
            except Exception as e:
                self.error_message = f"계산 오류: {e}"
                return None

    async def save_and_proceed(self, current_inputs: List[Dict[str, Any]]):
        """
        현재 페이지의 입력을 처리하고, API를 호출하여 계산 후 다음 페이지로 이동합니다.
        """
        self.is_loading = True
        self.error_message = ""
        
        # 1. 이전 활동 저장소에서 현재 카테고리 활동을 제거
        self.all_activities = [
            act for act in self.all_activities if act.get("category") != self.current_category
        ]
        
        # 2. 유효한 입력만 필터링하고 탄소 배출량 계산
        valid_activities = []
        
        for inp in current_inputs:
            # 값(value)이 0보다 큰 유효한 입력만 처리
            if inp.get("value", 0.0) > 0:
                inp["category"] = self.current_category
                
                # 🚨 비동기 API 호출 및 계산
                carbon_kg = await self._calculate_emission_for_activity(inp)
                
                if carbon_kg is not None:
                    inp["carbon_emission_kg"] = carbon_kg
                    valid_activities.append(inp)
                else:
                    # 계산 실패 시 로딩 해제 후 함수 종료 (에러 메시지는 _calculate_emission_for_activity에서 설정됨)
                    self.is_loading = False
                    return 
                    
        # 3. 전체 활동 목록에 추가
        self.all_activities.extend(valid_activities)
        
        # 4. 다음 페이지로 이동
        self.is_loading = False
        return self.next_category()
        
    def skip_and_proceed(self):
        """입력 없이 다음 페이지로 이동합니다."""
        # 입력값 저장 없이 다음 페이지로 이동
        return self.next_category()
        
    # --- 7. 최종 리포트 계산 함수 ---

    async def calculate_report(self):
        """
        저장된 모든 활동을 바탕으로 최종 리포트 데이터를 계산하고 리포트 페이지로 이동합니다.
        """
        self.is_loading = True
        self.error_message = ""
        
        total = 0.0
        breakdown = {cat: 0.0 for cat in self.CATEGORY_ORDER}
        
        for activity in self.all_activities:
            emission = activity.get("carbon_emission_kg", 0.0)
            category = activity.get("category")
            
            total += emission
            if category in breakdown:
                breakdown[category] += emission
        
        self.total_carbon_emission = total
        self.category_breakdown = breakdown
        self.is_report_calculated = True
        
        self.is_loading = False
        return rx.redirect("/report")