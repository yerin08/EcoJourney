# state.py

import reflex as rx
from typing import Dict, List, Any, Optional
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# CATEGORY_CONFIG: 모든 카테고리 데이터를 담는 핵심 딕셔너리
# NOTE: 이 딕셔너리의 순서(keys)는 페이지 이동 순서를 결정합니다.
CATEGORY_CONFIG = {
    "교통": {
        "path": "transportation", # URL 경로 ("/input/transportation")에 사용
        "description": "오늘의 교통 수단 이용량(거리 또는 시간)을 입력해주세요.",
        "activities": ["자동차", "지하철", "버스", "걷기", "자전거"],
        "units": ["km", "분"],
        "inputs_key": "transport_inputs"
    },
    "식품": {
        "path": "food",
        "description": "오늘 섭취한 주요 식품 카테고리를 입력해주세요.",
        "activities": ["육류", "채소/과일", "가공식품", "유제품"],
        "units": ["g", "회"],
        "inputs_key": "food_inputs"
    },
    "의류": {
        "path": "clothing",
        "description": "오늘 쇼핑한 의류 및 잡화의 종류와 개수를 입력해주세요.",
        "activities": ["상의", "하의", "신발", "가방/잡화"],
        "units": ["개"],
        "inputs_key": "clothing_inputs"
    }
}

CATEGORY_ORDER = list(CATEGORY_CONFIG.keys())

# 💡 서비스 함수를 직접 호출 (FastAPI 라우터 불필요)
# State에서 직접 서비스 로직을 호출합니다

# 탄소 배출량 데이터를 저장할 딕셔너리 구조 정의
# 필수 필드: category, activity_type, value, unit
CarbonActivity = Dict[str, Any]

TRANSPORT_LIST = ["자동차", "버스", "지하철", "걷기", "자전거"]

