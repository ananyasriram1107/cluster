import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime

from ai.clustering import assign_cluster
from ai.analytics import analyze_patterns, goal_prediction
from db.database import init_db

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Learning Engine", layout="wide")
st.title("🧠 AI Learning Engine: Memory & Goal Tracking")

# ---------- DATABASE ----------
conn = init_db()

# ---------- DATA ----------
@st.cache_data
def load_baseline():
    if os.path.exists('data/Student_Performance.csv'):
        return pd.read_csv('data/Student_Performance.csv')
    else:
        return pd.DataFrame({
            'math score': np.random.randint(30, 100, 1000),
            'reading score': np.random.randint(30, 100, 1000)
        })

df_baseline = load_baseline()

# ---------- SIDEBAR ----------
st.sidebar.header("📝 New Assessment")
m_new = st.sidebar.number_input("Math Mark", 0, 100, 75)
r_new = st.sidebar.number_input("Reading Mark", 0, 100, 70)
c_new = st.sidebar.slider("Engagement (Clicks)", 0, 1000, 200)

if st.sidebar.button("Save Entry"):
    cluster = assign_cluster(df_baseline, m_new, r_new)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn.execute(
        "INSERT INTO progress VALUES (?,?,?,?,?)",
        (now, m_new, r_new, c_new, cluster)
    )
    conn.commit()
    st.sidebar.success("Saved to Database!")

# ---------- DASHBOARD ----------
history_df = pd.read_sql_query("SELECT * FROM progress", conn)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🌌 Competency Galaxy")
    fig = px.scatter(
        df_baseline,
        x="math score",
        y="reading score",
        opacity=0.1
    )
    fig.add_scatter(
        x=[m_new],
        y=[r_new],
        mode='markers',
        marker=dict(size=18, color='gold', symbol='star'),
        name="YOU"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🕵️ Pattern Sensing")
    msg, velocity, current_math = analyze_patterns(history_df)
    st.write(msg)

    st.divider()

    default_goal = min(100, max(90, current_math + 1))
    target = st.number_input("Set Math Goal", int(current_math + 1), 100, default_goal)

    sessions = goal_prediction(current_math, velocity, target)
    if sessions:
        st.success(f"🎯 Goal achievable in ~{sessions} sessions")
    else:
        st.info("Increase learning velocity to estimate goal.")

# ---------- HISTORY ----------
st.markdown("---")
if not history_df.empty:
    st.subheader("📜 Learning Timeline")
    st.line_chart(history_df.set_index('date')[['math', 'reading']])
