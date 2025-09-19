import pandas as pd
import numpy as np
import pickle
import time

def get_signal_decision(predicted_scores):
    """
    Takes a dictionary of predicted scores for each lane and returns the signal state.
    """
    lanes = ["L1", "L2", "L3", "L4"]
    
    if not predicted_scores:
        return {lane: False for lane in lanes}
        
    highest_congestion_lane = max(predicted_scores, key=predicted_scores.get)
    
    signal_state = {lane: False for lane in lanes}
    signal_state[highest_congestion_lane] = True
    
    return signal_state


def run_controller():
    """
    Main function to load the model and run the traffic control logic.
    """
    # --- 1. EDIT THESE FILENAMES TO MATCH YOURS ---
    MODEL_FILE = "traffic_model.pkl"
    LIVE_DATA_FILE = "X_test_data.csv"
    # ----------------------------------------------------

    try:
        with open(MODEL_FILE, "rb") as f:
            model = pickle.load(f)
            
        live_data_df = pd.read_csv(LIVE_DATA_FILE)
        live_data_df = pd.read_csv(LIVE_DATA_FILE, index_col='DateTime', parse_dates=True)
        print("Live data file loaded.")

        expected_features = model.feature_name_
        print(f"Model expects these {len(expected_features)} features: {expected_features}")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find a required file. Please check your filenames.")
        print(e)
        return

    print("--- Starting Traffic Control Simulation ---")
    
    unique_timestamps = live_data_df.index.unique()

    for ts in unique_timestamps:
        current_data_snapshot = live_data_df.loc[ts]
        predicted_scores = {}
        
        for i in range(1, 5):
            lane = f"L{i}"
            junction_id = i
            
            try:
                # Find the data for the specific junction at this timestamp
                if isinstance(current_data_snapshot, pd.Series):
                    if current_data_snapshot['Junction'] == junction_id:
                        lane_data = current_data_snapshot.to_frame().T
                    else:
                        continue
                else:
                    lane_data = current_data_snapshot[current_data_snapshot['Junction'] == junction_id]
                
                if not lane_data.empty:
                    # Predict using the single row of features
                    prediction = model.predict(lane_data)[0]
                    predicted_scores[lane] = prediction
                
            except (KeyError, TypeError):
                continue

        signal_decision = get_signal_decision(predicted_scores)

        # This is the final output dictionary for each timestamp
        print(f"Timestamp: {ts}, Decision: {signal_decision}")

        time.sleep(2)

    print("--- Simulation Finished ---")

if __name__ == "__main__":
    run_controller()