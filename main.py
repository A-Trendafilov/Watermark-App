from PyQt6.QtWidgets import QApplication

from ui import ClientView


def main():
    # Create the application instance
    app = QApplication([])
    # Create the main window
    window = ClientView()
    # Apply style using external stylesheet
    with open("style.css", "r") as file:
        window.setStyleSheet(file.read())

    # Show the main window
    window.show()
    # Run the application event loop
    app.exec()


if __name__ == "__main__":
    main()
