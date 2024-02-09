from PIL import Image
import numpy as np
import cv2
import math
from typing import Tuple, Union
from deskew import determine_skew

"""
    Additional documentation:
    https://www.leadtools.com/help/sdk/v21/main/api/deskewing.html
"""

def get_skew_angle(cvImage) -> float:
    """ "
    Get the skew angle of the image using Hough Transform
    return the average angle of the lines in the image
    rtype: float
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(cvImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    edges = cv2.Canny(blur, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, 100, minLineLength=10, maxLineGap=250
    )
    angles = []
    # calculate the angle of each line
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi
        angles.append(angle)

    # return the average angle
    return np.mean(angles)


def deskew_and_rotate(image, output_path):
    """ "
    Deskew and rotate the image
    rtpe: PIL.Image.Image
    """
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, (0, 0, 0))
    cv2.imwrite(output_path, rotated)
    output_image = Image.open(output_path)
    return output_image


def convert_to_1bit(image):
    """ "
    Convert the image to 1-bit (black and white)
    rtype: PIL.Image.Image
    """
    np_image = np.array(image)
    np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(
        np_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )  # imgf contains Binary image

    return binary_image

def rotate(
    image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(
        np.cos(angle_radian) * old_width
    )
    height = abs(np.sin(angle_radian) * old_width) + abs(
        np.cos(angle_radian) * old_height
    )

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(
        image, rot_mat, (int(round(height)), int(round(width))), borderValue=background
    )


def improve_image_quality(input_image_path, output_image_path):

    raw_image = cv2.imread(input_image_path)
    skewed_angle = get_skew_angle(raw_image)
    if abs(skewed_angle) > 0.5:
        print(f"Image {input_image_path} is skewed by {skewed_angle} degrees")
        deskewed_image = deskew_and_rotate(raw_image, output_image_path)
    else:
        deskewed_image = raw_image
    bin_img = convert_to_1bit(deskewed_image)
    cv2.imwrite(output_image_path, bin_img)
    print(f"Image {input_image_path} improved and saved to {output_image_path}")
