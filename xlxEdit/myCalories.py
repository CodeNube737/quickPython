# myCalories.py
# this is actually just to test how easy it is to manipulate speadsheets in python
# this needs pandas installed
#___________________________________________________________________________________

import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Define constants
DAILY_CALORIE_TARGET = 2000
LOW_THRESHOLD = 1800
HIGH_THRESHOLD = 2200

def assess_calories(df):
    feedback_list = []
    explanation_list = []

    for i, row in df.iterrows():
        calories = row["calories"]
        prev_calories = df["calories"].iloc[i-1] if i > 0 else None

        # Determine feedback
        if calories < LOW_THRESHOLD:
            feedback = "Too Low"
            explanation = "Your intake is significantly below the recommended 2000 kcal. Consider adding more nutrient-dense foods like lean proteins, whole grains, and healthy fats."
        elif LOW_THRESHOLD <= calories < DAILY_CALORIE_TARGET:
            feedback = "Slightly Low"
            explanation = "Your intake is slightly below the recommended 2000 kcal. A small increase in portion sizes or adding a healthy snack could help."
        elif DAILY_CALORIE_TARGET <= calories <= HIGH_THRESHOLD:
            feedback = "Good"
            explanation = "Your intake is within a healthy range. Keep maintaining a balanced diet with a mix of macronutrients."
        elif HIGH_THRESHOLD < calories <= HIGH_THRESHOLD + 400:
            feedback = "Slightly High"
            explanation = "Your intake is slightly above the recommended 2000 kcal. Consider moderating portion sizes or reducing high-calorie foods."
        else:
            feedback = "Too High"
            explanation = "Your intake is significantly above the recommended 2000 kcal. Try focusing on portion control and choosing lower-calorie, nutrient-rich foods."

        # Adjust feedback based on previous days
        if prev_calories:
            if abs(calories - prev_calories) > 500:
                feedback = "Inconsistent"
                explanation = "Your intake fluctuates significantly compared to previous days. Consistency helps maintain stable energy levels and metabolism."

        feedback_list.append(feedback)
        explanation_list.append(explanation)

    df["feedback"] = feedback_list
    df["explanation"] = explanation_list
    return df

def select_file():
    """Opens a file dialog to select a CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    return file_path

def process_csv():
    input_file = select_file()
    if not input_file:
        print("No file selected. Exiting.")
        return
    
    output_file = input_file.replace(".csv", "_processed.csv")

    df = pd.read_csv(input_file)
    
    # Ensure correct column names
    if not {"number", "day", "calories"}.issubset(df.columns):
        raise ValueError("Input CSV must contain 'number', 'day', and 'calories' columns.")
    
    df = assess_calories(df)
    df.to_csv(output_file, index=False)
    print(f"Processed file saved as {output_file}")

# Run the script
if __name__ == "__main__":
    process_csv()
