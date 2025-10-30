from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.session import Base

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    categories = relationship('Category', back_populates='company', cascade='all, delete-orphan', lazy='selectin')
    products = relationship('Product', back_populates='company', cascade='all, delete-orphan', lazy='selectin')
