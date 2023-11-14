# forsit-demo-task
Demo task for e-commerce


**Dependencies**

Python 3.9+

Pip

Other listed in requirements.txt

**Clone this project**

`git clone https://github.com/aizazhussain341/forsit_demo_task.git`


**Create a Virtual Environment using**

`sudo pip install virtualenv

virtualenv env`

**Activate the virtualenv**

`source env/bin/activate`

**Install dependencies**

`pip install -r requirements.txt`

## Setting up environment variables

`cp env_example .env`

Set value for variables in .env

## Creating Tables

`alembic upgrade head`

## Added test data to database

`python populate_test_data.py`

**To run the project**

`uvicorn app.main:app --reload`


# Models

### Sales

- **id** : Unique identifier for this object in the table.
- **created_at** : Datetime when object is created.
- **updated_at** : Datetime when object is last updated.
- **quantity** : Quantity of the product sold.
- **amount** : total amount of the sales.

### Category

- **id** : Unique identifier for this object in the table.
- **created_at** : Datetime when object is created.
- **updated_at** : Datetime when object is last updated.
- **name** : Name of the category this cannot be duplicated.

### Inventory

- **id** : Unique identifier for this object in the table.
- **created_at** : Datetime when object is created.
- **updated_at** : Datetime when object is last updated.
- **product_id** : id of the product against which this inventory objejct is created.
- **quantity** : Latest quantity of the product in stocks

### Product

- **id** : Unique identifier for this object in the table.
- **created_at** : Datetime when object is created.
- **updated_at** : Datetime when object is last updated.
- **name** : Name of the product cannot be duplicated
- **price** : Price of the product
- **category_id** : Category id of category under which product exist.

# Endpoints

## /sales/
This endpoint returns sales data by date range, specific product or category.

### Allowed Methods
- GET

### parameters
- **start_date** : start date from when filter sales data from
- **end_date** : end date till when the data should be filters
- **product_id** : product id against which sales data should be listed
- **category_id** : category id against which sales data should be listed.

## /revenue/
This endpoint returns revenue for current day, week, month or year.

### Allowed Methods
- GET

### parameters
- **interval** : can be daily,weekly,monthly or annual which select the filter for revenue.

## /compare-revenue/
This endpoint returns list of revenue against multiple categories in specific time period.

### Allowed Methods
- GET

### parameters
- **start_date** : start date from when revenue should be calculated.
- **end_date** : end date till when revenue should be calculated.
- **category_ids** : List of category ids against which revenue data should be listed.

## /inventory/
This endpoint returns list of current inventory status of each product in database.

### Allowed Methods
- GET

## /inventory/{product_id}/
This endpoint returns inventory history of product in database and update inventory as well.

### Allowed Methods
- GET
- PUT

### parameters (GET)
- **product_id** : product id whos inventory history should be listed.

### parameters (PUT)
- **product_id** : product id to update inventory.
- **quantity** : New quantity of the product.

## /product/
This endpoint returns list of product in database and register new products.

### Allowed Methods
- GET
- POST

### parameters (GET)
- **category_id** : category id which will be used to filter product list.

### parameters (POST)
- **product_name** : Name of the new product.
- **category_id** : Category id of the category for new product.
- **price** : : Price of the new product.


