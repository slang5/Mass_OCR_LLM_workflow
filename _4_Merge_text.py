import utils

import os
from time import time as t
    
def merge_all_txt_from_directory(input_directory:str=".\\clean_text", output_dir:str=".\\merged_clean_text"):
    utils.ensure_directory_exists(output_dir)
    utils.ensure_directory_exists(input_directory)
    utils.ensure_directory_not_empty(input_directory)

    merged_content = ""
    min =  9999999
    max = -9999999

    for text_path in sorted(utils.get_paths(input_directory, format='.txt'), key=lambda x: int(x.split("_")[2])):
        start = t()
        print(f"Merging {text_path}...")
        page_nb = int(text_path.split("_")[2])
        if page_nb < min:
            min = page_nb
        if page_nb > max:
            max = page_nb
        text_content = utils.read_text(text_path)
        merged_content += f'\npage: {page_nb} \n\n{text_content}\n\n'
        
        end = t()
        print(f"Merged {text_path} in {end - start:.3f} seconds")

    output_file_path = os.path.join(output_dir, f"merged_text_pages_{min}_to_{max}.md")
    
    utils.write_text(output_file_path, merged_content)
    print(f"Saved merged text to {output_file_path}")

