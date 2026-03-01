from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
import os
import sys


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class InstructionsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instructions")
        self.resize(800, 600)

        # Create layout
        layout = QVBoxLayout(self)

        # Create text browser for displaying markdown/html
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        layout.addWidget(self.text_browser)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Load the instructions markdown file
        self.load_instructions()

    def load_instructions(self):
        """Load and display the instructions markdown file"""
        instructions_file = resource_path("instructions.md")

        if os.path.exists(instructions_file):
            try:
                with open(instructions_file, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()

                # Qt 5.14+ supports markdown rendering
                self.text_browser.setMarkdown(markdown_content)
            except Exception as e:
                self.text_browser.setPlainText(f"Error loading instructions: {str(e)}")
        else:
            self.text_browser.setHtml("""
                <h2>Instructions</h2>
                <p><i>instructions.md file not found</i></p>
                <p>Create an <b>instructions.md</b> file in the same directory as the executable
                to display custom instructions here.</p>
                <h3>Quick Start:</h3>
                <ul>
                    <li><b>File → Open</b>: Load a Run8 industry configuration file (.ind)</li>
                    <li><b>Double-click</b> any row to view and edit industry details</li>
                    <li><b>File → Save</b>: Save your changes back to a file</li>
                </ul>
            """)
