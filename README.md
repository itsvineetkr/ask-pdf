# Ask PDF

This web application utilizes Langchain and FAST Api to help query PDFs and ask questions about it. 
It also maintains history and supports speech-to-text functionality, so you can ask questions in any language by just saying it.
It is built using Web Sockets, making it seamless in terms of interactions.
It uses Mistral AI from Hugging Face for the language model and Huggingface embeddings for creating a vector database of documents collected out of PDF for retrieval.

## API endpoints

### 1. Homepage
- **GET `/`**: Renders the homepage with the `homepage.html` template.

### 2. Upload PDF
- **POST `/upload-pdf`**: Uploads a PDF, saves it, and creates a vector database for document retrieval.

### 3. Transcribe Audio
- **POST `/transcribe-audio`**: Accepts an audio file and returns the transcribed text.

### 4. Generate Response
- **POST `/generate-response`**: Accepts a PDF name and question, retrieves the document's content, and generates an AI-based response using tools.


## Data storing
There are two models. One is `questions` which store all the questions and their answers for a particular pdf and the other one is `pdfMetadata` which stores the metadata of all the pdfs ever uploaded.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/itsvineetkr/ask-pdf.git
    cd ask-pdf
    ```

2. **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Setting up the .env file

1. **Create a `.env` file in the root directory of your project.**

2. **Add the following environment variables to the `.env` file:**
    ```env
    HUGGINGFACEHUB_API_TOKEN = "hf_----xxxxxxx----"
    ```
    Replace `hf_----xxxxxxx----` and `<your-secret-key>` with your huggingface api key.

3. **Add the Tavily API key to the `.env` file:**
    ```env
    TAVILY_API_KEY = "<your-tavily-api-key>"
    ```
    Replace `<your-tavily-api-key>` with your Tavily API key.

## Running the Application

1. **Start the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```

    The application will be available at `http://localhost:8000/`.
