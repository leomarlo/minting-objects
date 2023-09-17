from PIL import Image

def compress_image(input_file_path, output_file_path, quality=50, max_size=300):
    """
    Compress and resize an image to reduce its file size.
    
    :param input_file_path: Path to the original image.
    :param output_file_path: Path to save the compressed image.
    :param quality: Quality of the compressed image (0 to 100). Lower means higher compression.
    :param max_size: Maximum width or height for the resized image.
    """
    
    # Open the image
    img = Image.open(input_file_path)
    
    # Check which dimension is bigger and then resize proportionally
    if img.width > img.height:
        new_width = max_size
        new_height = int((max_size / img.width) * img.height)
    else:
        new_height = max_size
        new_width = int((max_size / img.height) * img.width)
        
    # Resize the image
    img_resized = img.resize((new_width, new_height))
    
    # Save the image with compression
    img_resized.save(output_file_path, "JPEG", quality=quality)

