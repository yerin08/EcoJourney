# water.py

import reflex as rx
from ..state import AppState

UNITS = ["분", "회"]

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.button(
                "EcoJourney",
                on_click=rx.redirect("/"),
                background_color="transparent",
                color="white",
                font_size="1.5em",
                font_weight="bold",
                padding="0",
                border="none",
                border_radius="8px",
                cursor="pointer",
            ),
            justify="between",
            align="center",
            padding="1em 2em",
        ),
        width="100%",
        position="relative",
        z_index="10",
        background_color="transparent",
    )


def background_video() -> rx.Component:
    return rx.box(
        rx.html(
            """
            <video autoplay loop muted playsinline 
                src="/transportation_background.mp4"
                style='
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    z-index: -2; 
                    filter: brightness(0.65);'
            />
            """
        ),
        width="100%",
        height="100%",
        z_index="-2",
    )


# 공통 버튼 UI
def water_button(label: str, is_selected, on_click):

    disabled = AppState.water_input_mode

    base = rx.hstack(rx.text(label), spacing="2")

    selected_bg = rx.cond(disabled, "rgba(0,0,0,0.2)", "rgba(0,0,0,0.52)")
    default_bg  = rx.cond(disabled, "rgba(0,0,0,0.1)", "rgba(0,0,0,0.22)")

    cursor_style = rx.cond(disabled, "not-allowed", "pointer")

    return rx.button(
        base,
        on_click=rx.cond(disabled, None, on_click),
        disabled=disabled,
        background_color=rx.cond(is_selected, selected_bg, default_bg),
        border_radius="40px",
        padding=rx.cond(is_selected, "27px 40px", "24px 40px"),
        color="rgba(255,255,255,0.8)",
        border="4px solid rgba(255,255,255,0.5)",
        font_size="1.1em",
        font_weight="bold",
        cursor=cursor_style,
        transition="all 0.2s",
    )


# 입력 필드 UI
def shower_input_field():
    return rx.box(
        rx.hstack(
            rx.text(
                "샤워",
                font_weight="bold",
                min_width="80px",
                color="rgba(255, 255, 255, 0.8)",
            ),

            # 🔥 단위 select (회 / 분)
            rx.select(
                ["회", "분"],
                placeholder="단위",
                name="shower_unit",
                width="100px",
                background_color="rgba(255,255,255,0.9)",
                color="black",
                border_radius="8px",
            ),

            # 값 입력
            rx.input(
                placeholder="숫자 입력",
                type="number",
                name="shower_value",
                width="140px",
                background_color="rgba(255,255,255,0.9)",
                color="black",
                border_radius="8px",
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="16px 20px",
        border_radius="16px",
        background_color="rgba(0, 0, 0, 0.1)",
        border="2px solid rgba(255, 255, 255, 0.5)",
        margin_y="10px",
        width="100%",
        max_width="400px",
    )

def water_input_field(label: str, value_name: str):
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="80px",
                color="rgba(255,255,255,0.8)",
            ),

            rx.input(
                placeholder="횟수 입력",
                type="number",
                name=value_name,
                width="140px",
                background_color="rgba(255,255,255,0.9)",
                color="black",
                border_radius="8px",
            ),
            spacing="4",
            align="center",
            justify="center",
        ),
        padding="16px 20px",
        border_radius="16px",
        background_color="rgba(0,0,0,0.1)",
        border="2px solid rgba(255,255,255,0.5)",
        margin_y="10px",
        width="100%",
        max_width="350px",
    )


# 메인 페이지
def water_page():
    return rx.box(
        background_video(),
        header(),
        rx.container(
            rx.vstack(
                rx.heading("물 사용 입력", size="7", color="white"),
                rx.text(
                    "오늘 사용한 물 관련 활동을 모두 선택해주세요",
                    color="rgba(255,255,255,0.8)",
                    font_size="1.1em",
                ),

                rx.box(height="30px"),

                # 선택 버튼
                rx.hstack(
                    water_button("샤워", AppState.selected_shower, AppState.toggle_shower),
                    water_button("설거지", AppState.selected_dish, AppState.toggle_dish),
                    water_button("세탁", AppState.selected_laundry, AppState.toggle_laundry),
                    spacing="3",
                ),

                rx.box(height="20px"),

                # 입력하기 버튼
                rx.cond(
                    ~AppState.water_input_mode,
                    rx.button(
                        "입력하기",
                        on_click=AppState.show_water_input_fields,
                        color="rgba(255,255,255,0.8)",
                        background_color="rgba(34,139,34,0.7)",
                        border_radius="40px",
                        padding="24px 45px",
                        border="4px solid rgba(255,255,255,0.2)",
                        font_size="1.1em",
                        font_weight="600",
                        cursor="pointer",
                    ),
                ),

                # 입력 필드 표시
                rx.cond(
                    AppState.water_input_mode,
                    rx.form(
                        rx.vstack(

                            rx.text(
                                "사용 횟수/시간을 입력해주세요",
                                color="rgba(255,255,255,0.8)",
                                font_size="1.2em",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),

                            rx.cond(
                                AppState.show_shower,
                                shower_input_field()
                            ),

                            rx.cond(
                                AppState.show_dish,
                                water_input_field("설거지", "dish_count"),
                            ),

                            rx.cond(
                                AppState.show_laundry,
                                water_input_field("세탁", "laundry_count"),
                            ),

                            rx.box(height="20px"),

                            rx.button(
                                "다음",
                                type="submit",
                                color="rgba(255,255,255,0.8)",
                                background_color="rgba(34,139,34,0.7)",
                                border_radius="40px",
                                padding="20px 50px",
                                border="4px solid rgba(255,255,255,0.2)",
                                font_size="1.1em",
                                font_weight="600",
                                cursor="pointer",
                            ),
                            align="center",
                            width="100%",
                            spacing="2",
                        ),
                        on_submit=AppState.handle_water_submit,
                    ),
                ),

                spacing="4",
                padding="40px",
                align="center",
            ),
            max_width="800px",
            margin="0 auto",
        ),
    )
