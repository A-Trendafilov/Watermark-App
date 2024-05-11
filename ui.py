import ttkbootstrap as ttkb
from ttkbootstrap.constants import *


class UserInterface(ttkb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 20))
        self.pack(fill=BOTH, expand=YES)
        self.original_img = None
        self.watermark_text = ttkb.StringVar(value="")
        self.font_size = ttkb.DoubleVar(value=12)
        self.height = ttkb.DoubleVar(value=0)
        self.width = ttkb.DoubleVar(value=0)
        self.rotation = ttkb.DoubleVar(value=0)
        self.watermark_color = "#FFFFFF"

        self.create_labels(label="Font Size", variable=self.font_size)
        self.create_labels(label="Height", variable=self.height)
        self.create_labels(label="Width", variable=self.width)
        self.create_labels(label="Rotation", variable=self.rotation)

        self.create_scales(
            s_from=0,
            s_to=100,
            var=self.font_size,
            command=UserInterface.update_label(self.font_size.get, self.font_size.set),
        )

    # Create watermark text entry
    def create_text(self):
        return

    # Create all the labels
    def create_labels(self, label, variable):
        img_ctrl_container = ttkb.Frame(self)
        img_ctrl_container.pack(fill=X, expand=NO, pady=5)

        img_ctrl_label = ttkb.Label(
            master=img_ctrl_container,
            text=label,
            width=10,
        )
        img_ctrl_label.pack(side=LEFT, padx=3)

        img_ctrl_entry = ttkb.Entry(
            master=img_ctrl_container, textvariable=variable, width=8
        )
        img_ctrl_entry.pack(side=LEFT, padx=3)

    # Create all the buttons
    def create_buttons(self):
        return

    # Create all the scales
    def create_scales(
            self,
            command,
            s_from,
            s_to,
            var,
    ):
        img_ctrl_container = ttkb.Frame(self)
        img_ctrl_container.pack(fill=X, expand=NO, pady=5)

        img_ctrl_scale = ttkb.Scale(
            master=img_ctrl_container,
            from_=s_from,
            to=s_to,
            length=200,
            orient=ttkb.HORIZONTAL,
            style="primary",
            command=command,
            variable=var,
        )
        img_ctrl_scale.pack(side=LEFT, padx=3)

    # Open file func.
    def on_open(self):
        return

    # Save file func.
    def on_save(self):
        return

    # Add watermark func.
    def add_watermark(self):
        return

    # Remove watermark func.
    def remove_watermark(self):
        return

    # Update labels from scales input.
    @staticmethod
    def update_label(value, func):
        func(value)


def main():
    app = ttkb.Window("Watermarking Application", "superhero", minsize=(400, 400))
    UserInterface(app)
    app.mainloop()


if __name__ == "__main__":
    main()
