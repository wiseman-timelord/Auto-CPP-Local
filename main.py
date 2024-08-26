import time
import yaml
from scripts.utilities import clean_input, validate_yaml_file
from scripts.config import Config

# Global variables for settings
config = Config()

# Function to load settings into globals
def load_settings():
    global config
    config.load_config()

# Function to save global settings to YAML
def save_settings():
    config.save_config()

# Function to print a separator line of 120 characters width
def print_separator():
    print("=" * 120)

# Function to display the main menu
def display_main_menu():
    print_separator()
    print(" " * 39 + "AutoCPP-Lite")
    print("-" * 120)
    print(" " * 10 + "1. Program Settings")
    print(" " * 10 + "2. Session Settings")
    print(" " * 10 + "3. System Settings")
    print(" " * 10 + "4. LLM Model Settings")
    print(" " * 10 + "5. Browsing Settings")
    print_separator()
    choice = clean_input("Selection; Menu Options = 1-5, Begin AutoCPP-Lite = B, Exit and Save = X: ").strip().upper()
    return choice

# Function to display submenu for each setting
def display_submenu(settings_group):
    print_separator()
    print(" " * 39 + "AutoCPP-Lite")
    print("-" * 120)
    for idx, (key, value) in enumerate(settings_group.items(), 1):
        print(f" {idx}. {key},".ljust(30) + f"({value})".rjust(50))
    print_separator()
    choice = clean_input("Selection; Options = 1-#, Back To Main = B: ").strip().upper()
    return choice

# Function to handle user's selection in submenus
def handle_submenu_selection(settings_group):
    while True:
        choice = display_submenu(settings_group)
        if choice == 'B':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(settings_group):
            selected_key = list(settings_group.keys())[int(choice) - 1]
            new_value = clean_input(f"Enter new value for {selected_key}: ").strip()
            settings_group[selected_key] = new_value
            save_settings()  # Save after each change
        else:
            print("Invalid choice. Please select a valid option.")

# Main entry point
def main_menu():
    load_settings()
    
    while True:
        choice = display_main_menu()
        if choice == '1':
            handle_submenu_selection(vars(config).get('program_settings', {}))
        elif choice == '2':
            handle_submenu_selection(vars(config).get('session_settings', {}))
        elif choice == '3':
            handle_submenu_selection(vars(config).get('system_settings', {}))
        elif choice == '4':
            handle_submenu_selection(vars(config).get('llm_model_settings', {}))
        elif choice == '5':
            handle_submenu_selection(vars(config).get('browsing_settings', {}))
        elif choice == 'B':
            begin_autocpp_lite()
            break
        elif choice == 'X':
            exit_and_save()
            break
        else:
            print("Invalid choice. Please select a valid option.")

def begin_autocpp_lite():
    print("Importing .\scripts\main.py")
    time.sleep(2)
    from scripts.main import main
    main()
    print(".\scripts\main.py Finished.")
    time.sleep(2)
    print("Exiting .\main.py")
    time.sleep(5)

def exit_and_save():
    print("Exiting and Saving...")
    save_settings()
    print("Settings Saved To Yaml.")
    time.sleep(2)
    print("Exiting Configurator")
    time.sleep(5)

if __name__ == "__main__":
    main_menu()
