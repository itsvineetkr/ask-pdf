from fastapi import FastAPI, Request, File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path

from scripts.database import SessionLocal
from scripts.crud import *
from scripts.utils import VectorDBManager, save_pdf, get_transcript, get_agent
from scripts.schemas import RequestData


import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    """
    Returns the homepage with the `homepage.html` template.

    This endpoint renders the homepage of the application and is the default route.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-pdf")
async def upload_pdf(db: Session = Depends(get_db), file: UploadFile = File(...)):
    """
    Uploads a PDF, saves it to the server, and creates a vector database for retrieval.

    - **file**: The PDF file to upload.
    - **db**: Database session for storing file metadata.
    """
    try:
        await save_pdf(file, db, uploads_dir)
        await VectorDBManager.create_vector_db(file.filename, uploads_dir)

        return {"status": "ok", "response": "PDF Uploaded and Vector DB Created!"}

    except Exception as e:
        return {"status": "error", "response": f"error encountered: {e}"}


@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribes the uploaded audio file and returns the transcribed text.

    - **file**: The audio file to transcribe.
    """
    try:
        transcript = await get_transcript(file)

        return {
            "status": "ok",
            "response": "Transcript generated!",
            "transcript": transcript,
        }

    except Exception as e:
        return {"status": "error", "response": f"error encountered: {e}"}


@app.post("/generate-response")
async def generate_response(data: RequestData, db: Session = Depends(get_db)):
    """
    Generates a response based on the content of a specified PDF and a user question.

    - **pdf_name**: The name of the uploaded PDF file.
    - **question**: The question to be answered based on the PDF content.

    Returns a response from the agent's interpretation of the document.
    """
    if not data.pdf_name or not data.question:
        return {
            "status": "error",
            "response": "pdf_name and question are required fields",
        }

    pdf_name = data.pdf_name
    question = data.question

    try:
        agent = await get_agent(pdf_name, uploads_dir, db)
        response = agent.run(question)
        response = response[: response.find("Previous conversation history:")]
        add_question_in_db(db, pdf_name, question, response)
        return {"status": "ok", "response": response}

    except Exception as e:
        return {"status": "error", "response": f"error encountered: {e}"}
