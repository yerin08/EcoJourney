# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EcoJourney is a carbon footprint calculator web application built with Reflex (Python-based full-stack framework). It calculates carbon emissions from daily activities across 6 categories (Transportation, Food, Clothing, Electricity, Water, Waste) and provides AI-powered coaching using Google Gemini API.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r ecojourney/requirements.txt
```

### Running the Application
```bash
# Run the full-stack Reflex app (frontend + backend)
cd ecojourney
reflex run

# App runs on http://localhost:3000
```

### Environment Variables
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```
Get a free API key from: https://aistudio.google.com/app/apikey

## Architecture

### Full-Stack Integration (Reflex Framework)
Reflex is a full-stack Python framework that combines frontend (React) and backend in a single application:
- **No separate backend server needed** - everything runs on port 3000
- **State management**: `AppState` class in `state.py` manages global state
- **Event handlers**: React-like event handlers (e.g., `on_click`, `on_change`) trigger state methods
- **Page navigation**: Use `rx.redirect("/path")` for routing, NOT HTML `<a href>`

### Project Structure
```
ecojourney/
├── ecojourney.py          # Main app file - route registration
├── state.py              # Global state management (AppState class)
├── pages/                # Page components
│   ├── home.py          # Home page with video background
│   ├── intro.py         # Service introduction
│   ├── transportation.py # Transportation input
│   ├── food.py          # Food input
│   ├── clothing.py      # Clothing input
│   ├── electricity.py   # Electricity input
│   ├── water.py         # Water input
│   ├── waste.py         # Waste input
│   └── report.py        # Final results page
└── service/             # Business logic layer
    ├── carbon_calculator.py  # Emission calculations
    ├── ai_coach.py          # Gemini AI coaching
    ├── average_data.py      # Korean average data
    └── models.py           # Pydantic data models
```

### State Management Pattern

**CATEGORY_CONFIG**: Central configuration dictionary in `state.py` that defines:
- Category metadata (name, path, description)
- Available activities per category
- Supported units for each category
- Order of categories (determines page flow)

**AppState**: The global state class that:
- Stores user inputs across all pages
- Manages current category selection
- Stores all carbon activities in `all_activities` list
- Calculates final report data

**Key State Variables**:
- `all_activities: List[CarbonActivity]` - stores all user activities with calculated emissions
- `current_category: str` - tracks which category page user is on
- `CATEGORY_CONFIG` - read-only configuration for all categories

### Page Navigation Flow
1. Home (`/`) → Intro (`/intro`)
2. Intro → Category inputs (`/input/transportation`, `/input/food`, etc.)
3. Category inputs → Report (`/report`)

**Important**: All page routes are registered in `ecojourney.py` using `app.add_page()`. To add a new page, you MUST register it there.

### Carbon Calculation Logic

Located in `service/carbon_calculator.py`:

**Two-step process**:
1. **Unit Conversion**: `convert_to_standard_unit()` converts user-friendly inputs to standard units
   - Transportation: minutes → km (using avg speed)
   - Food: g or "1회 식사" → kg
   - Water: "회" (times) → L
   - Electricity: hours → kWh

2. **Emission Calculation**: `calculate_carbon_emission()` applies emission factors
   - Uses `EMISSION_FACTORS` dictionary with kgCO₂e per unit
   - Special handling for clothing (새제품/빈티지 variants)

**Example**: Transportation
- Input: 자동차, 30분
- Conversion: 30분 → 0.5시간 × 30 km/h = 15 km
- Calculation: 15 km × 0.171 kgCO₂e/km = 2.565 kgCO₂e

### AI Coaching (Gemini Integration)

Located in `service/ai_coach.py`:

**Model Selection**: Uses `get_available_gemini_model()` to find available free tier model
- Tries `gemini-2.5-flash` first, falls back to `gemini-pro`
- Implements retry logic with exponential backoff for rate limits

**Analysis Process**:
1. Takes user's activities, total carbon, and category breakdown
2. Generates structured prompt asking for:
   - Pattern analysis (2-3 sentences)
   - 3 specific reduction suggestions with emotional comparisons
   - Encouragement message
3. Parses response into `AICoachResponse` model
4. Generates alternative actions based on actual user activities (e.g., if user drove, suggest public transit)

**Error Handling**: Returns fallback coaching message if API fails or key is missing

### Korean Average Data

Located in `service/average_data.py`:
- Daily averages for each category (in kgCO₂e)
- Total Korean average: ~10.0 kgCO₂e/day
- Used for comparison in AI coaching

## Common Reflex Patterns

### Page Registration
```python
# In ecojourney.py
app = rx.App(_state=AppState)
app.add_page(home_page, route="/", title="EcoJourney | 시작")
```

### Event Handlers with State
```python
# In state.py
def toggle_transport(self, name: str):
    self.selected_transport = name

# In page component
rx.button(
    "자동차",
    on_click=lambda: AppState.toggle_transport("자동차")
)
```

### Conditional Rendering
```python
rx.cond(
    AppState.selected_transport,
    rx.text("선택됨: ", AppState.selected_transport),
    rx.text("선택 없음")
)
```

### Page Navigation
```python
# DO: Use rx.redirect()
rx.button("다음", on_click=rx.redirect("/next-page"))

# DON'T: Use HTML links
<a href="/next-page">  # This won't work in Reflex
```

## Important Notes

### Reflex-Specific Constraints
- Pages must return a single component (use `rx.container()` or `rx.vstack()` as wrapper)
- State changes trigger automatic UI updates via WebSocket
- Event handlers must be State class methods or lambda functions
- Use `_state=AppState` when creating `rx.App()` to enable state management

### Service Layer
- All business logic lives in `service/` directory
- Service functions are called directly from State methods (no REST API needed)
- Carbon calculations are stateless - they don't modify state directly

### Configuration File
`rxconfig.py` in project root:
- Sets app name, theme, and Reflex settings
- Disables SitemapPlugin to prevent warnings
- Backend runs on same port as frontend (3000)

### Assets
`assets/` directory contains:
- Video backgrounds for home/intro pages
- Static images and media files

## Troubleshooting

### Page not loading
- Check route is registered in `ecojourney.py`
- Verify page function returns single component
- Ensure `on_click=rx.redirect()` is used, not HTML links

### State not updating
- Verify `_state=AppState` in `rx.App()` initialization
- Check State method modifies `self.variable_name`
- Ensure page references State variable (e.g., `AppState.variable_name`)

### Gemini API errors
- 404: Model not found - check model name in `ai_coach.py`
- 429: Rate limit - implemented automatic retry with backoff
- Missing key: App works without key but AI coaching disabled
