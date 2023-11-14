from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.config import LOW_STOCKS
from app.models.base import CustomBaseModel


class Product(CustomBaseModel):
    __tablename__ = 'products'
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category")
    price = Column(Float)


class Sale(CustomBaseModel):
    __tablename__ = 'sales'
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product")
    quantity = Column(Integer)
    amount = Column(Float)


class Inventory(CustomBaseModel):
    __tablename__ = 'inventory'
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product")
    quantity = Column(Integer)

    @property
    def low_stocks(self):
        return self.quantity < LOW_STOCKS


class Category(CustomBaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
