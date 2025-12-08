# food.py

import reflex as rx
from ..state import AppState

FOOD_SUBCATEGORIES = {
    "유제품류": ["우유", "치즈", "두유"],
    "쌀밥": ["쌀밥", "잡곡밥", "현미밥", "보리밥", "콩밥", "김밥", "비빔밥불고기", "비빔밥산채", "김치볶음밥"],
    "커피": ["에스프레소", "카페라떼"],  # 한국일보 기준만
    "패스트푸드": ["피자", "햄버거세트", "후라이드치킨"],  # 한국일보 기준만
    "면류": ["물냉면", "비빔냉면", "잔치국수", "비빔국수", "해물칼국수"],  # 한국일보 기준만
    "국/찌개": ["된장국", "미역국", "콩나물국", "된장찌개", "김치찌개", "순두부찌개", "설렁탕", "갈비탕", "곰탕"],  # 한국일보 기준만
    "반찬": ["배추김치", "깍두기", "총각김치", "열무김치", "숙주나물", "콩나물무침", "시금치나물", "무생채", "소고기장조림", "멸치조림", "콩자반", "깻잎장아찌", "제육볶음", "오징어볶음", "불고기", "잡채", "고등어구이", "달걀프라이", "달걀찜"],
    "고기": ["소고기구이", "삼겹살구이"],
    "과일": ["딸기", "참외", "수박", "사과", "복숭아", "단감", "포도", "감귤", "키위", "토마토", "방울토마토"],
    # Climatiq API 사용 항목
    "파스타": ["카르보나라", "라자냐", "라비올리", "파스타샐러드"],  # Climatiq API 사용 (완성된 요리만)
}
UNITS = ["g", "ml", "회"]

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
                src="/food_background.mp4" 
                style='
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
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

def food_button(label: str, is_selected, on_click):

    
    disabled = AppState.food_input_mode

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
        color="rgba(255, 255, 255, 0.8)",
        border="4px solid rgba(255, 255, 255, 0.5)",
        font_size="1.1em",
        font_weight="bold",
        cursor=cursor_style,
        transition="all 0.2s ease",
    )

# =======================================================
# 입력 필드 UI
# =======================================================

def food_input_field(label: str, value_name: str, unit_name: str, sub_name: str):
    sub_items = FOOD_SUBCATEGORIES.get(label, [])
    has_subcategories = len(sub_items) > 0

    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="80px",
                color="rgba(255, 255, 255, 0.8)",
            ),
            rx.cond(
                has_subcategories,
                rx.select(
                    items=sub_items,
                    placeholder=f"세부 카테고리 선택",
                    name=sub_name,
                    width="140px",
                    background_color="rgba(255, 255, 255, 0.9)",
                    color="black",
                    border_radius="8px",
                ),
                rx.box(width="140px"),  # 하위 카테고리가 없으면 빈 공간
            ),
            rx.text(
                "회",
                min_width="100px",
                color="black",
                font_weight="bold",
                text_align="center",
            ),
            rx.input(
                placeholder="섭취량/횟수 입력",
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
        border="2px solid rgba(0, 0, 0, 0.2)",
        margin_y="10px",
        width="100%",
        max_width="550px",
    )


