import utils

import os
from ollama import Client
from time import time as t

def process_one_text(client:Client, prompt:str, text_raw:str, model:str="qwen3:8B", temperature:float=0.7, top_k:int=40) -> str:
    start = t()

    payload = utils.payload_llm(prompt=prompt, text_content=text_raw, model=model, temperature=temperature, top_k=top_k)
    response = client.chat(model=payload["model"], messages=payload["messages"], options=payload["options"]).message.content
    if response is None:
        response = ''
    response = 'vide' if response.strip() == '' else response

    end = t()
    print(f"Processed text in {end - start:.3f} seconds")
    return response

def process_texts(client:Client, prompt:str, input_directory:str=".\\raw_text_OCR", output_directory:str=".\\clean_text", model="qwen3:8B", temperature:float=0.7, top_k:int=40):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    text_paths = utils.get_paths(input_directory, format='.txt')
    for text_path in text_paths:
        print(f"Processing {text_path}...")
        
        response = process_one_text(client=client, prompt=prompt, text_raw=utils.read_text(text_path), model=model, temperature=temperature, top_k=top_k)
        
        base_name = os.path.basename(text_path)
        clean_text_file_path = os.path.join(output_directory, f"{os.path.splitext(base_name)[0]}_clean.txt")
        with open(clean_text_file_path, "w", encoding="utf-8") as f:
            f.write(response)
        
        print(f"Processed {text_path} and saved to {clean_text_file_path}")

