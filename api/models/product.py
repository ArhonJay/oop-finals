from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)
    product_quantity = Column(Integer, nullable=False)  
    product_description = Column(Text, nullable=True)
    product_review = Column(Text, nullable=True)
    product_image = Column(Text, nullable=True)
    seller_id = Column(Integer, nullable=False)

    