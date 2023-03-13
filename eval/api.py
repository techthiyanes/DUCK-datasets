"""
Write a query setup for the OpenAI API
"""
#%%
#%%
# Imports and setup
import argparse
from tqdm import tqdm
from utils import api_keys, call_chat_model, get_content, chat_message
import openai
api_keys()

U, A, S = "user", "assistant", "system"

#%%
# Import few-shot demonstrations and prompts
from prompt_eng import help_prompt_math, example_shot_aime_points

#%%
def oneshot_prompt(question : str, format_instructions : str) -> list[dict[str, str]]:
    return [
        chat_message(S, help_prompt_math),
        chat_message(U, example_shot_aime_points[U]),
        chat_message(A, example_shot_aime_points[A]),
        chat_message(U, f"Great answer! I have another question: [Q] {question}\n[Format] {format_instructions}")
        ]



