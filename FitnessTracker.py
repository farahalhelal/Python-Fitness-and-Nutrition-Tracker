import matplotlib.pyplot as plt 
import numpy as np 
import xml.etree.ElementTree as ET
import csv
from datetime import datetime




WORKOUT_CATEGORIES = ["Cardio", "Strength", "Flexibility"]
MEAL_CATEGORIES = ["Breakfast", "Lunch", "Dinner", "Snack"]



profiles = {}



def create_load_profile(username):
    """ Load existing profile or create a new profile if does not exist """

    if username not in profiles:
        
        profiles[username] = {
            'profile': {
                'weight': None,
                'height': None,
                'fitness_goal': None
            },
            'entries': []  
        }

        print(f"\n -> Profile does not exist... Creating new profile for user: {username}")
    else:
        print(f"\n -> Profile loaded for user: {username}")
    return username


def change_profile(username):
    create_load_profile(username)

def view_profile(username):
    """Allows the user to view his profile"""
    print(
        f"Your current profile stats:\nWeight: {profiles[username]['profile']['height']}\nHeight: {profiles[username]['profile']['height']}\nGoals: {profiles[username]['profile']['fitness_goal']}\n"
    )


def edit_profile(username):
    """Allows the user to edit his profile"""

    profile_data = profiles[username]['profile']

    print(
        f"Your current profile stats:\nWeight: {profiles[username]['profile']['height']}\nHeight: {profiles[username]['profile']['height']}\nGoals: {profiles[username]['profile']['fitness_goal']}\n"
    )

    weight = input("Enter new weight: ")
    height = input("Enter new height: ")
    fitness_goal = input("Enter new fitness goal: ")

    
    if weight:
        profile_data['weight'] = weight
    if height:
        profile_data['height'] = height
    if fitness_goal:
        profile_data['fitness_goal'] = fitness_goal

    print("Profile updated successfully.")




def add_entry(username):
    """Allows user to add a new entry"""

    entry_type = input("Enter type ('Workout' or 'Meal'): ").strip().title()
    if entry_type not in ["Workout", "Meal"]:
        print("Invalid type. Entry must be either 'Workout' or 'Meal'.")
        return


    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    try:
        entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return


    if entry_type == "Workout":
        print("Predefined workout categories: ", WORKOUT_CATEGORIES)
        category = input("Choose category (or type a new one): ").strip().title()
        duration_quantity = input("Enter duration for workout: ").strip()

    else:
        print("Predefined meal categories: ", MEAL_CATEGORIES)
        category = input("Cjoose category (or type a new one): ").strip().title()
        duration_quantity = input("Enter quantity for meal: ").strip()

    try:
        calories = int(
            input("Enter calories (burned for workout or consumed for meal): "
                ).strip())
    except ValueError:
        print("Invalid calories value. Please enter a number.")
        return


    entry = {
        'type': entry_type,
        'category': category,
        'duration_quantity': duration_quantity,
        'calories': calories,
        'date': entry_date
    }

    profiles[username]['entries'].append(entry)
    print(f"\n -> {entry_type} entry added successfully.")

def view_entries(username):
    entries = profiles[username]['entries']
    if not entries:
        print("No entries recorded yet.")
    else:
        i = 1
        for entry in entries:
            print(f"{i}.  [{entry['date']}] \t{entry['type']}\t - {entry['category']}, \t\tDuration/Quantity: {entry['duration_quantity']},\t Calories: {entry['calories']}")
            i += 1


def import_csv_entries(username):
        """Import entries from a CSV file."""

        file_path = input("Enter the CSV file path: ").strip()
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                count = 0
                for row in reader:
                    try:
                        entry_type = row['type'].strip().title()
                        category = row['category'].strip().title()
                        duration_quantity = row['duration_quantity'].strip()
                        calories = int(row['calories'])
                        entry_date = datetime.strptime(row['date'].strip(), "%Y-%m-%d").date()
                        entry = {
                            'type': entry_type,
                            'category': category,
                            'duration_quantity': duration_quantity,
                            'calories': calories,
                            'date': entry_date
                        }
                        profiles[username]['entries'].append(entry)
                        count += 1
                    except Exception as e:
                        print("Error processing row:", row, "\n", e)
                print(f"Imported {count} entries from CSV.")
        except FileNotFoundError:
            print("CSV file not found.")

def import_xml_entries(username):
    """Import entries from an XML file."""
    print("\n--- Import XML Entries ---")
    file_path = input("Enter the XML file path: ").strip()
    try:
        tree = ET.parse(file_path) 
        root = tree.getroot()
        count = 0
        for entry_elem in root.findall('entry'):
            try:
                entry_type = entry_elem.find('type').text.strip().title()
                category = entry_elem.find('category').text.strip().title()
                duration_quantity = entry_elem.find('duration_quantity').text.strip()
                calories = int(entry_elem.find('calories').text.strip())
                date_str = entry_elem.find('date').text.strip()
                entry_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                entry = {
                    'type': entry_type,
                    'category': category,
                    'duration_quantity': duration_quantity,
                    'calories': calories,
                    'date': entry_date
                }
                profiles[username]['entries'].append(entry)
                count += 1
            except Exception as e:
                print("Error processing an XML entry:", e)
        print(f"Imported {count} entries from XML.")
    except FileNotFoundError:
        print("XML file not found.")
    except ET.ParseError: 
        print("Error parsing XML file.")




def visualize_meal_distribution(username):
    """Visualize the distribution of meal categories for a specified month."""
    print("\n--- Visualize Meal Distribution ---")
    year = input("Enter year (YYYY): ").strip()
    month = input("Enter month (MM): ").strip()
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        print("Invalid year or month.")
        return

    from collections import defaultdict
    category_counts = defaultdict(int)
    for entry in profiles[username]['entries']:
        if entry['type'] == "Meal" and entry['date'].year == year and entry['date'].month == month:
            category_counts[entry['category']] += 1

    if not category_counts:
        print("No meal entries found for the specified month.")
        return

    categories = list(category_counts.keys())
    counts = list(category_counts.values())

    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts, color='skyblue')
    plt.title(f"Meal Category Distribution for {year}-{month:02d}")
    plt.xlabel("Meal Category")
    plt.ylabel("Count")
    plt.show()




def visualize_calories_comparison(username):
    """Visualize calories consumed vs. calories burned on a daily basis."""
    print("\n--- Visualize Calories Comparison ---")
    daily_stats = {}
    for entry in profiles[username]['entries']:
        entry_date = entry['date']
        if entry_date not in daily_stats:
            daily_stats[entry_date] = {'consumed': 0, 'burned': 0}
        if entry['type'] == "Meal":
            daily_stats[entry_date]['consumed'] += entry['calories']
        elif entry['type'] == "Workout":
            daily_stats[entry_date]['burned'] += entry['calories']

    if not daily_stats:
        print("No entries to visualize.")
        return

    sorted_dates = sorted(daily_stats.keys())
    dates_str = [d.strftime("%Y-%m-%d") for d in sorted_dates]
    consumed = [daily_stats[d]['consumed'] for d in sorted_dates]
    burned = [daily_stats[d]['burned'] for d in sorted_dates]

    x = range(len(sorted_dates))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x, consumed, width, label='Calories Consumed', color='green')
    plt.bar([i + width for i in x], burned, width, label='Calories Burned', color='red')
    plt.xlabel("Date")
    plt.ylabel("Calories")
    plt.title("Daily Calories: Consumed vs. Burned")
    plt.xticks([i + width/2 for i in x], dates_str, rotation=90)
    plt.legend()
    plt.tight_layout()
    plt.show()
