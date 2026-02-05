import utils

from PIL import Image
import pillow_heif
from time import time as t

def change_picture_format(path_str:str, output_directory:str) -> None:
    """
    Convert a picture of format X to PNG and save it to output_directory

    path_str : str : path to input picture and must end with extension in []
    output_directory : str : path to output directory and must end with .png
    """

    extension = path_str.split('.')[-1].lower()
    valid_extensions = ['heic', 'jpeg', 'jpg', 'bmp', 'tiff', 'gif', 'webp', 'png']

    if extension not in valid_extensions:
        raise ValueError(f"Unsupported file format: {extension}. Supported formats are: {', '.join(valid_extensions)}")
    else:
        start = t()
        if extension == 'heic':
            try:
                heif_file = pillow_heif.read_heif(path_str)
                img = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data, #type: ignore
                    "raw",
                )
            except Exception as e:
                print(f"Error converting HEIC image {path_str}: {e}")
                return None
        else:
            try:
                img = Image.open(path_str)  
            except Exception as e:
                print(f"Error opening image {path_str}: {e}")
                return None
        img.save(output_directory, format="png")
    end = t()
    print(f"Converted {path_str} to {output_directory} in {end - start:.3f} seconds.")
    return None

def convert_dir_by_format(input_directory:str=".\\raw_pics", output_directory:str=".\\clean_pics", input_format:str='.heic', output_format:str='.png', first_page_index=1):
    """
    Convert all picture in input_directory of format input_format to output_format and save them to output_directory
    first_page_index : int : index of the first page for naming convention
    """
    utils.ensure_directory_exists(output_directory)

    utils.ensure_directory_exists(input_directory)
    utils.ensure_directory_not_empty(input_directory)

    list_paths = utils.get_paths(input_directory, format=input_format)
    list_sorted = utils.sorting_str_by_filename(list_paths, output_directory, output_format, index_start=first_page_index)
    for input_path, output_path in list_sorted.items():
        change_picture_format(input_path, output_path)
