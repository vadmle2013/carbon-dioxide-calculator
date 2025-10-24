# Importing necessary libraries.
import os
import difflib
import pandas as pd
import sys

def carbon_footprint():
    print("Welcome to the Carbon Footprint Calculator")
    print("Answer the following questions to estimate your household's carbon footprint.")
    
    def ask(prompt, valid):
        while True:
            ans = input(prompt).strip().lower()
            if ans in valid:
                return ans
            print(f" Invalid choice. Please enter one of: {', '.join(sorted(valid))}")

    # Question 1
    print("\n1. How would you describe your household's overall energy consumption?")
    print(" a) Low (I'm very careful)")
    print(" b) Average")
    print(" c) High (I leave things on)")
    question1 = ask("Choose (a/b/c): ", {'a', 'b', 'c'})

    # Question 2
    print("\n2. What type of building do you live in?")
    print(" a) Apartment complex")
    print(" b) House in an urban area")
    print(" c) House in a rural place")
    question2 = ask("Choose (a/b/c): ", {'a', 'b', 'c'})

    # Question 3
    print("\n3. What is your primary source of heating?")
    print(" a) No central heat")
    print(" b) Natural Gas")
    print(" c) Heating Oil/Propane")
    print(" d) Electricity")
    question3 = ask("Choose (a/b/c/d): ", {'a', 'b', 'c', 'd'})

    # Question 4
    print("\n4. Do you actively buy green energy or use solar power?")
    print(" a) Yes, fully")
    print(" b) Partially")
    print(" c) No")
    question4 = ask("Choose (a/b/c): ", {'a', 'b', 'c'})

    # Scoring system
    score = 0
    # Question1 scoring
    if question1 == 'a': 
        score += 1
    elif question1 == 'b': 
        score += 3
    else:  # question 1 == 'c'
        score += 5

    # Question2 scoring
    if question2 == 'a': 
        score += 2
    elif question2 == 'b': 
        score += 3
    else:  # question 2 == 'c'
        score += 4

    # Question3 scoring
    if question3 == 'a': 
        score += 1
    elif question3 == 'b': 
        score += 3
    elif question3 == 'c': 
        score += 4
    else:  # question 3 == 'd': 
        score += 5

    # Question4 scoring
    if question4 == 'a': 
        score += 1
    elif question4 == 'b': 
        score += 3
    else:  # question 4 == 'c': 
        score += 5

    return score

# Load country CSV once (used for validation)
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "country.csv")

try:
    df = pd.read_csv(file_path)
    preferred = ["country", "Country"]
    chosen_col = None
    for col in preferred:
        if col in df.columns:
            chosen_col = col
            break
    if chosen_col is None:
        chosen_col = df.columns[0]
    my_list = df[chosen_col].astype(str).tolist()
    # case-insensitive map that preserves original casing
    available_map = {item.strip().lower(): item.strip() for item in my_list}
    available_keys = list(available_map.keys())
except FileNotFoundError:
    print(f"CSV file not found at: {file_path}; proceeding without CSV validation.")
    df = None
    my_list = []
    available_map = {}
    available_keys = []
except Exception as e:
    print("Error reading CSV:", e)
    df = None
    my_list = []
    available_map = {}
    available_keys = []

def get_name():
    while True:
        name = input("What is your name? ").strip()
        if name.replace(" ", "").isalpha():
            return name
        print("Use letters only, no numbers.")

def get_age():
    while True:
        try:
            age = int(input("How old are you? ").strip())
            if 17 <= age <= 99:
                return age
            print("Please enter an age between 17 and 99.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def ask_country_with_validation():
    # This loop will keep asking until a valid country from the list is entered (if CSV loaded),
    # or until the user provides a syntactically valid country when CSV is missing.
    if df is None:
        while True:
            country = input("What country are you from? ").strip()
            cleaned = country.replace(" ", "").replace("-", "")
            if cleaned != "" and cleaned.isalpha():
                return country
            print("Use letters, spaces and hyphens only; no numbers or symbols.")
    else:
        while True:
            country = input("What country are you from? ").strip()
            cleaned = country.replace(" ", "").replace("-", "")
            if cleaned == "":
                print("Please enter a country name.")
                continue
            if not cleaned.isalpha():
                print("Use letters, spaces and hyphens only; no numbers or symbols.")
                continue
            key = country.lower()
            if key in available_map:
                print(f"'{available_map[key]}' is available.")
                return available_map[key]
            print(f"'{country}' is not available.")
            suggestions_keys = difflib.get_close_matches(key, available_keys, n=3, cutoff=0.5)
            if suggestions_keys:
                suggestions = [available_map[k] for k in suggestions_keys]
                print("Did you mean:", ", ".join(suggestions))
            else:
                sample = ", ".join(my_list[:10])
                print("Available examples:", sample + (", ..." if len(my_list) > 10 else ""))

def main():
    while True:
        name = get_name()
        age = get_age()
        print("Now let's see where you're from.")
        country = ask_country_with_validation()

        # Run carbon footprint questionnaire
        score2 = carbon_footprint()
        print("\nCalculating your carbon footprint...")

        if score2 <= 8:
            result = "Low footprint, Great job! You're very eco friendly."
        elif 9 <= score2 <= 14:
            result = "Moderate footprint, You are doing okay, but there is room to improve."
        else:
            result = "High footprint, Try adopting more energy saving habits."

        print(f"\nYour total score: {score2}")
        print(result)

        # Ask whether to try again
        while True:
            retry = input("\nWould you like to try again? (y/n): ").strip().lower()
            if retry in ('y', 'yes'):
                print("\nRestarting...\n")
                break  # outer loop continues -> restart entire process
            if retry in ('n', 'no'):
                print("Goodbye.")
                sys.exit(0)
            print("Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()

