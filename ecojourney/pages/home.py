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

        /* 스크롤 애니메이션 */
        .scroll-fade-in,
        .scroll-fade-in-delay,
        .scroll-fade-in-text,
        .scroll-fade-in-button {
            opacity: 0;
            transform: translateY(30px);
            transition: opacity 0.8s ease, transform 0.8s ease;
        }

        .scroll-fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .scroll-fade-in-delay.visible {
            opacity: 1;
            transform: translateY(0);
            transition-delay: 0.2s;
        }

        .scroll-fade-in-text.visible {
            opacity: 1;
            transform: translateY(0);
            transition-delay: 0.4s;
        }

        .scroll-fade-in-button.visible {
            opacity: 1;
            transform: translateY(0);
            transition-delay: 0.6s;
        }
        </style>
        """),

        # 스크롤 애니메이션 JavaScript
        rx.script("""
        (function() {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -100px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, observerOptions);

            // DOM이 로드된 후 관찰 시작
            setTimeout(() => {
                const elements = document.querySelectorAll('.scroll-fade-in, .scroll-fade-in-delay, .scroll-fade-in-text, .scroll-fade-in-button');
                elements.forEach(el => observer.observe(el));
            }, 100);
        })();
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
                    rx.heading(
                        "지금, 우리가 마주한 기후 위기",
                        align="center",
                        font_weight="bold",
                        size="7",
                        class_name="scroll-fade-in",
                    ),

                    rx.hstack(
                        # =======================
                        # 왼쪽 50% : 이미지 영역
                        # =======================
                        rx.box(
                            rx.hstack(
                                rx.image(
                                    src="/dust.jpg",
                                    width="45%",
                                    height="100%",
                                    object_fit="cover",
                                    border_radius="18px",
                                ),
                                rx.vstack(
                                    rx.image(
                                        src="/trash.jpg",
                                        width="100%",
                                        height="48%",
                                        object_fit="cover",
                                        border_radius="14px",
                                    ),
                                    rx.image(
                                        src="/glacier.jpg",
                                        width="100%",
                                        height="48%",
                                        object_fit="cover",
                                        border_radius="14px",
                                    ),
                                    spacing="4",
                                    height="100%",
                                ),
                                spacing="4",
                                height="100%",
                            ),
                            width="50%",
                            height="420px",
                            class_name="scroll-fade-in-delay",
                        ),

                        # =======================
                        # 오른쪽 50% : 텍스트 영역
                        # =======================
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    "기후 변화는 더 이상 먼 미래의 이야기가 아닙니다.\n"
                                    "폭염, 이상 기후, 미세먼지, 해수면 상승과 같은 환경 문제는\n"
                                    "이미 우리의 일상과 안전을 직접적으로 위협하고 있습니다.",
                                    white_space="pre-line",
                                    color="#333333",
                                    size="4",
                                    font_weight="bold",
                                ),
                                rx.text(
                                    "특히 온실가스 배출로 인한 지구 온난화는\n"
                                    "자연 생태계의 붕괴뿐 아니라 식량 문제, 건강 문제,\n"
                                    "사회·경제적 불균형까지 초래하고 있습니다.",
                                    white_space="pre-line",
                                    color="#333333",
                                    size="4",
                                    font_weight="bold",
                                    margin_top="20px",
                                ),
                                rx.text(
                                    "하지만 기후 위기는 개인의 노력만으로 해결할 수 없는 문제인 동시에,\n"
                                    "개인의 작은 실천이 모였을 때\n"
                                    "가장 큰 변화를 만들 수 있는 문제이기도 합니다.\n"
                                    "지금 행동하지 않으면, 그 피해는 고스란히 우리의 미래가 됩니다.",
                                    white_space="pre-line",
                                    color="#333333",
                                    size="4",
                                    font_weight="bold",
                                    margin_top="20px",
                                ),
                                spacing="5",
                                justify="center",
                            ),
                            width="50%",
                            padding_left="80px",
                            class_name="scroll-fade-in-text",
                        ),

                        width="100%",
                        align="center",
                        margin_top="50px",
                    ),
                ),


                rx.divider(margin_top="40px"),

                # ECOJOURNEY 소개
                rx.box(
                    rx.vstack(
                        rx.hstack(
                            # 왼쪽 박스
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "ECOJOURNEY\n"
                                        "- 행동으로 이어지는 환경 실천 플랫폼 -",
                                        white_space="pre-line",
                                        text_align="center",
                                        font_weight="bold",
                                        size="6",
                                        margin_bottom="10px",
                                    ),
                                    rx.divider(width="100%"),
                                    rx.text(
                                        "EcoJourney는 환경 문제를 '알아보는 것'에서 끝내지 않고,\n"
                                        "실제 행동과 변화로 이어지도록 돕는 참여형 환경 플랫폼입니다.",
                                        white_space="pre-line",
                                        text_align="center",
                                        color="#333333",
                                        size="4",
                                        margin_top="20px",
                                    ),

                                    rx.text(
                                        "우리는 일상 속에서 발생하는 탄소 배출과 환경 행동을 기록하고,\n"
                                        "눈에 보이는 데이터와 보상 시스템을 통해\n"
                                        "지속 가능한 실천을 자연스럽게 이어갈 수 있도록 설계되었습니다.",
                                        white_space="pre-line",
                                        text_align="center",
                                        color="#333333",
                                        size="4",
                                    ),

                                    rx.text(
                                        "환경 보호는 거창한 결심이 아니라\n"
                                        "매일의 선택과 작은 습관에서 시작됩니다.\n"
                                        "EcoJourney는 그 시작을 함께합니다.",
                                        white_space="pre-line",
                                        text_align="center",
                                        color="#333333",
                                        size="4",
                                        font_weight="bold",
                                    ),

                                    spacing="5",
                                    align="center",
                                    justify="center",
                                    height="100%",
                                ),
                                flex="1",
                                height="500px",
                                background="linear-gradient(135deg, rgba(77, 171, 117, 0.1) 0%, rgba(77, 171, 117, 0.15) 100%)",
                                border_radius="20px",
                                padding="30px",
                                class_name="scroll-fade-in",
                            ),

                            # 오른쪽 박스
                            rx.box(
                                rx.vstack(
                                    rx.heading(
                                        "ECOJOURNEY 이렇게 활용하세요.",
                                        text_align="center",
                                        font_weight="bold",
                                        size="6",
                                        margin_bottom="10px",
                                    ),
                                    rx.divider(width="100%"),
                                    rx.hstack(
                                        rx.image(
                                            src="/report.png",
                                            width="17%",
                                        ),
                                        rx.text(
                                            "나의 환경 행동을 기록하고 확인하세요.",
                                            color="#333333",
                                            size="4",
                                            font_weight="bold",
                                        ),
                                        width="100%",
                                        justify="start",
                                        spacing="4",
                                        margin_top="20px",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            "챌린지와 배틀로 실천을 이어가세요.",
                                            color="#333333",
                                            size="4",
                                            font_weight="bold",
                                        ),
                                        rx.image(
                                            src="/battle.png",
                                            width="20%",
                                        ),
                                        width="100%",
                                        justify="end",
                                        spacing="4",
                                    ),
                                    rx.hstack(
                                        rx.image(
                                            src="/point.png",
                                            width="12%",
                                        ),
                                        rx.text(
                                            "포인트로 동기부여를 높이세요.",
                                            color="#333333",
                                            size="4",
                                            font_weight="bold",
                                        ),
                                        width="100%",
                                        justify="start",
                                        spacing="4",
                                    ),
                                    rx.hstack(
                                        rx.text(
                                            "환경을 '의식하는 습관'을 만들어 보세요.",
                                            color="#333333",
                                            size="4",
                                            font_weight="bold",
                                        ),
                                        rx.image(
                                            src="/earth2.png",
                                            width="12%",
                                        ),
                                        width="100%",
                                        justify="end",
                                        spacing="4",
                                    ),
                                    spacing="5",
                                    align="center",
                                    justify="center",
                                    height="100%",
                                ),
                                flex="1",
                                height="500px",
                                background="linear-gradient(135deg, rgba(77, 171, 117, 0.1) 0%, rgba(77, 171, 117, 0.15) 100%)",
                                border_radius="20px",
                                padding="30px",
                                class_name="scroll-fade-in-delay",
                            ),
                            spacing="7",
                            width="100%",
                            align="stretch",
                        ),
                        rx.vstack(
                            rx.text(
                                "환경 보호는 선택이 아닌 책임입니다.\n"
                                "그리고 그 책임은 오늘의 작은 실천에서 시작됩니다.",
                                white_space="pre-line",
                                text_align="center",
                                width="100%",
                            ),
                            rx.text(
                                "ECOJOURNEY와 함께 지금, 당신의 환경 여정을 시작해보세요",
                                text_align="center",
                                width="100%",
                            ),
                            spacing="2",
                            width="100%",
                            align="center",
                            class_name="scroll-fade-in-text",
                        ),
                        spacing="6",
                        width="100%",
                        max_width="1200px",
                        margin="0 auto",
                    ),
                    margin_top="30px",
                    width="100%",
                ),
                # 로그인 페이지 이동 버튼 (로그인 안 된 경우만 표시)
                rx.cond(
                    ~AppState.is_logged_in,
                    rx.box(
                        rx.button(
                            "함께하기",
                            on_click=rx.redirect("/auth"),
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
                            class_name="scroll-fade-in-button",
                        ),
                        width="100%",
                        display="flex",
                        justify_content="center",
                        padding_bottom="60px",
                    ),
                    rx.box(height="60px"),  # 로그인된 경우 빈 공간
                ),

                spacing="6",
                width="100%",
                max_width="1300px",
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