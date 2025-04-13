# backend/app/models/guide.py
from sqlalchemy import Column, Integer, String, Text
from app.models import Base

class Guide(Base):
    __tablename__ = "guides"

    id = Column(Integer, primary_key=True, index=True)
    guide_type = Column(String, index=True)
    patient_name = Column(String, index=True)
    provider_name = Column(String)
    operator_name = Column(String)
    xml_content = Column(Text)