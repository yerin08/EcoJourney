# waste.py

import reflex as rx
from ..state import AppState


def header():
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


def background_video():
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


# 공통 버튼 UI (Food 스타일 동일)
def waste_button(label, is_selected, on_click):

    disabled = AppState.waste_input_mode

    return rx.button(
        rx.text(label),
        on_click=rx.cond(disabled, None, on_click),
        disabled=disabled,
        background_color=rx.cond(
            is_selected,
            "rgba(0,0,0,0.52)",
            "rgba(0,0,0,0.22)"
        ),
        border_radius="40px",
        padding=rx.cond(is_selected, "27px 40px", "24px 40px"),
        color="rgba(255,255,255,0.8)",
        border="4px solid rgba(255,255,255,0.5)",
        font_size="1.1em",
        font_weight="bold",
        transition="all 0.2s",
    )


# 입력 필드 UI
def waste_input_field(label: str, value_name: str, unit_name: str):
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="100px",
                color="rgba(255,255,255,0.85)",
            ),

            # 🔥 단위 선택 (kg / 개)
            rx.select(
                ["kg", "개"],
                placeholder="단위",
                name=unit_name,
                width="100px",
                background_color="rgba(255,255,255,0.9)",
                color="black",
                border_radius="8px",
            ),

            rx.input(
                placeholder="숫자 입력",
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
        max_width="400px",
    )


def waste_page():
    return rx.box(
        background_video(),
        header(),
        rx.container(
            rx.vstack(
                rx.heading("쓰레기 배출량 입력", size="7", color="white"),
                rx.text(
                    "오늘 배출한 쓰레기를 모두 선택하고 양을 입력해주세요",
                    color="rgba(255,255,255,0.8)",
                    font_size="1.1em",
                ),

                rx.box(height="30px"),

                # 버튼 선택
                rx.hstack(
                    waste_button("일반쓰레기", AppState.selected_general, AppState.toggle_general),
                    waste_button("플라스틱", AppState.selected_plastic, AppState.toggle_plastic),
                    waste_button("종이", AppState.selected_paper, AppState.toggle_paper),
                    waste_button("유리", AppState.selected_glass, AppState.toggle_glass),
                    waste_button("캔", AppState.selected_can, AppState.toggle_can),
                    spacing="3",
                    wrap="wrap",
                    justify="center",
                ),

                rx.box(height="20px"),

                rx.cond(
                    ~AppState.waste_input_mode,
                    rx.button(
                        "입력하기",
                        on_click=AppState.show_waste_input_fields,
                        color="rgba(255,255,255,0.8)",
                        background_color="rgba(34,139,34,0.7)",
                        border_radius="40px",
                        padding="24px 45px",
                        border="4px solid rgba(255,255,255,0.2)",
                        font_size="1.1em",
                        font_weight="600",
                    ),
                ),

                # 입력 필드 렌더링
                rx.cond(
                    AppState.waste_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "배출량을 입력해주세요",
                                color="rgba(255,255,255,0.8)",
                                font_size="1.2em",
                                font_weight="bold",
                            ),

                            rx.cond(AppState.show_general,
                                waste_input_field("일반쓰레기", "general_value", "general_unit")
                            ),
                            rx.cond(AppState.show_plastic,
                                waste_input_field("플라스틱", "plastic_value", "plastic_unit")
                            ),
                            rx.cond(AppState.show_paper,
                                waste_input_field("종이", "paper_value", "paper_unit")
                            ),
                            rx.cond(AppState.show_glass,
                                waste_input_field("유리", "glass_value", "glass_unit")
                            ),
                            rx.cond(AppState.show_can,
                                waste_input_field("캔", "can_value", "can_unit")
                            ),

                            rx.box(height="20px"),

                            rx.button(
                                "완료",
                                type="submit",
                                color="rgba(255,255,255,0.8)",
                                background_color="rgba(34,139,34,0.7)",
                                border_radius="40px",
                                padding="20px 50px",
                                border="4px solid rgba(255,255,255,0.2)",
                                font_size="1.1em",
                                font_weight="600",
                            ),

                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        on_submit=AppState.handle_waste_submit,
                    ),
                ),

                spacing="4",
                padding="40px",
                align="center",
            ),
            max_width="900px",
            margin="0 auto",
        ),
    )