def food_input_field_api(label: str, value_name: str, unit_name: str, sub_name: str = None):
    """Climatiq API 사용 항목용 입력 필드 (단위 선택 가능: g, kg, 하위 카테고리 선택 가능)"""
    sub_items = FOOD_SUBCATEGORIES.get(label, [])
    has_subcategories = len(sub_items) > 0
    
    return rx.box(
        rx.hstack(
            rx.text(
                label,
                font_weight="bold",
                min_width="80px",
                color="black",
            ),
            rx.cond(
                has_subcategories,
                rx.select(
                    items=sub_items,
                    placeholder=f"세부 카테고리 선택",
                    name=sub_name,
                    width="140px",
                    background_color="rgba(255, 255, 255, 0.9)",
                    color="black",
                    border_radius="8px",
                ),
                rx.box(width="140px"),  # 하위 카테고리가 없으면 빈 공간
            ),
            rx.select(
                ["g", "kg"],
                placeholder="단위",
                name=unit_name,
                width="100px",
                background_color="rgba(255, 255, 255, 0.9)",
                color="black",
                border_radius="8px",
            ),
            rx.input(
                placeholder="무게 입력",
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
        max_width="550px",
    )


# =======================================================
# 메인 페이지
# =======================================================

def food_page():
    return rx.box(
        background_video(),
        header(),
        rx.container(
            rx.vstack(
                rx.heading("식품 선택", size="7", color="white"),
                rx.text(
                    "오늘 섭취한 식품을 모두 선택해주세요",
                    color="rgba(255, 255, 255, 0.8)",
                    font_size="1.1em",
                ),

                rx.box(height="30px"),

                # ----------------------------------
                # 버튼 선택 영역
                # ----------------------------------
                rx.vstack(
                    rx.hstack(
                        food_button("유제품류", AppState.selected_dairy, AppState.toggle_dairy),
                        food_button("쌀밥", AppState.selected_rice, AppState.toggle_rice),
                        food_button("커피", AppState.selected_coffee, AppState.toggle_coffee),
                        food_button("패스트푸드", AppState.selected_fastfood, AppState.toggle_fastfood),
                        food_button("면류", AppState.selected_noodles, AppState.toggle_noodles),
                        food_button("국/찌개", AppState.selected_cooked, AppState.toggle_cooked),
                        food_button("반찬", AppState.selected_side_dish, AppState.toggle_side_dish),
                        food_button("고기", AppState.selected_grilled_meat, AppState.toggle_grilled_meat),
                        food_button("과일", AppState.selected_fruit, AppState.toggle_fruit),
                        food_button("파스타", AppState.selected_pasta, AppState.toggle_pasta),
                        wrap="wrap",
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
                    ~AppState.food_input_mode,
                    rx.button(
                        "입력하기",
                        on_click=AppState.show_food_input_fields,
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
                    AppState.food_input_mode,
                    rx.form(
                        rx.vstack(
                            rx.text(
                                "섭취량을 입력해주세요",
                                color="rgba(255, 255, 255, 0.8)",
                                font_size="1.2em",
                                font_weight="bold",
                                margin_bottom="10px",
                            ),

                            rx.cond(AppState.show_dairy,
                                food_input_field("유제품류", "dairy_value", "dairy_unit", "dairy_sub")),
                            rx.cond(AppState.show_rice,
                                food_input_field("쌀밥", "rice_value", "rice_unit", "rice_sub")),
                            rx.cond(AppState.show_coffee,
                                food_input_field("커피", "coffee_value", "coffee_unit", "coffee_sub")),
                            rx.cond(AppState.show_fastfood,
                                food_input_field("패스트푸드", "fastfood_value", "fastfood_unit", "fastfood_sub")),
                            rx.cond(AppState.show_noodles,
                                food_input_field("면류", "noodles_value", "noodles_unit", "noodles_sub")),
                            rx.cond(AppState.show_cooked,
                                food_input_field("국/찌개", "cooked_value", "cooked_unit", "cooked_sub")),
                            rx.cond(AppState.show_side_dish,
                                food_input_field("반찬", "side_dish_value", "side_dish_unit", "side_dish_sub")),
                            rx.cond(AppState.show_grilled_meat,
                                food_input_field("고기", "grilled_meat_value", "grilled_meat_unit", "grilled_meat_sub")),
                            rx.cond(AppState.show_fruit,
                                food_input_field("과일", "fruit_value", "fruit_unit", "fruit_sub")),
                            rx.cond(AppState.show_pasta,
                                food_input_field("파스타", "pasta_value", "pasta_unit", "pasta_sub")),

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
                        on_submit=AppState.handle_food_submit,
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
