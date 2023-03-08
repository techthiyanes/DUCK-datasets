import openai
from logger import Logger
import json
import random
import argparse
import numpy as np
from tqdm import tqdm
import time
from datasets import load_dataset
from data_utils import filter_by_logs
from utils import load_jsonl, save_results


def query(prompts, max_tokens, temperature, model):
    responses = openai.Completion.create(engine=model, prompt=prompts, max_tokens=max_tokens, temperature=temperature)["choices"]
    responses = [response["text"] for response in responses]
    return responses


# Assumes prompts is a list of dicts, each of which contains a "prompt" key
def run_prompts(prompts, batch_size, max_tokens, temperature, model):
    num_batches = (len(prompts) + batch_size - 1) // batch_size
    batched_prompts = [prompts[i*batch_size : (i+1)*batch_size] for i in range(num_batches)]
    answers = []

    for batch in tqdm(batched_prompts):
        batch_prompts = [sample["prompt"] for sample in batch]
        try:
            responses = query(batch_prompts, max_tokens, temperature, model)
            for sample, response in zip(batch, responses):
                sample["response"] = response
            answers += responses

        except openai.error.RateLimitError:
            print("RATELIMIT ERROR")
            time.sleep(30)
        except openai.error.ServiceUnavailableError:
            print("SERVICE UNABAILABLE")
            time.sleep(15)
        except openai.error.Timeout:
            print("TIMEOUT")
            time.sleep(15)
        except:
            print("SOME OTHER EXCEPTION")
            time.sleep(30)
        time.sleep(15)  # Sleep to prevent rate limiting

    
def run_subjects(dataset, args):
    results = {}
    for model in args.models:
        for subject, qs in dataset.items():
            run_prompts(prompt_dataset, args.batch_size, args.max_num_tokens, args.temp, model)

    save_results(results, args.output_dir)
    evaluate_results()


def evaluate_results(results):
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--oai_key")
    parser.add_argument("--temp", default=0.7, type=float)
    parser.add_argument("--max_num_tokens", default=1024, type=int)
    parser.add_argument("--batch_size", default=10, type=int)
    parser.add_argument("--models", default=["code-davinci-002"])
    parser.add_argument("--output_dir", default="output")
    args = parser.parse_args()

    # Set openai api key
    openai.api_key = args.oai_key

    # Load evaluation dataset
    dataset = None

    # Run evaluation
    run_subjects(dataset)