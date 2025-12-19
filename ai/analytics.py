import numpy as np
import pandas as pd

def analyze_patterns(history_df):
    if len(history_df) < 2:
        return "Not enough history yet.", 0, 0, 0

    recent_math = history_df['math'].iloc[-1]
    recent_reading = history_df['reading'].iloc[-1]
    prev_math = history_df['math'].iloc[-2]
    velocity = recent_math - prev_math

    if velocity > 0:
        msg = f"🚀 Improving! You gained {velocity} points since last time."
    elif velocity < 0:
        msg = f"📉 Warning: Score dropped by {abs(velocity)}. Review requested."
    else:
        msg = "⚖️ Stable: No change in performance."

    return msg, velocity, recent_math, recent_reading


def goal_prediction(current_math, velocity, target_score):
    if velocity <= 0:
        return None

    points_needed = target_score - current_math
    sessions_needed = int(np.ceil(points_needed / velocity))
    return sessions_needed

def predict_improvement(current_score, velocity, sessions_ahead):
    """Predict score after a number of sessions based on current velocity."""
    return current_score + velocity * sessions_ahead

def calculate_increments(history_df):
    """Calculate session-to-session increments for math and reading."""
    if len(history_df) < 2:
        return pd.DataFrame()
    
    math_increments = history_df['math'].diff().dropna()
    reading_increments = history_df['reading'].diff().dropna()
    
    increments_df = pd.DataFrame({
        'session': range(1, len(math_increments) + 1),
        'math_increment': math_increments.values,
        'reading_increment': reading_increments.values
    })
    return increments_df
