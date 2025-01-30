from sqlalchemy import delete
from sqlalchemy.orm import Session
from .database import Questions, PdfMetadata


def add_pdf_in_db(db: Session, pdf_name: str):
    db_pdf = PdfMetadata(filename=pdf_name)
    db.add(db_pdf)
    db.commit()
    db.refresh(db_pdf)
    return db_pdf


def add_question_in_db(db: Session, pdf_name: str, question: str, answer: str):
    pdf = db.query(PdfMetadata).filter_by(filename=pdf_name).first()
    pdf_id = pdf.id
    db_question = Questions(pdf_id=pdf_id, question=question, answer=answer)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_questions_from_db(db: Session, pdf_name: str):
    pdf = db.query(PdfMetadata).filter(PdfMetadata.filename == pdf_name).first()
    if pdf is None:
        return []
    pdf_id = pdf.id
    return db.query(Questions).filter(Questions.pdf_id == pdf_id).all()


def delete_question_from_db(db: Session, pdf_name: str):
    pdf = db.query(PdfMetadata).get(PdfMetadata.filename == pdf_name)
    pdf_id = pdf.id
    db.query(Questions).filter(Questions.pdf_id == pdf_id).delete()
    db.commit()
    return True
