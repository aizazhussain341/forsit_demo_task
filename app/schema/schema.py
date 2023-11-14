from datetime import datetime
from pydantic import BaseModel


class CategoryBaseValidator(BaseModel):
    id: int
    name: str


class ProductBaseValidator(BaseModel):
    id: int
    name: str
    category_id: int


class SaleBaseValidator(BaseModel):
    id: int
    product: ProductBaseValidator
    quantity: int
    created_at: datetime


class InventoryBaseValidator(BaseModel):
    id: int
    quantity: int
    updated_at: datetime
    product_id: int
    low_stocks: bool

