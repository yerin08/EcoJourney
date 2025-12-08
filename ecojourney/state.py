import reflex as rx
from typing import Any, Dict, List
import plotly.graph_objects as go
import plotly.express as px

class AppState(rx.State):

    # -----------------------------------
    # 공통 전역 상태
    # -----------------------------------
    all_activities: List[Dict[str, Any]] = []
    current_category: str = "교통"

    # 페이지 이동용 결과 값
    total_carbon_emission: float = 0.0
    is_report_calculated: bool = False

    show_ai: bool = False
    # -----------------------------------
    # 공통 유틸 함수들
    # -----------------------------------

    # 1) boolean 변수 setter
    def set_bool(self, key: str, value: bool):
        setattr(self, key, value)

    # 2) toggle
    def toggle_bool(self, key: str):
        setattr(self, key, not getattr(self, key))

    # 3) 여러 필드 한 번에 reset
    def reset_fields(self, keys: list):
        for k in keys:
            setattr(self, k, False)

    # 4) 입력 필드 표시 로직 공통처리
    def show_fields(self, selected_keys: list, show_keys: list, mode_key: str):
        for sel, show in zip(selected_keys, show_keys):
            setattr(self, show, getattr(self, sel))
        setattr(self, mode_key, True)

    # 5) 제출 로직 완전 공통화
    def process_submit(
        self,
        form_data: dict,
        category_name: str,
        activity_names: list,
        value_keys: list,
        unit_keys: list,
        sub_keys: list,          # subcategory 없는 경우 None
        reset_keys: list,
        redirect_path: str
    ):
        """카테고리별 제출 로직을 완전히 공통화한 함수"""

        # 기존 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != category_name
        ]

        new_items = []

        for name, vkey, ukey, skey in zip(activity_names, value_keys, unit_keys, sub_keys):

            if form_data.get(vkey):  # 값이 입력되었을 때만 저장
                item = {
                    "category": category_name,
                    "activity_type": name,
                    "value": float(form_data[vkey]),
                }
                # unit 있는 경우만 저장
                if ukey:
                    item["unit"] = form_data.get(ukey)

                if skey:   # subcategory가 있는 경우만
                    item["subcategory"] = form_data.get(skey, "기타")

                new_items.append(item)

        # 저장
        for act in new_items:
            self.all_activities.append(act)

        # ------------------------------
        # 🔥 터미널 상태 출력 (디버깅용)
        # ------------------------------
        print(f"\n[{category_name}] 저장된 데이터:", new_items, flush=True)
        print(f"→ all_activities:", self.all_activities, flush=True)
        print("-" * 50, flush=True)

        # 상태 초기화
        self.reset_fields(reset_keys)

        # 다음 페이지 이동
        return rx.redirect(redirect_path)


    # ==========================================================
    # ----------- 각 카테고리별 상태 변수 + 처리 로직 ----------
    # ==========================================================


    # ==========================================================
    # 1) 교통 (Transportation)
    # ==========================================================

    selected_car: bool = False
    selected_bus: bool = False
    selected_subway: bool = False
    selected_walk: bool = False
    selected_bike: bool = False

    show_car: bool = False
    show_bus: bool = False
    show_subway: bool = False
    show_walk: bool = False
    show_bike: bool = False

    trans_input_mode: bool = False

    # toggle 메서드
    def toggle_car(self): self.toggle_bool("selected_car")
    def toggle_bus(self): self.toggle_bool("selected_bus")
    def toggle_subway(self): self.toggle_bool("selected_subway")
    def toggle_walk(self): self.toggle_bool("selected_walk")
    def toggle_bike(self): self.toggle_bool("selected_bike")

    # 입력 필드 표시
    def show_trans_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_car", "selected_bus", "selected_subway",
                "selected_walk", "selected_bike"
            ],
            show_keys=[
                "show_car", "show_bus", "show_subway",
                "show_walk", "show_bike"
            ],
            mode_key="trans_input_mode"
        )

    # 제출 처리
    def handle_transport_submit(self, form_data: dict):
        return self.process_submit(
            form_data=form_data,
            category_name="교통",
            activity_names=["자동차", "버스", "지하철", "걷기", "자전거"],
            value_keys=["car_value", "bus_value", "subway_value", "walk_value", "bike_value"],
            unit_keys=["car_unit", "bus_unit", "subway_unit", "walk_unit", "bike_unit"],
            sub_keys=[None, None, None, None, None],  # 교통은 subcategory 없음
            reset_keys=[
                "selected_car", "selected_bus", "selected_subway",
                "selected_walk", "selected_bike",
                "show_car", "show_bus", "show_subway",
                "show_walk", "show_bike",
                "trans_input_mode"
            ],
            redirect_path="/input/food"
        )


    # ==========================================================
    # 2) 음식 (Food)
    # ==========================================================

    selected_meat: bool = False
    selected_veg: bool = False
    selected_dairy: bool = False
    selected_other: bool = False

    show_meat: bool = False
    show_veg: bool = False
    show_dairy: bool = False
    show_other: bool = False

    food_input_mode: bool = False

    # toggle
    def toggle_meat(self): self.toggle_bool("selected_meat")
    def toggle_veg(self): self.toggle_bool("selected_veg")
    def toggle_dairy(self): self.toggle_bool("selected_dairy")
    def toggle_other(self): self.toggle_bool("selected_other")

    # 필드 표시
    def show_food_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_meat", "selected_veg",
                "selected_dairy", "selected_other"
            ],
            show_keys=[
                "show_meat", "show_veg",
                "show_dairy", "show_other"
            ],
            mode_key="food_input_mode"
        )

    # 제출
    def handle_food_submit(self, form_data: dict):
        return self.process_submit(
            form_data=form_data,
            category_name="음식",
            activity_names=["고기류", "채소류", "유제품류", "기타"],
            value_keys=["meat_value", "veg_value", "dairy_value", "other_value"],
            unit_keys=["meat_unit", "veg_unit", "dairy_unit", "other_unit"],
            sub_keys=["meat_sub", "veg_sub", "dairy_sub", "other_sub"],
            reset_keys=[
                "selected_meat", "selected_veg",
                "selected_dairy", "selected_other",
                "show_meat", "show_veg",
                "show_dairy", "show_other",
                "food_input_mode"
            ],
            redirect_path="/input/clothing"
        )


    # ==========================================================
    # 3) 의류 (Clothing)
    # ==========================================================

    selected_tshirts: bool = False
    selected_jeans: bool = False
    selected_shoes: bool = False
    selected_socks: bool = False
    selected_cap: bool = False

    show_tshirts: bool = False
    show_jeans: bool = False
    show_shoes: bool = False
    show_socks: bool = False
    show_cap: bool = False

    clothing_input_mode: bool = False

    # toggle
    def toggle_tshirts(self): self.toggle_bool("selected_tshirts")
    def toggle_jeans(self): self.toggle_bool("selected_jeans")
    def toggle_shoes(self): self.toggle_bool("selected_shoes")
    def toggle_socks(self): self.toggle_bool("selected_socks")
    def toggle_cap(self): self.toggle_bool("selected_cap")

    # 필드 표시
    def show_clothing_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_tshirts", "selected_jeans",
                "selected_shoes", "selected_socks",
                "selected_cap"
            ],
            show_keys=[
                "show_tshirts", "show_jeans",
                "show_shoes", "show_socks",
                "show_cap"
            ],
            mode_key="clothing_input_mode"
        )

    # 제출
    def handle_clothing_submit(self, form_data: dict):
        return self.process_submit(
            form_data=form_data,
            category_name="의류",
            activity_names=["티셔츠", "청바지", "신발", "양말", "모자"],
            value_keys=["tshirts_value", "jeans_value", "shoes_value", "socks_value", "cap_value"],
            unit_keys=[None, None, None, None, None],
            sub_keys=["tshirts_sub", "jeans_sub", "shoes_sub", "socks_sub", "cap_sub"],
            reset_keys=[
                "selected_tshirts", "selected_jeans",
                "selected_shoes", "selected_socks",
                "selected_cap",
                "show_tshirts", "show_jeans",
                "show_shoes", "show_socks",
                "show_cap",
                "clothing_input_mode"
            ],
            redirect_path="/input/electricity"
        )


    # ==========================================================
    # 4) 전기 (Electricity)
    # ==========================================================

    selected_ac: bool = False       # 냉방기
    selected_heater: bool = False   # 난방기

    show_ac: bool = False
    show_heater: bool = False

    electricity_input_mode: bool = False

    # toggle
    def toggle_ac(self): 
        self.toggle_bool("selected_ac")

    def toggle_heater(self): 
        self.toggle_bool("selected_heater")

    # 입력 필드 표시
    def show_electricity_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_ac",
                "selected_heater"
            ],
            show_keys=[
                "show_ac",
                "show_heater"
            ],
            mode_key="electricity_input_mode"
    )

    # 제출 로직
    def handle_electricity_submit(self, form_data: dict):
        return self.process_submit(
            form_data=form_data,
            category_name="전기",
            activity_names=["냉방기", "난방기"],
            value_keys=["ac_value", "heater_value"],

            # 단위는 "시간" 고정 → UI가 form_data에 넣도록 하면 OK
            # 또는 unit_keys=[None, None] 로 두고 unit을 제외할 수도 있음.
            unit_keys=[None, None],        # ← 단위 없음
            sub_keys=[None, None],         # ← 서브카테고리 없음

            reset_keys=[
                "selected_ac", "selected_heater",
                "show_ac", "show_heater",
                "electricity_input_mode"
            ],
            redirect_path="/input/water"    # 다음 페이지로 이동
    )

    # ==========================================================
    # 5) 물 (Water)
    # ==========================================================

    selected_shower: bool = False
    selected_dish: bool = False
    selected_laundry: bool = False

    show_shower: bool = False
    show_dish: bool = False
    show_laundry: bool = False

    water_input_mode: bool = False

    # toggle
    def toggle_shower(self): self.toggle_bool("selected_shower")
    def toggle_dish(self): self.toggle_bool("selected_dish")
    def toggle_laundry(self): self.toggle_bool("selected_laundry")

    # 입력 필드 표시
    def show_water_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_shower",
                "selected_dish",
                "selected_laundry",
            ],
            show_keys=[
                "show_shower",
                "show_dish",
                "show_laundry",
            ],
            mode_key="water_input_mode"
        )

    # 제출 처리
    def handle_water_submit(self, form_data: dict):

        # 기존 물 데이터 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "물"
        ]

        new_items = []

        # 샤워 — unit(회/분) 선택 + value
        if form_data.get("shower_value"):
            new_items.append({
                "category": "물",
                "activity_type": "샤워",
                "value": float(form_data["shower_value"]),
                "unit": form_data.get("shower_unit", "회")
            })

        # 설거지
        if form_data.get("dish_value"):
            new_items.append({
                "category": "물",
                "activity_type": "설거지",
                "value": float(form_data["dish_value"]),
                "unit": "회"
            })

        # 세탁
        if form_data.get("laundry_value"):
            new_items.append({
                "category": "물",
                "activity_type": "세탁",
                "value": float(form_data["laundry_value"]),
                "unit": "회"
            })

        # 저장
        for item in new_items:
            self.all_activities.append(item)

        print("\n[물] 저장된 데이터:", new_items, flush=True)
        print("→ all_activities:", self.all_activities, flush=True)
        print("-" * 50, flush=True)

        # 상태 초기화
        self.reset_fields([
            "selected_shower", "selected_dish", "selected_laundry",
            "show_shower", "show_dish", "show_laundry",
            "water_input_mode"
        ])

        return rx.redirect("/input/waste")

    # ==========================================================
    # 6) 쓰레기 (Waste)
    # ==========================================================

    selected_general: bool = False
    selected_plastic: bool = False
    selected_paper: bool = False
    selected_glass: bool = False
    selected_can: bool = False

    show_general: bool = False
    show_plastic: bool = False
    show_paper: bool = False
    show_glass: bool = False
    show_can: bool = False

    waste_input_mode: bool = False

    # toggle
    def toggle_general(self): self.toggle_bool("selected_general")
    def toggle_plastic(self): self.toggle_bool("selected_plastic")
    def toggle_paper(self): self.toggle_bool("selected_paper")
    def toggle_glass(self): self.toggle_bool("selected_glass")
    def toggle_can(self): self.toggle_bool("selected_can")

    # 입력 필드 표시
    def show_waste_input_fields(self):
        self.show_fields(
            selected_keys=[
                "selected_general",
                "selected_plastic",
                "selected_paper",
                "selected_glass",
                "selected_can",
            ],
            show_keys=[
                "show_general",
                "show_plastic",
                "show_paper",
                "show_glass",
                "show_can",
            ],
            mode_key="waste_input_mode"
        )

    # 제출 로직
    def handle_waste_submit(self, form_data: dict):

        # 기존 쓰레기 카테고리 제거
        self.all_activities = [
            act for act in self.all_activities
            if act.get("category") != "쓰레기"
        ]

        new_items = []

        # 공통 항목명
        names = ["일반쓰레기", "플라스틱", "종이", "유리", "캔"]
        value_keys = ["general_value", "plastic_value", "paper_value", "glass_value", "can_value"]
        unit_keys  = ["general_unit", "plastic_unit", "paper_unit", "glass_unit", "can_unit"]

        for name, vkey, ukey in zip(names, value_keys, unit_keys):
            if form_data.get(vkey):
                new_items.append({
                    "category": "쓰레기",
                    "activity_type": name,
                    "value": float(form_data[vkey]),
                    "unit": form_data.get(ukey, "개")
                })

        # 저장
        for item in new_items:
            self.all_activities.append(item)

        print("\n[쓰레기] 저장된 데이터:", new_items, flush=True)
        print("→ all_activities:", self.all_activities, flush=True)
        print("-" * 50, flush=True)

        # 상태 초기화
        self.reset_fields([
            "selected_general", "selected_plastic", "selected_paper",
            "selected_glass", "selected_can",
            "show_general", "show_plastic", "show_paper",
            "show_glass", "show_can",
            "waste_input_mode"
        ])

        return rx.redirect("/report")

    # ==========================================================
    # 리포트 페이지용 Computed Variables
    # ==========================================================

    # 카테고리별 평균 (한국 기준)
    _category_avg: Dict[str, float] = {
        "교통": 3.5,
        "음식": 2.8,
        "전기": 2.2,
        "물": 0.3,
        "의류": 0.5,
        "쓰레기": 0.7,
    }

    def toggle_ai(self):
        """AI 솔루션 표시 토글"""
        self.show_ai = not self.show_ai

    @rx.var
    def category_sums(self) -> Dict[str, float]:
        """카테고리별 탄소 배출 합계 계산"""
        result: Dict[str, float] = {}
        for act in self.all_activities:
            cat = act.get("category", "기타")
            # 임시로 value를 탄소 배출량으로 사용 (실제 계산 로직 필요시 수정)
            val = float(act.get("carbon_emission", act.get("value", 0)))
            result[cat] = result.get(cat, 0) + val
        return result

    @rx.var
    def total_emission(self) -> float:
        """총 탄소 배출량"""
        return sum(self.category_sums.values())

    @rx.var
    def total_emission_text(self) -> str:
        """총 배출량 텍스트"""
        return f"총 배출량: {self.total_emission:.2f} kgCO₂e"

    @rx.var
    def badge_text(self) -> str:
        """배출 등급 텍스트"""
        value = self.total_emission
        if value < 5:
            return "등급: 🌱 Beginner Level (매우 적음)"
        elif value < 10:
            return "등급: 🌿 Eco Learner (평균 이하)"
        elif value < 15:
            return "등급: 🌲 Sustainable Member (약간 높음)"
        elif value < 20:
            return "등급: 🌳 Green Guardian (높음)"
        else:
            return "등급: 🔥 Carbon Overload (매우 높음)"

    @rx.var
    def chart_categories(self) -> List[str]:
        """차트용 카테고리 목록"""
        if self.category_sums:
            return list(self.category_sums.keys())
        return ["데이터 없음"]

    @rx.var
    def chart_user_values(self) -> List[float]:
        """차트용 사용자 배출량"""
        if self.category_sums:
            return list(self.category_sums.values())
        return [0]

    @rx.var
    def chart_avg_values(self) -> List[float]:
        """차트용 한국 평균값"""
        return [self._category_avg.get(cat, 0) for cat in self.chart_categories]

    @rx.var
    def bar_chart_data(self) -> go.Figure:
        """Bar Chart Figure - 호버 툴팁 스타일"""
        fig = go.Figure()
        
        # 사용자 배출량 (초록색)
        fig.add_trace(go.Bar(
            name="사용자",
            x=self.chart_categories,
            y=self.chart_user_values,
            marker_color="#2E8B57",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "사용자 배출량: %{y:.2f} kgCO₂e<br>"
                "<extra></extra>"
            ),
        ))
        
        # 한국 평균 (주황색)
        fig.add_trace(go.Bar(
            name="평균",
            x=self.chart_categories,
            y=self.chart_avg_values,
            marker_color="#D2691E",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "평균 배출량: %{y:.2f} kgCO₂e<br>"
                "<extra></extra>"
            ),
        ))
        
        fig.update_layout(
            barmode='group',
            title=dict(
                text="카테고리별 탄소 배출 비교",
                font=dict(size=20, color="#2E8B57"),
                x=0.5,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                tickfont=dict(size=14),
                showgrid=False,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                zeroline=True,
                zerolinecolor="gray",
            ),
            bargap=0.15,
            bargroupgap=0.1,
            margin=dict(t=80, b=60),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial",
                bordercolor="gray",
            ),
        )
        
        return fig

    @rx.var
    def pie_chart_data(self) -> go.Figure:
        """Pie Chart Figure"""
        fig = px.pie(
            names=self.chart_categories,
            values=self.chart_user_values,
            title="탄소 배출 비중",
            hole=0.4
        )
        return fig