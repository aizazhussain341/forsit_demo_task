import datetime
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func, and_, desc
from sqlalchemy.orm import Session
from datetime import date

from app.dependancies import get_db
from app.schema import schema
from app.models import Sale, Category, Product, Inventory
from app.schema.schema import InventoryBaseValidator, ProductBaseValidator
from dateutil.relativedelta import relativedelta


app = FastAPI()


@app.get("/sales/", response_model=List[schema.SaleBaseValidator])
def get_sales(
        start_date: date = None,
        end_date: date = None,
        product_id: int = None,
        category_id: int = None,
        db: Session = Depends(get_db)
):
    sales_data_query = db.query(Sale)
    if product_id:
        sales_data_query = sales_data_query.filter(Sale.product_id == product_id)
    if category_id:
        join_condition = Category.id == Product.category_id
        sales_data_query = sales_data_query.join(Product)
        sales_data_query = sales_data_query.join(Category, join_condition).filter(Category.id == category_id)
    if start_date and end_date:
        sales_data_query = sales_data_query.filter(Sale.updated_at >= end_date, Sale.updated_at <= start_date)
    return sales_data_query.all()


@app.get("/revenue/")
def get_revenue(interval: str = "daily", db: Session = Depends(get_db)):
    start_date = date.today().strftime("%d/%m/%Y")
    end_date = (date.today() - relativedelta(days=1)).strftime("%d/%m/%Y")
    if interval == 'weekly':
        start_date = date.today().strftime("%d/%m/%Y")
        end_date = (date.today() - datetime.timedelta(days=7)).strftime("%d/%m/%Y")
    elif interval == 'monthly':
        start_date = date.today().strftime("%d/%m/%Y")
        end_date = (date.today() - relativedelta(months=1)).strftime("%d/%m/%Y")
    elif interval == 'annual':
        start_date = date.today().strftime("%d/%m/%Y")
        end_date = (date.today() - relativedelta(years=1)).strftime("%d/%m/%Y")
    sales = db.query(Sale).filter(Sale.updated_at >= end_date, Sale.updated_at <= start_date).all()
    total_revenue = sum(sale.amount for sale in sales)
    if total_revenue:
        total_revenue = round(total_revenue, 2)
    return {"total_revenue": total_revenue}


@app.get("/compare-revenue/")
def compare_revenue(start_date: date = None, end_date: date = None, category_ids: List[int] = None, db: Session = Depends(get_db)):
    if not start_date:
        start_date = date.today().strftime("%d/%m/%Y")
    if not end_date:
        end_date = (date.today() - relativedelta(days=1)).strftime("%d/%m/%Y")
    revenue_by_category = db.query(Category.name, func.sum(Sale.amount).label('total_revenue'))
    if category_ids:
        revenue_by_category = revenue_by_category.filter(Category.id.in_(category_ids))
    revenue_by_category = revenue_by_category.filter(Sale.updated_at >= end_date, Sale.updated_at <= start_date).group_by(Category.name).all()
    return revenue_by_category


@app.get("/inventory/", response_model=List[InventoryBaseValidator])
def get_inventory(db: Session = Depends(get_db)):
    subquery = db.query(Inventory).group_by(Inventory.product_id).with_entities(Inventory.product_id, func.max(Inventory.updated_at).label('max_updated_at')).subquery()
    inventory = (
        db.query(Inventory)
        .join(subquery, and_(Inventory.product_id == subquery.c.product_id,
                             Inventory.updated_at == subquery.c.max_updated_at))
        .all()
    )
    return inventory


@app.get("/inventory/{product_id}/", response_model=List[InventoryBaseValidator])
def get_product_inventory(product_id: int, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).order_by(Inventory.updated_at)
    return inventory


@app.put("/inventory/{product_id}/", response_model=InventoryBaseValidator)
def update_inventory(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).order_by(desc(Inventory.updated_at)).first()
    new_inventory = Inventory(product_id=product_id, quantity=quantity)
    if inventory:
        new_inventory.quantity = inventory.quantity + quantity
    new_inventory.save(db)
    return new_inventory


@app.get("/product/", response_model=List[ProductBaseValidator])
def get_products(category_id: int = None, db: Session = Depends(get_db)):
    products = db.query(Product)
    if category_id:
        products = products.filter(Product.category_id == category_id)
    return products


@app.post("/product/", response_model=ProductBaseValidator)
def add_product(product_name: str, category_id: int, price: float, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.name == product_name).first()
    if product:
        raise HTTPException(status_code=400, detail=f"Product with name {product_name} already exists.")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail=f"Category doesn't exists.")
    product = Product(name=product_name, category_id=category_id, price=price)
    product.save(db)
    return product


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
