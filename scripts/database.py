from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .constants import DATABASE_URL


Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Questions(Base):
    """
    To store the questions asked on a pdf.
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    pdf_id = Column(
        Integer, ForeignKey("pdfMetadata.id", ondelete="CASCADE"), nullable=False
    )
    question = Column(String, index=True)
    answer = Column(String, index=True)


class PdfMetadata(Base):
    """
    To store the metadata of the pdfs.
    """

    __tablename__ = "pdfMetadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    upload_date = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
