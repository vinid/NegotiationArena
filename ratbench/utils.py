import os
import copy
from ratbench.agents import ChatGPTAgent, ClaudeAgent, AnyScaleAgent, GeminiAgent

def factory_agent(name, agent_name):
    """
    Simple factory to create agents
    :param name:
    :param agent_name:
    :return:
    """
    if name == "gpt-4":
        return ChatGPTAgent(agent_name=agent_name, model="gpt-4-1106-preview")
    elif name == "claude-2":
        return ClaudeAgent(agent_name=agent_name, model="claude-2")
    elif name == "claude-2.1":
        return ClaudeAgent(agent_name=agent_name, model="claude-2.1")
    elif name == "gpt-3.5":
        return ChatGPTAgent(agent_name=agent_name, model="gpt-3.5-turbo-1106")
    elif name == "mixtral":
        return AnyScaleAgent(agent_name=agent_name, model="mistralai/Mixtral-8x7B-Instruct-v0.1")
    elif name == "llama":
        return AnyScaleAgent(agent_name=agent_name)
    elif name == "gemini-pro":
        return GeminiAgent(agent_name=agent_name, model="gemini-pro")





def get_tag_contents(response, interest_tag):
    start_index, end_index, length = get_tag_indices(response, interest_tag)
    contents = response[start_index + length : end_index].lstrip(" ").rstrip(" ")
    return copy.deepcopy(contents)


def get_tag_indices(response, interest_tag):
    start_index = response.find(f"<{interest_tag}>")
    end_index = response.find(f"</{interest_tag}>")
    return start_index, end_index, len(f"<{interest_tag}>")


def text_to_dict(s):
    return {k: int(v) for k, v in (item.split(": ") for item in s.split(", "))}


def get_next_filename(prefix, folder="."):
    prefix = prefix + "_"
    if not os.path.exists(folder):
        return prefix[:-1]
    # List all files with the given prefix in the current directory
    files = [file for file in os.listdir(folder) if file.startswith(prefix)]

    # Extract the numeric part of the file names and find the maximum
    numbers = [
        int(file[len(prefix) :]) for file in files if file[len(prefix) :].isdigit()
    ]

    # Determine the next integer in the sequence
    next_number = max(numbers, default=0) + 1

    # Generate the next file name
    next_filename = f"{prefix}{next_number}"

    return next_filename
