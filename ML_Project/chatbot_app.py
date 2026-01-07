# ipl_csk_chatbot.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# 🟡 CSK Linear Gradient Theme
st.set_page_config(page_title="🏏 CSK Player Performance Chatbot", layout="wide")

page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFD700 0%, #0B3D91 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(255, 204, 0, 0.9);
}
h1, h2, h3, h4, h5, h6 {
    color: #0B3D91 !important;
    font-family: 'Poppins', sans-serif;
}
.stButton>button {
    background-color: #FFD700;
    color: #0B3D91;
    border: 2px solid #0B3D91;
    border-radius: 12px;
    font-weight: bold;
    padding: 10px 24px;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #0B3D91;
    color: #FFD700;
    transform: scale(1.05);
}
.stSelectbox, .stNumberInput, .stTextInput {
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 6px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 🏏 Load Models
@st.cache_resource
def load_models():
    bat_model = joblib.load('batting_performance_model.pkl')
    bowl_model = joblib.load('bowling_performance_model.pkl')
    return bat_model, bowl_model

bat_model, bowl_model = load_models()

# 🟡 Header
st.title("🏏 **CSK Player Performance Chatbot**")
st.markdown("💛 Welcome to the **Chennai Super Kings** ML chatbot — powered by data, driven by passion 💙")
st.write("Predict **Runs** and **Wickets** like a champion. Choose your mode below 👇")

mode = st.selectbox(
    "Select Mode ⚙️",
    ["Predict Runs (Batting)", "Predict Wickets (Bowling)", "Conversational"],
    index=0
)

# Helper for number input
def number_input_col(key, label, default=0):
    return st.number_input(label, value=float(default), format="%.2f", key=key)

# 🟨 Batting Prediction
if mode == "Predict Runs (Batting)":
    st.header("💥 Predict Runs — Enter Batting Stats")
    Matches_Batted = number_input_col("mb", "Matches Batted", 10)
    Not_Outs = number_input_col("no", "Not Outs", 1)
    Balls_Faced = number_input_col("bf", "Balls Faced", 300)
    Batting_Strike_Rate = number_input_col("bsr", "Batting Strike Rate", 120)
    Centuries = number_input_col("cent", "Centuries", 0)
    Half_Centuries = number_input_col("half", "Half Centuries", 2)
    Fours = number_input_col("fours", "Fours", 30)
    Sixes = number_input_col("sixes", "Sixes", 10)

    if st.button("🚀 Predict Runs"):
        X = pd.DataFrame([{
            'Matches_Batted': Matches_Batted,
            'Not_Outs': Not_Outs,
            'Balls_Faced': Balls_Faced,
            'Batting_Strike_Rate': Batting_Strike_Rate,
            'Centuries': Centuries,
            'Half_Centuries': Half_Centuries,
            'Fours': Fours,
            'Sixes': Sixes
        }])
        pred = bat_model.predict(X)[0]
        st.success(f"🏏 **Predicted Runs:** {pred:.2f}")

# 💙 Bowling Prediction
elif mode == "Predict Wickets (Bowling)":
    st.header("🎯 Predict Wickets — Enter Bowling Stats")
    Matches_Bowled = number_input_col("mbw", "Matches Bowled", 8)
    Balls_Bowled = number_input_col("bbw", "Balls Bowled", 200)
    Runs_Conceded = number_input_col("rc", "Runs Conceded", 220)
    Bowling_Average = number_input_col("ba", "Bowling Average", 25)
    Economy_Rate = number_input_col("er", "Economy Rate", 7.5)
    Bowling_Strike_Rate = number_input_col("bsr_w", "Bowling Strike Rate", 20)
    Four_Wicket_Hauls = number_input_col("fw", "Four Wicket Hauls", 0)
    Five_Wicket_Hauls = number_input_col("fiw", "Five Wicket Hauls", 0)

    if st.button("🔥 Predict Wickets"):
        X = pd.DataFrame([{
            'Matches_Bowled': Matches_Bowled,
            'Balls_Bowled': Balls_Bowled,
            'Runs_Conceded': Runs_Conceded,
            'Bowling_Average': Bowling_Average,
            'Economy_Rate': Economy_Rate,
            'Bowling_Strike_Rate': Bowling_Strike_Rate,
            'Four_Wicket_Hauls': Four_Wicket_Hauls,
            'Five_Wicket_Hauls': Five_Wicket_Hauls
        }])
        pred = bowl_model.predict(X)[0]
        st.success(f"🎯 **Predicted Wickets:** {pred:.2f}")

# 💬 Conversational Mode
else:
    st.header("🗣️ Conversational Mode")
    st.write("Talk to the CSK bot! Try: `predict runs` or `predict wickets` 🏏")

    if 'state' not in st.session_state:
        st.session_state.state = {}

    user_input = st.text_input("You:", key="user_text")

    def ask_for_batting():
        st.session_state.state['mode'] = 'bat'
        st.session_state.state['ask'] = ['Matches_Batted','Not_Outs','Balls_Faced','Batting_Strike_Rate','Centuries','Half_Centuries','Fours','Sixes']
        st.session_state.state['answers'] = {}

    def ask_for_bowling():
        st.session_state.state['mode'] = 'bowl'
        st.session_state.state['ask'] = ['Matches_Bowled','Balls_Bowled','Runs_Conceded','Bowling_Average','Economy_Rate','Bowling_Strike_Rate','Four_Wicket_Hauls','Five_Wicket_Hauls']
        st.session_state.state['answers'] = {}

    if user_input:
        text = user_input.lower()
        if 'runs' in text or 'bat' in text:
            ask_for_batting()
            st.info("Alright 🦁 — Let’s predict some batting stats! Answer the questions below 👇")
        elif 'wicket' in text or 'bowl' in text:
            ask_for_bowling()
            st.info("Roaring into bowling stats! 🎯 Enter the details below 👇")
        else:
            st.warning("Please say something like `predict runs` or `predict wickets` 💬")

    if st.session_state.state.get('ask'):
        ask_list = st.session_state.state['ask']
        answers = st.session_state.state.get('answers', {})
        next_key = next((k for k in ask_list if k not in answers), None)
        if next_key:
            val = st.text_input(f"Enter value for **{next_key}**:", key=f"conv_{next_key}")
            if val != "":
                try:
                    answers[next_key] = float(val)
                    st.session_state.state['answers'] = answers
                    st.experimental_rerun()
                except:
                    st.error("⚠️ Please enter a numeric value.")
        else:
            if st.session_state.state['mode'] == 'bat':
                X = pd.DataFrame([answers])
                pred = bat_model.predict(X)[0]
                st.success(f"🏏 **Predicted Runs:** {pred:.2f}")
            else:
                X = pd.DataFrame([answers])
                pred = bowl_model.predict(X)[0]
                st.success(f"🎯 **Predicted Wickets:** {pred:.2f}")
            st.session_state.state = {}
