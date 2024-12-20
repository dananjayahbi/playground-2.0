import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout,
    QWidget, QLineEdit, QLabel, QFileDialog, QMessageBox, QHBoxLayout
)
import google.generativeai as genai

class GeminiTextGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Text Generator - Gemini API")
        self.setGeometry(100, 100, 600, 400)
        self.api_key = ""

        # Main Layout
        self.layout = QVBoxLayout()

        # Prompt Input
        self.prompt_label = QLabel("Enter your prompt:")
        self.layout.addWidget(self.prompt_label)
        self.prompt_input = QTextEdit()
        self.layout.addWidget(self.prompt_input)

        # Generate Button
        self.generate_button = QPushButton("Generate Text")
        self.generate_button.clicked.connect(self.generate_text)
        self.layout.addWidget(self.generate_button)

        # Generated Output
        self.output_label = QLabel("Generated Text:")
        self.layout.addWidget(self.output_label)
        self.generated_output = QTextEdit()
        self.generated_output.setReadOnly(True)
        self.layout.addWidget(self.generated_output)

        # Buttons for Save and Clear
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save to File")
        self.save_button.clicked.connect(self.save_to_file)
        button_layout.addWidget(self.save_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_button)

        self.layout.addLayout(button_layout)

        # API Key Input
        self.api_key_label = QLabel("API Key:")
        self.layout.addWidget(self.api_key_label)
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your Gemini API key")
        self.layout.addWidget(self.api_key_input)

        # Central Widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def generate_text(self):
        prompt = self.prompt_input.toPlainText()
        self.api_key = self.api_key_input.text()

        if not self.api_key or not prompt:
            QMessageBox.warning(self, "Error", "Please provide both API key and a prompt.")
            return

        try:
            # Configure the Gemini API with the provided key
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            # Generate content
            response = model.generate_content(prompt)
            generated_text = response.text if response else "No response received."

            self.generated_output.setPlainText(generated_text)

        except Exception as e:
            QMessageBox.critical(self, "API Error", f"An error occurred: {e}")
            self.generated_output.setPlainText("")

    def save_to_file(self):
        text = self.generated_output.toPlainText()
        if text:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options
            )
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text)

    def clear_output(self):
        self.generated_output.clear()
        self.prompt_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeminiTextGeneratorApp()
    window.show()
    sys.exit(app.exec())
