import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk, UnidentifiedImageError
import os
import io
import uuid

# Function to resize the image for display
def resize_image(image, max_size=(400, 400)):
    """Resize the image to fit within max_size while keeping the aspect ratio."""
    image.thumbnail(max_size, Image.LANCZOS)  # Use Image.LANCZOS for high-quality downsampling
    return image

# Function to remove background and display the processed image
def remove_background():
    global processed_image_data, output_image

    # Open file dialog to select an image file
    input_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.heic")]
    )
    if input_path:
        try:
            # Read image data and process background removal
            with open(input_path, "rb") as input_file:
                input_data = input_file.read()
            processed_image_data = remove(input_data)

            # Check if processed_image_data is valid
            try:
                # Load processed image from bytes into an Image object
                output_image = Image.open(io.BytesIO(processed_image_data))

                # Resize the image for displaying
                output_image_resized = resize_image(output_image)

                # Convert the Image object to an ImageTk object to display in the label
                processed_image = ImageTk.PhotoImage(output_image_resized)

                # Display the processed image in the label
                output_label.config(image=processed_image)
                output_label.image = processed_image

                messagebox.showinfo("Success", "Background removed! Now click 'Save Image' to save it.")
            except UnidentifiedImageError:
                messagebox.showerror("Error", "Failed to identify processed image data as a valid image format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")

# Function to save the processed image with a location of the user's choice
def save_image():
    if processed_image_data:
        # Open a "Save As" dialog to choose the save location and filename
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")],
            title="Save Image As"
        )
        if output_path:
            # Save the processed image at the selected location
            with open(output_path, "wb") as output_file:
                output_file.write(processed_image_data)

            messagebox.showinfo("Success", f"Image saved successfully at {output_path}!")
    else:
        messagebox.showwarning("Warning", "No processed image to save!")

# Initialize tkinter window
root = tk.Tk()
root.title("Background Remover")

# Button to select image and remove background
load_button = tk.Button(root, text="Load Image", command=remove_background)
load_button.pack(pady=10)

# Label to display the processed image
output_label = tk.Label(root)
output_label.pack()

# Button to save the processed image
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(pady=10)

processed_image_data = None
output_image = None

# Start the GUI event loop
root.mainloop()
