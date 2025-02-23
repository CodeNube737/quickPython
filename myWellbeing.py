# myWellBeing.py
# this program does a quick wellness check for the user's mental health. matplotlib needs to be installed.
# 2/22/2025
# By: Mikhail Rego, with the help of AI
############################################################################################################

import matplotlib.pyplot as plt

# Function to ask yes or no questions
def ask_question(question):
    yes_variations = ["yes", "y", "yeah", "yep", "sure", "of course", "yup"]
    no_variations = ["no", "n", "nope", "nah", "not really"]

    while True:
        answer = input(question + " (yes/no): ").strip().lower()
        if answer in yes_variations:
            return True
        elif answer in no_variations:
            return False
        else:
            print("Please answer with 'yes' or 'no' (or their variations).")

# List of well-being questions
questions = [
    "Are you feeling happy today?",
    "Have you been able to sleep well lately?",
    "Do you feel motivated to take on tasks?",
    "Have you been socializing with friends and family?",
    "Do you feel physically healthy?",
]

# Function to check on well-being
def check_well_being():
    print("Hi there! How are you doing today?")
    input("Press Enter to start the well-being check...")

    scores = []
    for question in questions:
        answer = ask_question(question)
        scores.append(1 if answer else 0)
    
    # Calculate the well-being score
    well_being_score = sum(scores) / len(questions)

    # Displaying the mental state
    if well_being_score > 0.8:
        state = "Excellent"
        color = "green"
    elif well_being_score > 0.6:
        state = "Good"
        color = "blue"
    elif well_being_score > 0.4:
        state = "Average"
        color = "yellow"
    else:
        state = "Low"
        color = "red"

    plt.figure(figsize=(6, 4))
    plt.text(0.5, 0.5, f"Mental State: {state}", ha='center', va='center', fontsize=16, color=color)
    plt.axis('off')
    plt.title("Your Current Mental State")
    plt.savefig("mental_state.png")
    plt.show()

    print(f"Based on your answers, your mental state is: {state}")
    print("A graphic explaining your mental state has been saved as 'mental_state.png'.")

if __name__ == "__main__":
    check_well_being()
