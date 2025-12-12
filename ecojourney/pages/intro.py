import reflex as rx
from ecojourney.state import AppState

def header() -> rx.Component:
    return rx.box(
        rx.hstack(
            # 로고 버튼
            rx.button(
                "ECOJOURNEY",
                on_click=rx.redirect("/"),
                background_color="transparent",
                color="#FFFFFF",
                font_size="1.5em",
                font_weight="bold",
                padding="0",
                border="none",
                border_radius="8px",
                cursor="pointer",
            ),

            # 로그인 상태에 따른 메뉴
            rx.cond(
                AppState.is_logged_in,
                rx.hstack(
                    rx.button(
                        "챌린지",
                        on_click=rx.redirect("/info"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "배틀",
                        on_click=rx.redirect("/battle"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "랭킹",
                        on_click=rx.redirect("/ranking"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
                    ),
                    rx.button(
                        "리포트",
                        on_click=rx.redirect("/intro"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="1px solid #FFFFFF",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                    ),
                    rx.text(
                        f"{AppState.current_user_id}님",
                        color="#FFFFFF",
                        font_size="1em",
                        margin_right="10px",
                    ),
                    rx.button(
                        "마이페이지",
                        on_click=rx.redirect("/mypage"),
                        background_color="transparent",
                        color="#FFFFFF",
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={
                            "border": "1px solid #FFFFFF",
                        },
                    ),
                    rx.button(
                        "로그아웃",
                        on_click=AppState.logout,
                        background_color="#FFFFFF",
                        color="#4DAB75",
                        border="1px solid #4DAB75",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"background_color": "rgba(255, 255, 255, 0.9)"},
                    ),
                    spacing="3",
                    align="center",
                ),

                # 로그인 안 된 상태 → 로그인 버튼
                rx.button(
                    "로그인",
                    on_click=rx.redirect("/auth"),
                    background_color="#FFFFFF",
                    color="#4DAB75",
                    border="1px solid #4DAB75",
                    border_radius="25px",
                    padding="8px 20px",
                    font_weight="500",
                    _hover={"background_color": "rgba(255, 255, 255, 0.9)"},
                ),
            ),

            justify="between",
            align="center",
            padding="1.5em 3em",
        ),

        width="100%",
        position="relative",
        z_index="10",
        background_color="#4DAB75",
        border_bottom="1px solid rgba(255, 255, 255, 0.1)",
    )

def footer() -> rx.Component:
    return rx.box(
        rx.center(
            # 💡 영상 위에서 잘 보이도록 텍스트 색상 조정
            rx.text("© 2025 EcoJourney. All rights reserved.", color="white", font_size="0.9em"),
            padding="1em",
        ),
        width="100%",
        position="fixed",
        bottom="0",
        z_index="100",
        background_color="transparent",
    )

def intro_page():
    return rx.cond(
        AppState.is_logged_in,
        rx.box(
            header(),

            # fade-in 애니메이션을 위한 CSS 삽입
        rx.html("""
        <style>
        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(20px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideUpFade {
            0% {
                opacity: 0;
                transform: translateY(40px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .article-card {
            opacity: 0;
            animation: slideUpFade 0.6s ease forwards;
        }

        .article-card:nth-child(1) {
            animation-delay: 0.1s;
        }

        .article-card:nth-child(2) {
            animation-delay: 0.2s;
        }

        .article-card:nth-child(3) {
            animation-delay: 0.3s;
        }

        .article-card:nth-child(4) {
            animation-delay: 0.4s;
        }

        .article-card:nth-child(5) {
            animation-delay: 0.5s;
        }

        .article-card:nth-child(6) {
            animation-delay: 0.6s;
        }

        .article-card:nth-child(7) {
            animation-delay: 0.7s;
        }

        .article-card:nth-child(8) {
            animation-delay: 0.8s;
        }

        .article-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.35);
            transition: all 0.3s ease;
        }
        </style>
        """),

        # 메인 콘텐츠
        rx.box(
            # 텍스트와 이미지 (세로 중앙 정렬)
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "리포트",
                        size="9",
                        color="#333333",
                        margin_bottom="18px",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 0.8s ease forwards",
                            "animation-delay": "0.1s",
                        },
                    ),
                    rx.text(
                        "일상 속 6가지 카테고리의 활동을 기록하고 나의 탄소 발자국 리포트를 확인하세요!",
                        color="gray.700",
                        size="5",
                        font_weight="bold",
                        text_align="left",
                        width="100%",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 1s ease forwards",
                            "animation-delay": "0.25s",
                        },
                    ),
                    spacing="2",
                    align="start",
                    justify="center",
                    padding_left="100px",
                ),

                # 이미지 영역
                rx.box(
                    rx.image(
                        src="/report.png",
                        width="90%",
                        height="auto",
                        object_fit="contain",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 0.8s ease forwards",
                            "animation-delay": "0.2s",
                        },
                    ),
                    width="50%",
                    display="flex",
                    align_items="center",
                    justify_content="center",
                    padding_left="30px",
                ),
                width="100%",
                height="70vh",
                align="center",
                justify="between",
            ),

            # 기록하기 버튼 (화면 하단)
            rx.box(
                rx.button(
                    "기록하기",
                    on_click=rx.redirect("/input/transportation"),
                    color="#FFFFFF",
                    background_color="#4DAB75",
                    border_radius="40px",
                    padding="30px 60px",
                    font_size="1.2em",
                    font_weight="bold",
                    _hover={
                        "background_color": "#3d8f5f",
                        "transform": "translateY(-8px)",
                        "box_shadow": "0 6px 20px rgba(77, 171, 117, 0.4)",
                    },
                    style={
                        "opacity": 0,
                        "animation": "fadeInUp 1s ease forwards",
                        "animation-delay": "0.5s",
                        "transition": "all 0.3s ease",
                    },
                ),
                width="100%",
                display="flex",
                justify_content="center",
                padding_bottom="60px",
            ),

            width="100%",
            min_height="100vh",
            background="linear-gradient(135deg, rgba(77, 171, 117, 0.1) 0%, rgba(77, 171, 117, 0.15) 100%)",
            display="flex",
            flex_direction="column",
            justify_content="center",
        ),

        ),
    )
