import tkinter
from tkinter import ttk


# Frames
class FramesCreator:
    @staticmethod
    def create_image():
        return ttk.LabelFrame(text="Image")

    @staticmethod
    def create_controls():
        return ttk.LabelFrame(text="Parameters:")


# Labels
class LabelsCreator:
    @staticmethod
    def create_image(frame):
        return ttk.Label(frame)

    @staticmethod
    def font_size(frame):
        return ttk.Label(frame, text=f"{'Font Size'}: {10}")

    @staticmethod
    def height_pos(frame):
        return ttk.Label(frame, text=f"{'Height'}: {10}")

    @staticmethod
    def width_pos(frame):
        return ttk.Label(frame, text=f"{'Width'}: {10}")

    @staticmethod
    def rotation_pos(frame):
        return ttk.Label(frame, text=f"{'Rotation'}: {10}")


# TextArea
class TextCreator:
    @staticmethod
    def watermark_text(frame):
        return tkinter.Text(frame, height=7, width=23)


# Sliders
class SlidersCreator:
    @staticmethod
    def font_size(frame, command):
        return ttk.Scale(
            frame,
            from_=10,
            to=100,
            orient=tkinter.HORIZONTAL,
            length=200,
            command=command,
        )

    @staticmethod
    def h_pos(frame, command, to):
        return ttk.Scale(
            frame,
            from_=10,
            to=to,
            orient=tkinter.HORIZONTAL,
            command=command,
        )

    @staticmethod
    def w_pos(frame, command, to):
        return ttk.Scale(
            frame,
            from_=10,
            to=to,
            orient=tkinter.HORIZONTAL,
            length=200,
            command=command,
        )

    @staticmethod
    def angle_pos(frame, command):
        return ttk.Scale(
            frame,
            from_=-180,
            to=180,
            orient=tkinter.HORIZONTAL,
            length=200,
            command=command,
        )


# Buttons
class ButtonsCreator:
    @staticmethod
    def select(frame, command):
        return ttk.Button(
            frame,
            text="Select Image",
            width=30,
            command=command,
        )

    @staticmethod
    def save(frame, command):
        return ttk.Button(
            frame,
            text="Save As",
            state=tkinter.DISABLED,
            width=30,
            command=command,
        )

    @staticmethod
    def add_watermark(frame, command):
        return ttk.Button(
            frame,
            text="Add Watermark",
            command=command,
            state=tkinter.DISABLED,
            width=30,
        )

    @staticmethod
    def remove_watermark(frame, command):
        return ttk.Button(
            frame,
            text="Remove Watermark",
            command=command,
            width=30,
        )
