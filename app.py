import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from datetime import datetime

from ai.clustering import assign_cluster
from ai.analytics import analyze_patterns, goal_prediction, predict_improvement, calculate_increments
from db.database import init_db

# ---------- CONFIG ----------
st.set_page_config(page_title="AI Learning Engine", layout="wide")
st.title("AI Learning Engine: Memory & Goal Tracking")

# ---------- DATABASE ----------
conn = init_db()

# ---------- DATA ----------
@st.cache_data
def load_baseline():
    if os.path.exists('data/student.csv'):
        try:
            df = pd.read_csv('data/student.csv')
            if not df.empty and 'math score' in df.columns and 'reading score' in df.columns:
                return df
        except pd.errors.EmptyDataError:
            pass
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
    st.plotly_chart(fig)

with col2:
    st.subheader("🕵️ Pattern Sensing")
    msg, velocity, current_math, current_reading = analyze_patterns(history_df)
    st.write(msg)

    st.divider()

    default_goal = min(100, max(90, current_math + 1))
    target = st.number_input("Set Math Goal", int(current_math + 1), 100, default_goal)

    sessions = goal_prediction(current_math, velocity, target)
    if sessions:
        st.success(f"🎯 Goal achievable in ~{sessions} sessions")
    else:
        st.info("Increase learning velocity to estimate goal.")
    
# ---------- CHATBOT ----------
st.markdown("---")
st.subheader("🤖 Study Analysis Chatbot")

def analyze_student_level(history_df, current_math, current_reading, velocity):
    if history_df.empty:
        return "Not enough data yet. Please log some assessments to get personalized analysis."
    
    avg_math = history_df['math'].mean()
    avg_reading = history_df['reading'].mean()
    
    # Determine level based on average scores
    if avg_math < 50 or avg_reading < 50:
        level = "Beginner"
    elif avg_math < 80 or avg_reading < 80:
        level = "Intermediate"
    else:
        level = "Advanced"
    
    # Analyze patterns
    math_scores = history_df['math'].tolist()
    reading_scores = history_df['reading'].tolist()
    
    math_trend = "improving" if len(math_scores) > 1 and math_scores[-1] > math_scores[0] else "stable"
    reading_trend = "improving" if len(reading_scores) > 1 and reading_scores[-1] > reading_scores[0] else "stable"
    
    # Identify weaknesses
    weak_subject = "Math" if avg_math < avg_reading else "Reading"
    
    # Recommendations based on level and weakness
    recommendations = {
        "Beginner": {
            "Math": ["Khan Academy: Basic Math Fundamentals", "Math Workbook for Beginners", "YouTube: Math Antics Series"],
            "Reading": ["Reading A-Z: Comprehension Basics", "Vocabulary.com App", "Books: 'The Very Hungry Caterpillar' for practice"]
        },
        "Intermediate": {
            "Math": ["Khan Academy: Algebra and Geometry", "Online Course: Mathway Tutorials", "Book: 'Algebra for Dummies'"],
            "Reading": ["SparkNotes: Literature Guides", "Grammarly for Writing Practice", "Book: 'How to Read a Book' by Mortimer Adler"]
        },
        "Advanced": {
            "Math": ["Khan Academy: Calculus and Advanced Topics", "Problem Sets from MIT OpenCourseWare", "Book: 'Calculus' by James Stewart"],
            "Reading": ["The New York Times: Daily Articles", "Critical Thinking Exercises", "Book: 'The Elements of Style' by Strunk and White"]
        }
    }
    
    recs = recommendations[level][weak_subject]
    
    # Velocity-based advice
    if velocity > 0:
        velocity_advice = f"Your learning velocity is positive ({velocity} points per session). Keep it up!"
    elif velocity < 0:
        velocity_advice = f"Your velocity is negative ({velocity}). Focus on reviewing mistakes and consistent practice."
    else:
        velocity_advice = "Your scores are stable. Try increasing study intensity to see improvement."
    
    return f"""
**Student Level Analysis:**

- **Overall Level:** {level}
- **Average Math Score:** {avg_math:.1f}
- **Average Reading Score:** {avg_reading:.1f}
- **Math Trend:** {math_trend}
- **Reading Trend:** {reading_trend}
- **Weakest Subject:** {weak_subject}

**Recommendations for Improvement:**
- **Study Materials for {weak_subject}:**
  {chr(10).join(f"  • {rec}" for rec in recs)}
- **Additional Advice:** {velocity_advice}
- **General Tip:** Practice daily, review errors, and use active recall techniques.
"""

if st.button("Analyze My Level & Get Recommendations"):
    analysis = analyze_student_level(history_df, current_math, current_reading, velocity)
    st.write(analysis)

# ---------- HISTORY ----------
st.markdown("---")
if not history_df.empty:
    st.subheader("📜 Learning Timeline")
    st.line_chart(history_df.set_index('date')[['math', 'reading']])
    
    # Prediction Facility
    st.subheader("🔮 Improvement Prediction")
    sessions_ahead = st.slider("Predict score after how many sessions?", 1, 20, 5)
    predicted_math = predict_improvement(current_math, velocity, sessions_ahead)
    predicted_reading = predict_improvement(current_reading, velocity, sessions_ahead)
    st.write(f"Predicted Math Score after {sessions_ahead} sessions: {predicted_math:.1f}")
    st.write(f"Predicted Reading Score after {sessions_ahead} sessions: {predicted_reading:.1f}")
    
    # Increment/Decrement Graph
    st.subheader("📈 Session-to-Session Increments")
    increments_df = calculate_increments(history_df)
    if not increments_df.empty:
        st.bar_chart(increments_df.set_index('session')[['math_increment', 'reading_increment']])
    else:
        st.write("Need more data points for increment analysis.")
