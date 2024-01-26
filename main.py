import cv2
import os
from tkinter import Tk, Label, Button, filedialog, Entry

def select_images():
    file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg")])
    image_entry.delete(0, "end")
    for file_path in file_paths:
        image_entry.insert("end", file_path + ";")

def select_logo():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    logo_entry.delete(0, "end")
    logo_entry.insert(0, file_path)

def select_output():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, "end")
    output_entry.insert(0, folder_path)

def overlay_images():
    image_paths = image_entry.get().split(";")
    logo_path = logo_entry.get()
    output_folder = output_entry.get()

    if logo_path == "" or output_folder == "":
        return

    for image_path in image_paths:
        image_path = image_path.strip()
        if image_path == "":
            continue

        # Load the logo image with alpha channel (PNG or transparent image)
        logo_image = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)

        # Load the JPEG image
        jpeg_image = cv2.imread(image_path)

        # Check if the logo image has an alpha channel (transparency)
        if logo_image.shape[2] == 4:
            # Convert the logo image to a transparent image (if needed)
            logo_image = cv2.cvtColor(logo_image, cv2.COLOR_BGRA2RGBA)
        else:
            # Create a blank alpha channel for the logo image
            alpha_channel = logo_image[:, :, 3]
            logo_image = cv2.cvtColor(logo_image, cv2.COLOR_BGR2BGRA)
            logo_image[:, :, 3] = alpha_channel

        # Resize the logo image to match the dimensions of the JPEG image
        logo_resized = cv2.resize(logo_image, (jpeg_image.shape[1], jpeg_image.shape[0]))

        # Create a mask from the logo image alpha channel
        logo_alpha = logo_resized[:, :, 3]
        mask = cv2.merge((logo_alpha, logo_alpha, logo_alpha))

        # Apply the mask to the JPEG image to keep only the logo area
        logo_area = cv2.bitwise_and(jpeg_image, mask)

        # Extract the alpha channel from the mask
        mask_alpha = mask[:, :, 0]

        # Merge the logo area with a blank alpha channel to make the background transparent
        result_with_transparency = cv2.cvtColor(logo_area, cv2.COLOR_BGR2BGRA)
        result_with_transparency[:, :, 3] = mask_alpha

        # Save the resulting image with transparency
        output_file = os.path.join(output_folder, os.path.splitext(os.path.basename(image_path))[0] + ".png")
        cv2.imwrite(output_file, result_with_transparency)

    result_label.config(text="Task completed successfully!")

# Create the main window
window = Tk()
window.title("Image Overlay")
window.geometry("400x250")

# Image entry
image_label = Label(window, text="JPEG Images:")
image_label.pack()
image_entry = Entry(window)
image_entry.pack()

# Logo entry
logo_label = Label(window, text="Logo Image (PNG):")
logo_label.pack()
logo_entry = Entry(window)
logo_entry.pack()

# Output entry
output_label = Label(window, text="Output Folder:")
output_label.pack()
output_entry = Entry(window)
output_entry.pack()

# Select buttons
# Select buttons
image_select_button = Button(window, text="Select Images", command=select_images)
image_select_button.pack()

logo_select_button = Button(window, text="Select Logo", command=select_logo)
logo_select_button.pack()

output_select_button = Button(window, text="Select Output Folder", command=select_output)
output_select_button.pack()

# Overlay button
overlay_button = Button(window, text="Overlay Images", command=overlay_images)
overlay_button.pack()

# Result label
result_label = Label(window, text="")
result_label.pack()

window.mainloop()

