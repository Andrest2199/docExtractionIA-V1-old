from PIL import Image, ImageFilter, ImageEnhance


def deskew_and_rotate(image):
    # Convert the image to grayscale

    # Apply edge detection to find the skew angle
    edges = image.filter(ImageFilter.FIND_EDGES)
    skew_angle = -edges.rotate(45, expand=True).getbbox()[2] / 2

    # Deskew the image
    deskewed_image = image.rotate(skew_angle, expand=True)

    # Rotate the image to make it upright
    upright_image = deskewed_image.rotate(90 - skew_angle, expand=True)

    return upright_image


def background_removal(image):
    # Convert the image to grayscale
    # grayscale_image = make_grayscale(image)
    # Apply thresholding to create a binary image
    threshold = 128
    binary_image = image.point(lambda p: p > threshold and 255)

    # Perform image segmentation to separate text from background
    segmented_image = binary_image.filter(ImageFilter.FIND_EDGES)
    segmented_image = segmented_image.filter(ImageFilter.SMOOTH_MORE)

    return segmented_image


def make_grayscale(image):
    # Convert the image to grayscale
    grayscale_image = image.convert("L")
    return grayscale_image


def convert_to_1bit(image):
    # Convert the image to 1-bit (black and white)
    binary_image = image.convert("1")
    return binary_image


def resize_image(image):
    # Calculate the desired DPI
    dpi = 400

    # Calculate the new size based on the desired DPI
    width, height = image.size
    new_width = int((width / 72) * dpi)
    new_height = int((height / 72) * dpi)

    # Resize the image to the new size
    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    # Set the DPI metadata of the image
    resized_image.info["dpi"] = (dpi, dpi)

    return resized_image


def improve_image_quality(input_image_path, output_image_path):
    # Open the image file
    image = Image.open(input_image_path).convert("RGB")

    # Deskew and rotate the image
    # processed_image = deskew_and_rotate(grayscale_image)
    processed_image = resize_image(image)

    enhancer = ImageEnhance.Brightness(processed_image)
    # Apply the enhancement
    enhanced_image = enhancer.enhance(1.5)
    enhanced_image = make_grayscale(enhanced_image)

    # Save the enhanced image
    enhanced_image.save(output_image_path)
