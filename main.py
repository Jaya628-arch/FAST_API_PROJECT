# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 02:06:04 2026

@author: JAYASAKTHI
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, Base, get_db

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI()


# -----------------------------
# User APIs
# -----------------------------

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    token = crud.login_user(db, user)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# -----------------------------
# Product APIs
# -----------------------------

@app.post("/products")
def create_product(product: schemas.ProductCreate,
                   db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get("/products/{product_id}")
def get_product(product_id: int,
                db: Session = Depends(get_db)):

    product = crud.get_product(db, product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.put("/products/{product_id}")
def update_product(product_id: int,
                   product: schemas.ProductUpdate,
                   db: Session = Depends(get_db)):

    updated_product = crud.update_product(
        db,
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int,
                   db: Session = Depends(get_db)):

    deleted_product = crud.delete_product(db, product_id)

    if deleted_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return {
        "message": "Product deleted successfully"
    }