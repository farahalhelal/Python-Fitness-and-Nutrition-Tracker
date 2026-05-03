
import FitnessTracker as fnt

def main():
    print(" \n\n\n\t\t###### Welcome to Fitness and Nutrition Tracker! ###### \n\n\n")
    username = input("Please enter your profile name: ")
    fnt.create_load_profile(username)
    while True:
        print("\n\n ==== Fitness & Nutrition Tracker Main Menu ====")
        print("1. Change profiles")
        print("2. View your profile")
        print("3. Edit your profile")
        print("4. View all entries")
        print("5. Add a new log entry interactively")
        print("6. Import entries from CSV")
        print("7. Import entries from XML")
        print("8. Visualize Meal Distribution")
        print("9. Visualize Calories Consume vs. Calories Burned")

        print("\n\n")
        choice = input("Select an option: ")
        print("\n\n")
        if choice == "1":
            username = input("Please enter profile name: ")
            fnt.change_profile(username)
        elif choice == "2":
            fnt.view_profile(username)
        elif choice == "3":
            fnt.edit_profile(username)
        elif choice == "4":
            fnt.view_entries(username)
        elif choice == "5":
            fnt.add_entry(username)
        elif choice == "6":
            fnt.import_csv_entries(username)
        elif choice == "7":
            fnt.import_xml_entries(username)
        elif choice == "8":
            fnt.visualize_meal_distribution(username)
        elif choice == "9":
            fnt.visualize_calories_comparison(username)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")
           
            



if __name__ == "__main__":
    main()

