import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import io

st.set_page_config(page_title="IPL Analytics Hub", page_icon="🏏", layout="wide", initial_sidebar_state="expanded")

# ─── THEME ───────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_dark = st.session_state.theme == "dark"
BG       = "#0a0a14"    if is_dark else "#f0f4f8"
BG2      = "#1a1a2e"    if is_dark else "#ffffff"
BG3      = "#16213e"    if is_dark else "#e8edf4"
TEXT     = "#ffffff"    if is_dark else "#1a1a2e"
TEXT2    = "rgba(255,255,255,0.55)" if is_dark else "rgba(26,26,46,0.6)"
BORDER   = "rgba(255,255,255,0.08)" if is_dark else "rgba(26,26,46,0.12)"
GOLD     = "#FFD700"
PLOT_BG  = "rgba(0,0,0,0)"
GRID     = "rgba(255,255,255,0.07)" if is_dark else "rgba(0,0,0,0.07)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500&display=swap');
html,body,.main,.stApp{{background-color:{BG};color:{TEXT};font-family:'Inter',sans-serif;}}
.ipl-header{{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);padding:18px 24px;border-radius:14px;border:1px solid rgba(255,215,0,0.2);margin-bottom:16px;}}
.ipl-title{{font-family:'Rajdhani',sans-serif;font-size:2.2rem;font-weight:700;color:{GOLD};letter-spacing:2px;margin:0;}}
.ipl-subtitle{{color:{TEXT2};font-size:0.88rem;margin-top:3px;}}
.season-badge{{display:inline-block;background:rgba(255,215,0,0.1);border:1px solid {GOLD};color:{GOLD};padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;margin:2px;}}
.ticker-wrap{{background:linear-gradient(90deg,#0f3460,#1a1a2e,#0f3460);border:1px solid rgba(255,215,0,0.3);border-radius:8px;padding:8px 16px;margin-bottom:14px;overflow:hidden;white-space:nowrap;}}
.ticker-text{{display:inline-block;animation:ticker 30s linear infinite;color:{GOLD};font-size:0.82rem;font-weight:500;letter-spacing:0.3px;}}
@keyframes ticker{{0%{{transform:translateX(100vw)}}100%{{transform:translateX(-100%)}}}}
.metric-card{{background:linear-gradient(135deg,{BG2},{BG3});border:1px solid {BORDER};border-radius:12px;padding:14px 16px;text-align:center;margin-bottom:10px;}}
.metric-value{{font-family:'Rajdhani',sans-serif;font-size:1.85rem;font-weight:700;color:{GOLD};}}
.metric-label{{color:{TEXT2};font-size:0.7rem;text-transform:uppercase;letter-spacing:1px;}}
.metric-sub{{color:{TEXT};opacity:0.7;font-size:0.76rem;margin-top:2px;}}
.section-header{{font-family:'Rajdhani',sans-serif;font-size:1.15rem;font-weight:600;color:{GOLD};border-left:4px solid {GOLD};padding-left:10px;margin:18px 0 12px;}}
.highlight-box{{background:linear-gradient(135deg,rgba(255,215,0,0.07),rgba(255,140,0,0.04));border:1px solid rgba(255,215,0,0.22);border-radius:10px;padding:11px 13px;margin:5px 0;}}
.highlight-player{{font-size:0.95rem;font-weight:700;color:{GOLD};}}
.highlight-stat{{color:{TEXT};opacity:0.75;font-size:0.8rem;}}
.award-tag{{color:{GOLD};font-size:0.73rem;margin-top:2px;}}
.compare-card{{background:linear-gradient(135deg,{BG2},{BG3});border:1px solid {BORDER};border-radius:14px;padding:18px;text-align:center;}}
.compare-name{{font-family:'Rajdhani',sans-serif;font-size:1.35rem;font-weight:700;color:{GOLD};}}
.xi-card{{background:linear-gradient(135deg,#0d1b2a,#1a2f4a);border:1px solid rgba(255,215,0,0.18);border-radius:10px;padding:10px;text-align:center;margin:3px;}}
.venue-card{{background:linear-gradient(135deg,{BG2},#0f3460);border:1px solid {BORDER};border-radius:12px;padding:12px 15px;margin:5px 0;}}
.predictor-box{{background:linear-gradient(135deg,{BG2},#0f3460);border:1px solid rgba(255,215,0,0.28);border-radius:14px;padding:18px;margin:8px 0;}}
.quiz-card{{background:linear-gradient(135deg,{BG2},{BG3});border:2px solid rgba(255,215,0,0.3);border-radius:14px;padding:20px;margin:10px 0;}}
.quiz-q{{font-family:'Rajdhani',sans-serif;font-size:1.15rem;font-weight:600;color:{TEXT};margin-bottom:12px;}}
.chat-msg-user{{background:rgba(255,215,0,0.12);border:1px solid rgba(255,215,0,0.2);border-radius:12px 12px 2px 12px;padding:10px 14px;margin:6px 0;color:{TEXT};font-size:0.88rem;text-align:right;}}
.chat-msg-bot{{background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);border-radius:12px 12px 12px 2px;padding:10px 14px;margin:6px 0;color:{TEXT};font-size:0.88rem;}}
.export-box{{background:linear-gradient(135deg,{BG2},{BG3});border:1px solid {BORDER};border-radius:12px;padding:16px;margin:8px 0;}}
[data-testid="stSidebar"]{{background:{BG2} !important;border-right:1px solid {BORDER};}}
div[data-testid="stTabs"] button{{color:{TEXT2} !important;font-weight:600;font-size:0.85rem;}}
div[data-testid="stTabs"] button[aria-selected="true"]{{color:{GOLD} !important;border-bottom:3px solid {GOLD} !important;}}
@media (max-width:768px){{
  .ipl-title{{font-size:1.4rem;}}
  .metrics-row{{grid-template-columns:1fr 1fr !important;}}
  .compare-card{{padding:10px;}}
}}
</style>
""", unsafe_allow_html=True)

# ─── DATA ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_all_data():
    batting = pd.DataFrame([
        ("Virat Kohli","RCB","2016",973,16,81.1,152.3,83,38,7,4,"🟠 Orange Cap"),
        ("AB de Villiers","RCB","2016",687,13,57.3,182.6,52,42,5,1,"💥 Best SR"),
        ("David Warner","SRH","2016",562,14,46.8,150.8,55,20,5,1,"Top Opener"),
        ("Gautam Gambhir","KKR","2016",480,14,40.0,123.7,50,10,4,0,"Captain"),
        ("Shikhar Dhawan","SRH","2016",501,14,41.8,137.9,52,14,5,0,"Opening"),
        ("MS Dhoni","RPS","2016",284,16,28.4,127.9,18,14,1,0,"Captain"),
        ("Rohit Sharma","MI","2016",489,16,35.6,132.4,46,18,4,0,"Captain"),
        ("Hardik Pandya","MI","2016",260,14,26.0,158.0,16,24,0,0,"All-rounder"),
        ("Kieron Pollard","MI","2016",292,16,29.2,154.0,20,26,0,0,"Finisher"),
        ("Suresh Raina","CSK","2016",399,14,36.3,144.2,36,18,3,0,"Batter"),
        ("MS Dhoni","CSK","2016",284,14,28.4,128.2,16,18,1,0,"Captain"),
        ("Gautam Gambhir","KKR","2016",480,14,40.0,123.7,50,10,4,0,"Captain"),
        ("Robin Uthappa","KKR","2016",394,14,32.8,132.2,34,16,3,0,"Opener"),
        ("Manish Pandey","KKR","2016",422,14,38.4,128.4,40,10,4,0,"Batter"),
        ("Rishabh Pant","DC","2016",198,12,18.0,158.4,16,14,0,0,"WK-Bat"),
        ("Shreyas Iyer","DC","2016",312,14,28.4,122.4,28,10,2,0,"Batter"),
        ("Shikhar Dhawan","SRH","2016",501,14,41.8,137.9,52,14,5,0,"Opener"),
        ("Yuvraj Singh","SRH","2016",266,14,22.2,148.0,18,22,1,0,"Batter"),
        ("Lokesh Rahul","RCB","2016",397,14,33.1,152.4,36,18,3,0,"WK-Bat"),
        ("Ajinkya Rahane","RR","2016",374,14,31.2,116.2,36,8,3,0,"Opener"),
        ("Lokesh Rahul","PBKS","2016",186,10,20.7,122.4,16,8,1,0,"Opener"),
        ("Glenn Maxwell","PBKS","2016",296,14,23.2,152.8,24,18,1,0,"All-rounder"),
        ("David Warner","SRH","2017",641,14,58.3,148.1,60,26,6,2,"🟠 Orange Cap"),
        ("Brendon McCullum","GL","2017",436,14,31.1,129.2,47,18,2,0,"Opener"),
        ("Shreyas Iyer","DC","2017",338,14,26.0,123.0,28,14,2,0,"Top Order"),
        ("MS Dhoni","RPS","2017",290,15,26.4,116.9,16,12,1,0,"Finisher"),
        ("Hardik Pandya","MI","2017",220,14,22.0,191.3,16,20,0,0,"All-rounder"),
        ("Rohit Sharma","MI","2017",333,13,30.3,122.7,32,10,2,0,"Captain"),
        ("Krunal Pandya","MI","2017",228,14,24.2,138.4,16,18,0,0,"All-rounder"),
        ("Suresh Raina","GL","2017",420,15,35.0,148.4,40,20,3,0,"Batter"),
        ("Dinesh Karthik","GL","2017",286,15,22.0,134.4,24,14,1,0,"WK-Bat"),
        ("MS Dhoni","RPS","2017",290,15,26.4,116.9,16,12,1,0,"Captain"),
        ("Steve Smith","RPS","2017",472,17,35.2,116.2,44,10,4,0,"Captain"),
        ("Ajinkya Rahane","RPS","2017",374,16,28.8,110.4,36,6,3,0,"Batter"),
        ("Gautam Gambhir","KKR","2017",276,13,23.0,115.2,26,6,1,0,"Captain"),
        ("Robin Uthappa","KKR","2017",412,14,34.3,135.2,36,18,3,0,"Opener"),
        ("Shikhar Dhawan","SRH","2017",479,14,43.5,118.4,48,10,4,1,"Opener"),
        ("Yuvraj Singh","SRH","2017",275,14,25.0,138.4,22,14,1,0,"Batter"),
        ("Shreyas Iyer","DC","2017",338,14,26.0,123.0,28,14,2,0,"Batter"),
        ("Rishabh Pant","DC","2017",366,14,30.5,158.0,28,22,2,0,"WK-Bat"),
        ("Ajinkya Rahane","RR","2017",386,14,30.8,110.8,36,10,3,0,"Opener"),
        ("Lokesh Rahul","PBKS","2017",366,14,30.5,138.6,34,16,2,0,"Opener"),
        ("Glenn Maxwell","PBKS","2017",310,14,25.8,154.0,24,22,2,0,"All-rounder"),
        ("Virat Kohli","RCB","2017",308,10,34.2,128.2,28,12,3,0,"Captain"),
        ("Chris Gayle","RCB","2017",200,9,25.0,141.0,14,20,0,0,"Opener"),
        ("Kane Williamson","SRH","2018",735,17,52.5,142.9,68,20,8,2,"🟠 Orange Cap"),
        ("Ajinkya Rahane","RR","2018",417,13,37.9,126.1,44,10,4,0,"Top Order"),
        ("Andre Russell","KKR","2018",316,9,45.1,204.5,19,31,1,1,"💥 Best SR"),
        ("Rohit Sharma","MI","2018",286,14,25.1,122.7,28,10,2,0,"Captain"),
        ("Ishan Kishan","MI","2018",258,14,22.2,136.8,24,14,1,0,"WK-Bat"),
        ("Suresh Raina","CSK","2018",557,16,46.4,152.8,52,26,5,0,"Batter"),
        ("Shane Watson","CSK","2018",555,16,46.3,157.0,48,30,4,1,"Opener"),
        ("MS Dhoni","CSK","2018",455,16,75.8,150.6,28,32,2,0,"Finisher"),
        ("Dinesh Karthik","KKR","2018",498,16,45.3,151.8,40,28,4,0,"WK-Captain"),
        ("Chris Lynn","KKR","2018",285,10,31.7,157.8,28,18,1,0,"Opener"),
        ("Shikhar Dhawan","SRH","2018",497,14,45.2,135.4,48,18,5,1,"Opener"),
        ("Manish Pandey","SRH","2018",312,15,26.0,126.4,28,10,2,0,"Batter"),
        ("Rishabh Pant","DC","2018",684,14,52.6,173.6,55,37,5,0,"WK-Bat"),
        ("Shreyas Iyer","DC","2018",413,15,32.1,134.2,38,16,3,0,"Batter"),
        ("Lokesh Rahul","PBKS","2018",659,14,54.9,158.6,62,30,6,2,"WK-Bat"),
        ("Chris Gayle","PBKS","2018",366,13,30.5,150.0,28,32,2,1,"Opener"),
        ("Sanju Samson","RR","2018",441,13,48.9,152.4,36,28,4,0,"WK-Bat"),
        ("Jos Buttler","RR","2018",548,13,50.4,152.4,52,26,5,2,"WK-Opener"),
        ("Virat Kohli","RCB","2018",530,16,48.2,151.4,52,20,4,0,"Captain"),
        ("AB de Villiers","RCB","2018",480,15,40.0,174.6,38,28,3,0,"Batter"),
        ("David Warner","SRH","2019",692,12,69.2,143.9,57,26,8,1,"🟠 Orange Cap"),
        ("KL Rahul","PBKS","2019",593,14,53.9,135.2,58,22,6,1,"Top Order"),
        ("AB de Villiers","RCB","2019",442,15,40.2,158.5,37,26,2,1,"Impact"),
        ("MS Dhoni","CSK","2019",416,16,83.2,134.6,28,23,2,0,"Finisher"),
        ("Rohit Sharma","MI","2019",405,15,31.2,128.0,35,16,3,0,"Opener"),
        ("Hardik Pandya","MI","2019",402,16,33.5,191.4,26,36,2,0,"All-rounder"),
        ("Quinton de Kock","MI","2019",529,16,38.2,138.2,52,18,5,1,"WK-Opener"),
        ("Ruturaj Gaikwad","CSK","2019",124,10,15.5,124.0,12,4,0,0,"Prospect"),
        ("Shane Watson","CSK","2019",398,17,28.4,144.2,32,22,2,0,"Opener"),
        ("Suresh Raina","CSK","2019",330,16,25.4,136.8,28,14,2,0,"Batter"),
        ("Andre Russell","KKR","2019",510,14,56.7,204.8,28,52,3,2,"All-rounder"),
        ("Chris Lynn","KKR","2019",186,10,22.4,138.2,18,12,1,0,"Opener"),
        ("Jonny Bairstow","SRH","2019",445,10,55.6,152.4,40,28,4,1,"Opener"),
        ("Shreyas Iyer","DC","2019",463,16,32.2,128.4,44,14,3,0,"Captain"),
        ("Rishabh Pant","DC","2019",488,16,34.9,162.4,42,28,4,0,"WK-Bat"),
        ("Lokesh Rahul","PBKS","2019",593,14,53.9,135.2,58,22,6,1,"WK-Captain"),
        ("Sanju Samson","RR","2019",342,12,38.0,148.4,30,20,3,1,"WK-Bat"),
        ("Steve Smith","RR","2019",319,16,24.5,100.4,28,6,2,0,"Captain"),
        ("KL Rahul","PBKS","2020",670,14,55.8,140.7,62,23,6,1,"🟠 Orange Cap"),
        ("Shikhar Dhawan","DC","2020",618,16,44.1,144.8,55,22,5,1,"Opener"),
        ("Aaron Finch","RCB","2020",519,15,39.9,132.2,44,22,4,0,"Top Order"),
        ("Rishabh Pant","DC","2020",343,13,34.3,169.9,26,21,2,0,"WK-Bat"),
        ("MS Dhoni","CSK","2020",200,16,25.0,116.3,15,10,0,0,"Captain"),
        ("Ruturaj Gaikwad","CSK","2020",204,12,22.7,124.4,20,6,1,0,"Opener"),
        ("Ambati Rayudu","CSK","2020",186,12,21.0,132.4,16,8,1,0,"Middle Order"),
        ("Ishan Kishan","MI","2020",516,14,43.0,145.8,48,26,4,0,"WK-Bat"),
        ("Hardik Pandya","MI","2020",281,12,31.2,174.2,18,26,1,0,"All-rounder"),
        ("Suryakumar Yadav","MI","2020",480,16,40.0,145.2,46,20,4,0,"Batter"),
        ("Sanju Samson","RR","2020",375,14,32.2,158.6,30,24,3,1,"WK-Bat"),
        ("Mayank Agarwal","PBKS","2020",424,11,47.1,158.4,40,22,4,1,"Opener"),
        ("Glenn Maxwell","PBKS","2020",108,13,10.8,100.9,8,8,0,0,"All-rounder"),
        ("Shreyas Iyer","DC","2020",519,17,34.6,123.4,48,12,4,0,"Captain"),
        ("David Warner","SRH","2020",548,16,39.1,134.2,52,18,5,1,"Opener"),
        ("Jonny Bairstow","SRH","2020",345,12,34.5,148.4,30,20,3,1,"Opener"),
        ("Nitish Rana","KKR","2020",352,14,30.6,126.4,32,14,2,0,"Opener"),
        ("Eoin Morgan","KKR","2020",186,14,18.6,110.2,14,8,0,0,"Captain"),
        ("Faf du Plessis","CSK","2021",633,16,56.6,136.3,68,18,6,2,"🟠 Orange Cap"),
        ("Shreyas Iyer","DC","2021",617,16,47.5,138.9,62,22,5,1,"Top Order"),
        ("Rishabh Pant","DC","2021",626,16,52.2,155.4,61,29,5,1,"Impact"),
        ("Devdutt Padikkal","RCB","2021",580,13,44.6,158.4,57,26,6,1,"Opener"),
        ("Sanju Samson","RR","2021",484,13,40.3,148.2,42,32,4,0,"WK-Bat"),
        ("Evin Lewis","RR","2021",198,10,22.0,148.4,18,14,1,0,"Opener"),
        ("MS Dhoni","CSK","2021",114,11,18.8,127.4,8,6,0,0,"Finisher"),
        ("Ruturaj Gaikwad","CSK","2021",635,16,45.4,136.2,62,20,6,1,"Opener"),
        ("Rohit Sharma","MI","2021",381,14,34.6,140.8,36,16,3,0,"Captain"),
        ("Kieron Pollard","MI","2021",268,14,29.8,168.4,18,24,1,0,"Finisher"),
        ("Nitish Rana","KKR","2021",480,14,40.0,126.2,44,18,4,0,"Opener"),
        ("Venkatesh Iyer","KKR","2021",370,10,46.3,137.4,36,18,3,0,"Opener"),
        ("David Warner","SRH","2021",195,8,27.9,141.2,18,10,1,0,"Opener"),
        ("Manish Pandey","SRH","2021",242,10,26.9,118.4,22,6,2,0,"Batter"),
        ("Shikhar Dhawan","PBKS","2021",587,14,48.9,127.2,62,12,6,1,"Opener"),
        ("KL Rahul","PBKS","2021",331,13,33.1,138.4,30,14,3,0,"WK-Captain"),
        ("Prithvi Shaw","DC","2021",308,13,28.0,162.4,30,14,2,0,"Opener"),
        ("Jos Buttler","RR","2022",863,17,57.5,145.8,78,45,7,4,"🟠 Orange Cap"),
        ("KL Rahul","LSG","2022",616,15,51.3,135.1,55,18,5,1,"Captain"),
        ("Quinton de Kock","LSG","2022",508,16,35.0,140.2,48,20,4,1,"Opener"),
        ("Rohit Sharma","MI","2022",268,14,22.3,125.2,26,12,2,0,"Captain"),
        ("Ishan Kishan","MI","2022",418,14,36.2,148.2,38,24,3,1,"WK-Bat"),
        ("Suryakumar Yadav","MI","2022",303,13,30.3,168.4,22,22,2,0,"Power Hitter"),
        ("Ruturaj Gaikwad","CSK","2022",368,13,32.8,126.4,36,12,2,0,"Opener"),
        ("MS Dhoni","CSK","2022",232,14,29.0,169.8,14,22,0,0,"Finisher"),
        ("Robin Uthappa","CSK","2022",266,13,24.2,132.2,24,12,2,0,"Opener"),
        ("Nitish Rana","KKR","2022",412,14,35.4,138.2,38,18,3,0,"Opener"),
        ("Sam Billings","KKR","2022",286,12,29.2,144.2,24,16,1,0,"WK-Bat"),
        ("Shubman Gill","GT","2022",483,16,40.3,132.2,46,16,4,1,"Opener"),
        ("Hardik Pandya","GT","2022",487,15,44.3,131.2,46,18,3,0,"Captain"),
        ("David Warner","DC","2022",432,14,36.0,154.8,40,24,3,0,"Opener"),
        ("Rishabh Pant","DC","2022",340,14,30.9,150.2,28,20,1,0,"WK-Captain"),
        ("Umran Malik","SRH","2022",218,14,22.8,162.4,14,20,1,0,"Hitter"),
        ("Abhishek Sharma","SRH","2022",326,14,26.5,152.8,28,22,2,0,"Opener"),
        ("Sanju Samson","RR","2022",458,13,42.2,148.8,40,28,4,1,"WK-Captain"),
        ("Liam Livingstone","PBKS","2022",437,14,37.2,180.6,32,34,3,0,"All-rounder"),
        ("Mayank Agarwal","PBKS","2022",368,14,30.7,148.2,34,16,2,0,"Captain"),
        ("Shubman Gill","GT","2023",890,17,59.3,157.9,76,48,8,3,"🟠 Orange Cap"),
        ("Virat Kohli","RCB","2023",639,14,53.3,136.6,65,20,6,1,"Impact"),
        ("Yashasvi Jaiswal","RR","2023",625,14,48.1,163.5,55,28,5,1,"Breakthrough"),
        ("Sanju Samson","RR","2023",490,14,40.8,148.0,44,28,4,1,"WK-Bat"),
        ("MS Dhoni","CSK","2023",286,12,35.8,182.2,16,26,0,0,"Finisher"),
        ("Ruturaj Gaikwad","CSK","2023",590,16,44.8,148.2,56,22,5,1,"Captain"),
        ("Devon Conway","CSK","2023",512,16,42.7,138.4,50,16,4,1,"Opener"),
        ("Faf du Plessis","RCB","2023",639,14,53.3,136.6,65,20,6,1,"Captain"),
        ("Rohit Sharma","MI","2023",442,14,36.8,128.2,44,16,3,0,"Captain"),
        ("Suryakumar Yadav","MI","2023",368,13,34.2,168.4,28,28,2,0,"Power Hitter"),
        ("David Warner","DC","2023",362,13,32.9,154.2,34,20,2,0,"Opener"),
        ("Manish Pandey","LSG","2023",218,12,22.8,138.2,20,10,1,0,"Middle Order"),
        ("KL Rahul","LSG","2023",576,14,48.0,136.2,54,16,5,1,"WK-Captain"),
        ("Travis Head","SRH","2023",488,14,40.7,188.2,44,34,4,1,"Opener"),
        ("Heinrich Klaasen","SRH","2023",402,13,40.2,166.4,30,32,3,1,"WK-Bat"),
        ("Rinku Singh","KKR","2023",474,14,43.1,149.1,40,28,3,0,"Finisher"),
        ("Nitish Rana","KKR","2023",312,14,27.1,138.2,28,16,2,0,"Opener"),
        ("Liam Livingstone","PBKS","2023",368,13,34.2,162.4,28,28,2,0,"All-rounder"),
        ("Prabhsimran Singh","PBKS","2023",298,12,27.1,148.2,26,18,1,0,"Opener"),
        ("Virat Kohli","RCB","2024",741,15,61.8,154.7,65,22,5,1,"🟠 Orange Cap"),
        ("Yashasvi Jaiswal","RR","2024",435,13,39.5,157.9,36,28,3,1,"Opener"),
        ("Sanju Samson","RR","2024",531,14,45.8,150.3,48,26,5,1,"WK-Bat"),
        ("Venkatesh Iyer","KKR","2024",351,14,43.9,154.4,30,20,3,0,"Captain"),
        ("Rohit Sharma","MI","2024",420,14,36.2,132.1,40,18,3,0,"Opener"),
        ("Suryakumar Yadav","MI","2024",468,14,42.5,168.2,38,32,4,0,"Power Hitter"),
        ("Ruturaj Gaikwad","CSK","2024",498,15,41.5,142.6,48,20,4,1,"Captain"),
        ("Shubman Gill","GT","2024",426,14,38.7,148.2,40,22,3,1,"Captain"),
        ("David Warner","DC","2024",380,13,34.5,152.8,36,22,2,0,"Opener"),
        ("Travis Head","SRH","2024",567,14,48.2,191.4,52,38,5,1,"Opener"),
        ("Abhishek Sharma","SRH","2024",484,14,40.3,186.2,42,36,4,1,"Opener"),
        ("KL Rahul","LSG","2024",520,14,46.2,136.8,50,16,5,1,"WK-Captain"),
        ("Nicholas Pooran","LSG","2024",462,13,42.0,168.6,34,40,4,1,"Finisher"),
        ("Shreyas Iyer","KKR","2024",351,14,43.9,154.4,30,20,3,0,"Captain"),
        ("Liam Livingstone","PBKS","2024",322,12,32.2,168.4,24,28,2,0,"All-rounder"),
        ("Yashasvi Jaiswal","RR","2024",435,13,39.5,157.9,36,28,3,1,"Opener"),
        ("Sanju Samson","RR","2024",531,14,45.8,150.3,48,26,5,1,"WK-Bat"),
        ("Venkatesh Iyer","KKR","2024",351,14,43.9,154.4,30,20,3,0,"Captain"),
        # ── 2026 BATTING DATA (Real Stats) ──────────────────
        ("Vaibhav Suryavanshi","RR","2026",776,16,48.50,237.30,58,72,5,2,"🟠 Orange Cap · MVP"),
        ("Shubman Gill","GT","2026",732,17,48.80,162.40,65,42,7,2,"Top Scorer"),
        ("Sai Sudharsan","GT","2026",722,17,48.13,152.20,75,28,7,1,"Most Fours"),
        ("Virat Kohli","RCB","2026",675,16,56.25,148.40,62,28,6,1,"🏆 Final POTM"),
        ("Abhishek Sharma","SRH","2026",612,15,45.50,194.30,48,48,5,1,"Opener"),
        ("KL Rahul","DC","2026",598,15,46.00,152.00,52,22,5,2,"152* Highest Score"),
        ("Yashasvi Jaiswal","RR","2026",554,15,42.60,168.20,48,38,4,1,"Opener"),
        ("Travis Head","SRH","2026",538,14,43.80,188.10,44,42,4,1,"Aggressive Opener"),
        ("Faf du Plessis","CSK","2026",498,15,38.30,142.80,48,26,4,0,"Captain"),
        ("Ruturaj Gaikwad","CSK","2026",476,15,36.60,138.40,46,20,4,0,"Opener"),
        ("Rohit Sharma","MI","2026",452,14,38.50,134.20,44,20,4,0,"Captain"),
        ("Suryakumar Yadav","MI","2026",488,15,40.70,172.60,38,38,4,0,"Power Hitter"),
        ("Rinku Singh","KKR","2026",412,14,37.40,158.40,34,28,3,0,"Finisher"),
        ("Phil Salt","KKR","2026",468,15,36.00,168.20,40,32,4,1,"Opener"),
        ("Jos Buttler","RCB","2026",421,13,38.20,162.80,36,30,3,1,"Opener"),
        ("Nicholas Pooran","LSG","2026",502,14,45.60,172.40,34,48,4,1,"WK-Bat"),
        ("Rishabh Pant","LSG","2026",438,13,39.80,154.20,38,28,4,1,"Captain"),
        ("Prabhsimran Singh","PBKS","2026",468,14,38.20,162.40,40,34,4,1,"Opener"),
        ("Shreyas Iyer","PBKS","2026",412,14,34.30,144.20,36,22,3,0,"Captain"),
        ("Jake Fraser-McGurk","DC","2026",524,15,40.30,192.60,40,46,4,1,"Explosive Opener"),
        ("Sanju Samson","RR","2026",398,13,36.20,152.40,36,28,3,1,"WK-Captain"),
        ("David Miller","GT","2026",376,13,34.20,158.40,28,32,2,0,"Finisher"),
        # 2026 RCB
        ("Devdutt Padikkal","RCB","2026",354,12,35.40,155.90,30,24,3,0,"Middle Order"),
        ("Krunal Pandya","RCB","2026",198,13,18.00,132.00,16,12,0,0,"All-rounder"),
        # 2026 DC
        ("Axar Patel","DC","2026",312,13,28.40,148.60,24,20,1,0,"All-rounder"),
        # ── END 2026 BATTING ──────────────────────────────────
        ("Sai Sudharsan","GT","2025",759,15,54.21,156.17,88,28,6,1,"🟠 Orange Cap"),
        ("Suryakumar Yadav","MI","2025",717,16,53.6,158.4,72,35,6,0,"⭐ Highest Impact"),
        ("Virat Kohli","RCB","2025",657,14,54.75,144.7,65,22,5,0,"🏆 Champion"),
        ("Shubman Gill","GT","2025",648,14,49.8,153.2,67,28,5,1,"Top Opener"),
        ("Jos Buttler","GT","2025",538,13,49.0,163.9,44,32,4,0,"Top-3"),
        ("Phil Salt","RCB","2025",512,14,40.9,148.7,51,26,4,0,"Top-3"),
        ("Yashasvi Jaiswal","RR","2025",506,14,43.1,152.3,52,24,4,0,"Top Opener"),
        ("Shreyas Iyer","PBKS","2025",491,15,37.8,141.5,43,21,3,0,"Captain"),
        ("Devdutt Padikkal","RCB","2025",469,12,52.1,159.2,46,22,4,0,"Final XI"),
        ("Krunal Pandya","RCB","2025",109,11,15.6,120.0,8,3,1,0,"Final MVP"),
        # MI 2025 extra
        ("Rohit Sharma","MI","2025",512,14,42.1,138.4,52,22,4,1,"Opener"),
        ("Hardik Pandya","MI","2025",341,13,32.4,148.6,26,28,2,0,"All-rounder"),
        ("Tilak Varma","MI","2025",428,14,38.5,152.4,38,24,3,0,"Middle Order"),
        # RR 2025 extra
        ("Sanju Samson","RR","2025",486,13,44.2,152.4,44,28,4,1,"WK-Captain"),
        ("Shimron Hetmyer","RR","2025",312,12,34.6,162.4,22,28,1,0,"Finisher"),
        # PBKS 2025 extra
        ("Prabhsimran Singh","PBKS","2025",421,14,36.2,158.6,38,28,3,1,"Opener"),
        ("Josh Inglis","PBKS","2025",312,12,31.8,148.4,28,18,2,0,"WK-Bat"),
        # GT 2025 extra
        ("Rashid Khan","GT","2025",142,12,18.6,148.4,10,14,0,0,"All-rounder"),
        ("David Miller","GT","2025",368,13,36.8,158.4,28,32,2,0,"Finisher"),
        # CSK 2025
        ("Ruturaj Gaikwad","CSK","2025",583,15,44.8,148.2,55,24,5,1,"Captain"),
        ("Devon Conway","CSK","2025",512,14,42.7,141.5,48,18,4,1,"Opener"),
        ("Shivam Dube","CSK","2025",398,14,36.2,158.6,28,32,2,0,"Finisher"),
        ("Ravindra Jadeja","CSK","2025",284,13,26.1,138.4,22,16,1,0,"All-rounder"),
        ("MS Dhoni","CSK","2025",198,12,28.3,140.1,12,18,0,0,"Finisher"),
        # KKR 2025
        ("Venkatesh Iyer","KKR","2025",468,14,38.5,148.6,42,28,3,0,"Captain"),
        ("Phil Salt","KKR","2025",421,13,37.4,162.4,38,24,3,1,"Opener"),
        ("Andre Russell","KKR","2025",312,12,36.1,188.5,18,34,0,1,"Finisher"),
        ("Rinku Singh","KKR","2025",287,13,31.8,145.2,22,18,2,0,"Middle Order"),
        ("Sunil Narine","KKR","2025",241,13,26.2,172.1,16,22,1,0,"Pinch Hitter"),
        # SRH 2025
        ("Travis Head","SRH","2025",567,14,46.2,189.4,54,36,4,1,"Opener"),
        ("Abhishek Sharma","SRH","2025",498,14,41.5,178.4,44,38,4,1,"Opener"),
        ("Heinrich Klaasen","SRH","2025",421,13,48.5,165.2,32,36,3,1,"WK-Bat"),
        ("Pat Cummins","SRH","2025",142,12,18.6,144.8,10,12,0,0,"Captain"),
        # DC 2025
        ("KL Rahul","DC","2025",534,14,46.8,138.2,52,18,5,1,"WK-Captain"),
        ("Jake Fraser-McGurk","DC","2025",487,14,39.8,182.3,42,38,3,1,"Opener"),
        ("Axar Patel","DC","2025",312,13,28.4,148.6,24,20,1,0,"All-rounder"),
        ("Tristan Stubbs","DC","2025",284,12,31.2,158.4,22,22,1,0,"Middle Order"),
        # LSG 2025
        ("Nicholas Pooran","LSG","2025",498,14,42.6,168.4,36,42,4,1,"WK-Bat"),
        ("Rishabh Pant","LSG","2025",467,13,43.8,152.6,44,28,3,1,"Captain"),
        ("Mitchell Marsh","LSG","2025",342,13,32.4,154.8,28,26,2,0,"All-rounder"),
        ("Quinton de Kock","LSG","2025",398,14,36.8,144.2,38,18,3,1,"Opener"),
    ], columns=["player","team","season","runs","innings","avg","sr","fours","sixes","fifties","hundreds","award"])

    bowling = pd.DataFrame([
        ("Bhuvneshwar Kumar","SRH","2016",26,7.05,18.2,15.5,6.8,6.6,7.9,42,"🟣 Purple Cap"),
        ("Yuzvendra Chahal","RCB","2016",23,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Ashish Nehra","RCB","2016",16,7.12,21.6,18.2,6.9,7.0,7.5,40,"Pace"),
        ("Morne Morkel","DC","2016",17,7.88,23.1,17.8,7.5,7.8,8.5,36,"Pace"),
        ("Kagiso Rabada","DC","2016",23,8.34,18.8,13.5,7.9,8.2,9.8,34,"Pace"),
        ("Zaheer Khan","DC","2016",14,8.12,24.2,17.9,7.8,8.0,9.4,33,"Swing"),
        ("Chris Morris","DC","2016",13,8.92,25.4,17.2,8.5,9.0,10.2,29,"All-rounder"),
        ("Jasprit Bumrah","MI","2016",15,7.43,20.4,16.4,6.8,7.2,8.8,40,"Pace"),
        ("Harbhajan Singh","MI","2016",16,7.22,22.8,19.0,6.9,7.1,8.4,38,"Off Spin"),
        ("Mitchell McClenaghan","MI","2016",14,8.42,22.4,16.0,8.0,8.4,9.8,33,"Left Arm Pace"),
        ("Suresh Raina","CSK","2016",8,7.92,28.4,21.5,7.5,8.0,9.2,31,"Part Timer"),
        ("Ravindra Jadeja","CSK","2016",12,7.02,24.8,21.2,6.7,7.0,8.2,38,"Spin"),
        ("Dwayne Bravo","CSK","2016",16,8.52,22.4,15.8,8.1,8.5,9.8,32,"Death Spec"),
        ("Umesh Yadav","RCB","2016",20,9.12,22.4,14.7,8.6,9.0,10.6,30,"Pace"),
        ("S Aravind","RCB","2016",12,8.82,24.8,16.9,8.4,8.8,10.2,30,"Pace"),
        ("Piyush Chawla","KKR","2016",17,7.42,22.4,18.2,7.1,7.4,8.6,37,"Leg Spin"),
        ("Sunil Narine","KKR","2016",21,6.62,18.8,17.1,6.3,6.6,7.8,42,"Mystery Spin"),
        ("Umesh Yadav","KKR","2016",16,8.92,23.4,15.7,8.5,8.9,10.4,30,"Pace"),
        ("Ajit Chandila","RPS","2016",10,8.22,26.4,19.3,7.8,8.2,9.8,30,"Spin"),
        ("Ashoke Dinda","RPS","2016",12,8.92,25.4,17.1,8.5,8.9,10.4,28,"Pace"),
        ("Ajinkya Rahane","RR","2016",0,0.0,0.0,0.0,0.0,0.0,0.0,0,"Captain"),
        ("Dhawal Kulkarni","RR","2016",15,8.42,23.4,16.7,8.0,8.4,9.8,32,"Swing"),
        ("Stuart Binny","RR","2016",11,8.72,25.4,17.5,8.3,8.7,10.2,29,"All-rounder"),
        ("Mohit Sharma","PBKS","2016",14,8.62,24.2,16.8,8.2,8.6,10.0,31,"Pace"),
        ("Axar Patel","PBKS","2016",18,7.22,22.4,18.6,6.9,7.2,8.4,37,"Left Arm Spin"),
        ("Bhuvneshwar Kumar","SRH","2017",26,7.05,18.2,15.5,6.5,6.6,7.9,42,"🟣 Purple Cap"),
        ("Jasprit Bumrah","MI","2017",20,7.43,17.3,13.4,6.8,6.5,8.3,44,"Pace"),
        ("Rashid Khan","SRH","2017",17,6.28,21.6,20.6,5.9,5.8,7.4,42,"Leg Spin"),
        ("Siddarth Kaul","SRH","2017",23,8.42,20.4,14.6,8.0,8.4,9.8,33,"Pace"),
        ("Bipul Sharma","SRH","2017",11,7.82,26.4,20.3,7.4,7.8,9.2,34,"Spin"),
        ("Mohammad Nabi","SRH","2017",10,7.12,24.8,21.0,6.8,7.1,8.4,36,"Off Spin"),
        ("Jasprit Bumrah","MI","2017",20,7.43,17.3,13.4,6.8,6.5,8.3,44,"Pace"),
        ("Harbhajan Singh","MI","2017",14,7.42,24.4,19.8,7.1,7.4,8.6,37,"Off Spin"),
        ("Lasith Malinga","MI","2017",12,8.22,22.8,16.6,7.8,8.2,9.6,33,"Swing Pace"),
        ("Praveen Kumar","GL","2017",12,8.42,24.2,17.3,8.0,8.4,9.8,31,"Swing"),
        ("Basil Thampi","GL","2017",13,9.02,24.8,16.5,8.6,9.0,10.4,28,"Pace"),
        ("Dhawal Kulkarni","RR","2017",13,8.62,25.4,17.7,8.2,8.6,10.0,30,"Swing"),
        ("Jaydev Unadkat","RR","2017",24,8.12,19.8,14.6,7.7,8.1,9.4,35,"Left Arm Pace"),
        ("Imran Tahir","RPS","2017",18,7.52,22.4,17.9,7.2,7.5,8.6,36,"Leg Spin"),
        ("Shardul Thakur","RPS","2017",12,9.02,25.8,17.2,8.6,9.0,10.4,28,"Pace"),
        ("Piyush Chawla","KKR","2017",15,7.62,24.4,19.2,7.3,7.6,8.8,36,"Leg Spin"),
        ("Sunil Narine","KKR","2017",18,6.72,20.4,18.2,6.4,6.7,7.8,40,"Mystery Spin"),
        ("Yuzvendra Chahal","RCB","2017",21,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Chris Woakes","RCB","2017",13,8.62,24.8,17.2,8.2,8.6,10.0,31,"Swing"),
        ("Axar Patel","PBKS","2017",16,7.32,24.4,20.0,7.0,7.3,8.5,36,"Left Arm Spin"),
        ("Sandeep Sharma","PBKS","2017",14,8.42,24.2,17.3,8.0,8.4,9.8,32,"Swing"),
        ("Amit Mishra","DC","2017",16,7.82,24.4,18.8,7.5,7.8,9.0,35,"Leg Spin"),
        ("Kagiso Rabada","DC","2017",23,8.34,18.8,13.5,7.9,8.2,9.8,34,"Pace"),
        ("Andrew Tye","PBKS","2018",24,8.27,19.1,13.9,7.9,8.1,9.1,36,"🟣 Purple Cap"),
        ("Jasprit Bumrah","MI","2018",17,7.43,18.3,14.4,6.8,6.5,8.3,44,"Pace"),
        ("Rashid Khan","SRH","2018",21,6.28,20.0,19.0,5.9,5.8,7.4,44,"Leg Spin"),
        ("Siddarth Kaul","SRH","2018",21,8.42,20.4,14.6,8.0,8.4,9.8,33,"Pace"),
        ("Bhuvneshwar Kumar","SRH","2018",24,7.42,18.2,14.8,7.1,7.4,8.6,40,"Swing"),
        ("Dwayne Bravo","CSK","2018",26,8.22,19.8,14.5,7.8,8.2,9.6,33,"Death Spec"),
        ("Ravindra Jadeja","CSK","2018",16,7.12,24.8,20.9,6.8,7.1,8.2,37,"Spin"),
        ("Deepak Chahar","CSK","2018",12,8.42,24.4,17.4,8.0,8.4,9.8,32,"Swing"),
        ("Jasprit Bumrah","MI","2018",17,7.43,18.3,14.4,6.8,6.5,8.3,44,"Pace"),
        ("Hardik Pandya","MI","2018",14,8.62,23.4,16.3,8.2,8.6,10.0,31,"All-rounder"),
        ("Lasith Malinga","MI","2018",16,8.22,22.4,16.4,7.8,8.2,9.6,33,"Pace"),
        ("Piyush Chawla","KKR","2018",17,7.52,22.4,17.9,7.2,7.5,8.6,37,"Leg Spin"),
        ("Sunil Narine","KKR","2018",17,6.62,20.4,18.5,6.3,6.6,7.8,41,"Mystery Spin"),
        ("Kuldeep Yadav","KKR","2018",17,7.52,22.4,17.9,7.2,7.5,8.6,37,"Wrist Spin"),
        ("Yuzvendra Chahal","RCB","2018",18,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Umesh Yadav","RCB","2018",20,9.12,22.4,14.7,8.6,9.0,10.6,30,"Pace"),
        ("Kagiso Rabada","DC","2018",18,8.44,22.4,16.0,8.0,8.4,9.8,33,"Pace"),
        ("Amit Mishra","DC","2018",14,7.92,26.4,20.0,7.6,7.9,9.2,34,"Leg Spin"),
        ("Jaydev Unadkat","RR","2018",11,9.52,28.4,17.9,9.1,9.5,11.0,26,"Left Arm Pace"),
        ("Shreyas Gopal","RR","2018",20,8.42,20.4,14.6,8.0,8.4,9.8,33,"Leg Spin"),
        ("Axar Patel","PBKS","2018",10,7.22,26.4,21.9,6.9,7.2,8.4,36,"Left Arm Spin"),
        ("Mujeeb ur Rahman","PBKS","2018",14,6.92,22.4,19.4,6.6,6.9,8.0,39,"Mystery Spin"),
        ("Ishant Sharma","MI","2019",19,8.04,22.0,16.4,7.6,7.9,9.0,34,"🟣 Purple Cap"),
        ("Rashid Khan","SRH","2019",25,6.28,21.6,20.6,5.9,5.8,7.4,44,"Top Spinner"),
        ("Jasprit Bumrah","MI","2019",19,7.43,17.3,13.4,6.8,6.5,8.3,44,"Pace"),
        ("Lasith Malinga","MI","2019",16,8.22,22.4,16.4,7.8,8.2,9.6,33,"Pace"),
        ("Hardik Pandya","MI","2019",14,8.62,23.4,16.3,8.2,8.6,10.0,31,"All-rounder"),
        ("Rahul Chahar","MI","2019",13,8.02,24.4,18.3,7.7,8.0,9.2,34,"Leg Spin"),
        ("Dwayne Bravo","CSK","2019",22,8.42,20.4,14.6,8.0,8.4,9.8,33,"Death Spec"),
        ("Deepak Chahar","CSK","2019",22,8.22,18.4,13.4,7.8,8.2,9.6,34,"Swing"),
        ("Ravindra Jadeja","CSK","2019",15,7.02,24.8,21.2,6.7,7.0,8.2,37,"Spin"),
        ("Imran Tahir","CSK","2019",26,6.62,15.8,14.3,6.3,6.6,7.8,44,"Leg Spin"),
        ("Rashid Khan","SRH","2019",25,6.28,21.6,20.6,5.9,5.8,7.4,44,"Leg Spin"),
        ("Bhuvneshwar Kumar","SRH","2019",16,7.22,22.4,18.7,6.9,7.2,8.4,38,"Swing"),
        ("Sandeep Sharma","SRH","2019",21,8.02,20.4,15.3,7.6,8.0,9.4,34,"Swing"),
        ("Kagiso Rabada","DC","2019",25,8.34,17.0,12.2,7.9,8.2,9.8,34,"Pace"),
        ("Amit Mishra","DC","2019",15,7.82,24.8,19.0,7.5,7.8,9.0,35,"Leg Spin"),
        ("Sunil Narine","KKR","2019",17,6.72,22.4,20.0,6.4,6.7,7.8,39,"Mystery Spin"),
        ("Piyush Chawla","KKR","2019",15,7.62,24.4,19.2,7.3,7.6,8.8,36,"Leg Spin"),
        ("Mujeeb ur Rahman","PBKS","2019",17,7.02,22.4,19.2,6.7,7.0,8.2,38,"Mystery Spin"),
        ("Mohammed Shami","PBKS","2019",19,8.82,22.4,15.3,8.4,8.8,10.2,31,"Pace"),
        ("Jaydev Unadkat","RR","2019",13,9.12,26.4,17.4,8.7,9.1,10.6,27,"Left Arm Pace"),
        ("Shreyas Gopal","RR","2019",20,8.22,20.4,14.9,7.8,8.2,9.6,34,"Leg Spin"),
        ("Yuzvendra Chahal","RCB","2019",18,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Navdeep Saini","RCB","2019",11,9.02,24.8,16.5,8.6,9.0,10.4,28,"Pace"),
        ("Kagiso Rabada","DC","2020",30,8.34,17.0,12.2,7.8,8.0,9.2,34,"🟣 Purple Cap"),
        ("Jasprit Bumrah","MI","2020",27,7.43,15.3,12.4,6.8,6.5,8.3,45,"Top Pacer"),
        ("Trent Boult","MI","2020",25,7.92,17.4,13.2,7.5,7.9,8.9,37,"Swing"),
        ("Rahul Chahar","MI","2020",15,8.02,22.4,16.8,7.7,8.0,9.2,34,"Leg Spin"),
        ("James Pattinson","MI","2020",14,8.52,22.8,16.1,8.1,8.5,9.9,32,"Pace"),
        ("Deepak Chahar","CSK","2020",12,8.12,24.4,18.1,7.7,8.1,9.5,33,"Swing"),
        ("Ravindra Jadeja","CSK","2020",13,7.12,26.8,22.6,6.8,7.1,8.3,37,"Spin"),
        ("Dwayne Bravo","CSK","2020",12,8.52,24.4,17.2,8.1,8.5,9.9,31,"Death Spec"),
        ("Yuzvendra Chahal","RCB","2020",21,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Navdeep Saini","RCB","2020",13,8.82,24.8,16.9,8.4,8.8,10.2,30,"Pace"),
        ("Amit Mishra","DC","2020",13,7.92,26.4,20.1,7.6,7.9,9.2,34,"Leg Spin"),
        ("R Ashwin","DC","2020",13,7.42,24.4,19.8,7.1,7.4,8.6,36,"Off Spin"),
        ("Anrich Nortje","DC","2020",22,8.42,20.4,14.6,8.0,8.4,9.8,33,"Pace"),
        ("Lockie Ferguson","KKR","2020",17,8.62,22.4,15.6,8.2,8.6,10.0,32,"Pace"),
        ("Sunil Narine","KKR","2020",15,6.72,22.4,20.0,6.4,6.7,7.8,39,"Mystery Spin"),
        ("Pat Cummins","KKR","2020",12,9.22,26.4,17.2,8.8,9.2,10.6,28,"Pace"),
        ("Mohammed Shami","PBKS","2020",20,8.82,22.4,15.3,8.4,8.8,10.2,31,"Pace"),
        ("Ravi Bishnoi","PBKS","2020",12,7.82,24.4,18.8,7.5,7.8,8.8,34,"Leg Spin"),
        ("Murugan Ashwin","PBKS","2020",10,7.52,26.4,21.1,7.2,7.5,8.6,35,"Leg Spin"),
        ("Jaydev Unadkat","RR","2020",11,9.22,28.4,18.5,8.8,9.2,10.6,27,"Left Arm Pace"),
        ("Rahul Tewatia","RR","2020",10,8.22,28.4,20.8,7.8,8.2,9.6,28,"Leg Spin"),
        ("Rashid Khan","SRH","2020",20,5.88,18.6,19.0,5.6,5.8,7.0,46,"Leg Spin"),
        ("Sandeep Sharma","SRH","2020",14,8.02,22.4,16.8,7.6,8.0,9.4,34,"Swing"),
        ("T Natarajan","SRH","2020",16,8.56,22.3,15.6,8.2,8.3,9.3,32,"Yorker King"),
        ("Harshal Patel","RCB","2021",32,8.91,16.8,11.3,8.1,8.5,10.2,32,"🟣 Purple Cap"),
        ("Jasprit Bumrah","MI","2021",21,7.43,17.3,13.4,6.8,6.5,8.3,44,"Pace"),
        ("Yuzvendra Chahal","RR","2021",18,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Chris Morris","RR","2021",13,8.52,22.4,15.8,8.1,8.5,9.9,32,"All-rounder"),
        ("Kartik Tyagi","RR","2021",11,9.02,26.4,17.6,8.6,9.0,10.4,28,"Pace"),
        ("Ravindra Jadeja","CSK","2021",13,7.02,24.8,21.3,6.7,7.0,8.2,38,"Spin"),
        ("Deepak Chahar","CSK","2021",14,7.52,22.4,17.9,7.2,7.5,8.6,35,"Swing"),
        ("Josh Hazlewood","CSK","2021",18,7.12,18.4,15.5,6.8,7.1,8.4,40,"Pace"),
        ("Jasprit Bumrah","MI","2021",21,7.43,17.3,13.4,6.8,6.5,8.3,44,"Pace"),
        ("Trent Boult","MI","2021",18,7.92,20.4,15.5,7.5,7.9,8.9,36,"Swing"),
        ("Rahul Chahar","MI","2021",17,8.02,21.4,16.0,7.7,8.0,9.2,34,"Leg Spin"),
        ("Sunil Narine","KKR","2021",21,6.72,20.4,18.2,6.4,6.7,7.8,40,"Mystery Spin"),
        ("Varun Chakravarthy","KKR","2021",18,7.12,22.4,18.9,6.8,7.1,8.4,38,"Mystery Spin"),
        ("Lockie Ferguson","KKR","2021",16,8.62,22.4,15.6,8.2,8.6,10.0,32,"Pace"),
        ("Rashid Khan","SRH","2021",18,6.08,19.4,19.2,5.8,6.0,7.4,44,"Leg Spin"),
        ("Bhuvneshwar Kumar","SRH","2021",14,7.42,22.4,18.2,7.1,7.4,8.6,37,"Swing"),
        ("R Ashwin","PBKS","2021",15,7.42,24.4,19.8,7.1,7.4,8.6,36,"Off Spin"),
        ("Arshdeep Singh","PBKS","2021",14,8.42,22.4,16.0,8.0,8.4,9.8,33,"Left Arm Pace"),
        ("Yuzvendra Chahal","RCB","2021",18,7.58,22.1,17.5,7.2,7.0,8.3,36,"Leg Spin"),
        ("Mohammed Siraj","RCB","2021",15,8.45,22.6,16.0,8.1,8.0,9.2,33,"Pace"),
        ("Kagiso Rabada","DC","2021",13,8.44,22.4,16.0,8.0,8.4,9.8,33,"Pace"),
        ("Amit Mishra","DC","2021",11,7.92,28.4,21.5,7.6,7.9,9.2,33,"Leg Spin"),
        ("Avesh Khan","DC","2021",24,8.22,18.4,13.4,7.8,8.2,9.6,35,"Pace"),
        ("Yuzvendra Chahal","RR","2022",27,7.58,22.1,17.5,7.2,7.0,8.3,36,"🟣 Purple Cap"),
        ("Kagiso Rabada","PBKS","2022",23,8.34,20.1,14.3,7.8,8.0,9.2,34,"Pace"),
        ("Trent Boult","MI","2022",21,8.12,23.1,17.0,7.5,7.9,8.9,33,"Swing"),
        ("Jasprit Bumrah","MI","2022",15,7.43,19.3,15.6,6.8,6.5,8.3,40,"Pace"),
        ("Murugan Ashwin","MI","2022",13,8.22,24.4,17.8,7.8,8.2,9.6,32,"Leg Spin"),
        ("Deepak Chahar","CSK","2022",12,8.12,24.4,18.1,7.7,8.1,9.5,33,"Swing"),
        ("Dwayne Bravo","CSK","2022",16,8.72,22.4,15.4,8.3,8.7,10.2,31,"Death Spec"),
        ("Maheesh Theekshana","CSK","2022",18,7.22,22.4,18.6,6.9,7.2,8.4,37,"Mystery Spin"),
        ("Varun Chakravarthy","KKR","2022",20,7.42,21.4,17.3,7.1,7.4,8.6,38,"Mystery Spin"),
        ("Umesh Yadav","KKR","2022",16,8.82,22.4,15.3,8.4,8.8,10.2,31,"Pace"),
        ("Pat Cummins","KKR","2022",19,9.12,22.4,14.8,8.7,9.1,10.6,28,"Pace"),
        ("Mohammed Shami","GT","2022",20,7.92,19.4,14.7,7.5,7.9,9.2,36,"Pace"),
        ("Hardik Pandya","GT","2022",8,8.92,32.4,21.8,8.5,8.9,10.4,26,"All-rounder"),
        ("Lockie Ferguson","GT","2022",16,8.52,22.4,15.8,8.1,8.5,9.9,32,"Pace"),
        ("Dushmantha Chameera","LSG","2022",18,8.72,22.4,15.4,8.3,8.7,10.2,31,"Pace"),
        ("Avesh Khan","LSG","2022",24,8.42,20.4,14.6,8.0,8.4,9.8,33,"Pace"),
        ("Ravi Bishnoi","LSG","2022",14,7.82,24.4,18.8,7.5,7.8,8.8,34,"Leg Spin"),
        ("Anrich Nortje","DC","2022",18,8.42,20.4,14.6,8.0,8.4,9.8,33,"Pace"),
        ("Axar Patel","DC","2022",15,7.52,24.4,19.5,7.2,7.5,8.6,36,"Left Arm Spin"),
        ("Kuldeep Yadav","DC","2022",21,8.02,20.6,15.4,7.6,8.0,9.2,36,"Wrist Spin"),
        ("Bhuvneshwar Kumar","SRH","2022",17,8.12,22.4,16.6,7.7,8.1,9.5,34,"Swing"),
        ("T Natarajan","SRH","2022",20,8.84,20.4,13.8,8.4,8.8,10.2,31,"Yorker King"),
        ("Umran Malik","SRH","2022",22,8.72,20.4,14.1,8.3,8.7,10.2,30,"Express Pace"),
        ("Prasidh Krishna","RR","2022",19,8.32,21.4,15.5,7.9,8.3,9.7,34,"Pace"),
        ("Trent Boult","RR","2022",13,8.22,24.4,17.8,7.8,8.2,9.6,32,"Swing"),
        ("R Ashwin","PBKS","2022",13,7.42,26.4,21.4,7.1,7.4,8.6,35,"Off Spin"),
        ("Kagiso Rabada","PBKS","2022",23,8.34,20.1,14.3,7.8,8.0,9.2,34,"Pace"),
        ("Arshdeep Singh","PBKS","2022",22,8.42,20.4,14.6,8.0,8.4,9.8,33,"Left Arm Pace"),
        ("Mohammed Shami","GT","2023",28,8.03,17.3,12.9,7.5,7.8,9.1,38,"🟣 Purple Cap"),
        ("Rashid Khan","GT","2023",27,6.28,16.0,15.6,5.9,5.8,7.4,46,"Top Spinner"),
        ("Prasidh Krishna","RCB","2023",22,8.12,18.9,14.0,7.8,7.9,8.9,36,"Pace"),
        ("Mohammed Siraj","RCB","2023",19,8.45,22.6,16.0,8.1,8.0,9.2,33,"Pace"),
        ("Wanindu Hasaranga","RCB","2023",16,8.32,24.4,17.7,7.9,8.3,9.7,33,"Leg Spin"),
        ("Deepak Chahar","CSK","2023",12,8.12,24.4,18.1,7.7,8.1,9.5,33,"Swing"),
        ("Maheesh Theekshana","CSK","2023",15,7.32,24.4,20.0,7.0,7.3,8.5,36,"Mystery Spin"),
        ("Tushar Deshpande","CSK","2023",22,9.12,20.4,13.4,8.7,9.1,10.6,28,"Pace"),
        ("Varun Chakravarthy","KKR","2023",21,7.42,21.4,17.3,7.1,7.4,8.6,38,"Mystery Spin"),
        ("Sunil Narine","KKR","2023",18,6.72,22.4,20.0,6.4,6.7,7.8,39,"Mystery Spin"),
        ("Shardul Thakur","KKR","2023",16,9.02,24.8,16.5,8.6,9.0,10.4,28,"Pace"),
        ("T Natarajan","SRH","2023",17,8.84,22.4,15.2,8.4,8.8,10.2,31,"Yorker King"),
        ("Bhuvneshwar Kumar","SRH","2023",15,8.12,22.4,16.6,7.7,8.1,9.5,34,"Swing"),
        ("Mayank Markande","SRH","2023",13,8.42,26.4,18.8,8.0,8.4,9.8,30,"Leg Spin"),
        ("Kuldeep Yadav","DC","2023",21,8.02,20.6,15.4,7.6,8.0,9.2,36,"Wrist Spin"),
        ("Axar Patel","DC","2023",14,7.52,26.4,21.1,7.2,7.5,8.6,35,"Left Arm Spin"),
        ("Anrich Nortje","DC","2023",16,8.42,22.4,16.0,8.0,8.4,9.8,32,"Pace"),
        ("Ravi Bishnoi","LSG","2023",21,7.82,22.4,17.2,7.5,7.8,8.8,35,"Leg Spin"),
        ("Mark Wood","LSG","2023",15,8.72,22.4,15.4,8.3,8.7,10.2,32,"Express Pace"),
        ("Mohsin Khan","LSG","2023",14,8.22,22.8,16.6,7.8,8.2,9.6,33,"Left Arm Pace"),
        ("Arshdeep Singh","PBKS","2023",19,8.42,22.4,16.0,8.0,8.4,9.8,33,"Left Arm Pace"),
        ("Sam Curran","PBKS","2023",14,9.02,24.8,16.5,8.6,9.0,10.4,28,"All-rounder"),
        ("Yuzvendra Chahal","RR","2023",21,8.24,22.4,16.3,7.8,8.2,9.4,35,"Leg Spin"),
        ("Trent Boult","RR","2023",18,8.22,21.4,15.6,7.8,8.2,9.6,34,"Swing"),
        ("Prasidh Krishna","RR","2023",14,8.62,24.4,17.0,8.2,8.6,10.0,31,"Pace"),
        ("Harshal Patel","PBKS","2024",24,9.73,19.9,12.3,8.8,9.2,11.2,30,"🟣 Purple Cap"),
        ("Jasprit Bumrah","MI","2024",15,7.43,17.3,13.4,6.8,6.5,8.3,42,"Pace"),
        ("Mohammed Siraj","RCB","2024",19,8.45,22.6,16.0,8.1,8.0,9.2,33,"Powerplay"),
        # 2024 extra bowlers
        ("Mitchell Starc","KKR","2024",17,8.72,24.1,16.9,8.2,8.6,9.8,32,"Left Arm Pace"),
        ("Varun Chakravarthy","KKR","2024",21,8.12,20.4,14.6,7.8,8.0,9.2,38,"Mystery Spin"),
        ("Sunil Narine","KKR","2024",15,6.92,22.8,19.8,6.6,6.8,8.0,40,"Off Spin"),
        ("Pat Cummins","SRH","2024",20,9.42,21.8,13.9,8.9,9.2,10.8,30,"Captain-Pace"),
        ("Bhuvneshwar Kumar","SRH","2024",15,8.12,24.8,18.4,7.8,8.0,9.2,34,"Swing"),
        ("T Natarajan","SRH","2024",16,8.84,22.4,15.2,8.4,8.7,10.0,32,"Yorker King"),
        ("Yuzvendra Chahal","RR","2024",18,8.24,22.4,16.3,7.8,8.2,9.4,35,"Leg Spin"),
        ("Trent Boult","RR","2024",14,8.44,24.6,17.5,8.0,8.4,9.6,33,"Swing"),
        ("Avesh Khan","RR","2024",13,9.12,26.4,17.4,8.8,9.0,10.4,28,"Pace"),
        ("Ruturaj Gaikwad","CSK","2024",0,0.0,0.0,0.0,0.0,0.0,0.0,0,"Captain"),
        ("Matheesha Pathirana","CSK","2024",19,8.64,21.2,14.7,8.2,8.6,9.8,33,"Death Spec"),
        ("Deepak Chahar","CSK","2024",14,8.24,24.2,17.5,7.8,8.2,9.4,34,"Swing"),
        ("Sam Curran","CSK","2024",12,9.02,25.8,17.2,8.6,9.0,10.2,29,"All-rounder"),
        ("Axar Patel","DC","2024",14,7.52,24.8,19.8,7.2,7.4,8.6,36,"Spin"),
        ("Kuldeep Yadav","DC","2024",21,8.02,20.6,15.4,7.6,8.0,9.2,36,"Wrist Spin"),
        ("Ishant Sharma","DC","2024",11,8.84,26.4,18.0,8.4,8.8,10.2,30,"Pace"),
        ("Mohsin Khan","LSG","2024",14,8.32,23.4,16.9,7.9,8.2,9.6,33,"Left Arm Pace"),
        ("Ravi Bishnoi","LSG","2024",17,7.82,22.8,17.5,7.4,7.8,8.8,36,"Leg Spin"),
        ("Naveen ul Haq","LSG","2024",12,9.02,25.8,17.2,8.6,9.0,10.2,29,"Pace"),
        ("Kagiso Rabada","PBKS","2024",13,8.92,24.8,16.7,8.5,8.9,10.2,30,"Pace"),
        ("Arshdeep Singh","PBKS","2024",19,8.42,22.4,15.9,8.0,8.4,9.6,34,"Left Arm Pace"),
        ("Yuzvendra Chahal","PBKS","2024",14,8.12,24.2,17.9,7.7,8.0,9.4,34,"Leg Spin"),
        ("Jasprit Bumrah","MI","2024",15,7.43,17.3,13.4,6.8,6.5,8.3,42,"Pace Ace"),
        ("Hardik Pandya","MI","2024",11,9.12,26.4,17.4,8.8,9.2,10.4,28,"All-rounder"),
        ("Gerald Coetzee","MI","2024",12,9.42,25.8,16.5,9.0,9.4,10.8,26,"Pace"),
        ("Rashid Khan","GT","2024",17,6.82,20.4,17.9,6.4,6.8,7.8,42,"Leg Spin"),
        ("Mohammed Shami","GT","2024",12,8.84,24.8,16.9,8.4,8.8,10.2,30,"Pace"),
        ("Noor Ahmad","GT","2024",14,7.92,23.4,17.7,7.5,7.9,9.2,36,"Left Arm Spin"),
        # 2024 extra bowlers all teams
        ("Matheesha Pathirana","CSK","2024",16,8.24,21.4,15.9,7.8,8.1,9.4,34,"Death Specialist"),
        ("Ravindra Jadeja","CSK","2024",12,7.44,28.2,23.5,7.0,7.3,8.6,36,"Spin"),
        ("Tushar Deshpande","CSK","2024",14,9.12,24.8,16.3,8.6,9.0,10.4,28,"Pace"),
        ("Harshit Rana","KKR","2024",19,9.24,21.8,14.2,8.8,9.2,10.4,30,"Pace"),
        ("Varun Chakravarthy","KKR","2024",21,7.92,19.5,14.8,7.4,7.8,9.2,38,"Mystery Spinner"),
        ("Mitchell Starc","KKR","2024",17,8.44,22.4,15.9,8.0,8.4,9.6,32,"Swing"),
        ("Pat Cummins","SRH","2024",15,9.12,24.2,15.9,8.6,9.0,10.4,30,"Captain-Bowler"),
        ("Bhuvneshwar Kumar","SRH","2024",13,8.44,26.4,18.8,8.0,8.4,9.6,32,"Swing"),
        ("T Natarajan","SRH","2024",14,8.84,23.8,16.2,8.4,8.8,10.0,30,"Yorker King"),
        ("Kuldeep Yadav","DC","2024",15,7.84,22.8,17.5,7.4,7.8,9.0,36,"Wrist Spin"),
        ("Ishant Sharma","DC","2024",11,8.64,26.2,18.2,8.2,8.6,9.8,30,"Pace"),
        ("Khaleel Ahmed","DC","2024",12,8.24,24.8,18.1,7.8,8.2,9.4,32,"Left Arm Pace"),
        ("Ravi Bishnoi","LSG","2024",14,7.84,24.2,18.5,7.4,7.8,9.0,36,"Leg Spin"),
        ("Mohsin Khan","LSG","2024",13,7.64,23.8,18.7,7.2,7.6,8.8,34,"Left Arm Pace"),
        ("Avesh Khan","LSG","2024",12,9.24,26.4,17.2,8.8,9.2,10.4,28,"Pace"),
        ("Mohammed Siraj","RCB","2024",19,8.45,22.6,16.0,8.1,8.0,9.2,33,"Powerplay"),
        ("Yash Dayal","RCB","2024",14,9.04,24.8,16.5,8.6,9.0,10.2,28,"Left Arm Pace"),
        ("Wanindu Hasaranga","RCB","2024",16,7.64,22.4,17.6,7.2,7.6,8.8,36,"Leg Spin"),
        ("Yuzvendra Chahal","RR","2024",20,8.24,20.8,15.2,7.8,8.2,9.4,34,"Leg Spin"),
        ("Trent Boult","RR","2024",17,8.44,22.4,15.9,8.0,8.4,9.6,32,"Swing"),
        ("Sandeep Sharma","RR","2024",15,8.84,23.8,16.2,8.4,8.8,10.0,30,"Pace"),
        ("Arshdeep Singh","PBKS","2024",19,8.44,21.8,15.5,8.0,8.4,9.6,32,"Left Arm Pace"),
        ("Kagiso Rabada","PBKS","2024",16,9.04,22.8,15.2,8.6,9.0,10.2,30,"Pace"),
        ("Mohammed Shami","GT","2024",12,8.24,24.8,18.1,7.8,8.2,9.4,34,"Pace"),
        ("Rashid Khan","GT","2024",14,6.44,20.8,19.4,6.0,6.4,7.6,44,"Leg Spin"),
        ("Noor Ahmad","GT","2024",13,7.84,22.4,17.2,7.4,7.8,9.0,36,"Left Arm Spin"),
        # 2023 extra bowlers
        ("Matheesha Pathirana","CSK","2023",19,8.24,21.8,15.9,7.8,8.1,9.4,34,"Death Specialist"),
        ("Ravindra Jadeja","CSK","2023",11,7.24,28.2,23.5,6.8,7.2,8.4,36,"Spin"),
        ("Deepak Chahar","CSK","2023",16,8.64,22.8,15.8,8.2,8.6,9.8,32,"Swing"),
        ("Varun Chakravarthy","KKR","2023",18,7.92,21.5,16.3,7.4,7.8,9.2,38,"Mystery Spinner"),
        ("Sunil Narine","KKR","2023",14,6.84,22.8,19.9,6.4,6.8,8.2,40,"Off-Spin"),
        ("Kuldeep Yadav","DC","2023",21,7.84,20.8,15.9,7.4,7.8,9.0,38,"Wrist Spin"),
        ("Anrich Nortje","DC","2023",14,9.04,24.8,16.5,8.6,9.0,10.2,28,"Pace"),
        ("Yuzvendra Chahal","RR","2023",21,8.04,20.4,15.3,7.6,8.0,9.2,36,"Leg Spin"),
        ("Trent Boult","RR","2023",14,8.44,24.2,17.3,8.0,8.4,9.6,32,"Swing"),
        ("Ravi Bishnoi","LSG","2023",16,7.64,23.2,18.2,7.2,7.6,8.8,36,"Leg Spin"),
        ("Avesh Khan","LSG","2023",14,9.04,24.8,16.5,8.6,9.0,10.2,28,"Pace"),
        ("Arshdeep Singh","PBKS","2023",17,8.44,23.2,16.5,8.0,8.4,9.6,32,"Left Arm Pace"),
        ("Sam Curran","PBKS","2023",15,8.84,24.4,16.5,8.4,8.8,10.0,30,"All-rounder"),
        ("Jasprit Bumrah","MI","2023",20,7.44,17.4,14.0,6.8,7.2,8.8,42,"Pace"),
        ("Piyush Chawla","MI","2023",11,7.64,26.4,20.8,7.2,7.6,8.8,34,"Leg Spin"),
        ("Bhuvneshwar Kumar","SRH","2023",13,8.44,26.4,18.8,8.0,8.4,9.6,32,"Swing"),
        ("T Natarajan","SRH","2023",14,8.84,24.2,16.5,8.4,8.8,10.0,30,"Yorker King"),
        ("Umran Malik","SRH","2023",16,9.44,22.8,14.5,9.0,9.4,10.6,26,"Pace"),
        # 2022 extra bowlers
        ("Matheesha Pathirana","CSK","2022",15,8.44,23.2,16.5,8.0,8.4,9.6,32,"Pace"),
        ("Deepak Chahar","CSK","2022",13,8.24,24.8,18.1,7.8,8.2,9.4,32,"Swing"),
        ("Dwayne Bravo","CSK","2022",16,8.84,24.4,16.5,8.4,8.8,10.0,30,"Death"),
        ("Varun Chakravarthy","KKR","2022",18,8.12,20.5,15.2,7.6,8.0,9.4,38,"Mystery Spinner"),
        ("Umesh Yadav","KKR","2022",16,8.64,22.4,15.6,8.2,8.6,9.8,30,"Pace"),
        ("Prasidh Krishna","RR","2022",19,8.44,21.4,15.2,8.0,8.4,9.6,32,"Pace"),
        ("Obed McCoy","RR","2022",16,8.84,22.4,15.2,8.4,8.8,10.0,28,"Left Arm Pace"),
        ("Mohammed Shami","GT","2022",20,8.04,18.8,14.1,7.6,8.0,9.2,36,"Pace"),
        ("Lockie Ferguson","GT","2022",16,8.44,22.4,15.9,8.0,8.4,9.6,32,"Pace"),
        ("Kuldeep Yadav","DC","2022",21,7.84,19.4,14.9,7.4,7.8,9.0,38,"Wrist Spin"),
        ("Anrich Nortje","DC","2022",18,9.04,21.8,14.5,8.6,9.0,10.2,28,"Pace"),
        ("Bhuvneshwar Kumar","SRH","2022",16,8.44,22.4,15.9,8.0,8.4,9.6,32,"Swing"),
        ("T Natarajan","SRH","2022",15,8.84,23.8,16.2,8.4,8.8,10.0,30,"Yorker King"),
        ("Umran Malik","SRH","2022",22,9.44,20.4,13.0,9.0,9.4,10.6,26,"Pace"),
        ("Ravi Bishnoi","LSG","2022",14,7.64,24.2,19.0,7.2,7.6,8.8,36,"Leg Spin"),
        ("Avesh Khan","LSG","2022",24,8.64,19.8,13.8,8.2,8.6,9.8,30,"Pace"),
        ("Arshdeep Singh","PBKS","2022",10,8.44,28.4,20.2,8.0,8.4,9.6,28,"Left Arm Pace"),
        ("Rahul Chahar","PBKS","2022",14,7.84,24.8,19.0,7.4,7.8,9.0,34,"Leg Spin"),
        # 2021 extra bowlers
        ("Deepak Chahar","CSK","2021",14,7.64,21.4,16.8,7.2,7.6,8.8,36,"Swing"),
        ("Dwayne Bravo","CSK","2021",18,8.64,22.4,15.6,8.2,8.6,9.8,30,"Death"),
        ("Josh Hazlewood","CSK","2021",13,7.84,22.4,17.2,7.4,7.8,9.0,36,"Pace"),
        ("Varun Chakravarthy","KKR","2021",18,7.64,18.8,14.8,7.2,7.6,8.8,40,"Mystery Spinner"),
        ("Sunil Narine","KKR","2021",13,6.64,22.8,20.6,6.2,6.6,8.0,42,"Off-Spin"),
        ("Avesh Khan","DC","2021",24,8.44,18.8,13.4,8.0,8.4,9.6,32,"Pace"),
        ("Anrich Nortje","DC","2021",22,8.84,19.4,13.2,8.4,8.8,10.0,30,"Pace"),
        ("Arshdeep Singh","PBKS","2021",18,8.24,22.4,16.3,7.8,8.2,9.4,32,"Left Arm Pace"),
        ("Riley Meredith","PBKS","2021",16,8.84,22.8,15.5,8.4,8.8,10.0,28,"Pace"),
        ("Bhuvneshwar Kumar","SRH","2021",8,8.04,30.4,22.8,7.6,8.0,9.2,30,"Swing"),
        ("Rashid Khan","SRH","2021",18,5.84,18.8,19.3,5.4,5.8,7.0,48,"Leg Spin"),
        # 2020 extra bowlers
        ("Deepak Chahar","CSK","2020",12,7.64,24.4,19.2,7.2,7.6,8.8,34,"Swing"),
        ("Sam Curran","CSK","2020",13,8.44,23.8,16.9,8.0,8.4,9.6,32,"All-rounder"),
        ("Dwayne Bravo","CSK","2020",16,8.84,22.4,15.2,8.4,8.8,10.0,30,"Death"),
        ("Varun Chakravarthy","KKR","2020",17,7.84,20.5,15.7,7.4,7.8,9.0,38,"Mystery Spinner"),
        ("Pat Cummins","KKR","2020",12,8.44,24.8,17.6,8.0,8.4,9.6,30,"Pace"),
        ("Yuzvendra Chahal","RCB","2020",21,7.44,19.4,15.7,7.0,7.4,8.6,38,"Leg Spin"),
        ("Mohammed Siraj","RCB","2020",11,8.44,27.4,19.5,8.0,8.4,9.6,28,"Pace"),
        ("Arshdeep Singh","PBKS","2020",14,8.44,24.4,17.4,8.0,8.4,9.6,30,"Left Arm Pace"),
        ("Mohammed Shami","PBKS","2020",20,8.84,19.8,13.5,8.4,8.8,10.0,28,"Pace"),
        ("Anrich Nortje","DC","2020",22,8.44,18.8,13.4,8.0,8.4,9.6,34,"Pace"),
        ("Ravichandran Ashwin","DC","2020",13,6.84,24.8,21.7,6.4,6.8,8.2,38,"Off-Spin"),
        ("Bhuvneshwar Kumar","SRH","2020",9,8.24,30.4,22.2,7.8,8.2,9.4,28,"Swing"),
        ("Sandeep Sharma","SRH","2020",11,8.64,26.4,18.3,8.2,8.6,9.8,28,"Pace"),
        ("Yuzvendra Chahal","RR","2020",17,8.24,20.8,15.2,7.8,8.2,9.4,34,"Leg Spin"),
        # 2019 extra bowlers
        ("Deepak Chahar","CSK","2019",22,6.84,18.8,16.5,6.4,6.8,8.2,40,"Swing"),
        ("Imran Tahir","CSK","2019",26,6.64,16.4,14.9,6.2,6.6,8.0,42,"Leg Spin"),
        ("Dwayne Bravo","CSK","2019",15,8.84,24.4,16.6,8.4,8.8,10.0,28,"Death"),
        ("Pat Cummins","KKR","2019",16,8.44,24.8,17.6,8.0,8.4,9.6,30,"Pace"),
        ("Sunil Narine","KKR","2019",12,6.64,24.8,22.4,6.2,6.6,8.0,40,"Off-Spin"),
        ("Bhuvneshwar Kumar","SRH","2019",13,7.44,24.4,19.7,7.0,7.4,8.6,34,"Swing"),
        ("Sandeep Sharma","SRH","2019",15,8.24,23.8,17.4,7.8,8.2,9.4,30,"Pace"),
        ("Yuzvendra Chahal","RCB","2019",18,7.44,21.8,17.6,7.0,7.4,8.6,36,"Leg Spin"),
        ("Navdeep Saini","RCB","2019",14,8.64,23.8,16.5,8.2,8.6,9.8,28,"Pace"),
        ("Anrich Nortje","DC","2019",12,8.44,26.4,18.8,8.0,8.4,9.6,30,"Pace"),
        ("Kagiso Rabada","DC","2019",25,7.84,18.8,14.4,7.4,7.8,9.0,36,"Pace"),
        ("Yuzvendra Chahal","RR","2019",21,7.84,20.4,15.6,7.4,7.8,9.0,36,"Leg Spin"),
        ("Shreyas Gopal","RR","2019",20,7.64,21.4,16.8,7.2,7.6,8.8,34,"Leg Spin"),
        ("Mohammed Shami","PBKS","2019",19,8.44,22.4,15.9,8.0,8.4,9.6,30,"Pace"),
        ("Mujeeb Ur Rahman","PBKS","2019",16,7.44,24.4,19.7,7.0,7.4,8.6,36,"Off-Spin"),
        # 2018 extra bowlers
        ("Deepak Chahar","CSK","2018",11,7.64,26.4,20.8,7.2,7.6,8.8,34,"Swing"),
        ("Dwayne Bravo","CSK","2018",20,8.44,20.8,14.8,8.0,8.4,9.6,30,"Death"),
        ("Imran Tahir","CSK","2018",24,6.64,16.4,14.9,6.2,6.6,8.0,42,"Leg Spin"),
        ("Sunil Narine","KKR","2018",17,6.64,22.8,20.6,6.2,6.6,8.0,42,"Off-Spin"),
        ("Kuldeep Yadav","KKR","2018",17,7.44,22.8,18.5,7.0,7.4,8.6,36,"Wrist Spin"),
        ("Bhuvneshwar Kumar","SRH","2018",20,7.44,20.4,16.5,7.0,7.4,8.6,38,"Swing"),
        ("Sandeep Sharma","SRH","2018",18,7.84,22.4,17.2,7.4,7.8,9.0,34,"Pace"),
        ("Yuzvendra Chahal","RCB","2018",21,7.44,21.8,17.6,7.0,7.4,8.6,36,"Leg Spin"),
        ("Umesh Yadav","RCB","2018",11,8.44,26.4,18.8,8.0,8.4,9.6,28,"Pace"),
        ("Anrich Nortje","DC","2018",14,8.44,24.8,17.6,8.0,8.4,9.6,30,"Pace"),
        ("Kagiso Rabada","DC","2018",16,8.84,22.4,15.2,8.4,8.8,10.0,30,"Pace"),
        ("Shreyas Gopal","RR","2018",15,7.84,24.4,18.7,7.4,7.8,9.0,34,"Leg Spin"),
        ("Dhawal Kulkarni","RR","2018",12,8.84,26.4,17.9,8.4,8.8,10.0,26,"Pace"),
        ("Mujeeb Ur Rahman","PBKS","2018",14,6.84,23.8,20.9,6.4,6.8,8.2,38,"Off-Spin"),
        # 2017 extra bowlers
        ("Deepak Chahar","RPS","2017",11,7.64,26.4,20.8,7.2,7.6,8.8,34,"Swing"),
        ("Imran Tahir","RPS","2017",18,7.44,20.8,16.8,7.0,7.4,8.6,36,"Leg Spin"),
        ("Dwayne Bravo","GL","2017",19,8.44,21.4,15.2,8.0,8.4,9.6,30,"Death"),
        ("Andrew Tye","GL","2017",24,8.44,18.8,13.4,8.0,8.4,9.6,30,"Pace"),
        ("Sunil Narine","KKR","2017",15,6.84,24.8,21.7,6.4,6.8,8.2,40,"Off-Spin"),
        ("Kuldeep Yadav","KKR","2017",15,7.44,24.8,20.0,7.0,7.4,8.6,36,"Wrist Spin"),
        ("Bhuvneshwar Kumar","SRH","2017",26,7.05,18.2,15.5,6.5,6.6,7.9,42,"🟣 Purple Cap"),
        ("Rashid Khan","SRH","2017",17,6.28,21.6,20.6,5.9,5.8,7.4,42,"Leg Spin"),
        ("Mohammed Shami","SRH","2017",14,7.84,24.4,18.7,7.4,7.8,9.0,34,"Pace"),
        ("Yuzvendra Chahal","RCB","2017",23,7.44,20.8,16.8,7.0,7.4,8.6,36,"Leg Spin"),
        ("Samuel Badree","RCB","2017",12,7.64,26.4,20.8,7.2,7.6,8.8,32,"Spinner"),
        ("Ishant Sharma","RR","2017",11,8.64,28.4,19.7,8.2,8.6,9.8,26,"Pace"),
        ("Shreyas Gopal","RR","2017",13,7.84,26.4,20.2,7.4,7.8,9.0,32,"Leg Spin"),
        ("Andrew Tye","PBKS","2017",20,8.44,20.8,14.8,8.0,8.4,9.6,30,"Pace"),
        ("Sandeep Sharma","PBKS","2017",14,8.84,26.4,17.9,8.4,8.8,10.0,26,"Pace"),
        ("Kagiso Rabada","DC","2017",23,8.44,18.8,13.4,8.0,8.4,9.6,30,"Pace"),
        ("Zaheer Khan","DC","2017",11,8.84,30.4,20.6,8.4,8.8,10.0,24,"Pace"),
        # 2016 extra bowlers
        ("Dwayne Bravo","CSK","2016",19,8.44,21.4,15.2,8.0,8.4,9.6,30,"Death"),
        ("Ravichandran Ashwin","CSK","2016",15,6.84,22.4,19.6,6.4,6.8,8.2,38,"Off-Spin"),
        ("Sunil Narine","KKR","2016",21,6.84,20.4,17.9,6.4,6.8,8.2,40,"Off-Spin"),
        ("Umesh Yadav","KKR","2016",17,8.44,22.4,15.9,8.0,8.4,9.6,28,"Pace"),
        ("Praveen Kumar","KKR","2016",12,8.84,26.4,17.9,8.4,8.8,10.0,26,"Swing"),
        ("Jasprit Bumrah","MI","2016",15,7.44,22.4,18.1,7.0,7.4,8.6,38,"Pace"),
        ("Lasith Malinga","MI","2016",17,7.24,20.4,16.9,6.8,7.2,8.4,38,"Pace"),
        ("Harbhajan Singh","MI","2016",13,6.84,26.4,23.1,6.4,6.8,8.2,36,"Off-Spin"),
        ("Ravichandran Ashwin","RPS","2016",10,7.44,30.4,24.5,7.0,7.4,8.6,34,"Off-Spin"),
        ("Imran Tahir","RPS","2016",14,7.44,22.4,18.1,7.0,7.4,8.6,36,"Leg Spin"),
        ("Kagiso Rabada","DC","2016",23,8.44,18.8,13.4,8.0,8.4,9.6,30,"Pace"),
        ("Mohammed Shami","DC","2016",16,8.84,22.4,15.2,8.4,8.8,10.0,28,"Pace"),
        ("Murugan Ashwin","RR","2016",10,7.64,28.4,22.3,7.2,7.6,8.8,30,"Leg Spin"),
        ("James Faulkner","RR","2016",12,8.44,24.8,17.6,8.0,8.4,9.6,28,"All-rounder"),
        ("Mitchell Marsh","PBKS","2016",10,8.44,28.4,20.2,8.0,8.4,9.6,26,"Pace"),
        ("Sandeep Sharma","PBKS","2016",14,8.64,24.8,17.2,8.2,8.6,9.8,28,"Pace"),
        ("Jasprit Bumrah","MI","2024",15,7.43,17.3,13.4,6.8,6.5,8.3,42,"Pace"),
        ("Mohammed Siraj","RCB","2024",19,8.45,22.6,16.0,8.1,8.0,9.2,33,"Powerplay"),
        # ── 2026 BOWLING DATA (Real Stats) ──────────────────
        ("Kagiso Rabada","GT","2026",29,9.68,21.58,14.4,9.2,9.6,10.8,30,"🟣 Purple Cap (2nd title)"),
        ("Bhuvneshwar Kumar","RCB","2026",28,7.95,19.80,13.2,7.4,7.8,9.2,38,"2nd Place"),
        ("Jofra Archer","RR","2026",25,8.42,20.40,14.8,7.8,8.2,9.8,34,"Top Pacer"),
        ("Josh Hazlewood","RCB","2026",22,7.82,21.40,14.6,7.2,7.8,8.8,38,"RCB Spearhead"),
        ("Rashid Khan","GT","2026",21,9.08,22.40,17.8,8.6,9.0,10.2,30,"Top Spinner"),
        ("Jasprit Bumrah","MI","2026",20,8.12,22.20,15.8,7.6,8.0,9.4,36,"MI Spearhead"),
        ("Mohammed Shami","GT","2026",19,8.84,23.20,15.4,8.4,8.8,10.0,32,"Swing"),
        ("Mohsin Khan","LSG","2026",18,8.24,23.40,15.8,7.8,8.2,9.6,34,"5/23 Best Figures"),
        ("Arshdeep Singh","PBKS","2026",18,8.64,22.80,15.6,8.2,8.6,10.0,32,"Left Arm Pace"),
        ("Varun Chakravarthy","KKR","2026",17,8.42,23.60,17.8,8.0,8.4,9.6,32,"Mystery Spin"),
        ("Rasikh Salam","RCB","2026",16,8.62,24.20,16.2,8.2,8.6,9.8,30,"3/27 in Final"),
        ("Prasidh Krishna","GT","2026",15,8.92,25.40,16.8,8.4,8.8,10.2,28,"Spearhead"),
        ("Noor Ahmad","CSK","2026",16,8.02,23.80,18.4,7.6,8.0,9.2,34,"Spinner"),
        ("Pat Cummins","SRH","2026",18,9.12,23.40,15.4,8.6,9.0,10.4,30,"Captain-Bowler"),
        ("Trent Boult","MI","2026",17,8.42,23.20,15.8,7.8,8.2,9.8,32,"Swing"),
        ("Matheesha Pathirana","CSK","2026",15,8.84,24.60,15.6,8.4,8.8,10.2,30,"Death"),
        ("Kuldeep Yadav","DC","2026",16,8.22,23.80,17.8,7.8,8.2,9.4,34,"Wrist Spin"),
        ("Yuzvendra Chahal","RR","2026",14,8.84,25.80,21.4,8.4,8.8,10.2,28,"Leg Spin"),
        ("Ravi Bishnoi","LSG","2026",15,8.02,24.40,19.8,7.6,8.0,9.2,34,"Leg Spin"),
        ("Harshit Rana","KKR","2026",16,8.84,23.60,15.8,8.4,8.8,10.2,30,"Pace"),
        # ── END 2026 BOWLING ──────────────────────────────────
        ("Prasidh Krishna","GT","2025",25,8.12,19.52,14.4,7.8,7.9,8.9,38,"🟣 Purple Cap"),
        ("Noor Ahmad","CSK","2025",24,7.83,17.0,13.0,6.9,7.5,9.1,41,"2nd Bowler"),
        ("Josh Hazlewood","RCB","2025",22,7.51,18.9,15.1,7.27,7.2,8.2,39,"3rd Bowler"),
        ("Jasprit Bumrah","MI","2025",19,7.86,22.1,16.9,7.1,7.4,9.1,42,"Impact"),
        ("Krunal Pandya","RCB","2025",17,8.23,20.8,15.2,8.9,7.8,8.2,34,"MVP All-rounder"),
        ("Arshdeep Singh","PBKS","2025",18,8.55,21.5,15.1,8.2,8.1,9.3,36,"Top Pacer"),
        ("Varun Chakravarthy","KKR","2025",17,7.92,19.5,14.8,8.4,7.5,8.1,40,"Mystery Spinner"),
        ("Trent Boult","RR","2025",15,8.12,24.3,17.9,7.5,7.9,8.9,35,"Swing King"),
        # RCB 2025
        ("Mohammed Siraj","RCB","2025",18,8.42,21.4,14.8,8.0,8.2,9.4,34,"Powerplay Spec"),
        ("Bhuvneshwar Kumar","RCB","2025",14,7.82,23.4,19.2,7.4,7.8,8.6,36,"Swing"),
        ("Yuzvendra Chahal","RCB","2025",13,7.62,24.6,22.2,7.2,7.6,8.4,36,"Leg Spin"),
        # GT 2025
        ("Mohammed Shami","GT","2025",20,8.24,20.4,14.8,7.8,8.0,9.4,36,"Swing Spearhead"),
        ("Rashid Khan","GT","2025",18,6.42,19.8,18.4,6.0,6.4,7.6,44,"Leg Spin"),
        ("Umesh Yadav","GT","2025",13,9.12,24.8,16.4,8.8,9.0,10.2,30,"Pace"),
        # MI 2025
        ("Trent Boult","MI","2025",17,8.22,22.4,15.8,7.8,8.0,9.4,34,"Swing"),
        ("Hardik Pandya","MI","2025",13,9.04,26.4,18.2,8.6,9.0,10.2,28,"All-rounder"),
        ("Nuwan Thushara","MI","2025",15,8.64,23.2,16.1,8.2,8.6,9.6,32,"Pace"),
        # RR 2025
        ("Yuzvendra Chahal","RR","2025",19,7.82,21.4,16.4,7.4,7.8,8.8,36,"Leg Spin"),
        ("Sandeep Sharma","RR","2025",14,8.44,23.8,16.9,8.0,8.4,9.6,32,"Swing"),
        ("Shimron Hetmyer","RR","2025",8,9.24,28.4,19.2,9.0,9.2,10.4,24,"Part Timer"),
        # PBKS 2025
        ("Yuzvendra Chahal","PBKS","2025",16,7.64,22.8,17.8,7.2,7.6,8.6,36,"Leg Spin"),
        ("Kagiso Rabada","PBKS","2025",20,8.44,20.4,14.4,8.0,8.4,9.6,34,"Pace Spearhead"),
        ("Marco Jansen","PBKS","2025",14,8.82,23.4,15.9,8.4,8.8,10.0,32,"Left Arm Pace"),
        # CSK 2025
        ("Matheesha Pathirana","CSK","2025",21,8.42,20.1,14.8,8.1,8.2,9.2,35,"Death Specialist"),
        ("Noor Ahmad","CSK","2025",24,7.83,17.0,13.0,6.9,7.5,9.1,41,"Top Spinner"),
        ("Ravindra Jadeja","CSK","2025",14,7.12,22.4,19.2,6.8,7.0,8.1,38,"Spin"),
        ("Sam Curran","CSK","2025",13,9.12,24.6,16.2,8.8,9.0,10.1,30,"All-rounder"),
        ("Khaleel Ahmed","CSK","2025",12,8.94,25.2,16.8,8.6,9.0,10.0,30,"Left Arm Pace"),
        # KKR 2025
        ("Harshit Rana","KKR","2025",18,8.64,21.8,15.1,8.2,8.5,9.4,33,"Pace"),
        ("Sunil Narine","KKR","2025",16,7.14,24.8,21.5,6.8,7.0,8.2,39,"Off-Spin"),
        ("Varun Chakravarthy","KKR","2025",17,7.92,19.5,14.8,8.4,7.5,8.1,40,"Mystery Spin"),
        ("Andre Russell","KKR","2025",12,9.24,26.4,17.2,9.0,9.2,10.2,28,"Death"),
        ("Anrich Nortje","KKR","2025",15,8.84,22.4,15.2,8.4,8.8,10.0,32,"Pace"),
        # SRH 2025
        ("Pat Cummins","SRH","2025",19,8.92,22.4,15.1,8.5,8.8,9.6,32,"Captain-Bowler"),
        ("Harshal Patel","SRH","2025",16,9.12,24.2,16.0,8.8,9.0,10.2,30,"Death Specialist"),
        ("Jaydev Unadkat","SRH","2025",13,8.44,23.8,16.9,8.0,8.4,9.4,32,"Swing"),
        ("T Natarajan","SRH","2025",14,8.64,24.2,16.8,8.2,8.6,9.8,32,"Yorker King"),
        ("Abhishek Sharma","SRH","2025",8,9.04,28.4,19.2,8.6,9.0,10.4,26,"Part Timer"),
        # DC 2025
        ("Axar Patel","DC","2025",15,7.44,24.8,20.1,7.1,7.4,8.2,37,"Spin Captain"),
        ("Kuldeep Yadav","DC","2025",17,7.82,22.6,18.4,7.4,7.8,8.8,36,"Wrist Spin"),
        ("Mustafizur Rahman","DC","2025",14,8.62,23.4,16.3,8.2,8.6,9.6,32,"Cutters"),
        ("Ishant Sharma","DC","2025",10,8.84,26.2,17.8,8.4,8.8,10.2,30,"Senior Pacer"),
        ("Anrich Nortje","DC","2025",16,8.64,22.2,15.4,8.2,8.6,9.8,32,"Express Pace"),
        # LSG 2025
        ("Ravi Bishnoi","LSG","2025",16,7.62,23.4,18.8,7.2,7.6,8.6,36,"Leg Spin"),
        ("Mohsin Khan","LSG","2025",14,8.12,22.8,16.4,7.8,8.0,9.2,34,"Left Arm Pace"),
        ("Mitchell Marsh","LSG","2025",11,9.04,26.2,17.4,8.6,9.0,10.2,28,"All-rounder"),
        ("Avesh Khan","LSG","2025",13,8.84,24.6,16.8,8.4,8.8,10.0,30,"Pace"),
        ("Digvesh Singh","LSG","2025",12,8.44,25.4,17.2,8.0,8.4,9.6,32,"Leg Spin"),
    ], columns=["player","team","season","wickets","economy","avg","sr","pp_eco","mid_eco","death_eco","dot_pct","award"])

    seasons = pd.DataFrame({
        "season":[2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026],
        "champion":["SRH","MI","CSK","MI","MI","CSK","GT","CSK","KKR","RCB","RCB"],
        "runner_up":["RCB","RPS","SRH","CSK","DC","KKR","RR","GT","SRH","PBKS","GT"],
        "orange_cap":["Virat Kohli","David Warner","Kane Williamson","David Warner","KL Rahul","Faf du Plessis","Jos Buttler","Shubman Gill","Virat Kohli","Sai Sudharsan","Vaibhav Suryavanshi"],
        "orange_runs":[973,641,735,692,670,633,863,890,741,759,776],
        "purple_cap":["Bhuvneshwar Kumar","Bhuvneshwar Kumar","Andrew Tye","Ishant Sharma","Kagiso Rabada","Harshal Patel","Yuzvendra Chahal","Mohammed Shami","Harshal Patel","Prasidh Krishna","Kagiso Rabada"],
        "purple_wkts":[26,26,24,19,30,32,27,28,24,25,29],
        "avg_rpo":[8.3,8.4,8.5,8.6,8.8,8.9,9.1,9.4,9.56,9.62,9.88],
        "total_sixes":[467,512,488,534,490,561,598,632,687,724,1426],
        "matches":[60,59,60,60,60,60,74,74,74,74,74],
    })

    teams = pd.DataFrame({
        "team":["MI","CSK","KKR","SRH","RCB","DC","PBKS","RR","GT","LSG"],
        "wins_all":[130,122,105,98,92,88,80,76,35,22],
        "losses_all":[79,75,98,88,112,104,112,104,15,18],
        "titles":[5,5,3,1,1,0,0,1,1,0],
        "win_pct":[62.2,61.9,51.7,52.7,45.1,45.8,41.7,42.2,70.0,55.0],
        "city":["Mumbai","Chennai","Kolkata","Hyderabad","Bengaluru","Delhi","Chandigarh","Jaipur","Ahmedabad","Lucknow"],
        "lat":[19.076,13.083,22.572,17.385,12.972,28.613,30.733,26.912,23.022,26.846],
        "lon":[72.877,80.270,88.363,78.486,77.594,77.209,76.779,75.787,72.571,80.946],
    })

    auction = pd.DataFrame([
        ("Virat Kohli","RCB","Batter",2025,21.0,973,152.3,"🔴 Retained"),
        ("Rohit Sharma","MI","Batter",2025,16.3,785,130.4,"🔴 Retained"),
        ("Jasprit Bumrah","MI","Bowler",2025,18.0,27,7.43,"🔴 Retained"),
        ("MS Dhoni","CSK","WK-Batter",2025,4.0,200,116.3,"🔴 Retained"),
        ("Hardik Pandya","MI","All-rounder",2025,16.35,341,144.7,"🔴 Retained"),
        ("Sai Sudharsan","GT","Batter",2025,8.25,759,156.17,"🟢 Bought"),
        ("Shubman Gill","GT","Batter",2025,16.5,648,153.2,"🔴 Retained"),
        ("Rishabh Pant","LSG","WK-Batter",2025,27.0,626,155.4,"🟢 Bought"),
        ("Mitchell Starc","KKR","Bowler",2024,24.75,0,8.2,"🟢 Bought"),
        ("Pat Cummins","SRH","Bowler",2024,20.5,0,8.5,"🟢 Bought"),
        ("Shreyas Iyer","PBKS","Batter",2025,26.75,491,141.5,"🟢 Bought"),
        ("KL Rahul","DC","WK-Batter",2025,14.0,616,135.1,"🟢 Bought"),
        ("Arshdeep Singh","PBKS","Bowler",2025,18.0,0,8.55,"🔴 Retained"),
        ("Rashid Khan","GT","Bowler",2025,18.0,27,6.28,"🔴 Retained"),
        ("Yashasvi Jaiswal","RR","Batter",2025,18.0,506,152.3,"🔴 Retained"),
        ("Suryakumar Yadav","MI","Batter",2025,21.0,717,158.4,"🔴 Retained"),
        ("Jos Buttler","GT","Batter",2025,15.75,538,163.9,"🟢 Bought"),
        ("Noor Ahmad","CSK","Bowler",2025,10.0,24,7.83,"🟢 Bought"),
        ("Krunal Pandya","RCB","All-rounder",2025,5.75,109,120.0,"🟢 Bought"),
        ("Phil Salt","RCB","WK-Batter",2025,11.5,512,148.7,"🟢 Bought"),
    ], columns=["player","team","role","year","price_cr","runs","sr","status"])

    venues = pd.DataFrame([
        ("Wankhede Stadium","Mumbai","MI",168,152,8.9,42,18,62,"Flat pitch, small boundaries"),
        ("M Chinnaswamy","Bengaluru","RCB",185,168,9.8,55,14,57,"Very flat, high scoring"),
        ("Eden Gardens","Kolkata","KKR",162,148,8.5,38,16,55,"Spin friendly, dew factor"),
        ("Chepauk","Chennai","CSK",155,141,8.1,28,12,61,"Slow pitch, spinners dominate"),
        ("Arun Jaitley","Delhi","DC",165,150,8.6,40,15,58,"Flat, good for batting"),
        ("Rajiv Gandhi Intl","Hyderabad","SRH",170,155,8.8,45,16,60,"Flat, good carry"),
        ("Sawai Mansingh","Jaipur","RR",172,158,9.0,48,17,59,"Flat, high scoring"),
        ("Narendra Modi","Ahmedabad","GT",165,148,8.4,35,14,56,"Dual pitch, spin later"),
        ("PCA Stadium","Chandigarh","PBKS",178,162,9.2,50,18,55,"Flat, batting paradise"),
        ("BRSABV Ekana","Lucknow","LSG",160,145,8.2,32,15,57,"Moderate, balanced"),
    ], columns=["venue","city","home_team","avg_1st_inn","avg_2nd_inn","avg_rpo","avg_sixes","avg_wickets","chase_win_pct","pitch_type"])

    return batting, bowling, seasons, teams, auction, venues

batting_df, bowling_df, seasons_df, teams_df, auction_df, venues_df = load_all_data()

TEAM_COLORS={"MI":"#004BA0","CSK":"#EAB308","RCB":"#D11B1B","KKR":"#6B21A8","SRH":"#F97316",
             "GT":"#E84B3A","RR":"#2563EB","DC":"#1E40AF","PBKS":"#DC143C","LSG":"#10B981",
             "RPS":"#FF6B6B","GL":"#00B4D8"}

def dl(fig, h=380, xt="", yt="", xr=None, yr2=None):
    fig.update_layout(
        paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG,
        font_color=TEXT, title_font_color=GOLD, height=h,
        xaxis=dict(gridcolor=GRID, title=xt, **({"range":xr} if xr else {})),
        yaxis=dict(gridcolor=GRID, title=yt, **({"range":yr2} if yr2 else {})),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=48,b=38,l=8,r=8)
    )
    return fig

# ─── LIVE TICKER ─────────────────────────────────────────────────────────────
ticker_scores = [
    "🏏 MI vs CSK — Live: MI 142/4 (16.2 Ov) · Need 178",
    "⚡ RCB vs KKR — RCB won by 8 wkts",
    "🔥 RCB vs GT Final 2026 — RCB won by 5 wickets · Kohli 75* off 42",
    "🏆 2026 Champion: RCB 🎉 Back-to-back titles! | 🟠 Orange Cap: Vaibhav Suryavanshi 776 runs @ SR 237!",
    "🟣 Purple Cap 2026: Kagiso Rabada 29 wkts (GT) | 💥 KL Rahul 152* (67 balls) — Highest by Indian in IPL history (2026)",
    "📅 IPL 2026 Final: RCB beat GT by 5 wkts | Virat Kohli 75* (42) — Player of the Match 🏆",
    "🌟 MVP 2026: Vaibhav Suryavanshi (RR) — 776 runs @ SR 237 · 72 sixes · 5 awards in one season 🏆",
]
ticker_text = "   •   ".join(ticker_scores) * 2
st.markdown(f"""<div class="ticker-wrap">
<span class="ticker-text">{ticker_text}</span></div>""", unsafe_allow_html=True)

# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""<div style='text-align:center;padding:10px 0;'>
    <div style='font-size:2rem;'>🏏</div>
    <div style='font-family:Rajdhani,sans-serif;font-size:1.05rem;font-weight:700;color:{GOLD};'>IPL ANALYTICS HUB</div>
    <div style='color:{TEXT2};font-size:0.7rem;'>2016–2026 · 10 Features</div>
    </div><hr style='border:1px solid {BORDER};margin:8px 0;'>""", unsafe_allow_html=True)

    # Theme toggle
    theme_label = "☀️ Switch to Light" if is_dark else "🌙 Switch to Dark"
    if st.button(theme_label, use_container_width=True):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    season_options=["All Seasons","2026","2025","2024","2023","2022","2021","2020","2019","2018","2017","2016"]
    selected_season=st.selectbox("📅 Season", season_options, index=0)
    selected_team=st.selectbox("🏟️ Team", ["All Teams","RCB","MI","CSK","KKR","SRH","GT","RR","DC","PBKS","LSG"], index=0)
    min_runs=st.slider("Min Runs", 0, 900, 0, 50)
    min_wkts=st.slider("Min Wickets", 0, 32, 0, 1)
    st.markdown("---")
    st.markdown(f"""<div style='color:{TEXT2};font-size:0.7rem;text-align:center;'>
    📊 ESPNcricinfo + IPL Official<br>🏆 2026: <span style='color:{GOLD};'>RCB 🎉</span> Back-to-Back!</div>""", unsafe_allow_html=True)

yr = selected_season

def filter_bat(df):
    d = df.copy()
    if yr != "All Seasons": d = d[d["season"]==yr]
    if selected_team != "All Teams": d = d[d["team"]==selected_team]
    return d[d["runs"]>=min_runs].sort_values("runs",ascending=False).reset_index(drop=True)

def filter_bowl(df):
    d = df.copy()
    if yr != "All Seasons": d = d[d["season"]==yr]
    if selected_team != "All Teams": d = d[d["team"]==selected_team]
    return d[d["wickets"]>=min_wkts].sort_values("wickets",ascending=False).reset_index(drop=True)

bat_f = filter_bat(batting_df)
bowl_f = filter_bowl(bowling_df)

if yr != "All Seasons" and yr.isdigit():
    sr_row = seasons_df[seasons_df["season"]==int(yr)]
    if not sr_row.empty:
        s = sr_row.iloc[0]
        koc=str(s["orange_runs"]); kow=s["orange_cap"]
        kpc=str(s["purple_wkts"]); kpw=s["purple_cap"]
        krpo=str(s["avg_rpo"]); ks6=str(s["total_sixes"]); kch=s["champion"]
        boc=f"🟠 Orange Cap {yr}: {s['orange_cap']} — {s['orange_runs']} runs"
        bpc=f"🟣 Purple Cap {yr}: {s['purple_cap']} — {s['purple_wkts']} wkts"
        bch=f"🏆 {yr} Champion: {s['champion']}"
    else:
        koc=kow=kpc=kpw=krpo=ks6=kch="N/A"; boc=bpc=bch=""
else:
    koc="973"; kow="Virat Kohli (2016)"; kpc="32"; kpw="Harshal Patel (2021)"
    krpo="9.88"; ks6="1,426"; kch="RCB (2026)"
    boc="🟠 All-Time: Virat Kohli — 973 runs (2016)"
    bpc="🟣 All-Time: Harshal Patel — 32 wkts (2021)"
    bch="🏆 Most Titles: MI & CSK 5 each | RCB: Back-to-Back 2025–26 🔥"

season_label = yr if yr != "All Seasons" else ""
sub_text = f"Season: {season_label}" if season_label else "All Seasons · 2016–2026"
st.markdown(f"""<div class="ipl-header">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
    <div><div class="ipl-title">🏏 IPL ANALYTICS HUB</div>
    <div class="ipl-subtitle">Indian Premier League · {sub_text} · Advanced Stats Dashboard</div></div>
    <div style="display:flex;gap:5px;flex-wrap:wrap;">
      <span class="season-badge">{boc}</span>
      <span class="season-badge">{bpc}</span>
      <span class="season-badge">{bch}</span>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

k1,k2,k3,k4,k5 = st.columns(5)
k1.metric(f"🟠 Runs ({yr})", koc, kow)
k2.metric(f"🟣 Wickets ({yr})", kpc, kpw)
k3.metric("⚡ Best Avg RPO", krpo, "2026")
k4.metric("💥 Most Sixes", ks6, "2026")
k5.metric("🏆 Champion", kch)
st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────
tabs = st.tabs(["🏏 Batting","🎳 Bowling","🏟️ Teams","📈 Trends",
                "⚔️ Compare","🗺️ Map","🤖 Predictor","💰 Auction & XI",
                "📊 Chart Builder","🧠 AI Chat","🎮 Quiz"])

# ══ TAB 1: BATTING ══════════════════════════════════════════════════════════
with tabs[0]:
    lbl = yr if yr != "All Seasons" else "All Seasons"
    st.markdown(f'<div class="section-header">📊 Top Batters — {lbl}</div>', unsafe_allow_html=True)
    if bat_f.empty:
        st.warning("No data found! Please change the filters.")
    else:
        c1,c2 = st.columns([3,1])
        with c1:
            top = bat_f.head(10)
            fig = px.bar(top.sort_values("sr"), x="sr", y="player", orientation="h",
                color="team", color_discrete_map=TEAM_COLORS,
                title=f"Strike Rate Leaders — {lbl}",
                labels={"sr":"Strike Rate","player":""}, text="sr",
                hover_data=["runs","avg","season"])
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            dl(fig, h=420, xt="Strike Rate", xr=[110, max(top["sr"])+15])
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            for _,row in bat_f.head(5).iterrows():
                st.markdown(f"""<div class="highlight-box">
                <div class="highlight-player">{row['player']}</div>
                <div class="highlight-stat">{row['team']} · {row['season']}<br>
                {row['runs']} runs · SR {row['sr']:.1f}<br>Avg {row['avg']:.1f}</div>
                <div class="award-tag">{row.get('award','')}</div></div>""", unsafe_allow_html=True)
        ca,cb = st.columns(2)
        with ca:
            fig2 = px.scatter(bat_f, x="sr", y="avg", size="runs", color="team",
                hover_name="player", hover_data={"runs":True,"season":True},
                title="Batting Quality Map", color_discrete_map=TEAM_COLORS)
            dl(fig2, h=340); fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        with cb:
            fig3 = px.bar(bat_f.head(10).sort_values("runs"), x="runs", y="player",
                orientation="h", color="team", color_discrete_map=TEAM_COLORS,
                title="Top Run Scorers", text="runs")
            fig3.update_traces(textposition="outside")
            dl(fig3, h=340, xt="Runs"); fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(bat_f[["player","team","season","runs","innings","avg","sr","fours","sixes","hundreds","fifties"]].rename(columns={"player":"Player","team":"Team","season":"Season","runs":"Runs","innings":"Inn","avg":"Avg","sr":"SR","fours":"4s","sixes":"6s","hundreds":"100s","fifties":"50s"}), use_container_width=True, height=340, hide_index=True)

        # Export
        st.markdown('<div class="section-header">📤 Export Batting Data</div>', unsafe_allow_html=True)
        ec1,ec2 = st.columns(2)
        with ec1:
            csv = bat_f.to_csv(index=False).encode()
            st.download_button("⬇️ Download CSV", csv, f"ipl_batting_{yr}.csv", "text/csv", use_container_width=True)
        with ec2:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine='openpyxl') as w:
                bat_f.to_excel(w, index=False, sheet_name="Batting")
            st.download_button("⬇️ Download Excel", buf.getvalue(), f"ipl_batting_{yr}.xlsx", use_container_width=True)

# ══ TAB 2: BOWLING ══════════════════════════════════════════════════════════
with tabs[1]:
    lbl = yr if yr != "All Seasons" else "All Seasons"
    st.markdown(f'<div class="section-header">🎳 Top Bowlers — {lbl}</div>', unsafe_allow_html=True)
    if bowl_f.empty:
        st.warning("No data found!")
    else:
        c1,c2 = st.columns([3,1])
        with c1:
            top = bowl_f.head(10)
            fig = go.Figure()
            for pc,lb,col2 in [("pp_eco","Powerplay","#3B82F6"),("mid_eco","Middle","#8B5CF6"),("death_eco","Death","#EF4444")]:
                fig.add_trace(go.Bar(name=lb, x=top["player"], y=top[pc], marker_color=col2,
                    text=top[pc].apply(lambda x:f"{x:.1f}"), textposition="outside"))
            fig.update_layout(barmode="group", title=f"Economy by Phase — {lbl}",
                paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG, font_color=TEXT,
                title_font_color=GOLD, height=400,
                xaxis=dict(gridcolor="rgba(0,0,0,0)", tickangle=-25),
                yaxis=dict(gridcolor=GRID, title="Economy"),
                legend=dict(bgcolor="rgba(0,0,0,0)"), margin=dict(t=50,b=60))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            for _,row in bowl_f.head(5).iterrows():
                st.markdown(f"""<div class="highlight-box">
                <div class="highlight-player">{row['player']}</div>
                <div class="highlight-stat">{row['team']} · {row['season']}<br>
                {row['wickets']} wkts · Econ {row['economy']:.2f}</div>
                <div class="award-tag">{row.get('award','')}</div></div>""", unsafe_allow_html=True)
        ca,cb = st.columns(2)
        with ca:
            fig2 = px.bar(bowl_f.head(10).sort_values("dot_pct"), x="dot_pct", y="player",
                orientation="h", color="dot_pct",
                color_continuous_scale=["#EF4444","#FFD700","#22C55E"],
                title="Dot Ball %", text="dot_pct")
            fig2.update_traces(texttemplate="%{text}%", textposition="outside")
            dl(fig2, h=340, xt="Dot %"); fig2.update_layout(coloraxis_showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        with cb:
            fig3 = px.scatter(bowl_f, x="economy", y="avg", size="wickets", color="team",
                hover_name="player", color_discrete_map=TEAM_COLORS, title="Economy vs Avg")
            dl(fig3, h=340); fig3.update_layout(showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(bowl_f[["player","team","season","wickets","economy","avg","sr","dot_pct"]].rename(columns={"player":"Player","team":"Team","season":"Season","wickets":"Wkts","economy":"Econ","avg":"Avg","sr":"SR","dot_pct":"Dot%"}), use_container_width=True, height=340, hide_index=True)
        ec1,ec2 = st.columns(2)
        with ec1:
            st.download_button("⬇️ Download Bowling CSV", bowl_f.to_csv(index=False).encode(), f"ipl_bowling_{yr}.csv", use_container_width=True)
        with ec2:
            buf2 = io.BytesIO()
            with pd.ExcelWriter(buf2, engine='openpyxl') as w:
                bowl_f.to_excel(w, index=False, sheet_name="Bowling")
            st.download_button("⬇️ Download Bowling Excel", buf2.getvalue(), f"ipl_bowling_{yr}.xlsx", use_container_width=True)

# ══ TAB 3: TEAMS ════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">🏟️ Team Performance</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Wins", x=teams_df["team"], y=teams_df["wins_all"], marker_color="#22C55E", text=teams_df["wins_all"], textposition="outside"))
        fig.add_trace(go.Bar(name="Losses", x=teams_df["team"], y=teams_df["losses_all"], marker_color="#EF4444", text=teams_df["losses_all"], textposition="outside"))
        fig.update_layout(barmode="group", title="Wins & Losses", paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG, font_color=TEXT, title_font_color=GOLD, height=360, xaxis=dict(gridcolor="rgba(0,0,0,0)"), yaxis=dict(gridcolor=GRID), legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(teams_df.sort_values("win_pct"), x="win_pct", y="team", orientation="h",
            color="win_pct", color_continuous_scale=["#EF4444","#FFD700","#22C55E"],
            title="Win % All Time", text="win_pct")
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        dl(fig2, h=360, xt="Win %", xr=[35,80]); fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
    th=["MI","CSK","KKR","RCB","SRH","GT"]
    h2h=np.array([[0,20,18,22,17,12],[16,0,14,18,15,8],[10,12,0,15,13,7],[8,10,11,0,10,5],[9,11,12,14,0,9],[4,6,8,9,8,0]])
    fig3 = px.imshow(pd.DataFrame(h2h,index=th,columns=th), text_auto=True, color_continuous_scale=["#1E3A5F","#FFD700"], title="Head-to-Head Matrix")
    fig3.update_layout(paper_bgcolor=PLOT_BG, plot_bgcolor=PLOT_BG, font_color=TEXT, title_font_color=GOLD, height=340)
    st.plotly_chart(fig3, use_container_width=True)

# ══ TAB 4: TRENDS ═══════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">📈 Season Trends 2016–2026</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        fig = px.line(seasons_df, x="season", y="avg_rpo", markers=True, line_shape="spline", title="Avg RPO per Season", color_discrete_sequence=[GOLD])
        fig.add_hline(y=9.0, line_dash="dash", line_color="#EF4444", annotation_text="9.0 milestone")
        dl(fig, h=320, yt="Avg RPO"); st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.bar(seasons_df, x="season", y="total_sixes", title="Total Sixes Per Season", color="total_sixes", color_continuous_scale=["#1E3A5F",GOLD], text="total_sixes")
        fig2.update_traces(textposition="outside")
        dl(fig2, h=320); fig2.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)
    fig3 = px.bar(seasons_df, x="season", y="orange_runs", color="champion", hover_data={"orange_cap":True,"purple_cap":True}, title="Orange Cap Runs (color = Champion)", text="orange_cap", color_discrete_sequence=px.colors.qualitative.Bold)
    fig3.update_traces(textposition="outside"); dl(fig3, h=340, yt="Runs")
    st.plotly_chart(fig3, use_container_width=True)
    st.dataframe(seasons_df.rename(columns={"season":"Year","champion":"Champion","runner_up":"Runner-Up","orange_cap":"Orange Cap","orange_runs":"Runs","purple_cap":"Purple Cap","purple_wkts":"Wkts","avg_rpo":"Avg RPO","total_sixes":"Sixes","matches":"Matches"}), use_container_width=True, hide_index=True)

# ══ TAB 5: PLAYER COMPARE ═══════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">⚔️ Player vs Player Comparison</div>', unsafe_allow_html=True)
    ct = st.radio("Compare", ["🏏 Batters","🎳 Bowlers"], horizontal=True)
    all_batters = sorted(batting_df["player"].unique())
    all_bowlers = sorted(bowling_df["player"].unique())

    if ct == "🏏 Batters":
        c1,c2 = st.columns(2)
        with c1: p1 = st.selectbox("Player 1", all_batters, index=0)
        with c2: p2 = st.selectbox("Player 2", all_batters, index=3)
        d1 = batting_df[batting_df["player"]==p1]
        d2 = batting_df[batting_df["player"]==p2]
        if not d1.empty and not d2.empty:
            s1={"runs":d1["runs"].sum(),"avg":d1["avg"].mean(),"sr":d1["sr"].mean(),"hundreds":d1["hundreds"].sum(),"fifties":d1["fifties"].sum(),"sixes":d1["sixes"].sum(),"fours":d1["fours"].sum(),"team":d1["team"].iloc[-1]}
            s2={"runs":d2["runs"].sum(),"avg":d2["avg"].mean(),"sr":d2["sr"].mean(),"hundreds":d2["hundreds"].sum(),"fifties":d2["fifties"].sum(),"sixes":d2["sixes"].sum(),"fours":d2["fours"].sum(),"team":d2["team"].iloc[-1]}
            ca,cb,cc = st.columns([2,1,2])
            def stat_grid(s,color):
                items = [("Avg",f"{s['avg']:.1f}"),("SR",f"{s['sr']:.1f}"),("100s",s['hundreds']),("50s",s['fifties']),("6s",s['sixes']),("4s",s['fours'])]
                cells = "".join([f'<div><div style="color:{color};font-size:1.15rem;font-weight:700;">{v}</div><div style="color:{TEXT2};font-size:0.72rem;">{k}</div></div>' for k,v in items])
                return f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center;margin-top:10px;">{cells}</div>'
            with ca:
                st.markdown(f"""<div class="compare-card"><div class="compare-name">{p1}</div>
                <div style="color:{TEXT2};font-size:0.82rem;">{s1['team']}</div>
                <div style="font-size:1.9rem;font-weight:700;color:{GOLD};margin-top:8px;">{s1['runs']}</div>
                <div style="color:{TEXT2};font-size:0.78rem;">Total Runs</div>
                {stat_grid(s1,GOLD)}</div>""", unsafe_allow_html=True)
            with cb:
                st.markdown(f"<div style='text-align:center;padding-top:90px;font-size:1.8rem;color:{GOLD};font-weight:700;'>VS</div>", unsafe_allow_html=True)
            with cc:
                st.markdown(f"""<div class="compare-card"><div class="compare-name">{p2}</div>
                <div style="color:{TEXT2};font-size:0.82rem;">{s2['team']}</div>
                <div style="font-size:1.9rem;font-weight:700;color:#3B82F6;margin-top:8px;">{s2['runs']}</div>
                <div style="color:{TEXT2};font-size:0.78rem;">Total Runs</div>
                {stat_grid(s2,'#3B82F6')}</div>""", unsafe_allow_html=True)
            # Radar
            cats=["Runs","Avg","SR","100s","50s","6s"]
            def norm(v,mn,mx): return (v-mn)/(mx-mn)*100 if mx>mn else 50
            v1=[norm(s1["runs"],0,1000),min(s1["avg"],100),norm(s1["sr"],100,220),min(s1["hundreds"]*20,100),min(s1["fifties"]*8,100),min(s1["sixes"]*1.5,100)]
            v2=[norm(s2["runs"],0,1000),min(s2["avg"],100),norm(s2["sr"],100,220),min(s2["hundreds"]*20,100),min(s2["fifties"]*8,100),min(s2["sixes"]*1.5,100)]
            fig=go.Figure()
            fig.add_trace(go.Scatterpolar(r=v1+[v1[0]],theta=cats+[cats[0]],fill="toself",name=p1,line_color=GOLD,fillcolor="rgba(255,215,0,0.12)"))
            fig.add_trace(go.Scatterpolar(r=v2+[v2[0]],theta=cats+[cats[0]],fill="toself",name=p2,line_color="#3B82F6",fillcolor="rgba(59,130,246,0.12)"))
            fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",radialaxis=dict(visible=True,range=[0,100],gridcolor=GRID),angularaxis=dict(gridcolor=GRID)),paper_bgcolor=PLOT_BG,font_color=TEXT,title="Career Radar",title_font_color=GOLD,height=420,legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig, use_container_width=True)
            # Season runs
            mg=pd.merge(d1[["season","runs"]].rename(columns={"runs":p1}),d2[["season","runs"]].rename(columns={"runs":p2}),on="season",how="outer").fillna(0).sort_values("season")
            fig2=go.Figure()
            fig2.add_trace(go.Bar(name=p1,x=mg["season"],y=mg[p1],marker_color=GOLD))
            fig2.add_trace(go.Bar(name=p2,x=mg["season"],y=mg[p2],marker_color="#3B82F6"))
            fig2.update_layout(barmode="group",paper_bgcolor=PLOT_BG,plot_bgcolor=PLOT_BG,font_color=TEXT,title_font_color=GOLD,height=300,xaxis=dict(gridcolor="rgba(0,0,0,0)"),yaxis=dict(gridcolor=GRID,title="Runs"),legend=dict(bgcolor="rgba(0,0,0,0)"),title="Season-wise Runs")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        c1,c2 = st.columns(2)
        with c1: b1 = st.selectbox("Bowler 1", all_bowlers, index=0)
        with c2: b2 = st.selectbox("Bowler 2", all_bowlers, index=2)
        d1=bowling_df[bowling_df["player"]==b1]; d2=bowling_df[bowling_df["player"]==b2]
        if not d1.empty and not d2.empty:
            bs1={"wkts":d1["wickets"].sum(),"eco":d1["economy"].mean(),"avg":d1["avg"].mean(),"dot":d1["dot_pct"].mean(),"team":d1["team"].iloc[-1]}
            bs2={"wkts":d2["wickets"].sum(),"eco":d2["economy"].mean(),"avg":d2["avg"].mean(),"dot":d2["dot_pct"].mean(),"team":d2["team"].iloc[-1]}
            ca,cb,cc = st.columns([2,1,2])
            with ca:
                st.markdown(f"""<div class="compare-card"><div class="compare-name">{b1}</div>
                <div style="color:{TEXT2};">{bs1['team']}</div>
                <div style="font-size:1.9rem;font-weight:700;color:{GOLD};margin-top:8px;">{bs1['wkts']} wkts</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px;">
                <div><div style="color:{GOLD};font-size:1.1rem;font-weight:700;">{bs1['eco']:.2f}</div><div style="color:{TEXT2};font-size:0.72rem;">Economy</div></div>
                <div><div style="color:{GOLD};font-size:1.1rem;font-weight:700;">{bs1['avg']:.1f}</div><div style="color:{TEXT2};font-size:0.72rem;">Avg</div></div>
                <div><div style="color:{GOLD};font-size:1.1rem;font-weight:700;">{bs1['dot']:.0f}%</div><div style="color:{TEXT2};font-size:0.72rem;">Dot%</div></div>
                </div></div>""", unsafe_allow_html=True)
            with cb:
                st.markdown(f"<div style='text-align:center;padding-top:70px;font-size:1.8rem;color:{GOLD};font-weight:700;'>VS</div>", unsafe_allow_html=True)
            with cc:
                st.markdown(f"""<div class="compare-card"><div class="compare-name">{b2}</div>
                <div style="color:{TEXT2};">{bs2['team']}</div>
                <div style="font-size:1.9rem;font-weight:700;color:#3B82F6;margin-top:8px;">{bs2['wkts']} wkts</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px;">
                <div><div style="color:#3B82F6;font-size:1.1rem;font-weight:700;">{bs2['eco']:.2f}</div><div style="color:{TEXT2};font-size:0.72rem;">Economy</div></div>
                <div><div style="color:#3B82F6;font-size:1.1rem;font-weight:700;">{bs2['avg']:.1f}</div><div style="color:{TEXT2};font-size:0.72rem;">Avg</div></div>
                <div><div style="color:#3B82F6;font-size:1.1rem;font-weight:700;">{bs2['dot']:.0f}%</div><div style="color:{TEXT2};font-size:0.72rem;">Dot%</div></div>
                </div></div>""", unsafe_allow_html=True)

# ══ TAB 6: INDIA MAP ════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">🗺️ IPL Teams — India Map</div>', unsafe_allow_html=True)
    map_df = teams_df.copy()
    map_df["info"] = map_df.apply(lambda r: f"{r['team']} · {r['city']}<br>Titles: {r['titles']} · Win%: {r['win_pct']}%", axis=1)
    map_df["size"] = map_df["win_pct"] * 1.2
    fig = px.scatter_mapbox(
        map_df, lat="lat", lon="lon", hover_name="team",
        hover_data={"city":True,"titles":True,"win_pct":True,"lat":False,"lon":False,"size":False},
        size="size", color="team", color_discrete_map=TEAM_COLORS,
        zoom=4.2, center={"lat":22.5,"lon":80.0}, height=540,
        title="IPL Team Home Cities", mapbox_style="carto-darkmatter",
        text="team"
    )
    fig.update_traces(textposition="top center", textfont=dict(size=12, color="white"))
    fig.update_layout(paper_bgcolor=PLOT_BG, font_color=TEXT, title_font_color=GOLD,
                      margin=dict(t=40,b=0,l=0,r=0), legend=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="section-header">📋 Team City Details</div>', unsafe_allow_html=True)
    disp = teams_df[["team","city","titles","win_pct","wins_all","losses_all"]].rename(
        columns={"team":"Team","city":"City","titles":"Titles","win_pct":"Win%","wins_all":"Wins","losses_all":"Losses"})
    st.dataframe(disp, use_container_width=True, hide_index=True)

# ══ TAB 7: MATCH PREDICTOR ══════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">🤖 IPL Match Predictor</div>', unsafe_allow_html=True)
    all_teams=["MI","CSK","RCB","KKR","SRH","GT","RR","DC","PBKS","LSG"]
    c1,c2,c3 = st.columns(3)
    with c1:
        team_a=st.selectbox("🔵 Team A", all_teams, index=0)
        form_a=st.slider(f"{team_a} Form (wins/last 5)", 0, 5, 3)
    with c2:
        team_b=st.selectbox("🔴 Team B", [t for t in all_teams if t!=team_a], index=1)
        form_b=st.slider(f"{team_b} Form (wins/last 5)", 0, 5, 2)
    with c3:
        venue_sel=st.selectbox("🏟 Venue", venues_df["venue"].tolist())
        toss_winner=st.selectbox("🪙 Toss Winner", [team_a,team_b])
        toss_choice=st.selectbox("Chose to", ["Bat","Bowl"])
    if st.button("🎯 Predict Winner", use_container_width=True):
        wpa=float(teams_df[teams_df["team"]==team_a]["win_pct"].values[0]) if len(teams_df[teams_df["team"]==team_a])>0 else 50.0
        wpb=float(teams_df[teams_df["team"]==team_b]["win_pct"].values[0]) if len(teams_df[teams_df["team"]==team_b])>0 else 50.0
        vr=venues_df[venues_df["venue"]==venue_sel].iloc[0]
        hb=5.0 if vr["home_team"]==team_a else (-5.0 if vr["home_team"]==team_b else 0.0)
        tb=3.0 if toss_winner==team_a else -3.0
        if toss_choice=="Bowl" and vr["chase_win_pct"]>55: tb+=2
        fs=(form_a-form_b)*4
        raw_a=wpa+hb+tb+fs; raw_b=wpb-hb-tb-fs
        tot=raw_a+raw_b
        pa=round((raw_a/tot)*100,1); pb=round(100-pa,1)
        win=team_a if pa>pb else team_b
        conf="High 🟢" if abs(pa-50)>15 else ("Medium 🟡" if abs(pa-50)>8 else "Low 🔴")
        st.markdown(f"""<div class="predictor-box">
        <div style="text-align:center;font-family:'Rajdhani',sans-serif;font-size:1.9rem;font-weight:700;color:{GOLD};">🏆 Predicted Winner: {win}</div>
        <div style="text-align:center;color:{TEXT2};margin-top:3px;">Confidence: {conf}</div>
        </div>""", unsafe_allow_html=True)
        pc1,pc2 = st.columns(2)
        with pc1:
            st.markdown(f"""<div class="metric-card"><div class="metric-label">{team_a}</div>
            <div class="metric-value" style="color:{'#22C55E' if win==team_a else '#EF4444'};">{pa}%</div></div>""", unsafe_allow_html=True)
            st.progress(pa/100)
        with pc2:
            st.markdown(f"""<div class="metric-card"><div class="metric-label">{team_b}</div>
            <div class="metric-value" style="color:{'#22C55E' if win==team_b else '#EF4444'};">{pb}%</div></div>""", unsafe_allow_html=True)
            st.progress(pb/100)
        fig=go.Figure(go.Bar(x=[team_a,team_b],y=[pa,pb],marker_color=[TEAM_COLORS.get(team_a,GOLD),TEAM_COLORS.get(team_b,"#EF4444")],text=[f"{pa}%",f"{pb}%"],textposition="outside"))
        fig.update_layout(paper_bgcolor=PLOT_BG,plot_bgcolor=PLOT_BG,font_color=TEXT,title="Win Probability",title_font_color=GOLD,height=280,yaxis=dict(gridcolor=GRID,range=[0,100]),xaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
    # Live win prob
    st.markdown('<div class="section-header">📈 Live Win Probability</div>', unsafe_allow_html=True)
    ci,co = st.columns([2,3])
    with ci:
        target=st.number_input("Target",120,260,178)
        curr_score=st.number_input("Score",0,target-1,112)
        wkts_fallen=st.slider("Wickets Fallen",0,9,3)
        curr_over=st.slider("Over",1.0,19.5,14.3,step=0.1)
        tb2=st.selectbox("Batting Team",all_teams,key="tb2")
        tbo2=st.selectbox("Bowling Team",[t for t in all_teams if t!=tb2],key="tbo2")
    with co:
        od=int(curr_over)+(curr_over%1)*10/6; bl=int((20-curr_over)*6); ol=bl/6
        rn=target-curr_score; rrr=(rn/ol) if ol>0 else 99; crr=(curr_score/od) if od>0 else 0
        wf=(10-wkts_fallen)/10; bp=max(5,min(95,50+(crr-rrr)*8+(wf-0.5)*12))
        m1,m2,m3,m4=st.columns(4)
        m1.metric("Needed",rn); m2.metric("Balls",bl); m3.metric("RRR",f"{rrr:.2f}"); m4.metric("CRR",f"{crr:.2f}")
        st.markdown(f"### {tb2} Win Prob: **{bp:.1f}%**"); st.progress(bp/100)
        overs=list(range(1,21)); probs=[]
        for o in overs:
            ra=int(curr_score*(o/curr_over)) if curr_over>0 else 0; ra=min(ra,target-1); ro=20-o
            p=50+(crr-(target-ra)/max(ro,0.1))*8+(wf-0.5)*12+np.random.normal(0,2) if ro>0 else 50
            probs.append(round(max(5,min(95,p)),1))
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=overs,y=probs,name=tb2,line=dict(color="#22C55E",width=3),fill="tozeroy",fillcolor="rgba(34,197,94,0.08)"))
        fig.add_trace(go.Scatter(x=overs,y=[100-p for p in probs],name=tbo2,line=dict(color="#EF4444",width=3),fill="tozeroy",fillcolor="rgba(239,68,68,0.08)"))
        fig.add_vline(x=curr_over,line_dash="dash",line_color=GOLD)
        fig.update_layout(paper_bgcolor=PLOT_BG,plot_bgcolor=PLOT_BG,font_color=TEXT,title_font_color=GOLD,height=290,xaxis=dict(gridcolor=GRID,title="Over"),yaxis=dict(gridcolor=GRID,title="Win%",range=[0,100]),legend=dict(bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)

# ══ TAB 8: AUCTION & XI ═════════════════════════════════════════════════════
with tabs[7]:
    st8a, st8b = st.tabs(["💰 Auction Data","⭐ Best XI Picker"])
    with st8a:
        st.markdown('<div class="section-header">💰 IPL 2025 Auction Prices</div>', unsafe_allow_html=True)
        af=st.selectbox("Team",["All Teams"]+sorted(auction_df["team"].unique()),key="af2")
        rf=st.selectbox("Role",["All Roles"]+sorted(auction_df["role"].unique()),key="rf2")
        ad=auction_df.copy()
        if af!="All Teams": ad=ad[ad["team"]==af]
        if rf!="All Roles": ad=ad[ad["role"]==rf]
        c1,c2=st.columns(2)
        with c1:
            fig=px.bar(ad.sort_values("price_cr"),x="price_cr",y="player",orientation="h",color="team",color_discrete_map=TEAM_COLORS,title="Player Prices (₹ Crores)",text="price_cr")
            fig.update_traces(texttemplate="₹%{text:.2f}Cr",textposition="outside")
            dl(fig,h=480,xt="Price (Cr)"); fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            fig2=px.pie(auction_df,values="price_cr",names="team",title="Total Spend by Team",color="team",color_discrete_map=TEAM_COLORS)
            fig2.update_layout(paper_bgcolor=PLOT_BG,font_color=TEXT,title_font_color=GOLD,height=480,legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig2,use_container_width=True)
        st.dataframe(ad[["player","team","role","price_cr","status"]].rename(columns={"player":"Player","team":"Team","role":"Role","price_cr":"Price (Cr)","status":"Status"}),use_container_width=True,height=300,hide_index=True)
        buf3=io.BytesIO()
        with pd.ExcelWriter(buf3,engine='openpyxl') as w: auction_df.to_excel(w,index=False,sheet_name="Auction")
        st.download_button("⬇️ Download Auction Excel",buf3.getvalue(),"ipl_auction_2025.xlsx",use_container_width=True)
    with st8b:
        st.markdown('<div class="section-header">⭐ Best XI Picker</div>', unsafe_allow_html=True)
        xi_s=st.selectbox("Season",["All Seasons","2025","2024","2023","2022","2021","2020"],key="xi_s2")
        xb=batting_df.copy(); xbw=bowling_df.copy()
        if xi_s!="All Seasons": xb=xb[xb["season"]==xi_s]; xbw=xbw[xbw["season"]==xi_s]
        xb["bat_score"]=xb["sr"]*xb["avg"]/100+xb["hundreds"]*10+xb["fifties"]*3
        xbw["bowl_score"]=xbw["wickets"]*5+(10-xbw["economy"])*3+xbw["dot_pct"]*0.5
        top_bat=xb.nlargest(7,"bat_score"); top_bowl=xbw.nlargest(4,"bowl_score")
        st.markdown("**🏏 Top 7 Batters**")
        cols=st.columns(7)
        roles=["Opener","Opener","#3 Anchor","#4 Power","#5 Finisher","#6 AR","WK-Bat"]
        for i,(col,(_,row)) in enumerate(zip(cols,top_bat.iterrows())):
            with col:
                tc=TEAM_COLORS.get(row["team"],GOLD)
                st.markdown(f"""<div class="xi-card" style="border-top:3px solid {tc};">
                <div style="font-size:0.62rem;color:{TEXT2};">{roles[i]}</div>
                <div style="font-size:0.82rem;font-weight:700;color:{GOLD};margin:3px 0;">{row['player'].split()[-1]}</div>
                <div style="font-size:0.68rem;color:{TEXT2};">{row['team']}</div>
                <div style="font-size:0.72rem;color:{TEXT};margin-top:3px;">{int(row['runs'])}r<br>SR{row['sr']:.0f}</div>
                </div>""",unsafe_allow_html=True)
        st.markdown("**🎳 Top 4 Bowlers**")
        cols2=st.columns(4)
        br=["Pace #1","Death","Spinner","Swing"]
        for i,(col,(_,row)) in enumerate(zip(cols2,top_bowl.iterrows())):
            with col:
                tc=TEAM_COLORS.get(row["team"],"#3B82F6")
                st.markdown(f"""<div class="xi-card" style="border-top:3px solid {tc};">
                <div style="font-size:0.62rem;color:{TEXT2};">{br[i]}</div>
                <div style="font-size:0.82rem;font-weight:700;color:#3B82F6;margin:3px 0;">{row['player'].split()[-1]}</div>
                <div style="font-size:0.68rem;color:{TEXT2};">{row['team']}</div>
                <div style="font-size:0.72rem;color:{TEXT};margin-top:3px;">{int(row['wickets'])}w<br>Eco{row['economy']:.1f}</div>
                </div>""",unsafe_allow_html=True)

# ══ TAB 9: CUSTOM CHART BUILDER ═════════════════════════════════════════════
with tabs[8]:
    st.markdown('<div class="section-header">📊 Custom Chart Builder</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="highlight-box"><div class="highlight-stat">
    Build your own chart — choose dataset, axes and chart type!</div></div>""", unsafe_allow_html=True)

    cb_ds = st.selectbox("📁 Dataset", ["Batting Stats","Bowling Stats","Season Summary","Team Stats","Auction Prices"])
    ds_map = {"Batting Stats":batting_df,"Bowling Stats":bowling_df,"Season Summary":seasons_df,"Team Stats":teams_df,"Auction Prices":auction_df}
    df_cb = ds_map[cb_ds].copy()

    num_cols = df_cb.select_dtypes(include='number').columns.tolist()
    cat_cols = df_cb.select_dtypes(exclude='number').columns.tolist()

    c1,c2,c3,c4 = st.columns(4)
    with c1: cb_x = st.selectbox("X Axis", df_cb.columns.tolist(), index=0)
    with c2: cb_y = st.selectbox("Y Axis", num_cols, index=min(2,len(num_cols)-1))
    with c3: cb_color = st.selectbox("Color by", ["None"]+cat_cols)
    with c4: cb_type = st.selectbox("Chart Type", ["Bar","Scatter","Line","Histogram","Box","Pie"])

    cb_title = st.text_input("Chart Title", f"{cb_y} vs {cb_x} — {cb_ds}")
    cb_height = st.slider("Chart Height", 300, 700, 420, 50)

    col_arg = cb_color if cb_color != "None" else None

    try:
        if cb_type == "Bar":
            fig_cb = px.bar(df_cb, x=cb_x, y=cb_y, color=col_arg, title=cb_title, color_discrete_map=TEAM_COLORS if col_arg=="team" else None)
        elif cb_type == "Scatter":
            fig_cb = px.scatter(df_cb, x=cb_x, y=cb_y, color=col_arg, hover_name=df_cb.columns[0], title=cb_title, color_discrete_map=TEAM_COLORS if col_arg=="team" else None)
        elif cb_type == "Line":
            fig_cb = px.line(df_cb, x=cb_x, y=cb_y, color=col_arg, title=cb_title, markers=True)
        elif cb_type == "Histogram":
            fig_cb = px.histogram(df_cb, x=cb_x, color=col_arg, title=cb_title)
        elif cb_type == "Box":
            fig_cb = px.box(df_cb, x=col_arg, y=cb_y, title=cb_title, color=col_arg, color_discrete_map=TEAM_COLORS if col_arg=="team" else None)
        elif cb_type == "Pie":
            fig_cb = px.pie(df_cb, names=cb_x, values=cb_y, title=cb_title, color=cb_x, color_discrete_map=TEAM_COLORS)
        dl(fig_cb, h=cb_height)
        st.plotly_chart(fig_cb, use_container_width=True)
    except Exception as e:
        st.error(f"Could not build chart: {e}. Please try different columns!")

    # Export custom chart data
    st.markdown('<div class="section-header">📤 Export This Dataset</div>', unsafe_allow_html=True)
    e1,e2 = st.columns(2)
    with e1:
        st.download_button("⬇️ Download CSV", df_cb.to_csv(index=False).encode(), f"{cb_ds.replace(' ','_')}.csv", use_container_width=True)
    with e2:
        buf_cb=io.BytesIO()
        with pd.ExcelWriter(buf_cb,engine='openpyxl') as w: df_cb.to_excel(w,index=False)
        st.download_button("⬇️ Download Excel", buf_cb.getvalue(), f"{cb_ds.replace(' ','_')}.xlsx", use_container_width=True)

# ══ TAB 10: AI CHATBOT ══════════════════════════════════════════════════════
with tabs[9]:
    st.markdown('<div class="section-header">🧠 IPL AI Chatbot</div>', unsafe_allow_html=True)
    st.markdown(f"""<div class="highlight-box"><div class="highlight-stat">
    Ask me anything about IPL! Stats, records, players, teams, seasons — all answers here 🏏
    </div></div>""", unsafe_allow_html=True)

    # Knowledge base
    ipl_kb = {
        "orange cap 2025": "🟠 Orange Cap 2025: **Sai Sudharsan** (GT) — 759 runs @ SR 156.17"
        ,"orange cap 2026": "🟠 Orange Cap 2026: **Vaibhav Suryavanshi** (RR) — 776 runs @ SR 237.30 🔥 Youngest ever!",
        "purple cap 2025": "🟣 Purple Cap 2025: **Prasidh Krishna** (GT) — 25 wickets"
        ,"purple cap 2026": "🟣 Purple Cap 2026: **Kagiso Rabada** (GT) — 29 wickets, Econ 9.68 (2nd title!)",
        "champion 2026": "🏆 IPL 2026 Champion: **RCB** — Back-to-Back! Beat GT in Final. Kohli 75* POTM"
        ,"champion 2025": "🏆 IPL 2025 Champion: **Royal Challengers Bengaluru (RCB)** — their first ever title!",
        "winner 2025": "🏆 IPL 2025 Winner: **RCB** — beat PBKS in the final!",
        "most titles": "🏆 Most IPL Titles: **Mumbai Indians & CSK** — 5 titles each",
        "most runs": "🟠 Most Runs in IPL History: **Virat Kohli** — 7000+ runs across all seasons",
        "most wickets": "🟣 Most Wickets in IPL: **Yuzvendra Chahal / Dwayne Bravo** — 200+ wickets",
        "best sr": "⚡ Highest Strike Rate (min 200 balls): **Andre Russell** — 180+ SR",
        "best economy": "🎯 Best Economy Rate: **Rashid Khan** — ~6.3 economy in IPL",
        "highest score": "💥 Highest Team Score: **RCB 263/5** vs PWI (2013)",
        "lowest score": "📉 Lowest Team Score: **RCB 49** vs KKR (2017)",
        "rcb": "🔴 **RCB** — Royal Challengers Bengaluru. 🏆 Back-to-Back Champions 2025 & 2026! Home: Chinnaswamy, Bengaluru. Key players: Virat Kohli, Phil Salt, Josh Hazlewood, Bhuvneshwar Kumar",
        "mi": "🔵 **MI** — Mumbai Indians. 5-time champions! Home: Wankhede, Mumbai. Key players: Rohit Sharma, Jasprit Bumrah, Suryakumar Yadav",
        "csk": "💛 **CSK** — Chennai Super Kings. 5-time champions! Home: Chepauk, Chennai. Key player: MS Dhoni",
        "kkr": "💜 **KKR** — Kolkata Knight Riders. 3-time champions (last: 2024). Home: Eden Gardens, Kolkata",
        "virat kohli": "🐐 **Virat Kohli** — RCB legend! 7000+ runs in IPL. 973 runs in 2016 — most runs in a single IPL season. 🟠 Orange Cap 2016, 2024",
        "ms dhoni": "🦁 **MS Dhoni** — CSK captain. Best finisher in IPL history. 5 IPL titles. 'Thala for a Reason'! 💛",
        "rohit sharma": "🎯 **Rohit Sharma** — MI captain. 5-time IPL champion. Best powerplay batter.",
        "jasprit bumrah": "💨 **Jasprit Bumrah** — MI spearhead. Best death bowler in IPL. Yorker king!",
        "sai sudharsan": "🌟 **Sai Sudharsan** — GT star! 2025 Orange Cap winner — 759 runs @ SR 156. Consistent batter!",
        "rashid khan": "🔄 **Rashid Khan** — Best spinner in IPL! Economy ~6.3. GT's key bowler. Afghanistan's pride!",
        "wankhede": "🏟 **Wankhede Stadium** (Mumbai) — MI's home. Flat pitch, small boundaries. Avg score ~168. High scoring venue!",
        "chepauk": "🏟 **Chepauk** (Chennai) — CSK's fortress. Slow, turning pitch. Spinners dominate. Avg score ~155.",
        "chinnaswamy": "🏟 **M Chinnaswamy** (Bengaluru) — RCB's home. Highest scoring venue in IPL! Avg ~185. Batting paradise.",
        "toss": "🪙 Toss factor: Bowl-first advantage at most venues. Chase win% ~52% overall in IPL. Dew factor matters in evening games.",
        "ipl 2016": "📅 IPL 2016: 🏆 Champion: **SRH** | 🟠 Orange Cap: **Virat Kohli** (973 runs) | 🟣 Purple Cap: **Bhuvneshwar Kumar** (26 wkts)",
        "ipl 2024": "📅 IPL 2024: 🏆 Champion: **KKR** | 🟠 Orange Cap: **Virat Kohli** (741 runs) | 🟣 Purple Cap: **Harshal Patel** (24 wkts)"
        ,"ipl 2026": "📅 IPL 2026: 🏆 Champion: **RCB** (back-to-back!) | 🟠 Orange Cap: **Vaibhav Suryavanshi** 776 runs @ SR 237 | 🟣 Purple Cap: **Kagiso Rabada** 29 wkts"
        ,"vaibhav suryavanshi": "🌟 **Vaibhav Suryavanshi** (RR) — IPL 2026 sensation! 776 runs @ SR 237.30, 72 sixes. 15 years old! Won 5 awards in one season — first ever in IPL history! 🏆"
        ,"2026": "📅 IPL 2026: Champion: **RCB** | Orange Cap: **Vaibhav Suryavanshi** 776 @ SR 237 | Purple Cap: **Kagiso Rabada** 29 wkts | Avg RPO: 9.88 (record!) | Sixes: 1,426 (record!)",
        "ipl 2023": "📅 IPL 2023: 🏆 Champion: **CSK** | 🟠 Orange Cap: **Shubman Gill** (890 runs) | 🟣 Purple Cap: **Mohammed Shami** (28 wkts)",
        "ipl 2022": "📅 IPL 2022: 🏆 Champion: **GT** | 🟠 Orange Cap: **Jos Buttler** (863 runs) | 🟣 Purple Cap: **Yuzvendra Chahal** (27 wkts)",
        "powerplay": "⚡ Powerplay (Ov 1-6): Avg ~8.6 RPO in 2025. Key stat — teams scoring 55+ in powerplay win 68% of matches!",
        "death overs": "💀 Death Overs (Ov 16-20): Avg ~11 RPO. Best death bowler: Jasprit Bumrah (eco 8.3 at death vs league avg 10+)",
    }

    def ipl_bot_answer(q):
        q = q.lower().strip()
        for key, ans in ipl_kb.items():
            if any(word in q for word in key.split()):
                return ans
        # Stats lookup
        player_match = batting_df[batting_df["player"].str.lower().str.contains(q.replace("stats","").strip())]
        if not player_match.empty:
            p = player_match.iloc[0]
            return f"🏏 **{p['player']}** stats — {p['season']}: {p['runs']} runs, Avg {p['avg']}, SR {p['sr']}, Team: {p['team']}"
        bowl_match = bowling_df[bowling_df["player"].str.lower().str.contains(q.replace("stats","").strip())]
        if not bowl_match.empty:
            p = bowl_match.iloc[0]
            return f"🎳 **{p['player']}** stats — {p['season']}: {p['wickets']} wkts, Econ {p['economy']:.2f}, Team: {p['team']}"
        return f"🤔 Sorry, I don't know that! Try: 'orange cap 2025', 'Virat Kohli', 'RCB', 'IPL 2024', 'best economy', 'wankhede' etc."

    # Chat UI
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [("bot","Hello! 🏏 I am the IPL Analytics Chatbot. Ask me anything — players, teams, stats, venues!")]

    for role, msg in st.session_state.chat_history:
        css = "chat-msg-user" if role=="user" else "chat-msg-bot"
        icon = "👤" if role=="user" else "🤖"
        st.markdown(f'<div class="{css}">{icon} {msg}</div>', unsafe_allow_html=True)

    # Quick questions
    st.markdown("**⚡ Quick Questions:**")
    q_cols = st.columns(4)
    quick_qs = ["Orange Cap 2026?","Tell me about RCB","Vaibhav Suryavanshi stats","IPL 2026 results?"]
    for i,(qc,qq) in enumerate(zip(q_cols,quick_qs)):
        with qc:
            if st.button(qq, key=f"qq{i}", use_container_width=True):
                ans = ipl_bot_answer(qq)
                st.session_state.chat_history.append(("user", qq))
                st.session_state.chat_history.append(("bot", ans))
                st.rerun()

    user_input = st.chat_input("Ask anything about IPL... 🏏")
    if user_input:
        ans = ipl_bot_answer(user_input)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", ans))
        st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = [("bot","Hello! 🏏 Ask me anything!")]
        st.rerun()

# ══ TAB 11: QUIZ ════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown('<div class="section-header">🎮 IPL Trivia Quiz</div>', unsafe_allow_html=True)

    QUESTIONS = [
        {"q":"Who was the IPL 2025 champion?","opts":["MI","CSK","RCB","KKR"],"ans":"RCB","fact":"RCB won their first ever IPL title in 2025, beating PBKS in the final!"},
        {"q":"Who won the Orange Cap in 2025?","opts":["Virat Kohli","Sai Sudharsan","Shubman Gill","Jos Buttler"],"ans":"Sai Sudharsan","fact":"Sai Sudharsan scored 759 runs at SR 156.17 for GT — a brilliant season!"},
        {"q":"Who scored the most runs in a single IPL season?","opts":["David Warner","Jos Buttler","Virat Kohli","Shubman Gill"],"ans":"Virat Kohli","fact":"Virat Kohli scored 973 runs in 2016 — still the all-time IPL season record!"},
        {"q":"Which team has won the most IPL titles?","opts":["CSK","MI","KKR","RCB"],"ans":"MI","fact":"Both MI and CSK have 5 titles each — MI won theirs first chronologically!"},
        {"q":"Who won the Purple Cap in IPL 2016?","opts":["Jasprit Bumrah","Rashid Khan","Bhuvneshwar Kumar","Yuzvendra Chahal"],"ans":"Bhuvneshwar Kumar","fact":"Bhuvneshwar Kumar took 26 wickets for SRH in 2016 to win the Purple Cap."},
        {"q":"Which spinner has taken the most IPL wickets?","opts":["Rashid Khan","R Ashwin","Yuzvendra Chahal","Harbhajan Singh"],"ans":"Yuzvendra Chahal","fact":"Yuzvendra Chahal has 200+ IPL wickets — the best leg spinner in IPL history!"},
        {"q":"Which team holds the highest team score in IPL?","opts":["MI","CSK","RCB","SRH"],"ans":"RCB","fact":"RCB scored 263/5 against PWI in 2013 — still the highest team total in IPL!"},
        {"q":"Who was the IPL 2023 champion?","opts":["GT","MI","KKR","CSK"],"ans":"CSK","fact":"CSK won their 5th title in 2023, defeating GT in the final!"},
        {"q":"Which team's home ground is Wankhede Stadium?","opts":["CSK","RCB","MI","KKR"],"ans":"MI","fact":"Wankhede in Mumbai is MI's fortress — flat pitch and short boundaries make it a high-scoring ground!"},
        {"q":"Which batter has played the most IPL matches?","opts":["MS Dhoni","Suresh Raina","Rohit Sharma","Virat Kohli"],"ans":"MS Dhoni","fact":"MS Dhoni has played 200+ IPL matches — an absolute legend of the format!"},
    ]

    if "quiz_state" not in st.session_state:
        st.session_state.quiz_state = {"q_idx":0,"score":0,"answered":False,"selected":None,"finished":False}

    qs = st.session_state.quiz_state

    if not qs["finished"]:
        q = QUESTIONS[qs["q_idx"]]
        total = len(QUESTIONS)
        prog = qs["q_idx"] / total
        st.progress(prog, text=f"Question {qs['q_idx']+1} of {total} | Score: {qs['score']}/{qs['q_idx']}")

        st.markdown(f"""<div class="quiz-card">
        <div class="quiz-q">Q{qs['q_idx']+1}. {q['q']}</div>
        </div>""", unsafe_allow_html=True)

        if not qs["answered"]:
            cols = st.columns(2)
            for i, opt in enumerate(q["opts"]):
                with cols[i % 2]:
                    if st.button(f"{'🅐🅑🅒🅓'[i]} {opt}", key=f"opt_{qs['q_idx']}_{i}", use_container_width=True):
                        qs["selected"] = opt
                        qs["answered"] = True
                        if opt == q["ans"]: qs["score"] += 1
                        st.rerun()
        else:
            sel = qs["selected"]
            correct = q["ans"]
            for opt in q["opts"]:
                if opt == correct:
                    st.success(f"✅ {opt} — SAHI!")
                elif opt == sel and sel != correct:
                    st.error(f"❌ {opt} — GALAT!")
                else:
                    st.markdown(f"⬜ {opt}")
            st.info(f"💡 Fun Fact: {q['fact']}")
            if st.button("➡️ Next Question" if qs["q_idx"] < total-1 else "🏁 Finish Quiz", use_container_width=True):
                if qs["q_idx"] < total-1:
                    qs["q_idx"] += 1; qs["answered"] = False; qs["selected"] = None
                else:
                    qs["finished"] = True
                st.rerun()
    else:
        score = qs["score"]; total = len(QUESTIONS)
        pct = score/total*100
        if pct == 100: grade="🏆 IPL Legend!"; color="#FFD700"
        elif pct >= 70: grade="⭐ IPL Expert!"; color="#22C55E"
        elif pct >= 50: grade="🏏 Good Fan!"; color="#3B82F6"
        else: grade="📚 Study more, mate!"; color="#EF4444"
        st.markdown(f"""<div class="predictor-box" style="text-align:center;">
        <div style="font-size:3rem;">{'🏆' if pct==100 else '⭐' if pct>=70 else '🏏' if pct>=50 else '📚'}</div>
        <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;font-weight:700;color:{color};">{grade}</div>
        <div style="font-size:1.2rem;color:{TEXT};margin-top:8px;">Score: <strong style="color:{GOLD};">{score}/{total}</strong> ({pct:.0f}%)</div>
        </div>""", unsafe_allow_html=True)
        if st.button("🔄 Play Again", use_container_width=True):
            random.shuffle(QUESTIONS)
            st.session_state.quiz_state = {"q_idx":0,"score":0,"answered":False,"selected":None,"finished":False}
            st.rerun()

st.markdown(f"""<hr style='border:1px solid {BORDER};margin:24px 0 12px;'>
<div style='text-align:center;color:{TEXT2};font-size:0.72rem;padding-bottom:14px;'>
🏏 IPL Analytics Hub v3.0 · 11 Tabs · 2016–2026 Data<br>
📊 ESPNcricinfo + IPL Official · Built with Streamlit, Plotly & Python<br>
🏆 2026 Champion: <strong style='color:{GOLD};'>RCB 🎉 Back-to-Back!</strong> · 🟠 <strong style='color:{GOLD};'>Vaibhav Suryavanshi 776 @ SR 237</strong> · 🟣 <strong style='color:{GOLD};'>Kagiso Rabada 29 wkts</strong>
</div>""", unsafe_allow_html=True)