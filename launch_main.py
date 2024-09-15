# `.\launch_main.py` - This script needs to run standalone until importing `.\scripts\engine.py`

# Imports
import os
from scripts.config import Config

# Initialize the Config object
config = Config()

def load_settings():
    config.load_config()

def save_settings():
    config.save_config()

def print_separator():
    print("=" * 120)

def display_menu(menu_title, settings_group):
    print_separator()
    print(" " * 39 + menu_title)
    print("-" * 120)
    for idx, (key, value) in enumerate(settings_group.items(), 1):
        print(f" {idx}. {key},".ljust(30) + f"({value})".rjust(50))
    print_separator()
    return clean_input("Selection; Options = 1-#, Back To Main = B: ").strip().upper()

def select_model_file(model_path):
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

def handle_llm_model_settings():
    while True:
        choice = display_menu("Auto-CPP-Local - LLM Model Settings", config.llm_model_settings)
        
        if choice == 'B':
            break
        elif choice == '1':  # model_path option
            new_model_path = clean_input("Enter new model path: ").strip()
            config.llm_model_settings['model_path'] = new_model_path
            save_settings()
        elif choice == '2':  # chat_llm_model option
            model_path = config.llm_model_settings['model_path']
            if os.path.isdir(model_path):
                selected_model = select_model_file(model_path)
                if selected_model:
                    config.llm_model_settings['chat_llm_model'] = selected_model
                    save_settings()
            else:
                print(f"Invalid model path: {model_path}")
        elif choice == '3':  # code_llm_model option
            model_path = config.llm_model_settings['model_path']
            if os.path.isdir(model_path):
                selected_model = select_model_file(model_path)
                if selected_model:
                    config.llm_model_settings['code_llm_model'] = selected_model
                    save_settings()
            else:
                print(f"Invalid model path: {model_path}")
        else:
            print("Invalid choice. Please select a valid option.")

def handle_optional_modes():
    while True:
        choice = display_menu("Auto-CPP-Local - Optional Modes", config.program_settings)
        
        if choice == 'B':
            break
        elif choice == '1':  # continuous_mode
            config.program_settings['continuous_mode'] = not config.program_settings['continuous_mode']
            save_settings()
        elif choice == '2':  # debug_mode
            config.program_settings['debug_mode'] = not config.program_settings['debug_mode']
            save_settings()
        elif choice == '3':  # speak_mode
            config.system_settings['speak_mode'] = not config.system_settings['speak_mode']
            save_settings()
        else:
            print("Invalid choice. Please select a valid option.")

def handle_submenu_selection(settings_group_name):
    if settings_group_name == 'llm_model_settings':
        handle_llm_model_settings()
    elif settings_group_name == 'optional_modes':
        handle_optional_modes()
    else:
        while True:
            settings_group = getattr(config, settings_group_name, {})
            choice = display_menu(f"Auto-CPP-Local - {settings_group_name.capitalize()} Settings", settings_group)
            if choice == 'B':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(settings_group):
                selected_key = list(settings_group.keys())[int(choice) - 1]
                new_value = clean_input(f"Enter new value for {selected_key}: ").strip()
                settings_group[selected_key] = new_value
                save_settings()  # Save after each change
            else:
                print("Invalid choice. Please select a valid option.")

def main_menu():
    load_settings()
    
    while True:
        choice = display_menu("Auto-CPP-Local - Engine Window", {
            "1": "Program Settings",
            "2": "Session Settings",
            "3": "System Settings",
            "4": "LLM Model Settings",
            "5": "Browsing Settings",
            "6": "Optional Modes"
        })
        if choice in ['1', '2', '3', '4', '5', '6']:
            handle_submenu_selection(f"{choice}_settings")
        elif choice == 'B':
            begin_autocpp_lite()
            break
        elif choice == 'X':
            exit_and_save()
            break
        else:
            print("Invalid choice. Please select a valid option.")

def begin_autocpp_lite():
    print("Importing .\scripts\engine.py")
    from scripts.main import main
    main()
    print(".\scripts\main.py Finished.")

def exit_and_save():
    print("Exiting and Saving...")
    save_settings()
    print("Settings Saved To Yaml.")

# Import clean_input here to ensure it is available when needed
from scripts.utilities_one import clean_input

if __name__ == "__main__":
    main_menu()