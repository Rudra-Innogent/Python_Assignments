from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)

    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    company = relationship('Company', back_populates='products', lazy='joined')
    category = relationship('Category', back_populates='products', lazy='joined')
