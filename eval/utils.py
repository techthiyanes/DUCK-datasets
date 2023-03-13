# %%
from typing import Literal
import openai
U, A, S = "user", "assistant", "system"

def api_keys():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

#%%
# Define call_chat_model function which adds the prompt to the returned JSON
def call_chat_model(prompt : list[dict[str, str]], model : str = "gpt-3.5-turbo-0301", temperature : float = 0., **kwargs) -> dict:
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt,
        temperature=temperature,
        **kwargs
    )
    response["prompt"] = prompt
    return response

def call_model(prompt : str, model : str = "text-davinci-003", temperature : float = 0., **kwargs) -> dict:
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        **kwargs
    )
    response["prompt"] = prompt

#%%
# Basic functions
def chat_message(role : Literal["user", "assistant", "system"], content : str) -> dict[str, str]:
    assert role in ["user", "assistant", "system"]
    return {"role": role, "content": content}

def get_content(response : dict) -> str:
    if response["choices"].hasattr("text"):
        return response["choices"]["text"]
    else:
        assert response["choices"][0]["message"]["role"] == "assistant"
        return response["choices"][0]["message"]["content"]



def is_good_float(ans : float, correct : float, tol : float = 0.01) -> bool:
    return abs(ans - correct) < tol

def is_good_latex(ans : str, correct : str) -> bool:
    correct = correct.replace("$", "")
    ans = ans.replace("$", "")
    if correct == ans:
        return True
    else:
        print(f"Correct: {correct}, Answer: {ans}")



