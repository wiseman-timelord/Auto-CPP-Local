# `.\scripts\gradio.py`

# Imports
import gradio as gr
from scripts.utilities_one import get_memory
from scripts.config import Config

# Initialize memory space
config = Config()
memory_space = get_memory(config)

# Function to update chat with user message
def update_chat(user_message):
    if user_message:
        memory_space.add(f"User: {user_message}")
        # Here you could simulate a response (or handle it from another script)
        memory_space.add("Bot: Response placeholder")
    
    # Return the updated chat history
    return "\n".join(memory_space.get_relevant("chat_history", 10)), ""

# Function to get current project plan
def get_project_plan():
    return memory_space.get_relevant("project_plan", 1)[0]

# Function to get current tasks
def get_current_tasks():
    return memory_space.get_relevant("current_tasks", 1)[0]

# Gradio Layout
def create_gradio_interface():
    with gr.Blocks() as interface:
        with gr.Row():
            # Left side - Two equal vertical sections for Chat interface
            with gr.Column(scale=1):
                with gr.Row():
                    chat_output = gr.Textbox(label="Chat History", interactive=False, lines=10, max_lines=10)
                with gr.Row():
                    user_input = gr.Textbox(label="Enter Message", placeholder="Type here...")
                    send_button = gr.Button("Send")
                
                # When button is clicked, update chat history
                send_button.click(update_chat, inputs=user_input, outputs=[chat_output, user_input])

            # Right side - Two equal vertical sections for Project Plan and Current Tasks
            with gr.Column(scale=1):
                with gr.Row():
                    project_plan = gr.Textbox(value=get_project_plan(), label="Project Plan", interactive=False, lines=10)
                with gr.Row():
                    current_tasks = gr.Textbox(value=get_current_tasks(), label="Current Tasks", interactive=False, lines=10)

    interface.launch(inbrowser=True)  # Launch in the default browser

# Launch the Gradio interface
if __name__ == "__main__":
    create_gradio_interface()