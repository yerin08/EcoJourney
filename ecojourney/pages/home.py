# home.py (수정된 최종 코드)

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
                        border="none",
                        border_radius="25px",
                        padding="8px 20px",
                        font_weight="500",
                        _hover={"border": "1px solid #FFFFFF"},
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
                        _hover={"border": "1px solid #FFFFFF"},
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
        z_index="20",
        background_color="#4DAB75",
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

# --- 홈 페이지 본문 ---
def home_page() -> rx.Component:
    """홈 페이지 컴포넌트"""
    return rx.box(
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
        </style>
        """),

        # 세션 복원 스크립트 (페이지 로드 시 localStorage 확인 후 백엔드 호출)
        rx.script("""
            (function() {
                // localStorage에서 세션 정보 확인
                const userId = localStorage.getItem('eco_user_id');
                const isLoggedIn = localStorage.getItem('eco_is_logged_in');

                // 로그인 상태이고 세션 정보가 있으면 복원 시도
                if (isLoggedIn === 'true' && userId && userId !== 'null' && userId !== 'None') {
                    // Reflex 이벤트 발생시키기 위해 커스텀 이벤트 사용
                    setTimeout(function() {
                        // window에 user_id 저장 (이후 on_mount에서 접근 가능)
                        window.ecoSessionUserId = userId;
                    }, 50);
                }
            })();
        """),

         # 배경 레이어 구성
        rx.box(
            # ---------------------------------------------
            # 1) 배경 (가장 아래 레이어)
            # ---------------------------------------------
            rx.box(
                width="100%",
                height="55vh",
                background="#4DAB75",
                position="absolute",
                top="0",
                left="0",
                z_index="0",
            ),

            # ---------------------------------------------
            # 2) 이미지 (중간 레이어)
            # ---------------------------------------------
            rx.box(
                rx.image(
                    src="/earth.png",
                    width="50%",
                    height="auto",
                    object_fit="contain",
                    style={
                        "opacity": 0,
                        "transform": "translateY(20px)",
                        "animation": "fadeInUp 0.8s ease forwards",
                        "animation-delay": "0.2s",
                    },
                ),
                width="100%",
                height="100vh",
                position="absolute",
                top="15",
                left="0",
                z_index="10",
                display="flex",
                align_items="center",
                justify_content="center",
            ),

            # ---------------------------------------------
            # 3) 텍스트 (이미지보다 위 레이어)
            # ---------------------------------------------
            rx.box(
                rx.vstack(
                    rx.heading(
                        "ECOJOURNEY",
                        size="9",
                        color="#FFFFFF",
                        margin_bottom="18px",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 0.8s ease forwards",
                            "animation-delay": "0.1s",
                        },
                    ),
                    rx.text(
                        "줄일수록 보이는 나의 변화.",
                        color="#FFFFFF",
                        size="6",
                        font_weight="bold",
                        text_align="center",
                        width="100%",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 1s ease forwards",
                            "animation-delay": "0.25s",
                        },
                    ),
                    rx.text(
                        "다함께 지속 가능한 에코 라이프를 만들어요.",
                        color="#FFFFFF",
                        size="6",
                        font_weight="bold",
                        text_align="center",
                        width="100%",
                        style={
                            "opacity": 0,
                            "transform": "translateY(20px)",
                            "animation": "fadeInUp 1s ease forwards",
                            "animation-delay": "0.35s",
                        },
                    ),
                    spacing="2",
                    align="center",
                    justify="center",
                ),
                width="100%",
                height="100vh",
                position="absolute",
                top="10",
                left="0",
                z_index="15",
                display="flex",
                align_items="center",
                justify_content="center",
            ),
        ),
        rx.box(
            rx.vstack(
                rx.divider(),

                # 현재 기후 상황
                rx.box(
                    rx.heading()
                ),
                rx.divider(margin_top="40px"),
                # 사이트 콘텐츠 소개
                rx.box(),
                # 로그인 페이지 이동 버튼

                spacing="6",
                width="100%",
                max_width="1200px",
                align="center",
            ),
            width="100%",
            z_index="2",
            padding="40px 20px",
            display="flex",
            justify_content="center",
            margin_top="95vh",
        ),
    )