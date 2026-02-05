import utils

import cv2, os

def prep_show_image(image_path:str, width:int):
    """
    Prepare an image for display by resizing it to the specified width while maintaining aspect ratio and decreasing quality.
    """

    img = cv2.imread(image_path)
    if img is None:
            return f"Error loading image {image_path}"
    
    display_width = width 
    scale = display_width / img.shape[1]
    display_height = int(img.shape[0] * scale)
    img_display = cv2.resize(img, (display_width, display_height))

    return img, scale, img_display

def cropping_box(img_display, img, scale):
    """
    Showing the image and allowing user to select a cropping box.
    """
    
    box = cv2.selectROI("Select ROI", img_display, False)
    
    box = [int(b / scale) for b in box]
    cropped_img = img[int(box[1]):int(box[1]+box[3]), int(box[0]):int(box[0]+box[2])]
    cv2.destroyAllWindows()
    return cropped_img, box

def saving_image(cropped_img, image_path:str, output_directory:str):
    """
    Save the cropped image to the output directory.
    """
    cv2.imwrite(os.path.join(output_directory, os.path.basename(image_path)), cropped_img)


def selec_crop_image(image_path:str, width:int, output_directory:str=".\\clean_pics"):
    utils.ensure_directory_exists(output_directory)

    try:
        img, scale, img_display = prep_show_image(image_path, width=width)
        if isinstance(img_display, str):
            return "Wrong format for img_display"
    except:
        return "Error preparing image for display"

    try:
        cropped_img, box = cropping_box(img_display, img, scale)
        saving_image(cropped_img, image_path, output_directory)
        if box == [0,0,0,0]:
            print(f"No crop selected for {image_path}. Skipping.")
            return
        else:
            return f"Image {image_path} cropped and saved to {output_directory}"
    except:
        return "Error during cropping process"
    
def cropping_pictures_of_directory(input_directory=".\\raw_pics", output_directory=".\\clean_pics", width:int | None = None):

    """
    main feature, allowing user to massively crop images in input_directory and save them to output_directory
    
    """

    if width is None:
        screen_size = utils.get_screen_size()
        width = int(screen_size['width'] * 0.5)

    image_paths = utils.get_paths(input_directory, format='.png')
    for image_path in image_paths:
        print(selec_crop_image(image_path, width, output_directory))
