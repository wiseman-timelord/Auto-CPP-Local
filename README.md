# AutoCPP-Lite: A Fork and Remake, of AutoGPT 1.3
Status: Alpha - Processing files, for easier maintenance.

### DEVELOPMENT:
- Have removed image generation. Prompting an assessment of the tools available to the AI, cutting down some of the features. At same time, check, correctness and completenes, of current implementations, fix any logical errors, ensure everything is investigated.
- to `make up` for the removal of image generation, the user should be generating their own images optimally with other software, and making them available in the .\working folder, or maybe the introduction of an ".\intput" folder, where the AI will become aware of new files, and ask the user what to do with them, also option in same prompt, to re-detect, incase the user has not completed insertion of files.
- due to less scripts, sKim over as many scripts together in 1 long input session starts with claude, checking compatibility with updates so far, ensure everything is logical and sound, and possibility of streamlining for methods of doing things we are no-longer using.
- review the memory code, determine if there is any clever code we can introduce to enhance the memory of the AI. Rag, is that what we need, is there something better? What is best solution for best results?
- Installer works, and sets up folders correctly, however, Launcher requires, run and thorough debug.
- I will at some point want to do my prompt engineering magic on the prompts sent to local modes, obviously its not prompt.txt anymore, so, I am a little unfamilliar.


## DESCRIPTION:
- This fork "AutoCPP-Lite", is a remake of the last release of "AutoGPT v1", that has be been streamlined and tuned, to basic windows non-wsl offline operation, and will be designed to run of local models, such as "qwencode 1.5". Auto-GPT is currently at v5.1, so dont expect that level of operation/compitence, however, we will be finding better alternates to things such as huggingface and google websearch, as well as giving the code a good optimization and going over. The main goal we will have something robust and compitent on local models, and the second goal is GPU Acelleration for both, entry level nVidia and Non-ROCM AMD, users. 
- Quoted from the original v1.3 "README.md": `Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model. This program, driven by GPT-4, chains together LLM "thoughts", to autonomously achieve whatever goal you set. As one of the first examples of GPT-4 running fully autonomously, Auto-GPT pushes the boundaries of what is possible with AI.`

### PREVIEW:
- The Env is now a yaml, as we have no APIs, this will have a gradio configurator for logical keys...
```
# General Settings
execute_local_commands: Allow
ai_settings_file: ai_settings.yaml
speak_mode: false

# LLM Model Settings
smart_llm_model: ./models/YourModel.gguf
smart_token_limit: 8000
embed_dim: 1536
gpu_threads_used: 1024
temperature: 1

# Browsing Settings
browse_chunk_max_length: 8192
browse_summary_max_token: 300
user_agent: "Mozilla/5.0"

# Playwright Settings
playwright_headless: true
playwright_timeout: 30000

# AI Configuration
ai_name: ""
ai_role: ""
ai_goals: []

# Memory Settings
memory_backend: local
memory_index: autogpt-cppvulkan

# Debug Settings
debug_mode: false

# Continuous Mode Settings
continuous_mode: false
continuous_limit: 0

# Context Settings
context_size: 8192
max_tokens: 4000

# File Paths
model_path: ./models
```
- Check out the new files structure, its now manageable...
```
.\data
.\Installer.bat
.\Launcher.bat
.\main.py
.\models
.\scripts
.\working
.\docs
.\docs\*programming notes*
.\data\libraries\
.\data\libraries\**Llama.Cpp Library**
.\data\persistent_settings.yaml
.\data\requirements.txt
.\models\**GGUF Model**
.\scripts\config.py
.\scripts\main.py
.\scripts\management.py
.\scripts\models.py
.\scripts\operations.py
.\scripts\prompt.py
.\scripts\utilities.py
.\scripts\__init__.py
```

### REQUIREMENTS:
- Python 3.9 - It will find "...Python39\pip.exe" in, user folder or either program files, though you can change Python 3.9 consistently to any version in the 2 batches.
- Python Requirements - Installed by `Installer.Bat`, from, Web-Request on GitHub and what is now `.\data\requirements.txt`.  
- No Environments - Such as, Dockers or WSL, no, just normal windows operations, we are using the Llama Pre-compiled binaries, they run in windows, no issues there. 

### INSTALL AND USAGE:
1. Run the `.\Installer.Bat`, ensure firewall is off temprarely, or allow through. 
2. Ensure to insert a `*.GGUF` model into `.\models` folder, only one.
2. Configure the `.\.ENV` file, its now cut down, and should be simple enough.
3. Run the `.\Launcher.Bat`, it will find "...Python39\python.exe" and use that. unless you installed it in a non-optional location.

### NOTATION:
- Check it out, stable-diffusion 2.1 model in GGUF `https://huggingface.co/jiaowobaba02/stable-diffusion-v2-1-GGUF`. We can use this offline instead of "huggingface.co".
- No gradio interface, scripts are too large as it is for AI programming. At least not for now, until I have full release, at which point I will produce a decision.

# DISCLAIMER
- This fork AutoCPP-Lite, is a experimental application, and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise. But be safe in knowing, you will not incur any more Online fees for usage of what is essentially Auto-GPT. 
- Continuous mode is not recommendedm It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorise. This version will have features such as system commands, to be enabled by default, though this is configurable in the .ENV, and intended so for development purposes.
