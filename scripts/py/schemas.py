from pydantic import BaseModel


class RequestData(BaseModel):
    question: str
    pdf_name: str
