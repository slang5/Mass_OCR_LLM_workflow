
import os, base64
from ctypes import windll
from time import time as t
from ollama import Client

def read_text(file_path:str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
def write_text(file_path:str, content:str) -> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_paths(directory, format='.png') -> list[str]:
    """
    Retrieve all file paths with the specified format from the given directory and its subdirectories.
    """
    heic_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(format):
                heic_files.append(os.path.join(root, file))
    return heic_files

def sorting_str_by_filename(list_str:list[str], output_directory=".\\clean_pics", format:str=".png", index_start:int=1) -> dict[str, str]:
    """
    Sorting list or string by ascending order of filename 
    Stored in a dict by ascending order with specific format : 
    
    - output_directory\\page_{index + index_start}.png
    """
    list_str.sort()
    str_name_dict = {}
    
    for index, path in enumerate(list_str):
        str_name_dict[path] = f"{output_directory}\\page_{index + index_start}{format}"
    
    return str_name_dict

def ensure_directory_exists(directory:str) -> None:
    """
    Ensure that the specified directory exists; create it if it does not.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    
def ensure_directory_not_empty(directory:str) -> None:
    """
    Ensure that the specified directory is not empty; raise an error if it is.
    """
    if not os.path.exists(directory) or not os.listdir(directory):
        raise ValueError(f"Directory {directory} does not exist or is empty.")

def clear_directory(directory:str, exclude_extensions:list[str]=[]) -> None:

    """
    Clear all files in the specified directory, excluding files with extensions in exclude_extensions.
    """
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist. No files to clear.")
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and not any(filename.lower().endswith(ext) for ext in exclude_extensions):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")


def get_screen_size() -> dict[str, int]:
    """
    Get the screen size of the primary monitor.
    Returns a dict with keys 'width' and 'height'.

    https://stackoverflow.com/questions/3129322/how-do-i-get-monitor-resolution-in-python
    """
    user32 = windll.user32
    return {'width': user32.GetSystemMetrics(0), 'height': user32.GetSystemMetrics(1)}

def move_files_from_to(source_directory:str, destination_directory:str, format:str='.png') -> None:
    """
    Move all files of a specific format from source_directory to destination_directory.
    """
    ensure_directory_exists(destination_directory)

    ensure_directory_exists(source_directory)
    ensure_directory_not_empty(source_directory)

    file_paths = get_paths(source_directory, format=format)
    
    start = t()
    for file_path in file_paths:
        base_name = os.path.basename(file_path)
        dest_path = os.path.join(destination_directory, base_name)
        os.rename(file_path, dest_path)
        print(f"Moved {file_path} to {dest_path}")
    end = t()
    print(f"Moved {len(file_paths)} files from {source_directory} to {destination_directory} in {end - start:.3f} seconds.")

def payload_ocr(image_path, model="deepseek-ocr", prompt="Free OCR", stream:bool=False):
    """
    Build to be used payload for OCR model with Ollama package.
    """

    with open(image_path, "rb") as img_file:
        b64_image = base64.b64encode(img_file.read()).decode("utf-8")
    
    _stream = stream
    
    return {
        "model": model,
        "messages": [{
            "role": "user",
            "content": prompt,
            "images": [b64_image],
        }],
        "stream": _stream
    }

def payload_llm(prompt:str, text_content:str, model:str="qwen3:8B", stream:bool=False, temperature:float=0.7, top_k:int=40):
    """
    Build to be used payload for LLM model with Ollama package.
    """

    return {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"{prompt}:\n{text_content}",
        }],
        "options": {
            "temperature": temperature,
            "top_k": top_k,
        },
        "stream": stream
    }

class Ollama_Client(Client):
    """
    Subclass of Ollama Client to add custom methods if needed in the future.
    Currently, it behaves the same as the base Client.
    
    Arguments:
        host: str = "http://localhost:11434" by default
        timeout: int = 120 seconds by default
    """
    def __init__(self, host: str = "http://localhost:11434", timeout:int=120) -> None:
        super().__init__(host, timeout=timeout)