import reflex as rx
from ..state import AppState # EcoJourney 모듈 상위 state.py에서 AppState를 가져옴

def home_page():
    return rx.center(
        rx.vstack(
            rx.heading("EcoJourney", size="9", color="green.700"),

            rx.text(
                "당신의 하루가 지구의 내일이 됩니다. 🌍",
                size="6",
                margin_bottom="20px",
                color="gray.600"
            ),

            rx.button(
                "탄소 발자국 측정 시작하기 🚀",
                # AppState의 go_to_intro 함수 사용
                on_click=AppState.go_to_intro,
                size="3",
                color_scheme="green",
                padding="15px 30px",
                border_radius="lg",
                _hover={"opacity": 0.8}
            ),
            spacing="5",
            align="center",
        ),
        width="100%",
        height="100vh",
        padding_top="100px",
    )