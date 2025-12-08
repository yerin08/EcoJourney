import reflex as rx
from ..state import AppState

UNITS = ["km", "분"]

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
            rx.cond(
                AppState.is_logged_in,
                rx.hstack(
                    rx.button(
                        "마이페이지",
                        on_click=rx.redirect("/mypage"),
                        background_color="rgba(255, 255, 255, 0.2)",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        border_radius="20px",
                        padding="8px 20px",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.3)",
                        },
                    ),
                    rx.text(
                        f"{AppState.current_user_id}님",
                        color="white",
                        font_size="1em",
                        margin_right="10px",
                    ),
                    rx.button(
                        "로그아웃",
                        on_click=AppState.logout,
                        background_color="rgba(255, 255, 255, 0.2)",
                        color="white",
                        border="1px solid rgba(255, 255, 255, 0.3)",
                        border_radius="20px",
                        padding="8px 20px",
                        _hover={
                            "background_color": "rgba(255, 255, 255, 0.3)",
                        },
                    ),
                    spacing="3",
                    align="center",
                ),
                rx.button(
                    "로그인",
                    on_click=rx.redirect("/auth"),
                    background_color="rgba(255, 255, 255, 0.2)",
                    color="white",
                    border="1px solid rgba(255, 255, 255, 0.3)",
                    border_radius="20px",
                    padding="8px 20px",
                    _hover={
                        "background_color": "rgba(255, 255, 255, 0.3)",
                    },
                ),
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
                    object-position: center bottom;
                    z-index: -2; 
                    filter: brightness(0.6);'
            />
            """
        ),
        width="100%",
        height="100%",
        z_index="-2",
    )

# =======================================================
# 공통 버튼 UI
# =======================================================

def transport_button(label: str, is_selected, on_click):


    disabled = AppState.trans_input_mode

    base = rx.hstack(
        rx.text(label),
        spacing="2",
    )

    
    selected_bg = rx.cond(disabled, "rgba(0,0,0,0.2)", "rgba(0,0,0,0.52)")
    default_bg  = rx.cond(disabled, "rgba(0,0,0,0.1)", "rgba(0,0,0,0.22)")

    cursor_style = rx.cond(disabled, "not-allowed", "pointer")

    return rx.button(
        base,
        
        on_click=rx.cond(disabled, None, on_click),

        disabled=disabled,

        # 선택 여부에 따른 스타일
        background_color=rx.cond(is_selected, selected_bg, default_bg),

        border_radius="40px",
        padding=rx.cond(is_selected, "27px 40px", "24px 40px"),
        border="4px solid rgba(255, 255, 255, 0.5)",
        font_size="1.1em",
        font_weight="bold",
        cursor=cursor_style,
        transition="all 0.2s ease",
    )

# =======================================================
# 입력 필드 UI
# =======================================================

def transport_input_field(label: str, value_name: str, unit_name: str):
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="80px",
                color="rgba(255, 255, 255, 0.8)",
            ),
            rx.select(
                UNITS,
                placeholder="단위",
                name=unit_name,
                width="100px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            rx.input(
                placeholder="거리/시간 입력",
                type="number",
                name=value_name,
                width="140px",
                background_color="rgba(255, 255, 255, 0.9)",
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


# =======================================================
# 메인 페이지
# =======================================================

def transportation_page():
    return rx.box(
        background_video(),
        header(),
        rx.container(
            rx.vstack(
                rx.heading("교통수단 선택", size="7", color="white"),
                rx.text(
                    "오늘 이용한 교통수단을 모두 선택해주세요",
                    color="rgba(255, 255, 255, 0.8)",
                    font_size="1.1em",
                ),

                rx.box(height="30px"),

                # ----------------------------------
                # 버튼 선택 영역
                # -------------------------------Trans_
                rx.vstack(
                    rx.hstack(
                        transport_button("자동차", AppState.selected_car, AppState.toggle_car),
                        transport_button("버스", AppState.selected_bus, AppState.toggle_bus),
                        transport_button("지하철", AppState.selected_subway, AppState.toggle_subway),
                        transport_button("걷기", AppState.selected_walk, AppState.toggle_walk),
                        transport_button("자전거", AppState.selected_bike, AppState.toggle_bike),
                        wrap="nowrap",
                        justify="center",
                        spacing="3",
                    ),
                    spacing="3",
                ),

                rx.box(),

                # ----------------------------------
                # 입력하기 버튼
                # ----------------------------------
                rx.cond(
                    ~AppState.trans_input_mode,
                    rx.button(
                        "입력하기",
                        on_click=AppState.show_trans_input_fields,
                        color="rgba(255, 255, 255, 0.8)",
                        background_color="rgba(34,139,34,0.7)",
                        border_radius="40px",
                        padding="24px 45px",
                        border="4px solid rgba(255,255,255,0.2)",
                        font_size="1.1em",
                        font_weight="600",
                        cursor="pointer",
                        _hover={"background_color": "rgba(34,139,34,0.9)"},
                    ),
                ),

                rx.box(),

                # ----------------------------------
                # 입력 필드 렌더링
                # ----------------------------------
                rx.cond(
                    AppState.trans_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "이용량을 입력해주세요",
                                color="rgba(255, 255, 255, 0.8)",
                                font_size="1.2em",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),

                            rx.cond(AppState.show_car,
                                    transport_input_field("자동차", "car_value", "car_unit")),
                            rx.cond(AppState.show_bus,
                                    transport_input_field("버스", "bus_value", "bus_unit")),
                            rx.cond(AppState.show_subway,
                                    transport_input_field("지하철", "subway_value", "subway_unit")),
                            rx.cond(AppState.show_walk,
                                    transport_input_field("걷기", "walk_value", "walk_unit")),
                            rx.cond(AppState.show_bike,
                                    transport_input_field("자전거", "bike_value", "bike_unit")),

                            rx.box(height="20px"),

                            # 다음 버튼
                            rx.button(
                                "다음",
                                type="submit",
                                color="rgba(255, 255, 255, 0.8)",
                                background_color="rgba(34,139,34,0.7)",
                                border_radius="40px",
                                padding="20px 50px",
                                border="4px solid rgba(255,255,255,0.2)",
                                font_size="1.1em",
                                font_weight="600",
                                cursor="pointer",
                                _hover={"background_color": "rgba(34,139,34,0.9)"},
                            ),

                            align="center",
                            width="100%",
                            spacing="2",
                        ),
                        on_submit=AppState.handle_transport_submit,
                    ),
                ),

                spacing="4",
                align="center",
                padding="40px",
            ),
            max_width="800px",
            margin="0 auto",
        ),
    )
