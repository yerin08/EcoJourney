import reflex as rx
from ..state import AppState


TOTAL_KOREAN_AVG = 10.0


# ---------------------------
# AI 솔루션 영역
# ---------------------------
def ai_solution_area():
    return rx.box(
        rx.heading("AI 솔루션 추천", size="5"),
        rx.text("EcoJourney AI가 당신의 생활 패턴을 기반으로 탄소 절감 팁을 제공합니다."),
        rx.button(
            "AI 솔루션 보기",
            background_color="#2C7A7B",
            color="white",
            padding="12px 22px",
            border_radius="10px",
            on_click=AppState.toggle_ai,
        ),
        rx.cond(
            AppState.show_ai,
            rx.box(
                rx.text("- 전기: 냉난방 온도 1°C 조정 시 최대 7% 절감."),
                rx.text("- 교통: 5km 이내는 도보/자전거로 전환."),
                rx.text("- 식품: 육류섭취량 20% 감소 → 최대 1kgCO₂e 절감."),
                padding="15px",
                background_color="rgba(0,0,0,0.05)",
                border_radius="8px",
                margin_top="10px",
            ),
        ),
        padding="20px",
    )


# ---------------------------
# 메인 리포트 UI
# ---------------------------
def report_page():
    return rx.box(
        rx.vstack(
            rx.heading("탄소 배출 리포트", size="8", margin_bottom="30px"),

            rx.grid(
                # ① Bar Chart
                rx.box(
                    rx.plotly(data=AppState.bar_chart_data),
                    padding="10px",
                ),

                # ② Pie Chart
                rx.box(
                    rx.plotly(data=AppState.pie_chart_data),
                    padding="10px",
                ),

                # ③ Badge (등급)
                rx.box(
                    rx.heading("당신의 탄소 배출 등급", size="6"),
                    rx.text(AppState.total_emission_text),
                    rx.text(AppState.badge_text, font_size="1.3em"),
                    rx.text(
                        f"한국 평균({TOTAL_KOREAN_AVG}kgCO₂e) 기준 비교 분석",
                        color="gray",
                        margin_top="10px"
                    ),
                    padding="20px",
                    background_color="rgba(0,0,0,0.05)",
                    border_radius="10px",
                ),

                # ④ AI 솔루션
                ai_solution_area(),

                columns="2",
                spacing="6",
            ),

            padding="40px",
            width="90%",
            margin="0 auto",
        )
    )