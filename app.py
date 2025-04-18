import streamlit as st
import pandas as pd
import joblib
import os

# Set page configuration for a wider layout and football theme
st.set_page_config(page_title="⚽ Football Momentum Predictor", page_icon="⚽", layout="wide")

# Define global variables for feature engineering
event_types = [
    'Crucial_Save', 'Goal_Conceded', 'Goal_Scored', 'Missed_Chance',
    'Red_Card_Opp', 'Red_Card_Own', 'Sub_In', 'Sub_Out',
    'Yellow_Card_Opp', 'Yellow_Card_Own'
]
stages = ['0-15', '15-30', '30-45', '45-60', '60-75', '75-90', '90+']
momentum_bins = ['Strong_Negative', 'Negative', 'Positive', 'Strong_Positive']
numerical_cols = [
    'Score_Differential', 'Possession_Pre_Event', 'Shots_Pre_Event',
    'Passes_Completed_Pre_Event', 'Opponent_Strength', 'Fatigue_Index',
    'Crowd_Influence', 'Momentum_Swing', 'Recent_Form', 'Event_Severity',
    'Sub_Impact', 'Pressure_Index', 'Possession_x_Shots', 'Pressure_x_Fatigue'
]

# Create display-friendly event types (replace underscores with spaces)
display_event_types = [et.replace('_', ' ') for et in event_types]

# Load model, scaler, and feature names
model = joblib.load("logistic_model.pkl")
scaler = joblib.load("scaler.pkl")
training_features = joblib.load("feature_names.pkl")