class AppState(rx.State):
    """
    EcoJourney 앱의 전역 상태를 관리하는 클래스.
    """
    current_category: str = "교통"
    
    # 2. 카테고리별 사용자 입력값 저장소
    all_activities: List[CarbonActivity] = []

    # ---------- 교통수단 선택 상태 ----------
    # 1단계: 버튼으로 선택 (selected_XXX)
    selected_car: bool = False
    selected_bus: bool = False
    selected_subway: bool = False
    selected_walk: bool = False
    selected_bike: bool = False
    
    # 2단계: 입력하기 버튼 누른 후 입력 필드 표시 (show_XXX)
    show_car: bool = False
    show_bus: bool = False
    show_subway: bool = False
    show_walk: bool = False
    show_bike: bool = False
    
    # 입력 모드 (입력하기 버튼 눌렀는지)
    input_mode: bool = False

    # 카테고리별 입력 임시 저장소 (현재 페이지의 입력값)
    # transport_inputs: List[Dict[str, Any]] = []
    # food_inputs: List[Dict[str, Any]] = []
    # clothing_inputs: List[Dict[str, Any]] = []
    # electricity_inputs: List[Dict[str, Any]] = []
    # water_inputs: List[Dict[str, Any]] = []
    # waste_inputs: List[Dict[str, Any]] = []
    
    # UI 및 오류 메시지
    # is_loading: bool = False
    # error_message: str = ""
    
    # 결과 리포트 데이터
    total_carbon_emission: float = 0.0
    # category_breakdown: Dict[str, float] = {}
    is_report_calculated: bool = False

    # ------------------------------
    # 1단계: 버튼 토글 (선택/해제)
    # ------------------------------
    
    def toggle_car(self):
        self.selected_car = not self.selected_car
        print(f"자동차 선택: {self.selected_car}", flush=True)
    
    def toggle_bus(self):
        self.selected_bus = not self.selected_bus
        print(f"버스 선택: {self.selected_bus}", flush=True)
    
    def toggle_subway(self):
        self.selected_subway = not self.selected_subway
        print(f"지하철 선택: {self.selected_subway}", flush=True)
    
    def toggle_walk(self):
        self.selected_walk = not self.selected_walk
        print(f"걷기 선택: {self.selected_walk}", flush=True)
    
    def toggle_bike(self):
        self.selected_bike = not self.selected_bike
        print(f"자전거 선택: {self.selected_bike}", flush=True)

    # ------------------------------
    # 2단계: 입력하기 버튼 클릭 -> 입력 필드 표시
    # ------------------------------
    
    def show_input_fields(self):
        """선택된 항목들의 입력 필드를 표시"""
        self.show_car = self.selected_car
        self.show_bus = self.selected_bus
        self.show_subway = self.selected_subway
        self.show_walk = self.selected_walk
        self.show_bike = self.selected_bike
        self.input_mode = True
        print(f"입력 모드 활성화! 자동차:{self.show_car}, 버스:{self.show_bus}, 지하철:{self.show_subway}, 걷기:{self.show_walk}, 자전거:{self.show_bike}", flush=True)

    # ------------------------------
    # 3단계: 데이터 제출 및 다음 페이지 이동
    # ------------------------------
    
    def handle_transport_submit(self, form_data: dict):
        """교통 입력값 폼 제출 -> 데이터 저장 -> 다음 페이지 이동"""
        print(f"교통 데이터 수신: {form_data}", flush=True)
        
        # 기존 교통 데이터 제거
        self.all_activities = [
            act for act in self.all_activities 
            if act.get("category") != "교통"
        ]
        
        # 선택된 교통수단 데이터 저장
        transport_data = []
        
        if self.show_car and form_data.get("car_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "자동차",
                "value": float(form_data.get("car_value", 0)),
                "unit": form_data.get("car_unit", "km"),
            })
        
        if self.show_bus and form_data.get("bus_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "버스",
                "value": float(form_data.get("bus_value", 0)),
                "unit": form_data.get("bus_unit", "km"),
            })
        
        if self.show_subway and form_data.get("subway_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "지하철",
                "value": float(form_data.get("subway_value", 0)),
                "unit": form_data.get("subway_unit", "km"),
            })
        
        if self.show_walk and form_data.get("walk_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "걷기",
                "value": float(form_data.get("walk_value", 0)),
                "unit": form_data.get("walk_unit", "km"),
            })
        
        if self.show_bike and form_data.get("bike_value"):
            transport_data.append({
                "category": "교통",
                "activity_type": "자전거",
                "value": float(form_data.get("bike_value", 0)),
                "unit": form_data.get("bike_unit", "km"),
            })
        
        # 전체 활동 목록에 추가
        self.all_activities = self.all_activities + transport_data
        
        print(f"저장된 교통 데이터: {transport_data}", flush=True)
        
        # 다음 페이지로 이동
        return rx.redirect("/input/food")


    # --- 헬퍼 함수 및 라우팅 로직 ---

    # def get_current_input_list(self) -> List[Dict[str, Any]]:
    #     """현재 카테고리에 해당하는 입력 리스트를 반환합니다."""
    #     if self.current_category == "교통":
    #         return self.transport_inputs
    #     elif self.current_category == "식품":
    #         return self.food_inputs
    #     elif self.current_category == "의류":
    #         return self.clothing_inputs
    #     elif self.current_category == "전기":
    #         return self.electricity_inputs
    #     elif self.current_category == "물":
    #         return self.water_inputs
    #     elif self.current_category == "쓰레기":
    #         return self.waste_inputs
    #     return []

    # def set_current_input_list(self, new_list: List[Dict[str, Any]]):
    #     """현재 카테고리에 해당하는 입력 리스트를 설정합니다."""
    #     if self.current_category == "교통":
    #         self.transport_inputs = new_list
    #     elif self.current_category == "식품":
    #         self.food_inputs = new_list
    #     elif self.current_category == "의류":
    #         self.clothing_inputs = new_list
    #     elif self.current_category == "전기":
    #         self.electricity_inputs = new_list
    #     elif self.current_category == "물":
    #         self.water_inputs = new_list
    #     elif self.current_category == "쓰레기":
    #         self.waste_inputs = new_list
        
    # def set_current_category(self, category_name: str):
    #     """ URL 경로에 따라 현재 카테고리를 설정"""
    #     if category_name in self.CATEGORY_ORDER:
    #         self.current_category = category_name
    #         logger.info(f"State: current_category 설정됨 -> {category_name}")
    #     else:
    #         logger.error(f"State:존재하지 않는 카테고리 시도: {category_name}")
    
    # def _get_category_path(self, category_name: str) -> str:
    #     """카테고리 이름을 URL 경로로 조회합니다."""
    #     # 예: '교통' -> 'transportation' (URL에서 영문 사용 가정)
    #     return self.CATEGORY_CONFIG.get(category_name, {}).get("path", "")

    # --- 5. 핵심 라우팅 및 액션 함수 ---
    
    # def back_category(self):
        # """이전 카테고리 입력 페이지로 돌아갑니다."""
        # self.error_message = "" # 오류 메시지 초기화
        
        # try:
            # current_index = self.CATEGORY_ORDER.index(self.current_category)
            
            # if current_index > 0:
                # 이전 카테고리로 이동
                # prev_category_name = self.CATEGORY_ORDER[current_index - 1]
                # self.current_category = prev_category_name
                # prev_path = self._get_category_path(prev_category_name)
                # return rx.redirect(f"/input/{prev_path}")
            # else:
                # 첫 카테고리에서는 소개 페이지로 이동
                # self.current_category = ""
                # return rx.redirect("/intro")
                
        # except ValueError:
            # 오류 방지
            # return rx.redirect("/intro")
        
    # async def save_and_proceed(self, current_inputs: List[Dict[str, Any]]):
    #     """
    #     현재 페이지의 입력을 처리하고, API를 호출하여 계산 후 다음 페이지로 이동합니다.
    #     """
    #     logger.info("=" * 50)
    #     logger.info("💾 save_and_proceed 함수 호출됨!")
    #     print("=" * 50, flush=True)
    #     self.is_loading = True
    #     self.error_message = ""

    #     # 1. 이전 활동 저장소에서 현재 카테고리 활동을 제거
    #     self.all_activities = [
    #     act for act in self.all_activities if act.get("category") != self.current_category
    #     ]

    #     # 2. 유효한 입력만 필터링하고 탄소 배출량 계산 (로직 유지)
    #     valid_activities = []
    #     for inp in current_inputs:
    #         if inp.get("value", 0.0) > 0:
    #             inp["category"] = self.current_category
    #             carbon_kg = await self._calculate_emission_for_activity(inp)
    #             if carbon_kg is not None:
    #                 inp["carbon_emission_kg"] = carbon_kg
    #                 valid_activities.append(inp)
    #             else:
    #                 self.is_loading = False
    #                 return 

    #     # 3. 전체 활동 목록에 추가
    #     self.all_activities.extend(valid_activities)

    #     # 4. 다음 페이지로 이동 (UI에서 직접 처리하므로, 여기서는 이동 경로만 반환)
    #     self.is_loading = False
 
    #     # 💡 다음 페이지 경로를 반환합니다. (호출하는 UI에서 rx.redirect에 사용)
    #     config = self.CATEGORY_CONFIG.get(self.current_category, {})
    #     next_path = config.get("next_path", "/report") # 마지막 카테고리가 아니라면 다음 경로, 아니면 /report
    #     return rx.redirect(next_path) # 👈 직접 리다이렉트 실행
    
    # # 임시 더미 함수 (추후 슬롯 추가 함수로 구현 예정)
    # def add_input_slot(self, activity_type: str):
    #     pass
            
    # # --- 6. API 호출 및 데이터 저장 로직 ---
    
    # async def _calculate_emission_for_activity(self, activity: CarbonActivity) -> Optional[float]:
    #     """서비스 함수를 직접 호출하여 탄소 배출량을 계산합니다."""
        
    #     try:
    #         # 서비스 함수를 직접 호출
    #         from service.carbon_calculator import calculate_carbon_emission
            
    #         result = calculate_carbon_emission(
    #             category=activity.get("category"),
    #             activity_type=activity.get("activity_type"),
    #             value=activity.get("value"),
    #             unit=activity.get("unit"),
    #             sub_category=activity.get("sub_category", None)
    #         )
            
    #         return result.get("carbon_emission_kg")
                
    #     except Exception as e:
    #         self.error_message = f"계산 오류: {e}"
    #         return None

        
    # # --- 7. 최종 리포트 계산 함수 ---

    # async def calculate_report(self):
    #     """
    #     저장된 모든 활동을 바탕으로 최종 리포트 데이터를 계산하고 리포트 페이지로 이동합니다.
    #     """
    #     logger.info("=" * 50)
    #     logger.info("📊 calculate_report 함수 호출됨!")
    #     logger.info(f"활동 개수: {len(self.all_activities)}")
    #     print("=" * 50, flush=True)
    #     print(f"📊 calculate_report 함수 호출됨! 활동: {len(self.all_activities)}개", flush=True)
    #     print("=" * 50, flush=True)
    #     self.is_loading = True
    #     self.error_message = ""
        
    #     total = 0.0
    #     breakdown = {cat: 0.0 for cat in self.CATEGORY_ORDER}
        
    #     for activity in self.all_activities:
    #         emission = activity.get("carbon_emission_kg", 0.0)
    #         category = activity.get("category")
            
    #         total += emission
    #         if category in breakdown:
    #             breakdown[category] += emission
        
    #     self.total_carbon_emission = total
    #     self.category_breakdown = breakdown
    #     self.is_report_calculated = True
        
    #     self.is_loading = False
    #     return rx.redirect("/report")