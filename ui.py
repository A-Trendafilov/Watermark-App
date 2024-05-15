from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QLabel,
    QMessageBox,
    QFileDialog,
    QLineEdit,
    QComboBox,
    QColorDialog,
    QSlider,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
)


class ClientView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark App")
        # Create layout handler widget to manage the layout
        self.layout_handler = LayoutHandler()
        # Set layout handler as central widget
        self.setCentralWidget(self.layout_handler)


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        # Upload image button
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.setFixedWidth(170)
        # Save image button
        self.save_btn = QPushButton("Save Image")
        self.save_btn.setFixedWidth(170)
        # Add watermark button
        self.add_mark_btn = QPushButton("Add Watermark")
        self.add_mark_btn.setFixedWidth(170)
        # Remove watermark button
        self.rmv_mark_btn = QPushButton("Remove Watermark")
        self.rmv_mark_btn.setFixedWidth(170)
        # Pick color button
        self.color_btn = QPushButton("Pick Color")
        self.color_btn.setFixedWidth(170)
        self.color_btn.setFixedHeight(41)
        # Image display label
        self.image = QLabel()
        self.image.setMinimumSize(500, 500)

        # Watermark text label
        self.watermark_text_label = QLabel("  Watermark Text:")
        # Watermark font label
        self.watermark_font_label = QLabel("  Watermark Font:")
        # Watermark text input field
        self.watermark_text = QLineEdit("Watermark")
        # Watermark font selection dropdown
        self.watermark_font = QComboBox()
        self.watermark_font.addItems(
            [
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
        )
        # Transparency label
        self.transparency_label = QLabel("  Transparency:")
        # Transparency value input field
        self.transparency_value = QLineEdit("128")
        # Transparency slider
        self.transparency = QSlider(Qt.Orientation.Horizontal)
        self.transparency.setRange(0, 255)
        self.transparency.setValue(int(self.transparency_value.text()))

        # Color code input field
        self.color_code = QLineEdit("#000000")
        # Color pallet display label
        self.color_pallet = QLabel()
        self.color_pallet.setMinimumSize(170, 40)
        self.color_pallet.setStyleSheet("background-color: #000000;")


class LayoutHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.widget = Widget()
        # Main layout manager for the window
        self.main_layout = QHBoxLayout(self)

        # Control frame for buttons and inputs
        self.ctrl_frame = QFrame()
        self.ctrl_frame.setFixedWidth(365)
        # Layout manager for control frame
        self.ctrl_layout = QFormLayout(self.ctrl_frame)
        # Image display frame
        self.img_frame = QFrame()
        # Layout manager for image frame
        self.img_layout = QVBoxLayout(self.img_frame)

        # Add buttons and inputs to the control layout
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

        # Add image display to the image layout
        self.img_layout.addWidget(self.widget.image)

        # Connect button clicks and slider changes to event handlers
        self.on = ButtonHandler(self.widget)
        self.widget.upload_btn.clicked.connect(self.on.upload_img)
        self.widget.save_btn.clicked.connect(self.on.save_img)
        self.widget.add_mark_btn.clicked.connect(self.on.add_mark)
        self.widget.rmv_mark_btn.clicked.connect(self.on.rmv_mark)
        self.widget.color_btn.clicked.connect(self.on.pick_color)
        self.widget.transparency.valueChanged.connect(self.on.update_transparency_value)

        # Add control frame and image frame to the main layout
        self.main_layout.addWidget(self.ctrl_frame)
        self.main_layout.addWidget(self.img_frame)


class ButtonHandler:
    def __init__(self, widget):
        self.widget = widget
        self.original_image = None

    def upload_img(self):
        # Open file dialog to upload an image file
        file, _ = QFileDialog.getOpenFileName(
            None, "Open File", "C:\\", "Image Files (*.png *.jpg *.bmp)"
        )
        if file:
            # Load the selected image and display it
            self.original_image = QPixmap(file)
            self.widget.image.setPixmap(self.original_image)
            self.widget.image.adjustSize()

    def save_img(self):
        if not self.original_image:
            # Show warning if no image is loaded
            QMessageBox.warning(None, "Warning", "No image to save.")
            return

        # Open file dialog to save the image
        file, _ = QFileDialog.getSaveFileName(
            None, "Save Image", "C:\\", "PNG File (*.png);;JPEG File (*.jpg)"
        )
        if file:
            # Save the image
            pixmap = self.widget.image.pixmap()
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
                # Show warning if no image is loaded
                QMessageBox.warning(None, "Warning", "No image to watermark.")
                return

            # Create a copy of the original image
            image = self.original_image.copy()
            painter = QPainter(image)
            color = QColor(self.widget.color_code.text())
            alpha = int(self.widget.transparency_value.text())
            color.setAlpha(alpha)
            painter.setPen(color)

            # Calculate font size (one-tenth of the smaller dimension of the image)
            font_size = min(image.size().width(), image.size().height()) // 10
            font = QFont(self.widget.watermark_font.currentText(), font_size)
            painter.setFont(font)

            # Calculate text position (centered diagonally)
            text_center = image.rect().center()
            text_rect = QRect(
                text_center.x()
                - font_size * len(self.widget.watermark_text.text()) // 2,
                text_center.y() - font_size // 2,
                font_size * len(self.widget.watermark_text.text()),
                font_size,
            )

            # Rotate painter by 45 degrees
            painter.translate(text_rect.center())
            painter.rotate(-45)
            painter.translate(-text_rect.center())

            # Draw diagonal text
            painter.drawText(
                text_rect,
                Qt.AlignmentFlag.AlignCenter,
                self.widget.watermark_text.text(),
            )
            painter.end()

            # Display the watermarked image
            self.widget.image.setPixmap(image)
        except Exception as err:
            # Show error message if an error occurs
            QMessageBox.warning(
                None, "Error", f"An error occurred while adding watermark: {err}"
            )

    def rmv_mark(self):
        if self.original_image:
            # Restore the original image
            self.widget.image.setPixmap(self.original_image)

    def pick_color(self):
        # Open color picker dialog
        color = QColorDialog.getColor()
        if color.isValid():
            # Update color code input field and color pallet label
            self.widget.color_pallet.setStyleSheet(f"background-color: {color.name()};")
            self.widget.color_code.setText(color.name())

    def update_transparency_value(self, value):
        # Update transparency value input field
        self.widget.transparency_value.setText(str(value))