# Custom CSS for football theme with updated footer styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        min-height: 100vh; /* Ensure the main container covers the full viewport height */
        padding-bottom: 60px; /* Reserve space for the fixed footer */
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSlider .st-bx {
        background-color: #e0e0e0;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    h1, h2, h3 {
        color: #2e7d32;
        font-family: 'Arial', sans-serif;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-right: 2px solid #4CAF50;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        color: #2e7d32;
        border-radius: 5px 5px 0 0;
        margin-right: 5px;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .footer {
        position: fixed; /* Fix to bottom of viewport */
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        font-family: 'Roboto', sans-serif; /* Clean, modern font */
        font-size: 16px;
        color: #2e7d32; /* Match theme color */
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.8); /* Slight background for contrast */
        border-top: 1px solid #4CAF50; /* Subtle border */
        font-weight: 500; /* Medium boldness */
        z-index: 1000; /* Ensure it stays above other elements */
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar with app info and football image
with st.sidebar:
    #st.image("https://cdn.pixabay.com/photo/2013/07/13/12/51/soccer-160109_1280.png", width=150)
    st.header("⚽ Momentum Predictor")
    st.write("Predict your team's recovery probability after key match events.")
    st.markdown("""
        **Features:**
        - 📊 Manual input for single predictions
        - 📂 Upload CSV for batch predictions
        - 🏟️ Football-themed interface
        - 🔍 Detailed match scenario analysis
    """)

# Main app
st.title("⚽ Football Momentum Shifts: Recovery Probability Predictor")

# Header for prediction
st.header("🏆 Predict Recovery Probability")

# Tabs for input methods
tab1, tab2 = st.tabs(["📋 Manual Input", "📂 Upload CSV"])

# Tab 1: Manual Input
with tab1:
    st.markdown("Input match scenario details to predict the likelihood of team recovery. 🥅")
    with st.form("prediction_form"):
        st.subheader("Match Scenario Inputs")
        col1, col2 = st.columns(2)
        with col1:
            event_type_display = st.selectbox("Event Type ⚽", display_event_types)
            # Map display value back to model-compatible value
            event_type = event_type_display.replace(' ', '_')
            score_diff = st.slider("Score Differential 📈", -3, 3, 0)
            possession = st.slider("Possession Pre-Event (%) ⚖️", 20.0, 80.0, 50.0)
            shots = st.slider("Shots Pre-Event 🎯", 0, 10, 3)
            passes = st.slider("Passes Completed Pre-Event 🏃", 30, 100, 60)
            opp_strength = st.slider("Opponent Strength 💪", 0.4, 1.0, 0.7)
            fatigue = st.slider("Fatigue Index 😓", 0.3, 0.9, 0.6)
        with col2:
            crowd = st.slider("Crowd Influence 👏", 0.2, 0.8, 0.5)
            key_player = st.selectbox("Key Player Involved 🌟", [0, 1])
            tactical_shift = st.selectbox("Tactical Shift 🔄", [0, 1])
            momentum = st.slider("Momentum Swing 📉📈", -30.0, 30.0, 0.0)
            recent_form = st.slider("Recent Form 🏅", 0.3, 0.9, 0.6)
            sub_impact = st.slider("Substitution Impact 🔄", 0.0, 0.7, 0.3)
            pressure = st.slider("Pressure Index 😰", 0.3, 1.0, 0.6)
            time_event = st.slider("Time of Event (Minutes) ⏱️", 0.0, 95.0, 45.0)
            event_severity = st.slider("Event Severity 🚨", 0.2, 1.0, 0.6)

        submitted = st.form_submit_button("Predict Recovery 🚀")

    if submitted:
        # Create input DataFrame
        input_data = pd.DataFrame({
            'Event_Type': [event_type],
            'Score_Differential': [score_diff],
            'Time_of_Event': [time_event],
            'Home_Away': [1],  # Default, as in training
            'Possession_Pre_Event': [possession],
            'Shots_Pre_Event': [shots],
            'Passes_Completed_Pre_Event': [passes],
            'Opponent_Strength': [opp_strength],
            'Fatigue_Index': [fatigue],
            'Crowd_Influence': [crowd],
            'Key_Player_Involved': [key_player],
            'Tactical_Shift': [tactical_shift],
            'Momentum_Swing': [momentum],
            'Recent_Form': [recent_form],
            'Event_Severity': [event_severity],
            'Sub_Impact': [sub_impact],
            'Pressure_Index': [pressure]
        })

        # Feature engineering
        # 1. One-hot encode Event_Type
        input_encoded = pd.get_dummies(input_data, columns=['Event_Type'], prefix='Event')
        for et in event_types:
            col = f'Event_{et}'
            if col not in input_encoded.columns:
                input_encoded[col] = 0

        # 2. Bin Time_of_Event into Game_Stage
        input_encoded['Game_Stage'] = pd.cut(
            input_encoded['Time_of_Event'],
            bins=[0, 15, 30, 45, 60, 75, 90, 100],
            labels=stages,
            include_lowest=True
        )
        input_encoded = pd.get_dummies(input_encoded, columns=['Game_Stage'], prefix='Stage')
        for s in stages:
            col = f'Stage_{s}'
            if col not in input_encoded.columns:
                input_encoded[col] = 0

        # 3. Create Momentum_Bin
        input_encoded['Momentum_Bin'] = pd.cut(
            input_encoded['Momentum_Swing'],
            bins=[-float('inf'), -10, 0, 10, float('inf')],
            labels=momentum_bins,
            include_lowest=True
        )
        input_encoded = pd.get_dummies(input_encoded, columns=['Momentum_Bin'], prefix='Momentum')
        for m in momentum_bins:
            col = f'Momentum_{m}'
            if col not in input_encoded.columns:
                input_encoded[col] = 0

        # 4. Interaction features
        input_encoded['Possession_x_Shots'] = input_encoded['Possession_Pre_Event'] * input_encoded['Shots_Pre_Event']
        input_encoded['Pressure_x_Fatigue'] = input_encoded['Pressure_Index'] * input_encoded['Fatigue_Index']

        # 5. Drop unnecessary columns
        input_encoded = input_encoded.drop(['Time_of_Event'], axis=1)

        # 6. Align with training features
        input_encoded = input_encoded.reindex(columns=training_features, fill_value=0)

        # 7. Scale numerical features
        input_encoded[numerical_cols] = scaler.transform(input_encoded[numerical_cols])

        # 8. Predict
        prob = model.predict_proba(input_encoded)[:, 1][0]
        pred = model.predict(input_encoded)[0]

        st.subheader("Prediction Results 🏟️")
        st.markdown(f"**Recovery Probability**: {prob:.1%}")
        st.markdown(f"**Prediction**: {'Recovery Likely ✅' if pred == 1 else 'No Recovery ❌'}")
        st.progress(prob)

# Tab 2: Upload CSV
with tab2:
    st.markdown("Upload a CSV file with match data to predict recovery probabilities for multiple scenarios. 📊")
    uploaded_file = st.file_uploader("Choose a CSV file 📂", type=["csv"])
    if uploaded_file is not None:
        try:
            # Read the uploaded CSV
            df = pd.read_csv(uploaded_file)

            # Expected columns based on football_momentum.csv
            expected_columns = [
                'Event_Type', 'Score_Differential', 'Time_of_Event', 'Home_Away',
                'Possession_Pre_Event', 'Shots_Pre_Event', 'Passes_Completed_Pre_Event',
                'Opponent_Strength', 'Fatigue_Index', 'Crowd_Influence', 'Key_Player_Involved',
                'Tactical_Shift', 'Momentum_Swing', 'Recent_Form', 'Event_Severity',
                'Sub_Impact', 'Pressure_Index'
            ]

            # Check if all required columns are present
            missing_cols = [col for col in expected_columns if col not in df.columns]
            if missing_cols:
                st.error(f"Uploaded CSV is missing columns: {', '.join(missing_cols)}")
            else:
                # Feature engineering on the dataset
                input_encoded = df[expected_columns].copy()

                # 1. One-hot encode Event_Type
                input_encoded = pd.get_dummies(input_encoded, columns=['Event_Type'], prefix='Event')
                for et in event_types:
                    col = f'Event_{et}'
                    if col not in input_encoded.columns:
                        input_encoded[col] = 0

                # 2. Bin Time_of_Event into Game_Stage
                input_encoded['Game_Stage'] = pd.cut(
                    input_encoded['Time_of_Event'],
                    bins=[0, 15, 30, 45, 60, 75, 90, 100],
                    labels=stages,
                    include_lowest=True
                )
                input_encoded = pd.get_dummies(input_encoded, columns=['Game_Stage'], prefix='Stage')
                for s in stages:
                    col = f'Stage_{s}'
                    if col not in input_encoded.columns:
                        input_encoded[col] = 0

                # 3. Create Momentum_Bin
                input_encoded['Momentum_Bin'] = pd.cut(
                    input_encoded['Momentum_Swing'],
                    bins=[-float('inf'), -10, 0, 10, float('inf')],
                    labels=momentum_bins,
                    include_lowest=True
                )
                input_encoded = pd.get_dummies(input_encoded, columns=['Momentum_Bin'], prefix='Momentum')
                for m in momentum_bins:
                    col = f'Momentum_{m}'
                    if col not in input_encoded.columns:
                        input_encoded[col] = 0

                # 4. Interaction features
                input_encoded['Possession_x_Shots'] = input_encoded['Possession_Pre_Event'] * input_encoded[
                    'Shots_Pre_Event']
                input_encoded['Pressure_x_Fatigue'] = input_encoded['Pressure_Index'] * input_encoded['Fatigue_Index']

                # 5. Drop unnecessary columns
                input_encoded = input_encoded.drop(['Time_of_Event'], axis=1)

                # 6. Align with training features
                input_encoded = input_encoded.reindex(columns=training_features, fill_value=0)

                # 7. Scale numerical features
                input_encoded[numerical_cols] = scaler.transform(input_encoded[numerical_cols])

                # 8. Predict for all rows
                probs = model.predict_proba(input_encoded)[:, 1]
                preds = model.predict(input_encoded)

                # Add predictions to the original dataframe
                df['Predicted_Recovery_Probability'] = probs
                df['Predicted_Recovery'] = ['Recovery Likely ✅' if pred == 1 else 'No Recovery ❌' for pred in preds]

                st.subheader("Prediction Results for Uploaded Data 📊")
                st.markdown("Predictions have been added to the dataset. You can download the results below.")
                st.dataframe(df)

                # Provide download button for the results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Predictions 📥",
                    data=csv,
                    file_name="predictions.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Error processing the uploaded file: {str(e)}")
    else:
        st.info("Please upload a CSV file to get predictions. 📂")

# Footer
st.markdown("""
    <div class="footer">
        ⚽ Developed by Pavan Krishna | Football Momentum Predictor | 2025 ⚽
    </div>
""", unsafe_allow_html=True)