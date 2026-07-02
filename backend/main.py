# from contextlib import asynccontextmanager
# from fastapi import Depends, FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import Session

# import models
# from database import get_db, init_db, SessionLocal

# @asynccontextmanager
# async def lifespan(_app: FastAPI):
#     init_db()
#     db = SessionLocal()
#     try:
#         models.seed_initial_products(db)
#     finally:
#         db.close()
#     yield

# app = FastAPI(lifespan=lifespan)

# @app.exception_handler(SQLAlchemyError)
# async def database_exception_handler(_request, _exc):
#     return JSONResponse(
#         status_code=503,
#         content={"detail": "Database connection failed. Check your config."}
#     )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class UserAuth(BaseModel):
#     username: str
#     password: str

# class CartItemCreate(BaseModel):
#     user_id: int
#     product_id: int

# # --- API ROUTES ---

# @app.post("/api/login")
# def login(user_data: UserAuth, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
#     if not db_user:
#         db_user = models.User(username=user_data.username, password_hash=user_data.password, is_logged_in=True)
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#     else:
#         db_user.is_logged_in = True
#         db.commit()
#     return {"message": "Logged in successfully", "user_id": db_user.id, "username": db_user.username}

# @app.post("/api/logout/{user_id}")
# def logout(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(models.User.id == user_id).first()
#     if db_user:
#         db_user.is_logged_in = False
#         db.commit()
#     return {"message": "Logged out successfully"}

# @app.get("/api/products/{category}")
# def get_products(category: str, db: Session = Depends(get_db)):
#     products = db.query(models.Product).filter(models.Product.category == category).all()
#     return products

# # 🔥 DYNAMIC CUMULATIVE MULTI-PRODUCT DISCOUNT LOGIC
# @app.post("/api/cart/add")
# def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db)):
#     product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
        
#     base_price = float(product.base_price)
    
#     # Check karein ki user ne pehle se cart me kitne items le rakhe hain
#     existing_items_count = db.query(models.Cart).filter(models.Cart.user_id == item.user_id).count()
    
#     # Har item selection par 5% cut logic: (Pehle ke items + Naya Item) * 5
#     current_selection_rank = existing_items_count + 1
#     discount_percentage = float(current_selection_rank * 5.0)
    
#     # Cap discount at 50% max taaki item free ya negative me na chala jaye (Safety feature)
#     if discount_percentage > 50.0:
#         discount_percentage = 50.0
        
#     discount_amount = base_price * (discount_percentage / 100)
#     final_price = base_price - discount_amount
    
#     # Save parameters directly to MySQL via SQLAlchemy
#     cart_entry = models.Cart(
#         user_id=item.user_id,
#         product_id=item.product_id,
#         original_price=base_price,
#         discount_applied_percentage=discount_percentage,
#         final_price=final_price
#     )
#     db.add(cart_entry)
#     db.commit()
    
#     return {
#         "message": f"Product #{current_selection_rank} selected! Multi-Item Discount applied.",
#         "original_price": base_price,
#         "discount_applied": f"{discount_percentage}%",
#         "final_price": final_price,
#         "total_items_in_cart": current_selection_rank
#     }

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List

import models
from database import get_db, init_db, SessionLocal

@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        models.seed_initial_products(db)
    finally:
        db.close()
    yield

app = FastAPI(lifespan=lifespan)

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(_request, _exc):
    return JSONResponse(
        status_code=503,
        content={"detail": "Database connection failed. Check your config or MySQL status."}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserAuth(BaseModel):
    username: str
    password: str

# Expected list of multiple product IDs from frontend
class CartBulkCreate(BaseModel):
    user_id: int
    product_ids: List[int]

# --- API ROUTES ---

@app.post("/api/login")
def login(user_data: UserAuth, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user_data.username).first()
    if not db_user:
        db_user = models.User(username=user_data.username, password_hash=user_data.password, is_logged_in=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    else:
        db_user.is_logged_in = True
        db.commit()
    return {"message": "Logged in successfully", "user_id": db_user.id, "username": db_user.username}

@app.post("/api/logout/{user_id}")
def logout(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.is_logged_in = False
        db.commit()
    return {"message": "Logged out successfully"}

@app.get("/api/products/{category}")
def get_products(category: str, db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(models.Product.category == category).all()
    return products

# 🔥 CUMULATIVE BULK SUM & MINUS CALCULATION API
@app.post("/api/cart/add-bulk")
def add_bulk_to_cart(cart_data: CartBulkCreate, db: Session = Depends(get_db)):
    if not cart_data.product_ids:
        raise HTTPException(status_code=400, detail="select any product")

    # 1. Database se saare selected products ka pricing data nikalna
    db_products = db.query(models.Product).filter(models.Product.id.in_(cart_data.product_ids)).all()
    
    if not db_products:
        raise HTTPException(status_code=404, detail="Selected product not in option")

    # 2. Total Sum Calculation
    total_base_sum = sum(float(p.base_price) for p in db_products)
    total_items = len(db_products)

    # 3. Cumulative Discount logic (Jitne items utne * 5% cut)
    discount_percentage = float(total_items * 5.0)
    if discount_percentage > 50.0:  # Max 50% safety cap
        discount_percentage = 50.0

    # 4. Amount minus workflow
    discount_amount = total_base_sum * (discount_percentage / 100)
    final_payable_amount = total_base_sum - discount_amount

    # Comma-separated product string for records
    prod_str_list = ",".join(str(pid) for pid in cart_data.product_ids)

    # 5. MySQL me entry store karna
    cart_entry = models.Cart(
        user_id=cart_data.user_id,
        product_ids=prod_str_list,
        total_base_sum=total_base_sum,
        discount_percentage=discount_percentage,
        discount_amount=discount_amount,
        final_payable_amount=final_payable_amount
    )
    db.add(cart_entry)
    db.commit()

    return {
        "message": f"Successfully calculated for {total_items}",
        "total_base_sum": total_base_sum,
        "discount_percentage": f"{discount_percentage}%",
        "discount_amount": discount_amount,
        "final_payable_amount": final_payable_amount
    }