import reflex as rx
from typing import Dict, List, Any

# 탄소 배출량 데이터를 저장할 딕셔너리 구조 정의
# 예: {"activity_type": "지하철", "value": 10.5, "unit": "km", "carbon_emission": 0.5}
CarbonActivity = Dict[str, Any]

class AppState(rx.State):
    """
    EcoJourney의 전역 상태를 관리하는 클래스.
    사용자 입력, 계산 결과, 화면 흐름 등을 저장
    """

    # 1. 화면 흐름 제어 변수
    # 현재 사용자가 어떤 카테고리 입력 페이지에 있는지 추적
    # 'transportation, 'food, 'clothing', 'waste', 'electricity', 'water', 'report' 순
    current_category: str = "transportation"

    # 카테고리 순서 정의 (라우팅 이동 및 다음 버튼 처리에 사용)
    CATEGORY_ORDER: List[str] = [
        "transportation",
        "food",
        "clothing",
        "waste",
        "electricity",
        "water"
    ]

    # 2. 카테고리별 사용자 입력값 저장소
    # 모든 카테고리의 활동 데이터를 리스트 형태로 저장
    all_activities: List[CarbonActivity] = []

    # 카테고리별 입력 임시 저장소 (현재 페이지의 입력값을 다음 페이지로 넘기기 전 임시 저장)
    transport_inputs: List[Dict[str, Any]] = [] # 예: [{"type": "Bus", "value": 5, "unit": "km"}, ...]
    food_inputs: List[Dict[str, Any]] = []
    clothing_inputs: List[Dict[str, Any]] = []
    waste_inputs: List[Dict[str, Any]] = []
    electricity_inputs: List[Dict[str, Any]] = []
    water_inputs: List[Dict[str, Any]] = []

    # 3. 결과 리포트 데이터
    total_carbon_emission: float = 0.0
    category_breakdown: Dict[str, float] = {}
    is_report_calculated: bool = False

    # 4. 라우팅 처리 함수 (다음 버튼 클릭 시 다음 카테고리로 이동)
    def next_category(self):
        """
        현재 카테고리 입력 완료 후 다음 페이지로 이동
        마지막 카테고리 후에는 리포트 페이지로 이동
        """
        try:
            current_index = self.CATEGORY_ORDER.index(self.current_category)

            if current_index < len(self.CATEGORY_ORDER) - 1:
                # 다음 카테고리로 이동
                next_category_name = self.CATEGORY_ORDER[current_index + 1]
                self.current_category = next_category_name
                return rx.redirect(f"/input/{next_category_name}")
            else:
                # 마지막 카테고리 후 리포트 페이지 이동
                self.current_category = "report"
                return rx.redirect("/report")
            
        except ValueError:
            # current_category가 CATEGORY_ORDER에 없는 경우 (예: 초기 intro 페이지)
            return rx.redirect("input/transportation")
        
    # TODO: 이전 페이지로 돌아가는 back_category 함수 구현 필요
    # TODO: 입력 값을 all_activities에 추가하고 carbon_emission을 계산하는 함수 구현 필요