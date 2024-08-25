# Script: .\window_1.py

import subprocess
from scripts import interface, model as agent_module, utility
import time
import argparse
import sys
import os
import ctypes

# Set window title for Windows
ctypes.windll.kernel32.SetConsoleTitleW("Chat-VulkanLlama-Window1")

# Handle 'reset' input
def handle_reset():
    utility.reset_keys_to_empty()
    config_data = utility.read_yaml()
    human_name, agent_name, agent_role, scenario_location = (config_data.get('human_name'), config_data.get('agent_name'), 
                                                            config_data.get('agent_role'), config_data.get('scenario_location'))
    agent_emotion, session_history = config_data.get('agent_emotion'), config_data.get('session_history')
    yaml_data =
        'agent_name': agent_name,
        'agent_role': agent_role,
        'scenario_location': scenario_location,
        'agent_emotion': agent_emotion,
        'session_history': session_history,
        'human_input': "Empty",
        'agent_output_1': "Empty",
        'agent_output_2': "Empty",
        'agent_output_3': "Empty",
        'sound_event': "None",
        'context_length': "Empty",
        'syntax_type': "Empty",
        'model_path': "Empty"
    }
    for key, value in yaml_data.items():
        utility.write_to_yaml(key, value)

# Handle 'quit' input
def handle_quit():
    print("\n Quitting the script. Goodbye!")
    time.sleep(2)
    sys.exit(0)

# Handle 'other' input
def handle_other(user_input):
    global rotation_counter, loaded_models
    data = utility.read_yaml()
    start_time = time.time()
    current_task = 'converse'
    
    agent_type = 'chat' if current_task == 'converse' else 'instruct'

    response_dict = agent_module.prompt_response(current_task, rotation_counter, enable_logging=args.logs, 
                                                 loaded_models=loaded_models, save_to='agent_output_1', agent_type=agent_type)
    
    if rotation_counter == 2:
        emotion_dict = agent_module.prompt_response('emotions', rotation_counter, enable_logging=args.logs, 
                                                    loaded_models=loaded_models, save_to='agent_emotion')
        new_emotion = emotion_dict.get('new_emotion')
        if new_emotion:
            utility.write_to_yaml('agent_emotion', new_emotion)
    
    consolidate_dict = agent_module.prompt_response('consolidate', rotation_counter, enable_logging=args.logs, 
                                                    loaded_models=loaded_models, save_to='session_history')
    new_session_history = consolidate_dict.get('new_session_history')
    if new_session_history:
        utility.write_to_yaml('session_history', new_session_history)
    
    end_time = time.time()
    print(f"\n ...Time taken: {end_time - start_time:.2f} seconds...")
    utility.shift_responses()
    print(" ...Key Display window updated.\n")

# Main function adjustments:
def main(args):
    try:
        optimal_threads = utility.calculate_optimal_threads()
        time.sleep(1)
        utility.reset_keys_to_empty()
        selected_model = interface.display_model_selection()
        if not selected_model:
            print("No Models, Exiting!")
            return

        model_path = selected_model.get('model_path')
        if model_path:
            agent_module.initialize_model(model_path, optimal_threads)
            utility.write_to_yaml('model_path', model_path)

        data = utility.read_yaml()
        rotation_counter = 0
        loaded_models = {}

        while True:
            interface.display_engine()  
            user_input = input(f" Enter your message to {data['agent_name']} or 'reset' to Restart or 'quit' to Exit?:\n").lower()
            if user_input == 'reset':
                handle_reset()
            elif user_input == 'quit':
                handle_quit()
            else:
                utility.write_to_yaml('human_input', user_input)
                handle_other(user_input, rotation_counter, args, loaded_models)
            rotation_counter = (rotation_counter + 1) % 4
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat-VulkanLlama")
    parser.add_argument("--logs", action="store_true", help="Enable logging")
    args = parser.parse_args()
    main()