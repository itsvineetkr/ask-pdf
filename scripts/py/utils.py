from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent

import requests
from sqlalchemy.orm import Session
from fastapi import File

from .crud import add_pdf_in_db
from .constants import HUGGINGFACEHUB_API_TOKEN, API_URL_WHISPER, MODEL_ID
from .tools import get_retrieval_tool, get_search_tool
from .prompts import AGENT_SYSTEM_MESSAGE


def get_llm():
    llm = HuggingFaceEndpoint(
        repo_id=MODEL_ID, huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
    )
    return llm


class VectorDBManager:
    def __init__(self):
        pass

    async def create_vector_db(pdf_name: str, uploads_dir: str):
        """
        Create a vector database from a PDF file.

        Args:
            pdf_name (str): Name of the PDF file.
            uploads_dir (str): Path to the uploads folder.

        ReturnspdfMetadata:
            vector database (FAISS)
        """
        pdf_path = uploads_dir / "pdfs" / pdf_name
        document = PyPDFLoader(pdf_path).load()
        splitter = RecursiveCharacterTextSplitter()
        documents = splitter.split_documents(document)

        db = FAISS.from_documents(documents, HuggingFaceEmbeddings())
        db.save_local(uploads_dir / "vec_dbs" / pdf_name)

    async def get_retriever(pdf_name: str, uploads_dir: str):
        """
        Asynchronously loads a FAISS vector database and returns a retriever object.

        Args:
            pdf_name (str): The name of the PDF file for which the retriever is to be created.
            uploads_dir (str): Path to the uploads folder.
        Returns:
            retriever: A retriever object that can be used to query the vector database.
        """
        vector_db_path = uploads_dir / "vec_dbs" / pdf_name
        vector_db = FAISS.load_local(
            vector_db_path,
            embeddings=HuggingFaceEmbeddings(),
            allow_dangerous_deserialization=True,
        )

        retriever = vector_db.as_retriever()
        return retriever


async def save_pdf(file: File, db: Session, uploads_dir: str):
    """
    Save a PDF file to the specified location and add its entry to the database.

    Args:
        file (File): The PDF file to be saved.
        db (Session): The database session to use for adding the PDF entry.
        uploads_dir (str): Path to the uploads folder.

    Returns:
        None
    """
    with open(uploads_dir / "pdfs" / file.filename, "wb") as f:
        content = await file.read()
        f.write(content)
    add_pdf_in_db(db, pdf_name=file.filename)


async def get_transcript(file: File):
    """
    Asynchronously retrieves the transcription of an audio file using the Whisper API.

    Args:
        file (File): The audio file to be transcribed.

    Returns:
        str: The transcribed text from the audio file.

    Raises:
        requests.exceptions.RequestException: If there is an issue with the API request.
    """
    audio_data = await file.read()
    headers = {"Authorization": f"Bearer {HUGGINGFACEHUB_API_TOKEN}"}
    response = requests.post(API_URL_WHISPER, headers=headers, data=audio_data)
    transcript = response.json()["text"]
    return transcript


async def get_agent(pdf_name: str, uploads_dir: str):
    """
    Asynchronously initializes and returns an agent configured for conversational interactions with a PDF document.

    Args:
        pdf_name (str): The name of the PDF document to be used for retrieval.
        uploads_dir (str): Path to the uploads folder.

    Returns:
        Agent: An initialized agent configured with tools for search and retrieval,
               a language model, and a conversational memory buffer.

    The agent is set up with the following components:
    - A conversation buffer memory to keep track of chat history.
    - A retriever obtained from the VectorDBManager using the provided PDF name.
    - A language model (LLM) obtained from the get_llm function.
    - Tools for search and retrieval.
    - A system message defined by AGENT_SYSTEM_MESSAGE.
    """
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = await VectorDBManager.get_retriever(pdf_name, uploads_dir)
    llm = get_llm()
    tools = [get_search_tool(), get_retrieval_tool(retriever)]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="conversational-react-description",
        memory=memory,
        verbose=True,
        agent_kwargs={"system_message": AGENT_SYSTEM_MESSAGE},
    )

    return agent

