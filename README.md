# Auto-CPP-Local: A Vivid Fork of AutoGPT v1.3
Status: Alpha.

## Recent Updates:
- Resume for of project due to DeepSeek v2.5.
- Overhaul of scripts.
- Logic and Sanity.
- Upgrading and implementing new AI/model processes.

## DESCRIPTION:
- The project `Auto-CPP-Local` is a fork of "AutoGPT v1.3", while current version is `Auto-GPT v5.1`, so purposely went for a streamlined design for less service related code to cut later. `Auto-CPP-Local` is designed to automate project completion through AI, The primary differences include no reliance on online services other than web access through Playwright, launching. Two windows, one for a Gradio WebUI chat interface with chat model and one window for the engine window, and using appropriate relating multi-role prompted local models for AI processing. The fork has be been streamlined and tuned, to windows non-wsl python operation, though enhanced through, Llama.Cpp pre-compiled binaries and 2 DeepSeek v2 model. The image generation is removed, the user should instead provide AutoCPP-Lite with images/music/videos/others they, intend to use with projects via `.\Input` folder. The main goal is to turn AutoGPT into, Text model `AI Manager` and Code model `AI Agents`, and the second goal is GPU Acelleration for both, entry level nVidia and Non-ROCM AMD, users, which is the case due to the pre-compiled binaries. 

### FEATURES:
- Does not use online services other than webaccess typically through playwright library. 
- IS designed to launch 2 windows, one WebUi Gradio Chat Interface, and one as the engine window containing concise printed lines of output such as, actions and confirmations.
- The ai powering the chat will be the chat model `.\Models\DeepSeek-V2-Lite-Chat.Q8_0.gguf` with a context of `8192`, that will additionally, manage the user assigned project, break down goals into tasks, and digest descriptive content (chunked if required), and process smaller descriptive text, and generate descriptive text, and create prompts with instruction for the instruct models, etc.
- To carry out instruct related tasks we will use the instruct model `.\Models\DeepSeek-Coder-V2-Lite-Instruct-GGUF-Q8_0.gguf`, this model is cabable of `~200,000` context, we do not want to over-fit the context length, but, this model will enable. python programming, WindowsSystem/Powershell/Python command formulation, etc. 
- New commands: summarize_multiple_urls, compare_information, generate_report, prioritize_tasks, break_down_task, evaluate_task_success, TaskTracker class.

### PREVIEW:
- The Env is now a yaml, as we have no APIs, this will have a gradio configurator for logical keys...
```
# Program Settings
execute_local_commands: Allow
continuous_mode: false
continuous_limit: 0
debug_mode: false

# Session Settings
ai_settings_file: ai_settings.yaml
user_name: ""
ai_name: ""
ai_role: ""
ai_goals: []

# System Settings
memory_backend: local
memory_index: autoccp-lite
speak_mode: false

# LLM Model Settings
model_path: ./models
smart_llm_model: ./models/YourModel.gguf
context_size: 8192
max_tokens: 4000
smart_token_limit: 8000
embed_dim: 1536
gpu_threads_used: 1024
temperature: 1

# Browsing Settings
browse_chunk_max_length: 8192
browse_summary_max_token: 300
user_agent: "Mozilla/5.0"
playwright_headless: true
playwright_timeout: 30000
```
- The combined, `Setup-Installer` and `Launcher`, is the current form of `Auto-Cpp-Local.Bat`...
```
=======================================================================================================================
    Auto-CPP-Local v009
=======================================================================================================================









    1. Run Auto-CPP-Local v009 on Python v39

    2. Check Folders and Install Libraries

    3. Upgrade Pip Version to Current









-----------------------------------------------------------------------------------------------------------------------
Selection; Menu Options = 1-3, Exit Menu = X:

```

### REQUIREMENTS:
- Python 3.9 - It will find "...Python39\pip.exe" in, user folder or either program files, though you can change Python 3.9 consistently to any version in the 2 batches.
- Python Libraries - Now listed in `.\data\requirements.txt`, able to be Installed through `.\Auto-Cpp-Local.Bat`, the requirements are same as `AutoGPT v1.3`, other than, removal of online services, then insertion so far of: `Gradio`. 
- Pre-Compiled Llama.Cpp - Downloaded/Installed by `.\Auto-Ccp-Local.Bat` during processes around selection of install of `.\data\requirements.txt`.
- No Environments - Such as, Dockers or WSL, no, just normal windows operations, and set python location installs.
- Suitable Models - Currently its, `.\Models\DeepSeek-Coder-V2-Lite-Instruct-GGUF-Q*.gguf` and `.\Models\DeepSeek-V2-Lite-Chat.Q*.gguf`, this will be expanded later, need working version.


### INSTALL AND USAGE:
- Note, it does not work yet, but when it does, it will be like...
1. This program is currently for the version of Python it was created on, that is `Python 3.9`, install it to one of the 2 possible default file locations, do not install Python 3.9 in a un-usual location.  
2. Run the `.\Auto-CCP-Local.Bat`, tou first should install requirements/libraries, it will find "...Python39\scripts\pip.exe", invoke-webrequest will download llama.cpp pre-compiled binary.
3. Ensure to insert the `Suitable Models` in `*.GGUF` formmat into `.\Models` folder, we need both of them for the AI to work.
4. On the `.\Auto-CCP-Local.Bat` menu, launch the program, it will find "...Python39\python.exe" and use that for the launch commands.
4. First the user must configure some things in the text based `Engine Window`, then the user may, begin using AutoCPP-Lite in the based `Chat Window` Server, that should popup the interface in the default web browser.

### DEVELOPMENT:
- review the memory code, determine if there is any clever code we can introduce to enhance the memory of the AI. Rag, is that what we need, is there something better? What is best solution for best results?
- The prompts sent to local modes, obviously its not prompt.txt anymore, so, I am a little unfamilliar. It must work most, logicall and effectively, the prompting should be customized to best compatibility with the applicable model in use for the task. 

### NOTATION:
- If we re-implement image generation, stable-diffusion 2.1 model in GGUF here `https://huggingface.co/jiaowobaba02/stable-diffusion-v2-1-GGUF`.
- No gradio interface, scripts are too large as it is for AI programming. At least not for now, until I have full release, at which point I will produce a decision.
- Optimally I want 2 models, user would be `director` and `creative artist`, and frank model would be `assistant-director` and `liason-officer` and `agent manager`, and Qwen would be `task agents` and `programmers`, Something like that.
- The folders have been re-imagined...
```
    .\Input: Folder for input files; if present, prompts the user for descriptions.
    .\Output: Folder for completed tasks and final output files.
    .\cache\working: Temporary workspace for file and project creation.
    .\cache\downloads: Temporary storage for downloaded files.
```
- Quoted from the original v1.3 "README.md": `Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model.`, from this, we take from it, that its only as good as the model, albeit you want models on par with gpt 4.


# DISCLAIMER
- This fork AutoCPP-Lite, is a experimental application, and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise. But be safe in knowing, you will not incur any more Online fees for usage of what is essentially Auto-GPT. 
- Continuous mode is not recommendedm It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorise, however, be safe in the knowledge, that any endless loops, that gpt and early versions of AutoGPT were known for, will not result in a huge APT bill, as we are on LOCAL models in the fork.
- This Forked version will have features such as system commands, to be enabled by default, though this is configurable at startup, and intended so for development purposes. The fork will also not simply be able to all be inputted into GPT or Claude, due to the size of the code, so the features not used by myself, will likely, be removed or go un-tested.
