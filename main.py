import time
import yaml
import os
from typing import Dict, Any
from scripts.utilities import clean_input, validate_yaml_file
from scripts.config import Config

# Constants
MAIN_MENU_OPTIONS = {
    '1': 'program_settings',
    '2': 'session_settings',
    '3': 'system_settings',
    '4': 'llm_model_settings',
    '5': 'browsing_settings'
}

# Global variables for settings
config = Config()

def load_settings() -> None:
    """Load settings into globals."""
    global config
    config.load_config()

def save_settings() -> None:
    """Save global settings to YAML."""
    config.save_config()

def print_separator() -> None:
    """Print a separator line of 120 characters width."""
    print("=" * 120)

def display_main_menu() -> str:
    """Display the main menu and return user's choice."""
    print_separator()
    print(" " * 39 + "AutoCPP-Lite")
    print("-" * 120)
    for number, setting in MAIN_MENU_OPTIONS.items():
        print(f" {number}. {setting.replace('_', ' ').title()}")
    print_separator()
    return clean_input("Selection; Menu Options = 1-5, Begin AutoCPP-Lite = B, Exit and Save = X: ").strip().upper()

def display_submenu(settings_group: Dict[str, Any]) -> str:
    """Display submenu for each setting group and return user's choice."""
    print_separator()
    print(" " * 39 + "AutoCPP-Lite")
    print("-" * 120)
    for idx, (key, value) in enumerate(settings_group.items(), 1):
        print(f" {idx}. {key},".ljust(30) + f"({value})".rjust(50))
    print_separator()
    return clean_input("Selection; Options = 1-#, Back To Main = B: ").strip().upper()

def select_model_file(model_path: str) -> str:
    """Display available model files and let the user select one."""
    gguf_files = [f for f in os.listdir(model_path) if f.lower().endswith('.gguf')]
    if not gguf_files:
        print(f"No .gguf files found in directory: {model_path}")
        return ""

    print_separator()
    print(" " * 39 + "Select Model File")
    print("-" * 120)
    for idx, model_file in enumerate(gguf_files, 1):
        print(f" {idx}. {model_file}")
    print_separator()
    model_choice = clean_input("Selection; Model Options = 1-#: ").strip()
    
    if model_choice.isdigit() and 1 <= int(model_choice) <= len(gguf_files):
        return os.path.join(model_path, gguf_files[int(model_choice) - 1])
    else:
        print("Invalid selection. Please choose a valid model number.")
        return ""

def handle_llm_model_settings() -> None:
    """Handle LLM Model Settings submenu."""
    while True:
        choice = display_submenu(config.llm_model_settings)
        
        if choice == 'B':
            break
        elif choice == '1':  # model_path option
            new_model_path = clean_input("Enter new model path: ").strip()
            config.llm_model_settings['model_path'] = new_model_path
            save_settings()
        elif choice == '2':  # smart_llm_model option
            model_path = config.llm_model_settings['model_path']
            if os.path.isdir(model_path):
                selected_model = select_model_file(model_path)
                if selected_model:
                    config.llm_model_settings['smart_llm_model'] = selected_model
                    save_settings()
            else:
                print(f"Invalid model path: {model_path}")
        else:
            print("Invalid choice. Please select a valid option.")

def handle_submenu_selection(settings_group_name: str) -> None:
    """Handle user's selection in submenus."""
    if settings_group_name == 'llm_model_settings':
        handle_llm_model_settings()
    else:
        while True:
            settings_group = getattr(config, settings_group_name, {})
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

def main_menu() -> None:
    """Main entry point for the configuration menu."""
    load_settings()
    
    while True:
        choice = display_main_menu()
        if choice in MAIN_MENU_OPTIONS:
            handle_submenu_selection(MAIN_MENU_OPTIONS[choice])
        elif choice == 'B':
            begin_autocpp_lite()
            break
        elif choice == 'X':
            exit_and_save()
            break
        else:
            print("Invalid choice. Please select a valid option.")

def begin_autocpp_lite() -> None:
    """Start the AutoCPP-Lite main script."""
    print("Importing .\scripts\main.py")
    time.sleep(2)
    from scripts.main import main
    main()
    print(".\scripts\main.py Finished.")
    time.sleep(2)
    print("Exiting .\main.py")
    time.sleep(5)

def exit_and_save() -> None:
    """Save settings and exit the configurator."""
    print("Exiting and Saving...")
    save_settings()
    print("Settings Saved To Yaml.")
    time.sleep(2)
    print("Exiting Configurator")
    time.sleep(5)

if __name__ == "__main__":
    main_menu()