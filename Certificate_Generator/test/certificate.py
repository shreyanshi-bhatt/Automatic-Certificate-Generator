from PIL import ImageFont, ImageDraw, Image
import cv2
import numpy as np
import os
from datetime import date

# Function to resize the image to fit within a specific width
def resize_image(img, max_width=800):
    height, width = img.shape[:2]
    if width > max_width:
        scale = max_width / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height))
    return img

# Read names from file
with open("names.txt", "r") as f:
    names_list = f.read().strip().split("\n")

# Read coordinates from file
with open("../coords.txt", "r") as f:
    coordinates = f.read().strip().split("\n")

# Initialize flag for displaying sample image once
flag = True

# Process each name in the names list
for i in range(len(names_list)):
    name_to_print = names_list[i]
    date_to_print = date.today()  # Change this date as per requirement
    signature_to_print = "Shreyanshi Bhatt"

    # Load image using OpenCV
    image = cv2.imread("../static/ce1.png")

    # Resize image to fit within a maximum width for better display
    image = resize_image(image)

    # Convert image from BGR to RGB (required by PIL)
    cv2_im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Convert image to PIL format
    pil_im = Image.fromarray(cv2_im_rgb)

    # Create a drawing object
    draw = ImageDraw.Draw(pil_im)

    # Define fonts and sizes (adjust paths as needed)
    font = ImageFont.truetype("./fonts/OLDENGL.TTF", 30)
    font1 = ImageFont.truetype("./fonts/MATURASC.TTF", 17)

    # Draw text on the image
    draw.text((int(coordinates[0]), int(coordinates[1])), name_to_print, font=font, fill='#283361')
    draw.text((int(coordinates[2]), int(coordinates[3])), str(date_to_print), font=font1, fill='#283361')
    draw.text((int(coordinates[4]), int(coordinates[5])), str(signature_to_print), font=font1, fill='#283361')

    # Convert PIL image back to OpenCV format
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

    # Display sample image on first iteration
    if flag:
        cv2.imshow('Certificate', cv2_im_processed)
        flag = False

    # Save processed image to output folder
    cv2.imwrite('./output/' + name_to_print + '.png', cv2_im_processed)

    # Wait for key press and close windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
