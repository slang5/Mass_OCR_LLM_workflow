import utils

import os, cv2
from time import time as t
from ollama import Client

def read_pic(pic_path:str):
    img = cv2.imread(pic_path)
    if img is None:
        raise ValueError(f"Could not load image at {pic_path}")
    return img

def save_pic(pic_path:str, img, params) -> None:
    cv2.imwrite(pic_path, img, params)
    return None

def resize_image(img, max_dim:int=1600):
    h, w = img.shape[:2]
    scale = min(1.0, max_dim / max(h, w))
    if scale < 1.0:
        img = cv2.resize(img, (int(w*scale), int(h*scale)), interpolation=cv2.INTER_AREA)
    return img

def enchace_image(img, blur:tuple=(0,0,1), weights:tuple=(1.25, -0.25)) -> None:
    # slight unsharp mask
    blurred = cv2.GaussianBlur(img, (blur[0], blur[1]), sigmaX=blur[2])
    img = cv2.addWeighted(img, weights[0], blurred, weights[1], 0)
    return img

def greyscale_image(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def shrink_keep_quality(in_path, out_path, max_dim=1600, jpeg_quality=85, greyscale=False) -> None:
    img = read_pic(in_path)
    img = resize_image(img, max_dim=max_dim)
    if greyscale:
        img = greyscale_image(img)
    img = enchace_image(img, blur=(0,0,1), weights=(1.25, -0.25))

    save_pic(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality])
    return None

def build_payload(image_path, model="deepseek-ocr", prompt="Free OCR"):
    return utils.payload_ocr(image_path, model=model, prompt=prompt, stream=False)

def resize_all_images_of_directory(input_directory:str=".\\raw_pics", output_directory:str=".\\clean_pics", max_dim:int=1600, jpeg_quality:int=85, greyscale:bool=False):
    utils.ensure_directory_exists(output_directory)
    utils.ensure_directory_exists(input_directory)
    utils.ensure_directory_not_empty(input_directory)

    for img in utils.get_paths(input_directory, format='.png'):
        start = t()
        base_name = os.path.basename(img)
        out_path = os.path.join(output_directory, base_name)
        shrink_keep_quality(img, out_path, max_dim=max_dim, jpeg_quality=jpeg_quality, greyscale=greyscale)
        end = t()
        print(f"Resized {img} and saved to {out_path} in {end - start:.3f} seconds")

def apply_ocr_to_all_images_in_directory(client:Client, input_directory:str=".\\clean_pics", output_directory:str=".\\raw_text_OCR", model_ocr:str="deepseek-ocr", prompt_ocr:str="Free OCR"):
    utils.ensure_directory_exists(output_directory)
    utils.ensure_directory_exists(input_directory)
    utils.ensure_directory_not_empty(input_directory)

    for img in utils.get_paths(input_directory, format='.png'):
        start = t()
        print(f"Processing {img}...")
        
        payload = build_payload(img, model=model_ocr, prompt=prompt_ocr)

        try:
            response = client.chat(model=payload["model"], messages=payload["messages"]).message.content 
            if response is None:
                response = '[Too complex page for OCR, please complete manually.]'
            _response = 'vide' if response.strip() == '' else response
        
        except Exception as e:
            print(f"Error during OCR for {img}: {e}")
            response = '[Too complex page for OCR, please complete manually.]'
            _response = 'vide' if response.strip() == '' else response
        
        base_name = os.path.basename(img)
        text_file_path = os.path.join(output_directory, f"{os.path.splitext(base_name)[0]}.txt")
        with open(text_file_path, "w", encoding="utf-8") as f:
            f.write(_response)

        end = t()
        print(f"Saved OCR text to {text_file_path} in {end - start:.3f} seconds")
