import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageBrowserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Browser")
        self.root.geometry("800x600")

        self.images_per_page = 20
        self.total_images = 100  # Total number of images
        self.current_page = 0
        self.image_folder = "images"  # Folder containing images
        self.image_list = self.load_images()

        self.create_widgets()
        self.display_images()

    def create_widgets(self):
        # Create a frame for image thumbnails
        self.thumbnail_frame = tk.Frame(self.root)
        self.thumbnail_frame.pack(expand=True, fill=tk.BOTH)

        # Navigation buttons
        self.nav_frame = tk.Frame(self.root)
        self.nav_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=20)

        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.RIGHT, padx=20)

        self.select_button = tk.Button(self.nav_frame, text="Select Query Image", command=self.select_image)
        self.select_button.pack(side=tk.RIGHT, padx=20)

    def load_images(self):
        # Load the actual images from the folder
        image_list = []
        for i in range(1, self.total_images + 1):
            image_path = os.path.join(self.image_folder, f"{i}.jpg")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                image_list.append(img)
            else:
                # If the image does not exist, append a placeholder (optional)
                img = Image.new("RGB", (100, 100), (255, 0, 0))  # Placeholder red image
                image_list.append(img)
        return image_list

    def display_images(self):
        # Clear the previous thumbnails
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()

        start_index = self.current_page * self.images_per_page
        end_index = min(start_index + self.images_per_page, self.total_images)

        for i in range(start_index, end_index):
            img = self.image_list[i]
            img_resized = img.resize((100, 100))  # Resize for thumbnail
            img_tk = ImageTk.PhotoImage(img_resized)

            label = tk.Label(self.thumbnail_frame, image=img_tk)
            label.image = img_tk  # Keep a reference to prevent garbage collection
            label.pack(side=tk.LEFT, padx=5, pady=5)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_images()

    def next_page(self):
        if (self.current_page + 1) * self.images_per_page < self.total_images:
            self.current_page += 1
            self.display_images()

    def select_image(self):
        # Handle query image selection
        selected_image = filedialog.askopenfilename(initialdir=self.image_folder, title="Select an Image")
        if selected_image:
            messagebox.showinfo("Query Image", f"Selected: {selected_image}")
        else:
            messagebox.showwarning("No Image Selected", "Please select a query image.")