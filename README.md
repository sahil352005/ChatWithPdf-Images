Here’s the updated `README.md` with a section for screenshots:

```markdown
# Chat with PDF and Images 📄🤖

A Streamlit-based app that enables users to upload PDF documents or images, extracts text from them, and allows interactive chat about the contents. This app uses Google Generative AI (Gemini API) to answer questions based on the uploaded documents.

## Features
- Upload PDF or Image (PNG, JPG, JPEG) files.
- Extract text from PDF documents or images.
- Ask questions related to the uploaded content.
- Interactive chat interface with animated styling.
- Simple, clean UI with custom CSS styles.

## Tech Stack
- **Streamlit**: For creating an interactive UI.
- **PyPDF2**: To extract text from PDF files.
- **Tesseract OCR**: To extract text from images.
- **Google Generative AI (Gemini API)**: For generating answers based on extracted text.
- **Pillow**: For image processing.

## Getting Started

### Prerequisites
1. Python 3.7+
2. [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed (ensure the path to `tesseract.exe` is correct).
3. Google Generative AI (Gemini API) key.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ChatWithPdf-Images.git
   cd ChatWithPdf-Images
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up `.env` file for API key:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```plaintext
   GOOGLE_API_KEY=your_gemini_api_key
   ```

5. **Configure Tesseract OCR Path:**
   Update the path to `tesseract.exe` in `app.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update if needed
   ```

### Usage

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Upload PDF or Image**:
   - Go to the sidebar to upload a PDF or image.
   - The app will extract text and display it in the sidebar.

3. **Interact with Chat**:
   - Ask questions about the uploaded content, and the chatbot will generate responses based on extracted text.

### File Structure

```
ChatWithPdf-Images/
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
└── .env                  # Contains the Gemini API key
```

## Screenshots

Here are some screenshots to give you a glimpse of the app's interface and functionality:
![Screenshot 2024-10-24 212659](https://github.com/user-attachments/assets/44b98534-7b22-4541-a268-56eb5ecfe9e0)
![Screenshot 2024-10-24 212907](https://github.com/user-attachments/assets/c2431c96-12e4-4d22-b49d-c98e34ddec33)
![Screenshot 2024-10-24 213032](https://github.com/user-attachments/assets/b75b8c8a-57da-49d2-a384-d23a727f8320)



## Dependencies

Refer to `requirements.txt` for all dependencies, including:
- `streamlit`
- `PyPDF2`
- `Pillow`
- `pytesseract`
- `google-generativeai`
- `langchain`

## Acknowledgements
- Thanks to [Google Generative AI (Gemini API)](https://cloud.google.com/generative-ai) for the content generation capability.
- Icons and animations inspired by CSS libraries.

## License
This project is open-source and available under the MIT License.
```

### Instructions for Adding Screenshots:
1. Place your screenshots (e.g., `home_screen.png`, `pdf_upload.png`, `chat_interface.png`) in an `assets` folder.
2. Commit the changes to GitHub to ensure the images appear in the `README.md`.

This setup gives users a visual guide along with installation and usage instructions. Let me know if you need further customization!

## License
This project is open-source and available under the MIT License.
```

Replace `yourusername` with your GitHub username. This README will provide clear guidance for setup and usage. Let me know if you'd like any other customizations!
