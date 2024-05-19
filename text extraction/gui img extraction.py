from PIL import Image, ImageTk
import pytesseract
import tkinter as tk
from tkinter import filedialog
import subprocess

class TextExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Extractor")

        # Specify the full path to your Tesseract executable
        self.tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

        self.image_path = None
        self.crop_coordinates = None

        # Create widgets
        self.label = tk.Label(root, text="Select an image file:")
        self.label.pack(pady=10)

        self.button_browse = tk.Button(root, text="Browse", command=self.browse_image)
        self.button_browse.pack(pady=10)

        self.canvas = tk.Canvas(root)
        self.canvas.pack()

        self.button_crop = tk.Button(root, text="Crop Text", command=self.crop_text)
        self.button_crop.pack(pady=10)

        self.text_display = tk.Text(root, height=10, width=50)
        self.text_display.pack(pady=10)

        self.button_copy = tk.Button(root, text="Copy Text", command=self.copy_text)
        self.button_copy.pack(pady=10)

        self.label_prompt = tk.Label(root, text="")
        self.label_prompt.pack(pady=5)

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if self.image_path:
            self.show_image()

    def show_image(self):
        image = Image.open(self.image_path)
        photo = ImageTk.PhotoImage(image)

        self.canvas.config(width=photo.width(), height=photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

    def crop_text(self):
        if self.image_path:
            self.root.bind("<ButtonPress-1>", self.on_click_start)
            self.root.bind("<B1-Motion>", self.on_drag)
            self.root.bind("<ButtonRelease-1>", self.on_click_end)

    def on_click_start(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_click_end(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)

        self.crop_coordinates = (min(self.start_x, end_x), min(self.start_y, end_y), max(self.start_x, end_x), max(self.start_y, end_y))

        self.root.unbind("<ButtonPress-1>")
        self.root.unbind("<B1-Motion>")
        self.root.unbind("<ButtonRelease-1>")

        extracted_text = self.extract_text_from_cropped_image()
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, extracted_text)

    def extract_text_from_cropped_image(self):
        if self.image_path and self.crop_coordinates:
            image = Image.open(self.image_path)
            cropped_image = image.crop(self.crop_coordinates)
            text = pytesseract.image_to_string(cropped_image, config='--psm 6')  # Use psm 6 for treating image as sparse text

            return text
        else:
            return "Please select an image and crop the text region first."

    def copy_text(self):
        text_to_copy = self.text_display.get(1.0, tk.END).strip()
        if text_to_copy:
            self.root.clipboard_clear()
            self.root.clipboard_append(text_to_copy)
            self.root.update()
            self.label_prompt.config(text="Text copied!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextExtractorApp(root)
    root.mainloop()

