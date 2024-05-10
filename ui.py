import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk, ImageFont, ImageDraw

from widgets import *


class UserInterface(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_all_widgets()

    def create_all_widgets(self):
        self.create_frames()
        self.create_labels()
        self.create_text()
        self.create_buttons()
        self.create_sliders()

    def create_frames(self):
        self.image_frame = FramesCreator.create_image()
        self.image_frame.grid(row=0, column=0, padx=10, pady=10)
        self.controls_frame = FramesCreator.create_controls()
        self.controls_frame.grid(row=0, column=1, rowspan=5, padx=10, pady=10)

    def create_labels(self):
        self.image_label = LabelsCreator.create_image(self.image_frame)
        self.image_label.grid(row=0, column=0, padx=0, pady=0)

        self.font_size_label = LabelsCreator.font_size(self.controls_frame)
        self.font_size_label.grid(row=1, column=2, padx=0, pady=0)

        self.height_pos_label = LabelsCreator.height_pos(self.controls_frame)
        self.height_pos_label.grid(row=2, column=2, padx=0, pady=0)

        self.width_pos_label = LabelsCreator.width_pos(self.controls_frame)
        self.width_pos_label.grid(row=3, column=2, padx=0, pady=0)

        self.rotation_pos_label = LabelsCreator.rotation_pos(self.controls_frame)
        self.rotation_pos_label.grid(row=4, column=2, padx=0, pady=0)

    def create_text(self):
        self.watermark_text = TextCreator.watermark_text(self.controls_frame)
        self.watermark_text.grid(row=1, column=0, rowspan=4, padx=1, pady=1)

    def create_sliders(self):
        self.font_size_slider = SlidersCreator.font_size(
            self.controls_frame, self.update_font_labels
        )
        self.font_size_slider.grid(row=1, column=1, padx=1, pady=1)

        self.h_pos_slider = SlidersCreator.h_pos(
            self.controls_frame, self.update_height_labels
        )
        self.h_pos_slider.grid(row=2, column=1, padx=1, pady=1)

        self.w_pos_slider = SlidersCreator.w_pos(
            self.controls_frame, self.update_width_labels
        )
        self.w_pos_slider.grid(row=3, column=1, padx=1, pady=1)

        self.angle_pos_slider = SlidersCreator.angle_pos(
            self.controls_frame, self.update_rotation_labels
        )
        self.angle_pos_slider.grid(row=4, column=1, padx=1, pady=1)

    def create_buttons(self):
        self.select_button = ButtonsCreator.select(self.controls_frame, self.open_image)
        self.select_button.grid(row=0, column=0, padx=2, pady=2)

        self.save_button = ButtonsCreator.save(self.controls_frame, self.save_image)
        self.save_button.grid(row=0, column=1, padx=2, pady=2)

        self.add_watermark_button = ButtonsCreator.add_watermark(
            self.controls_frame, self.add_watermark
        )
        self.add_watermark_button.grid(row=5, column=0, padx=2, pady=2)

        self.remove_watermark_button = ButtonsCreator.remove_watermark(
            self.controls_frame, self.remove_watermark
        )
        self.remove_watermark_button.grid(row=5, column=1, padx=2, pady=2)

    def open_image(self):
        file_path = filedialog.askopenfilename(
            initialdir="c:\\", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.original_image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.original_image)
            self.image_label.config(image=self.photo)
            self.add_watermark_button.config(state=tk.NORMAL)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpeg",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg"),
                ("All files", "*.*"),
            ],
        )
        if file_path:
            self.image.save(file_path)
            self.save_button.config(state=tk.NORMAL)

    def add_watermark(self):
        font_size = int(self.font_size_slider.get())
        watermark_font = ImageFont.truetype("arial.ttf", font_size)
        self.watermarked_image = self.original_image.copy()
        draw = ImageDraw.Draw(self.watermarked_image)
        draw.text(
            xy=(int(self.h_pos_slider.get()), int(self.w_pos_slider.get())),
            text=self.watermark_text.get("1.0", "end-1c"),
            fill="white",
            font=watermark_font,
        )
        self.photo = ImageTk.PhotoImage(self.watermarked_image)
        self.image_label.config(image=self.photo)

    def remove_watermark(self):
        self.image_label.config(image=self.photo)

    def update_font_labels(self, value):
        rounded_value = int(round(float(value)))
        self.font_size_label.config(text=f"Font Size: {rounded_value}")

    def update_height_labels(self, value):
        rounded_value = int(round(float(value)))
        self.height_pos_label.config(text=f"Height: {rounded_value}")

    def update_width_labels(self, value):
        rounded_value = int(round(float(value)))
        self.width_pos_label.config(text=f"Width: {rounded_value}")

    def update_rotation_labels(self, value):
        rounded_value = int(round(float(value)))
        self.rotation_pos_label.config(text=f"Rotation: {rounded_value}")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermarking Application")
        self.minsize(400, 400)

        self.labelFrame = ttk.LabelFrame(self, text="Select file")
        self.labelFrame.grid(row=0, column=0, padx=20, pady=20)
        self.user_interface = UserInterface(self.labelFrame)
        self.user_interface.grid(row=0, column=0)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
