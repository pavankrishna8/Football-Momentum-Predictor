# Football-Momentum-Predictor

### Overview

The Football Momentum Predictor is a Streamlit-based web application designed to predict a football team's likelihood of recovering from key match events based on real-time match scenarios. By leveraging a logistic regression model trained on a comprehensive dataset (football_momentum.csv), the application provides actionable insights for coaches, analysts, and fans. It evaluates critical match events—such as goals scored, cards issued, or substitutions—and estimates the probability of a team regaining momentum and recovering from setbacks.

### The application offers two modes:

Manual Input: Allows users to input specific match scenarios to predict recovery probability for a single event.
Batch Prediction: Enables users to upload a CSV file with multiple match scenarios to generate predictions for an entire dataset.

With a football-themed interface, the application is intuitive, visually appealing, and tailored for football stakeholders seeking data-driven insights to inform tactical decisions or enhance match analysis.

### Features:
⚽ Recovery Probability Prediction: Predicts the likelihood of a team recovering from events like goals conceded, red cards, or missed chances.
📋 Manual Input Mode: Users can input match details (e.g., event type, score differential, possession, time of event) to get real-time predictions.
📂 Batch Prediction Mode: Upload a CSV file to predict recovery probabilities for multiple match scenarios, with results downloadable as a CSV.
🏟️ Football-Themed Interface: A sleek, football-inspired design with a green-and-white color scheme, progress bars, and intuitive sliders.
🔍 Feature Engineering: Incorporates advanced feature engineering, including one-hot encoding of event types, time-based game stages, momentum bins, and interaction features like possession-shots and pressure-fatigue.
📊 Scalable Predictions: Uses a pre-trained logistic regression model, standardized with a scaler, to ensure robust predictions across varied inputs.
📥 Downloadable Results: Batch predictions can be downloaded as a CSV file for further analysis.

### Dataset Description:

The application is built on the football_momentum.csv dataset, which contains detailed records of football match events and their impact on team momentum. Each row represents a match event with the following key columns:

Event_Type: Type of event (e.g., Goal_Scored, Goal_Conceded, Yellow_Card_Own, Red_Card_Opp, Sub_In).
Score_Differential: The goal difference at the time of the event (e.g., -3 to +3).
Time_of_Event: The minute of the match when the event occurred (0 to 95).
Home_Away: Whether the team is playing at home (1) or away (0).
Possession_Pre_Event: Team's possession percentage before the event (20% to 80%).
Shots_Pre_Event: Number of shots taken before the event (0 to 10).
Passes_Completed_Pre_Event: Number of passes completed before the event (30 to 100).
Opponent_Strength: Strength of the opposing team (0.4 to 1.0).
Fatigue_Index: Team's fatigue level (0.3 to 0.9).
Crowd_Influence: Impact of the crowd (0.2 to 0.8).
Key_Player_Involved: Whether a key player was involved (0 or 1).
Tactical_Shift: Whether a tactical change occurred (0 or 1).
Momentum_Swing: The momentum shift caused by the event (-30 to +30).
Recent_Form: Team's recent performance (0.3 to 0.9).
Event_Severity: Severity of the event (0.2 to 1.0).
Sub_Impact: Impact of substitutions (0.0 to 0.7).
Pressure_Index: Level of pressure on the team (0.3 to 1.0).
Recovery_Probability: Target variable indicating the actual recovery probability (used for training).

A synthteic dataset with these features was generated and used to train a logistic regression model that predicts the binary outcome of recovery (Recovery Likely or No Recovery) and the associated probability.


### The Football Momentum Predictor provides valuable insights for various stakeholders in the football ecosystem:

Coaches and Managers:
Make informed tactical decisions by understanding how events like substitutions or yellow cards affect recovery chances.
Adjust strategies in real-time based on predicted momentum shifts (e.g., when to push for an attack or reinforce defense).
Evaluate the impact of substitutions and their timing to maximize team performance.

Analysts and Scouts:
Analyze match data to identify patterns in momentum swings and recovery probabilities across different scenarios.
Assess the impact of opponent strength, fatigue, and crowd influence on team performance.
Generate reports for pre-match planning or post-match analysis using batch predictions.

Fans and Commentators:
Gain deeper insights into critical match moments and their likely outcomes.
Enhance engagement by understanding the data-driven likelihood of a comeback after a setback.
Use the tool to simulate hypothetical scenarios and discuss potential match outcomes.

### Usage:

Manual Input:
Navigate to the "Manual Input" tab.
Select the event type (e.g., Goal Scored) and input match details using sliders (e.g., score differential, possession, time of event).
Submit the form to view the recovery probability and prediction (e.g., "Recovery Likely ✅" with a 75% probability).

Batch Prediction:
Navigate to the "Upload CSV" tab.
Upload a CSV file with match data in the format of football_momentum.csv.
View the predictions added to the dataset as new columns (Predicted_Recovery_Probability and Predicted_Recovery).
Download the results as a CSV file for further analysis.

### Technical Details:
Model: Logistic regression trained on the football_momentum.csv dataset to predict binary recovery outcomes.

Feature Engineering:
One-Hot Encoding: Event types (e.g., Event_Goal_Scored) and categorical bins (e.g., Stage_0-15, Momentum_Positive).
Time Binning: Converts Time_of_Event into game stages (e.g., 0-15, 15-30).
Momentum Binning: Categor Categorizes Momentum_Swing into bins (e.g., Strong_Negative, Positive).
Interaction Features: Includes Possession_x_Shots and Pressure_x_Fatigue to capture combined effects.
Preprocessing: Numerical features are standardized using a pre-trained scaler (scaler.pkl).
Frontend: Streamlit with custom CSS for a football-themed interface, including green buttons, progress bars, and a fixed footer.

