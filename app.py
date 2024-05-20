from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import (QColorDialog, QComboBox, QFileDialog, QFormLayout,
                             QFrame, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton, QSlider,
                             QVBoxLayout, QWidget)

FONTS = [
    "Helvetica",
    "Futura",
    "Garamond",
    "Times",
    "Arial",
    "Verdana",
    "Comic Sans",
    "Trebuchet",
    "Gill Sans",
    "Georgia",
    "Segoe Script",
    "Gabriola",
]


class ClientViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark App")
        self.app_layout = AppLayoutWidget()
        self.setCentralWidget(self.app_layout)


class AppWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.original_image = None

        self.upload_btn = self.create_btn("Upload Image")
        self.save_btn = self.create_btn("Save Image")
        self.add_mark_btn = self.create_btn("Add Watermark")
        self.rmv_mark_btn = self.create_btn("Remove Watermark")
        self.color_btn = self.create_btn("Pick Color", height=41)

        self.image = self.create_label()
        self.watermark_text_label = self.create_label("  Watermark Text:")
        self.watermark_font_label = self.create_label("  Watermark Font:")
        self.transparency_label = self.create_label("  Transparency:")
        self.color_pallet = self.create_label(
            size=(170, 40), style="background-color: #000000;"
        )

        self.color_code = self.create_line_edit("#000000")
        self.watermark_text = self.create_line_edit("Watermark")
        self.transparency_value = self.create_line_edit("128")

        self.transparency = self.create_slider((0, 255), self.transparency_value.text())

        self.watermark_font = self.create_combobox(fonts=FONTS)

        self.upload_btn.clicked.connect(self.upload_img)
        self.save_btn.clicked.connect(self.save_img)
        self.add_mark_btn.clicked.connect(self.add_mark)
        self.rmv_mark_btn.clicked.connect(self.rmv_mark)
        self.color_btn.clicked.connect(self.pick_color)
        self.transparency.valueChanged.connect(self.update_transparency_value)

    @staticmethod
    def create_btn(name, width=170, height=None):
        btn = QPushButton(name)
        btn.setFixedWidth(width)
        if height:
            btn.setFixedHeight(height)
        return btn

    @staticmethod
    def create_label(name=None, size=None, style=None):
        label = QLabel(name)
        if size:
            label.setMinimumSize(size[0], size[1])
        if style:
            label.setStyleSheet(style)
        return label

    @staticmethod
    def create_line_edit(name):
        line_edit = QLineEdit(name)
        return line_edit

    @staticmethod
    def create_slider(s_range=None, value=None):
        slider = QSlider(Qt.Orientation.Horizontal)
        if s_range:
            slider.setRange(s_range[0], s_range[1])
        if value:
            slider.setValue(int(value))
        return slider

    @staticmethod
    def create_combobox(fonts=None):
        combobox = QComboBox()
        if fonts:
            combobox.addItems(fonts)

        return combobox

    def upload_img(self):

        file, _ = QFileDialog.getOpenFileName(
            None, "Open File", "C:\\", "Image Files (*.png *.jpg *.bmp)"
        )
        if file:
            self.original_image = QPixmap(file)
            self.image.setPixmap(self.original_image)
            self.image.adjustSize()

    def save_img(self):
        if not self.original_image:
            QMessageBox.warning(None, "Warning", "No image to save.")
            return

        file, _ = QFileDialog.getSaveFileName(
            None, "Save Image", "C:\\", "PNG File (*.png);;JPEG File (*.jpg)"
        )
        if file:
            pixmap = self.image.pixmap()
            if pixmap:
                pixmap.save(file)
                QMessageBox.information(None, "Success", "Image saved successfully.")
            else:
                QMessageBox.warning(None, "Warning", "No image to save.")
        else:
            QMessageBox.warning(None, "Warning", "No file selected.")

    def add_mark(self):
        try:
            if not self.original_image:

                QMessageBox.warning(None, "Warning", "No image to watermark.")
                return

            image = self.original_image.copy()
            painter = QPainter(image)
            color = QColor(self.color_code.text())
            alpha = int(self.transparency_value.text())
            color.setAlpha(alpha)
            painter.setPen(color)

            font_size = min(image.size().width(), image.size().height()) // 10
            font = QFont(self.watermark_font.currentText(), font_size)
            painter.setFont(font)

            text_center = image.rect().center()
            text_rect = QRect(
                text_center.x() - font_size * len(self.watermark_text.text()) // 2,
                text_center.y() - font_size // 2,
                font_size * len(self.watermark_text.text()),
                font_size,
            )

            painter.translate(text_rect.center())
            painter.rotate(-45)
            painter.translate(-text_rect.center())

            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignCenter,
                self.watermark_text.text(),
            )
            painter.end()

            self.image.setPixmap(image)
        except Exception as err:
            QMessageBox.warning(
                None, "Error", f"An error occurred while adding watermark: {err}"
            )

    def rmv_mark(self):
        if self.original_image:
            self.image.setPixmap(self.original_image)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_pallet.setStyleSheet(f"background-color: {color.name()};")
            self.color_code.setText(color.name())

    def update_transparency_value(self, value):
        self.transparency_value.setText(str(value))


class AppLayoutWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = AppWidget()
        self.main_layout = QHBoxLayout(self)
        self.ctrl_frame = QFrame()
        self.ctrl_frame.setFixedWidth(365)
        self.ctrl_layout = QFormLayout(self.ctrl_frame)
        self.img_frame = QFrame()
        self.img_layout = QVBoxLayout(self.img_frame)

        self.ctrl_layout.addRow(self.widget.upload_btn, self.widget.save_btn)
        self.ctrl_layout.addRow(self.widget.add_mark_btn, self.widget.rmv_mark_btn)
        self.ctrl_layout.addRow(
            self.widget.watermark_text_label, self.widget.watermark_text
        )
        self.ctrl_layout.addRow(
            self.widget.watermark_font_label, self.widget.watermark_font
        )
        self.ctrl_layout.addRow(
            self.widget.transparency_label, self.widget.transparency
        )
        self.ctrl_layout.addRow(QWidget(), self.widget.transparency_value)
        self.ctrl_layout.addRow(self.widget.color_btn, self.widget.color_code)
        self.ctrl_layout.addRow(QWidget(), self.widget.color_pallet)

        self.img_layout.addWidget(self.widget.image)

        self.main_layout.addWidget(self.ctrl_frame)
        self.main_layout.addWidget(self.img_frame)
