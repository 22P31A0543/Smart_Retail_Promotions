import random
from models import Product, SessionLocal

sample_products = [
    ("P001", "Blue T-shirt"),
    ("P002", "Wireless Mouse"),
    ("P003", "Red Mug"),
    ("P004", "Notebook"),
    ("P005", "Bluetooth Speaker"),
    ("P006", "Desk Lamp"),
    ("P007", "Water Bottle"),
    ("P008", "USB-C Cable"),
    ("P009", "Backpack"),
    ("P010", "Fitness Tracker"),
]

placeholder_url = "https://via.placeholder.com/150"

def populate_products():
    db = SessionLocal()
    for sku, name in sample_products:
        price = round(random.uniform(5, 200), 2)
        product = Product(
            SKU=sku,
            ProductName=name,
            Price=price,
            ImageURL=placeholder_url
        )
        db.merge(product)  # merge to avoid duplicate PK errors
    db.commit()
    db.close()

if __name__ == "__main__":
    populate_products()
