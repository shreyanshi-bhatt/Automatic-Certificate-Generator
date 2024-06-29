import cv2 as cv

# Function to resize the image to fit within a specific width
def resize_image(img, max_width=800):
    height, width = img.shape[:2]
    if width > max_width:
        scale = max_width / width
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv.resize(img, (new_width, new_height))
    return img

# Open a file to write coordinates
f = open("../coords.txt", "w")

# Mouse callback function
def draw_circle(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        # Display coordinates as green text on the image
        cv.putText(img, "coordinates (%d,%d)" % (x, y), (60, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Write coordinates to file
        f.write(str(x) + "\n")
        f.write(str(y) + "\n")

# Load an image (replace with your image path)
img = cv.imread("../static/ce1.png")

# Resize image to fit within a maximum width for better display
img = resize_image(img)

# Create a window and bind the mouse callback function
cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)

# Display the image and wait for user interaction
while True:
    cv.imshow('image', img)
    if cv.waitKey(10) & 0xFF == 27:  # Press Esc to close the window
        break

# Close all windows and release resources
cv.destroyAllWindows()
f.close()  # Close the file
