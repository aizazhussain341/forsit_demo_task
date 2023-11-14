import datetime
import random

from app.database import SessionLocal
from app.models import Product, Inventory, Category, Sale


def create_test_data():
    db = SessionLocal()
    category_names = ["Electronics", "Clothing", "Home Appliances"]
    categories = [Category(name=name) for name in category_names]
    db.add_all(categories)
    db.commit()

    products = []
    for category in categories:
        for i in range(5):
            product_name = f"{category.name} Product {i+1}"
            product = Product(name=product_name, category_id=category.id, price=random.randint(0, 1000))
            products.append(product)

    db.add_all(products)
    db.commit()

    inventories = []
    inventory_start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    for product in products:
        inventory = Inventory(product_id=product.id, quantity=100, created_at=inventory_start_date, updated_at=inventory_start_date)
        inventories.append(inventory)

    new_inventories = []
    sales = []
    for inventory in inventories:
        sales_start_date = datetime.datetime.now() - datetime.timedelta(days=30)
        product_id = inventory.product_id
        product = db.query(Product).filter(Product.id == product_id).first()
        quantity = inventory.quantity
        for _ in range(1, 3):
            quantity_sold = random.randint(1, 10)
            new_quantity = quantity - quantity_sold
            quantity = new_quantity
            sale = Sale(product_id=product_id, quantity=quantity_sold, amount=product.price * quantity_sold, created_at=sales_start_date, updated_at=sales_start_date)
            sales.append(sale)
            inventory = Inventory(product_id=product.id, quantity=new_quantity, created_at=sales_start_date, updated_at=sales_start_date)
            new_inventories.append(inventory)
            sales_start_date = sales_start_date + datetime.timedelta(days=5)
    inventories = inventories + new_inventories
    db.add_all(inventories)
    db.add_all(sales)
    db.commit()


create_test_data()
