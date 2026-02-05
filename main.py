from utils import move_files_from_to, Ollama_Client, clear_directory
from _0_Picture_Change_Format import convert_dir_by_format
from _1_Picture_Mass_Cropping import cropping_pictures_of_directory
from _2_Picture_to_OCR import resize_all_images_of_directory, apply_ocr_to_all_images_in_directory
from _3_Cleaning_text import process_texts
from _4_Merge_text import merge_all_txt_from_directory

"""
This script orchestrates the entire workflow of processing scanned document images, extracting text, cleaning it,and merging it into a single file. The steps include:
1. Converting all images of the specified format to PNG format.
2. Allow user to crop all images in the directory to focus on the relevant content.
3. Resizing and enhancing all images in the directory to optimize them for OCR with greyscale filter.
4. Applying OCR to all images in the directory and saving the extracted text.
5. Cleaning the extracted text using a language model to produce a more readable and faithful version of the original content.
6. Merging all cleaned text files into a single markdown file for easier review and use.


Please ensure you have pictures in the raw_pics directory and to define the right input_format value at line 27 before running the script/

"""

if __name__ == "__main__":

    # Step 1: Convert all images to PNG format
    convert_dir_by_format(input_directory=".\\raw_pics", output_directory=".\\clean_pics", input_format='.heic', output_format='.png')

    clear_directory(".\\raw_pics", exclude_extensions=['.png'])
    move_files_from_to(source_directory=".\\clean_pics", destination_directory=".\\raw_pics", format='.png')

    # Step 2: Crop all images in the directory
    cropping_pictures_of_directory(input_directory=".\\raw_pics", output_directory=".\\clean_pics")
    
    clear_directory(".\\raw_pics", exclude_extensions=[])
    move_files_from_to(source_directory=".\\clean_pics", destination_directory=".\\raw_pics", format='.png')
    
    # Step 3: Resize and enhance all images in the directory
    resize_all_images_of_directory(input_directory=".\\raw_pics", output_directory=".\\clean_pics", max_dim=1600, jpeg_quality=85, greyscale=True)

    clear_directory(".\\raw_pics", exclude_extensions=[])
    
    # Step 4: Apply OCR to all images in the directory and save the extracted text
    client = Ollama_Client(host="http://localhost:11434")
    prompt_ocr = "Convert the document to markdown"
    apply_ocr_to_all_images_in_directory(client=client, input_directory=".\\clean_pics", output_directory=".\\raw_text_OCR", model_ocr="deepseek-ocr", prompt_ocr=prompt_ocr)
    
    # Step 5: Clean the extracted text using LLM and save the cleaned text
    prompt_cleaning = ("Role: You are an assistant for proofreading and cleaning OCR-generated text."
                    "Goal: Produce a clean, readable, faithful version of the provided text without adding content."
                    "Context: The text comes from a scanned document (OCR) and may include artifacts (OCR noise, layout elements, headers/footers, etc.)."
                    "Cleaning instructions (apply consistently):"
                    "Remove all copyright marks, watermarks, and institutional slogans."
                    "Remove pagination and parasitic layout elements: page numbers, “Page X/Y,” repetitive headers/footers, separators, print marks, etc."
                    "Correct obvious typographical and OCR errors (confused characters, broken words, aberrant punctuation) without changing the substance."
                    "Normalize spacing: remove unnecessary spaces, reduce excessive line breaks, and merge artificially broken lines."
                    "Preserve essential formatting: titles, subtitles, bullet/numbered lists, simple equations, and tables when possible in text form."
                    "Do not “translate”: if the text mixes French and English, keep the mixture as is."
                    "Special case (images/figures/graphs): If part of the text refers to an image, graph, figure, or chart (e.g., “see figure,” “graph below,” “chart”), replace the corresponding content with: [Graphique not included]."
                    "Expected output: Return only the final cleaned text, without comments, action lists, or explanations.")
    
    process_texts(client=client, prompt=prompt_cleaning, input_directory=".\\raw_text_OCR", output_directory=".\\clean_text", model="qwen3:8b", temperature=0.7, top_k=40)
    
    # Step 6: Merge all cleaned text files into a single file
    merge_all_txt_from_directory(input_directory=".\\clean_text", output_dir=".\\merged_clean_text")

