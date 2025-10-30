from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    company = relationship('Company', back_populates='categories', lazy='selectin')

    products = relationship('Product', back_populates='category', cascade='all, delete-orphan', lazy='selectin')
