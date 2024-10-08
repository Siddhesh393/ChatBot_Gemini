# Chat PDF with Gemini 💬📄

This project allows users to interact with PDF documents by asking questions. It leverages Google's Gemini API and FAISS for embedding and searching through the text chunks of the PDFs, enabling conversational interaction with document contents. The app is built using Streamlit for the frontend, making it simple to use and deploy.

## Features

- **PDF Upload**: Users can upload multiple PDF files.
- **PDF Text Extraction**: Extract text from uploaded PDF files.
- **Text Chunking**: The extracted text is split into manageable chunks using `RecursiveCharacterTextSplitter`.
- **Vector Search with FAISS**: Convert text chunks into embeddings and store them in a FAISS vector store for similarity search.
- **Conversational AI with Google Gemini**: Uses Google's Gemini (PaLM) for answering questions based on the provided context extracted from PDFs.
- **Simple Frontend**: Built using Streamlit, allowing for easy user interaction.

## Tech Stack

- **Python**
- **Streamlit**: Frontend for interacting with the user.
- **LangChain**: For managing the document loading, vector store integration, and building the QA chain.
- **Google Generative AI (Gemini)**: Used for embeddings and conversational AI.
- **FAISS**: Vector similarity search.
- **PyPDF**: To read and extract text from PDF files.
- **dotenv**: For loading environment variables like API keys.
  
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/Chat_PDF_Gemini.git
   cd Chat_PDF_Gemini
   ```
2. Create a virtual environment
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux/macOS
    venv\Scripts\activate      # Windows
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up the environment variables. Create a .env file in the root of the project and add your Google Gemini API key:
    ```bash
    GOOGLE_API_KEY=your_google_gemini_api_key
    ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Launch the application using the above command.
2. Upload PDF files via the sidebar.
3. Once the files are uploaded, click the "Submit & Process" button to extract and process the text from the PDFs.
4. In the main interface, type your question in the input field and click enter to receive a detailed answer from the contents of the uploaded PDF files.

## File Structure

- **app.py:** Main file that contains the logic for the Streamlit app, including PDF text extraction, chunking, and conversational logic.
- **requirements.txt:** List of required Python packages.
- **.env:** File where API keys and other environment variables are stored (not included in the repo, you need to create your own).
