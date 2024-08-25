import json
from typing import Any, Dict, Union
from call_ai_function import call_ai_function
from config import Config
from json_utils import correct_json
from logger import logger

cfg = Config()
model = Llama(model_path=cfg.smart_llm_model)

JSON_SCHEMA = """
{
    "command": {
        "name": "command name",
        "args":{
            "arg name": "value"
        }
    },
    "thoughts":
    {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    }
}
"""


def fix_and_parse_json(
    json_str: str,
    try_to_fix_with_gpt: bool = True
) -> Union[str, Dict[Any, Any]]:
    """Fix and parse JSON string"""
    try:
        json_str = json_str.replace('\t', '')
        return json.loads(json_str)
    except json.JSONDecodeError as _:  # noqa: F841
        try:
            json_str = correct_json(json_str)
            return json.loads(json_str)
        except json.JSONDecodeError as _:  # noqa: F841
            pass
    # Let's do something manually:
    # sometimes GPT responds with something BEFORE the braces:
    # "I'm sorry, I don't understand. Please try again."
    # {"text": "I'm sorry, I don't understand. Please try again.",
    #  "confidence": 0.0}
    # So let's try to find the first brace and then parse the rest
    #  of the string
    try:
        brace_index = json_str.index("{")
        json_str = json_str[brace_index:]
        last_brace_index = json_str.rindex("}")
        json_str = json_str[:last_brace_index+1]
        return json.loads(json_str)
    # Can throw a ValueError if there is no "{" or "}" in the json_str
    except (json.JSONDecodeError, ValueError) as e:  # noqa: F841
        if try_to_fix_with_gpt:
            logger.warn("Warning: Failed to parse AI output, attempting to fix."
                  "\n If you see this warning frequently, it's likely that"
                  " your prompt is confusing the AI. Try changing it up"
                  " slightly.")
            # Now try to fix this up using the ai_functions
            ai_fixed_json = fix_json(json_str, JSON_SCHEMA)

            if ai_fixed_json != "failed":
                return json.loads(ai_fixed_json)
            else:
                # This allows the AI to react to the error message,
                #   which usually results in it correcting its ways.
                logger.error("Failed to fix AI output, telling the AI.")
                return json_str
        else:
            raise e


def fix_json(json_str: str, schema: str) -> str:
    function_string = "def fix_json(json_str: str, schema:str=None) -> str:"
    args = [f"'''{json_str}'''", f"'''{schema}'''"]
    description_string = "Fixes the provided JSON string to make it parseable"\
        " and fully compliant with the provided schema.\n If an object or"\
        " field specified in the schema isn't contained within the correct"\
        " JSON, it is omitted.\n This function is brilliant at guessing"\
        " when the format is incorrect."

    if not json_str.startswith("`"):
        json_str = "```json\n" + json_str + "\n```"
    
    prompt = f"{function_string}\n\nArgs:\n{args}\n\nDescription:\n{description_string}\n\nJSON to fix:\n{json_str}"
    
    result_string = model.create_completion(prompt, max_tokens=1000, temperature=cfg.temperature)['choices'][0]['text']
    
    logger.debug("------------ JSON FIX ATTEMPT ---------------")
    logger.debug(f"Original JSON: {json_str}")
    logger.debug("-----------")
    logger.debug(f"Fixed JSON: {result_string}")
    logger.debug("----------- END OF FIX ATTEMPT ----------------")

    try:
        json.loads(result_string)
        return result_string
    except:
        return "failed"