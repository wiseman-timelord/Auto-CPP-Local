# AutoGPT-CPPVulkan: A Fork and Remake of AutoGPT 1.3
Status: Alpha

### DEVELOPMENT:
- merge and optimize files in `.\memory\`, then move single merged script to ".\scripts", and update compatibility with other functions that mention it in other scripts. Also, hardcode memory choice to always just use local settings, so as to not have .env entry, and streamline where appropriate. additionally review the memory code, determine if there is any clever code we can introduce to enhance the memory of the AI.
- Merging of smaller scripts in ".\scripts\" with simlarly themed scripts, while optimizing and compacting, functions. overall scripts should be reduced to multiple 150-200 line scripts, but as few as as possible.
- SKim over all scripts, checking compatibility with updates so far, ensure everything is logical and sound, and possibility of streamlining for methods of doing things we are no-longer using.
- use of Yaml instead of Json, this was a later advancement in Auto-GPT, as I remember, yet I see mentions of Yaml, so I guess it uses yaml, maybe the json references are for OpenAI, in which case, will requre converting to llama.cpp binaries.
- Installer works, and sets up folders correctly, however, Launcher requires, run and thorough debug.
- Pre-Launch Gradio-Interface run with "Configure.Bat" for Configuring ENV, that will now be kept in the Yaml, env will be deleted.
- Solutions need to be found to HuggingFace, local stable diffusion GGUF files are a thing, but will they do the job, albeit more simple version. 
- Depending upon how many scripts were the result, there is the possibility of a gradio interface for `Launcher.Bat`, for the display of engine, output and printed lines, in a box on the right, and a chat interface on the left, similar to the interface of claude.

## DESCRIPTION:
Auto-GPT is an experimental open-source application showcasing the capabilities of the GPT-4 language model. This program, driven by GPT-4, chains together LLM "thoughts", to autonomously achieve whatever goal you set. As one of the first examples of GPT-4 running fully autonomously, Auto-GPT pushes the boundaries of what is possible with AI. This forf "AutoGPT=CPPVulkan", is a remake of an early version of Auto-GPT, that has been streamlined to basic windows non-wsl operation, and will be designed to run of local models, such as "qwencode 1.5". Auto-GPT is currently at v5.1, so dont expect that level of operation, however, we will be finding better alternates to things such as huggingface and google websearch.

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

# DISCLAIMER
- This fork AutoGPT-CPPVulkan, is a experimental application, and is provided "as-is" without any warranty, express or implied. By using this software, you agree to assume all risks associated with its use, including but not limited to data loss, system failure, or any other issues that may arise. But be safe in knowing, you will not incur any more Online fees for usage of what is essentially Auto-GPT. 
- Continuous mode is not recommendedm It is potentially dangerous and may cause your AI to run forever or carry out actions you would not usually authorise. This version will have features such as system commands, to be enabled by default, though this is configurable in the .ENV, and intended so for development purposes.
