# AutoGPT-CPPVulkan: A Fork and Remake, of AutoGPT 1.3
Status: Alpha

### DEVELOPMENT:
- Merging of smaller scripts in ".\scripts\" with simlarly themed scripts, while optimizing and compacting, functions. overall scripts should be reduced to multiple 150-200 line scripts, but as few as as possible. prediction 1/3 of scripts in ".\scripts" are mergeable.
- due to less scripts, sKim over as many scripts together in 1 long input session starts with claude, checking compatibility with updates so far, ensure everything is logical and sound, and possibility of streamlining for methods of doing things we are no-longer using.
- use of Yaml instead of Json, this was a later advancement in Auto-GPT, as I remember, yet I see mentions of Yaml, so I guess it uses yaml, maybe the json references are for OpenAI, in which case, will requre converting to llama.cpp binaries.
- Solutions have been found to HuggingFace and google, see "NOTATION" section. 
- We could use a yaml instead of the .env, as it will contain no sensitive data such as API keys, and delete and do away with the env system. this could also result in some form of configurator batch "Configure.Bat" with gradio interface, for the yaml, and we could hide the yaml in .\scripts or something and instead use a batch run gradio configurator. Batch files will then be required to be numbered, 1., 2., 3., for foolproofing.
- Data visualization, spinner should be replaced with data visualization line during "thinking" phase, time taken, throughput rate, memory/processor usage, whats possible and fitting?
- review the memory code, determine if there is any clever code we can introduce to enhance the memory of the AI. Rag, is that what we need, is there something better? What is best solution for best results?
- Installer works, and sets up folders correctly, however, Launcher requires, run and thorough debug.
- I will at some point want to do my prompt engineering magic on the prompts sent to local modes, obviously its not prompt.txt anymore, so, I am a little unfamilliar.
- Depending upon how many scripts were the result, there is the possibility of a gradio interface for `Launcher.Bat`, for the display of engine, output and printed lines, in a box on the right, and a chat interface on the left, similar to the interface of claude.

## DESCRIPTION:
- This fork "AutoGPT-CPPVulkan", is a remake of the last release of "AutoGPT v1", that has be been streamlined and tuned, to basic windows non-wsl offline operation, and will be designed to run of local models, such as "qwencode 1.5". Auto-GPT is currently at v5.1, so dont expect that level of operation/compitence, however, we will be finding better alternates to things such as huggingface and google websearch, as well as giving the code a good optimization and going over. The main goal we will have something robust and compitent on local models, and the second goal is GPU Acelleration for both, entry level nVidia and Non-ROCM AMD, users. 
- Quoted from the original v1.3 "README.md": `Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model. This program, driven by GPT-4, chains together LLM "thoughts", to autonomously achieve whatever goal you set. As one of the first examples of GPT-4 running fully autonomously, Auto-GPT pushes the boundaries of what is possible with AI.`

### PREVIEW:
- The Env gives a better idea of where its going...
```
################################################################################
### AUTOGPT-CPPVULKAN 
################################################################################

################################################################################
### GENERAL SETTINGS
################################################################################

### ENGINE
EXECUTE_LOCAL_COMMANDS=Allow
AI_SETTINGS_FILE=ai_settings.yaml

################################################################################
### LLM MODELS
################################################################################

### LLM MODEL SETTINGS
SMART_LLM_MODEL=.\models\YourModel.gguf
SMART_TOKEN_LIMIT=8000
EMBED_DIM=1536
TEMPERATURE=1

################################################################################
### INTERNET USAGE
################################################################################

### BROWSING
BROWSE_CHUNK_MAX_LENGTH=8192
BROWSE_SUMMARY_MAX_TOKEN=300
# USER_AGENT - Define the user-agent used by the requests library to browse website (Example, Chrome/83.0.4103.97)
# USER_AGENT="Mozilla/5.0"  #--- Options, Chrome/83.0.4103.97, Mozilla/5.0

### GOOGLE
# GOOGLE_API_KEY - Google API key (Example: my-google-api-key)
# CUSTOM_SEARCH_ENGINE_ID - Custom search engine ID (Example: my-custom-search-engine-id)
GOOGLE_API_KEY=your-google-api-key
CUSTOM_SEARCH_ENGINE_ID=your-custom-search-engine-id

################################################################################
### IMAGE GENERATION
################################################################################

### HUGGINGFACE
# HUGGINGFACE_API_TOKEN - HuggingFace API token (Example: my-huggingface-api-token)
HUGGINGFACE_API_TOKEN=your-huggingface-api-token
```

### REQUIREMENTS:
- HuggingFace - For now, AutoGPT-CCPVulkan uses Stable Diffusion, get a [HuggingFace API Token](https://huggingface.co/settings/tokens) , then see ENV section.
- Python 3.9 - It will find "...Python39\pip.exe" in, user folder or either program files, though you can change Python 3.9 consistently to any version in the 2 batches.
- No Environments - Such as, Dockers or WSL, no, just normal windows operations, we are using the Llama Pre-compiled binaries, they run in windows, no issues there. 

### INSTALL AND USAGE:
1. Run the `.\Installer.Bat`, ensure firewall is off temprarely, or allow through. 
2. Ensure to insert a `*.GGUF` model into `.\models` folder, only one.
2. Configure the `.\.ENV` file, its now cut down, and should be simple enough.
3. Run the `.\Launcher.Bat`, it will find "...Python39\python.exe" and use that. unless you installed it in a non-optional location.

### NOTATION:
- Check it out, stable-diffusion 2.1 model in GGUF `https://huggingface.co/jiaowobaba02/stable-diffusion-v2-1-GGUF`. We can use this offline instead of "huggingface.co".
- Playwright is a library for browser interaction in python, Chrome Driver enables local server to interact with chrome in headless mode, together we can replace google requirement.

# DISCLAIMER
- This fork AutoGPT-CPPVulkan, is a experimental application, and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise. But be safe in knowing, you will not incur any more Online fees for usage of what is essentially Auto-GPT. 
- Continuous mode is not recommendedm It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorise. This version will have features such as system commands, to be enabled by default, though this is configurable in the .ENV, and intended so for development purposes.
