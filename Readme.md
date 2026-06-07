# 🏏 IPL Analytics Hub

A production-grade **Streamlit dashboard** for Indian Premier League (IPL) statistics from **2016 to 2026**, built with Python, Plotly and Pandas.

---

## 🏆 IPL 2026 Highlights

| Award | Winner | Stat |
|-------|--------|------|
| 🏆 Champion | Royal Challengers Bengaluru | Back-to-Back titles (2025 & 2026)! |
| 🟠 Orange Cap | Vaibhav Suryavanshi (RR) | 776 runs · SR 237.30 · 72 sixes |
| 🟣 Purple Cap | Kagiso Rabada (GT) | 29 wickets · 2nd Purple Cap |
| 🏅 Final POTM | Virat Kohli (RCB) | 75* off 42 balls in Final |
| 📈 Best Avg RPO | 9.88 | Highest ever in IPL history |
| 💥 Most Sixes | 1,426 | New all-time IPL record |

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ipl-analytics-hub.git
cd ipl-analytics-hub
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

Open in browser: **http://localhost:8501**

---

## 📋 Dashboard Tabs (11 Total)

### 🏏 Batting Stats
- Strike rate leaders bar chart (per season / team)
- Batting quality scatter plot — Avg vs SR (bubble = runs)
- Top run scorers horizontal bar chart
- Full leaderboard with filters (season, team, min runs)
- Phase-wise stats — Powerplay / Middle / Death RPO
- Export data to CSV and Excel

### 🎳 Bowling Stats
- Economy rate by phase — Powerplay, Middle, Death overs
- Dot ball percentage ranking
- Economy vs Average scatter plot
- Full bowling leaderboard with filters
- Export data to CSV and Excel

### 🏟️ Teams
- All-time wins and losses grouped bar chart
- Win percentage horizontal bar chart
- Head-to-head matrix heatmap (top 6 teams)

### 📈 Season Trends (2016–2026)
- Average RPO trend across all seasons
- Total sixes per season bar chart
- Orange Cap runs by season (color = that year's champion)
- Full champions table 2016–2026

### ⚔️ Player Comparison
- Side-by-side batter or bowler comparison cards
- Career radar chart across 6 key metrics
- Season-by-season runs / wickets grouped bar chart

### 🗺️ India Map
- Interactive Plotly map with all 10 IPL team home cities
- Hover info — titles, win%, city name

### 🤖 Match Predictor
- Pre-match winner prediction using win%, form, toss, venue, home advantage
- Live win probability simulator with over-by-over chart
- RRR / CRR / Balls remaining tracker

### 💰 Auction & Best XI
- IPL 2025 auction prices for all major players
- Team total spend pie chart
- Value-for-money scatter — SR vs Price
- Best XI auto-picker by season using impact score algorithm

### 📊 Custom Chart Builder
- Choose dataset — Batting, Bowling, Seasons, Teams, Auction
- Select X axis, Y axis, color grouping
- Chart types — Bar, Scatter, Line, Histogram, Box, Pie
- Export chart data to CSV or Excel

### 🧠 AI Chatbot
- Ask anything about IPL — players, teams, venues, records
- Quick question buttons for instant answers
- Covers full 2016–2026 history and stats

### 🎮 IPL Quiz
- 10 trivia questions about IPL history
- Score tracking with final grade
- Fun facts revealed after each answer
- Shuffle and play again option

---

## 🔧 Sidebar Filters

| Filter | Description |
|--------|-------------|
| 📅 Season | Any year 2016–2026, or All Seasons |
| 🏟️ Team | Filter by any of the 10 IPL franchises |
| Min Runs | Show batters above a minimum run threshold |
| Min Wickets | Show bowlers above a minimum wicket threshold |
| 🌙 Theme | Toggle Dark / Light mode instantly |

---

## 📊 Data Coverage

| Season | Batters | Bowlers |
|--------|---------|---------|
| 2016–2021 | 30+ per season | 30+ per season |
| 2022–2024 | 35+ per season | 35+ per season |
| 2025 | 40+ (all 10 teams) | 40+ (all 10 teams) |
| 2026 | 45+ (all 10 teams) | 20+ (all 10 teams) |

---

## 📁 Project Structure

```
ipl-stats-dashboard/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Git ignore rules
```

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select `app.py` as the main file
5. Click **Deploy**

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Streamlit** | Web UI and layout |
| **Plotly** | Interactive charts and India map |
| **Pandas** | Data filtering and processing |
| **NumPy** | Win probability calculations |
| **OpenPyXL** | Excel file export |

---

## 📦 requirements.txt

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

## 📊 Data Sources

- [ESPNcricinfo](https://www.espncricinfo.com)
- [IPL Official](https://www.iplt20.com)
- IPL 2025 & 2026 stats verified from official records

---

# 👤 Author
 
**Prince Kumar**
 
- GitHub: [@princekushwaha9142](https://github.com/princekushwaha9142)
- 💻 Python Developer | Backend & Data Science Enthusiast
Built as a **Phase Project** for GitHub portfolio.

---

*IPL Analytics Hub · 2016–2026 · Streamlit + Plotly + Python*