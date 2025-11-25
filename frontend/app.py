import reflex as rx
# 현재 프로젝트 구조 (frontend/pages/ 에 페이지 파일 만들 예정)
from frontend.pages import (
    index,
    intro,
    transportation,
    food,
    clothing,
    waste,
    electricity,
    water,
    report
)
# frontend/state.py 에 AppState를 정의한다고 가정
from frontend.state import AppState

# 앱 정의 및 페이지 라우팅

# AppState를 사용하여 앱 초기화
app = rx.App(state=AppState)

# 1. 메인 홈 화면 라우팅(/)
app.add_page(index.index_page, route="/", title="EcoJourney | 시작")

# 2. 서비스 소개 화면 라우팅(/intro)
app.add_page(intro.intro_page, route="/intro", title="EcoJourney | 소개")

# 3. 카테고리 입력 화면 라우팅(/input/*)
# 입력 페이지는 순차적으로 진행되므로 명확한 경로 사용
app.add_page(transportation.transportation_page, route="/input/transportation", title="EcoJourney | 교통")
app.add_page(food.food_page, route="/input/food", title="EcoJourney | 식품")
app.add_page(clothing.clothing_page, route="/input/clothing", title="EcoJourney | 의류")
app.add_page(waste.waste_page, route="/input/waste", title="EcoJourney | 쓰레기 배출")
app.add_page(electricity.electricity_page, route="/input/electricity", title="EcoJourney | 전기")
app.add_page(water.water_page, route="/input/water", title="EcoJourney | 물")

# 4. 결과 리포트 화면 라우팅(/report)
app.add_page(report.report_page, route="/report", title="EcoJourney | 결과 리포트")