# Auto-CPP-Local: A Fork and Remake, of AutoGPT 1.3
Status: Alpha - Improvement, Optimization, Correction, Refinement, not testing yet.

### DEVELOPMENT:
- Been over the scripts twice in the new `DeepSeek v2.5`, logic and sanity.
- Updated to streamline token counting and costs (lopped it off).
- Updated all GPT code to become LlamaCPP Binary code.

## DESCRIPTION:
- This fork "AutoCPP-Lite", is a remake of the last release of "AutoGPT v1.3", that has be been streamlined and tuned, to basic windows non-wsl offline operation, and will be designed to run of local models, such as "qwencode 1.5". Auto-GPT is currently at v5.1, so dont expect that level of operation/compitence. however, we have found alternates to things such as google websearch, as well as giving the code a good optimization. The image generation is removed, the user should instead provide AutoCPP-Lite with images/music/videos they, generate elsewhere and communicate inclusion of. The main goal is to have AutoGPT, robust and compitent, on local models, and the second goal is GPU Acelleration for both, entry level nVidia and Non-ROCM AMD, users. 
- Quoted from the original v1.3 "README.md": `Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model.`, from this, we take from it, that its only as good as the model, albeit you want models on par with gpt 4.

### NEW FEATURES:
- summarize_multiple_urls: Summarizes the content from multiple URLs based on a given question.
- compare_information: Compares information from multiple URLs in relation to a specific question.
- generate_report: Creates a comprehensive report on a given topic using collected information.
- prioritize_tasks: Organizes a list of tasks in order of priority.
- break_down_task: Divides a large task into smaller, more manageable subtasks.
- evaluate_task_success: Assesses the success of a completed task and provides a score and explanation.
- TaskTracker class: Manage and track tasks; Add new task, Update task status, Get task status, Retrieve all tasks.

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
- Check out the new files structure, its now manageable...
```
.\Installer.bat
.\Launcher.bat
.\main.py
.\working
.\docs
.\docs\*programming notes*
.\data
.\data\libraries\
.\data\libraries\**Llama.Cpp Library**
.\data\persistent_settings.yaml
.\data\requirements.txt
.\models
.\models\**default models location**
.\scripts
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
- Suitable Models - I predict `codeqwen-1_5-7b-chat-q8_0.gguf`, is worthy; `context length max 64K`, `92 coding languages`, `text-to-SQL, bug fix, etc`.

### INSTALL AND USAGE:
- Note, it does not work yet, but when it does, it will be like...
1. Run the `.\Installer.Bat`, ensure firewall is off temprarely, or allow through. it will find "...Python39\scripts\pip.exe" and use that, unless you installed Python 3.9 in a un-usual location.
2. Ensure to insert a `*.GGUF` model into `.\models` folder, we are only using one for now, it must be capable of chat and code, and have its own embeddings in the model.
3. Run the `.\Launcher.Bat`, it will find "...Python39\python.exe" and use that, unless you installed Python 3.9 in a un-usual location. 4. First the may user to configure some things, then the user may, Begin AutoCPP-Lite or Exit and Save.


### NOTATION:
- If we re-implement image generation, stable-diffusion 2.1 model in GGUF here `https://huggingface.co/jiaowobaba02/stable-diffusion-v2-1-GGUF`.
- No gradio interface, scripts are too large as it is for AI programming. At least not for now, until I have full release, at which point I will produce a decision.
- Optimally I want 2 models, user would be `director` and `creative artist`, and frank model would be `assistant-director` and `liason-officer` and `agent manager`, and Qwen would be `task agents` and `programmers`, Something like that.

## DEVELOPMENT:
- to make up for removal of image generation, the user should be generating their own media such as, images, samples, movies, optimally with other software, and making them available in a ".\input" folder, where the AI will become aware of new files periodically, and ask the user what to do with them, or possibly be asking the user to produce certain media, for the ai to be using in the project, and can instruct upon proposed filenames, so they fit the code. Finished projects would be in `.\output` folder, ensure auto-creation in installer. `.\working` should literally be the working folder, logically it would be `.\data\working`, and it would be cleared upon starting a new project.
- I want all scripts and files, to have labeles with two words, eg `example_name.py` for clarity while editing/programming, as there is some close resemblence between references and actual code.
- review the memory code, determine if there is any clever code we can introduce to enhance the memory of the AI. Rag, is that what we need, is there something better? What is best solution for best results?
- Installer works, and sets up folders correctly, however, need review of import modules, and check requirements.txt.
- I will at some point want to do my prompt engineering magic on the prompts sent to local modes, obviously its not prompt.txt anymore, so, I am a little unfamilliar.
- (needs larger context solution) Checking logic and sanity, in script, while ensuring updates to produce, optimizaton, improvement, completeness and correctness, in scripts. There may still be some incomplete and/or inefficient processes. About 35 sripts have been consolidated into 10, many functions were in separate scripts, some features added/cut, and so there will be some streamlining to be had also.

# DISCLAIMER
- This fork AutoCPP-Lite, is a experimental application, and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise. But be safe in knowing, you will not incur any more Online fees for usage of what is essentially Auto-GPT. 
- Continuous mode is not recommendedm It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorise, however, be safe in the knowledge, that any endless loops, that gpt and early versions of AutoGPT were known for, will not result in a huge APT bill, as we are on LOCAL models in the fork.
- This Forked version will have features such as system commands, to be enabled by default, though this is configurable at startup, and intended so for development purposes. The fork will also not simply be able to all be inputted into GPT or Claude, due to the size of the code, so the features not used by myself, will likely, be removed or go un-tested.
