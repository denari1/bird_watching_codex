"""
This program allows users to enter and save bird watching data to a CSV file. Users can also load and view saved entries.
"""

__author__ = "Tristan Boscia"

import csv
import os


def print_heading():
    """
    Print the program heading.
    """
    title = "Bird Watching Codex"  # Title of the program
    border_length = len(title) + 4  # Calculate the length of the border
    border = '*' * border_length  # Create the border
    print(border)
    print(f"* {title} *")
    print(border)


def enter_bird_watching_data():
    """
    Prompt the user to enter bird watching data and return it as a dictionary.
    """
    entry = {
        'Entry Name': input("Enter a name for this entry: "),
        'Species': input("Enter bird species: "),
        'Number of Birds': None,
        'Location': input("Enter location: "),
        'Date and Time': None
    }
    
    while entry['Number of Birds'] is None:
        try:
            entry['Number of Birds'] = int(input("Enter the number of birds observed: "))  # Convert input to int
        except ValueError:
            print("Invalid input for number of birds. Please enter an integer.")  # Error message
    
    while entry['Date and Time'] is None:
        try:
            entry['Date and Time'] = input("Enter the date and time of observation: ")  # Input for date and time
            # Add additional validation for date and time if needed
            if not entry['Date and Time']:
                raise ValueError
        except ValueError:
            print("Invalid input for date and time. Please enter a valid date and time.")  # Error message
    
    confirm_save = input("Press Enter to save entry")  # Confirmation to save the entry
    while confirm_save != "":
        confirm_save = input("You need to press Enter to save.")
    
    return entry


def save_data_to_csv(file_path, data):
    """
    Save bird watching data to a CSV file.
    """
    try:
        file_exists = os.path.isfile(file_path)  # Check if the file already exists
        fieldnames = ['Entry Name', 'Species','Number of Birds', 'Location', 'Date and Time'] # Define field names
        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # Create a DictWriter object
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except IOError:
        print("Unable to write to file.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def load_data_from_csv(file_path):
    """
    Load bird watching data from a CSV file.
    """
    data = [] # Initialize an empty list to store the data
    if not os.path.isfile(file_path):
        return data

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Ensure each row has all required fields
                if all(field in row and row[field] is not None for field in ['Entry Name', 'Species', 'Number of Birds', 'Location', 'Date and Time']):
                    data.append(row)
    except IOError:
        print("Unable to read file.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return data


def display_data(entry):
    """
    Display the bird watching data entry.
    """
    print("-" * 40)
    for key, value in entry.items():
        print(f"{key}: {value}")
    print("-" * 40)


def select_entry(data):
    """
    Select an entry from the list of bird watching data.
    """
    # Check if there are any entries
    if not data:
        print("No entries found.")
        return None

    valid_entries = [entry for entry in data if 'Entry Name' in entry and entry['Entry Name']] # Filter out entries without a name

    # Check if there are any valid entries
    if not valid_entries:
        print("No named entries found.")
        return None

    print("\nSaved Entries:")
    for i, entry in enumerate(valid_entries):
        print(f"{i + 1}. {entry['Entry Name']}")

    # Prompt the user to select an entry
    while True:
        choice = input("Select an entry by number or type 'back' to return to the main menu: ")
        if choice.lower() == 'back':
            return None
        try:
            choice = int(choice) - 1
            if 0 <= choice < len(valid_entries):
                return valid_entries[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'back'.")


def delete_entry(file_path):
    """
    Allow the user to delete an entry from the CSV file.
    """
    data = load_data_from_csv(file_path) # Load data from the CSV file
    if not data:
        print("No entries found.")
        return

    entry = select_entry(data) # Select an entry to delete
    if not entry:
        return

    data.remove(entry)
    fieldnames = ['Entry Name', 'Species', 'Number of Birds', 'Location', 'Date and Time'] # Define field names
    
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow(entry)
        print("Entry deleted")
    except IOError:
        print("Unable to write to file")
    except Exception as e:
        print(f"Unexpected error: {e}")


def main():
    print_heading()
    file_path = 'bird_watching_data.csv'
    running = True
    
    while running:
        print("\nMain Menu")
        print("1. New Entry")
        print("2. Load Entry")
        print("3. Delete Entry")
        print("4. Exit")
        choice = input(">  ")
        if choice == '1':
            try:
                data = enter_bird_watching_data()
                if data:
                    save_data_to_csv(file_path, data)
            except Exception as e:
                print(f"An error occurred while entering or saving data: {e}")
        elif choice == '2':
            try:
                all_data = load_data_from_csv(file_path)
                if not all_data:
                    print("No entries found.")
                else:
                    entry = select_entry(all_data)
                    if entry:
                        display_data(entry)
            except Exception as e:
                print(f"An error occurred while loading data: {e}")
        elif choice == '3':
            try:
                delete_entry(file_path)
            except Exception as e:
                print(f"An error occurred while deleting the entry: {e}")
        elif choice == '4':
            print("Exiting program.")
            running = False
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
