# import enum
# from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Enum
# from sqlalchemy.orm import relationship, Session
# from database import Base

# class CategoryEnum(str, enum.Enum):
#     cloth = "cloth"
#     accessory = "accessory"

# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     username = Column(String(100), unique=True, nullable=False)
#     password_hash = Column(String(255), nullable=False)
#     is_logged_in = Column(Boolean, default=False)

# class Product(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     name = Column(String(100), nullable=False)
#     category = Column(Enum(CategoryEnum), nullable=False)
#     base_price = Column(Numeric(10, 2), nullable=False)

# # Updated Cart: Stores current cumulative checkout orders
# class Cart(Base):
#     __tablename__ = "cart"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     product_id = Column(Integer, ForeignKey("products.id"))
    
#     # Store calculated aggregate pricing logs per purchase unit
#     original_price = Column(Numeric(10, 2))
#     discount_applied_percentage = Column(Numeric(5, 2))
#     final_price = Column(Numeric(10, 2))

#     user = relationship("User")
#     product = relationship("Product")

# def seed_initial_products(db: Session):
#     count = db.query(Product).count()
#     if count == 0:
#         dummy_products = [
#             Product(name="Jeans", category=CategoryEnum.cloth, base_price=1200.00),
#             Product(name="T-Shirt", category=CategoryEnum.cloth, base_price=600.00),
#             Product(name="Shirt", category=CategoryEnum.cloth, base_price=900.00),
#             Product(name="Jacket", category=CategoryEnum.cloth, base_price=2500.00),
#             Product(name="Socks", category=CategoryEnum.cloth, base_price=150.00),
            
#             Product(name="Smart Watch", category=CategoryEnum.accessory, base_price=3500.00),
#             Product(name="Sunglasses", category=CategoryEnum.accessory, base_price=1500.00),
#             Product(name="Leather Belt", category=CategoryEnum.accessory, base_price=500.00),
#             Product(name="Wallet", category=CategoryEnum.accessory, base_price=700.00),
#             Product(name="Sports Cap", category=CategoryEnum.accessory, base_price=350.00),
#         ]
#         db.add_all(dummy_products)
#         db.commit()


import enum
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship, Session
from database import Base

class CategoryEnum(str, enum.Enum):
    cloth = "cloth"
    accessory = "accessory"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_logged_in = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)

# Updated Cart Table: Ek purchase order me Total Sum aur Minus ki hui Final Amount store karega
class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_ids = Column(String(255))  # Selected items IDs stored as comma separated (e.g., "1,4,5")
    total_base_sum = Column(Numeric(10, 2))  # Sabhi products ka plus total sum
    discount_percentage = Column(Numeric(5, 2))  # Kitna total % cut hua
    discount_amount = Column(Numeric(10, 2))  # Kitna amount minus hua
    final_payable_amount = Column(Numeric(10, 2))  # Minus hone ke baad bachi hui net amount

    user = relationship("User")

def seed_initial_products(db: Session):
    count = db.query(Product).count()
    if count == 0:
        dummy_products = [
            Product(name="Jeans", category=CategoryEnum.cloth, base_price=1200.00),
            Product(name="T-Shirt", category=CategoryEnum.cloth, base_price=600.00),
            Product(name="Shirt", category=CategoryEnum.cloth, base_price=900.00),
            Product(name="Jacket", category=CategoryEnum.cloth, base_price=2500.00),
            Product(name="Socks", category=CategoryEnum.cloth, base_price=150.00),
            
            Product(name="Smart Watch", category=CategoryEnum.accessory, base_price=3500.00),
            Product(name="Sunglasses", category=CategoryEnum.accessory, base_price=1500.00),
            Product(name="Leather Belt", category=CategoryEnum.accessory, base_price=500.00),
            Product(name="Wallet", category=CategoryEnum.accessory, base_price=700.00),
            Product(name="Sports Cap", category=CategoryEnum.accessory, base_price=350.00),
        ]
        db.add_all(dummy_products)
        db.commit()