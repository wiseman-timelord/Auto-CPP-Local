import gradio as gr

# Placeholder memory space (for communication between scripts)
memory_space = {
    "chat_history": [],
    "project_plan": "Initial Project Plan",
    "current_tasks": "Task 1\nTask 2\nTask 3"
}

# Function to update chat with user message
def update_chat(user_message):
    if user_message:
        memory_space["chat_history"].append(f"User: {user_message}")
        # Here you could simulate a response (or handle it from another script)
        memory_space["chat_history"].append("Bot: Response placeholder")
    
    # Return the updated chat history
    return "\n".join(memory_space["chat_history"]), ""

# Function to get current project plan
def get_project_plan():
    return memory_space["project_plan"]

# Function to get current tasks
def get_current_tasks():
    return memory_space["current_tasks"]

# Gradio Layout
def create_interface():
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

    return interface

# Launch the Gradio interface
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
