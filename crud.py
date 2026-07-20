# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 02:05:29 2026

@author: JAYASAKTHI
"""

from sqlalchemy.orm import Session
import models
import schemas
import auth


# -------------------------
# User CRUD
# -------------------------

def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = auth.hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def login_user(db: Session, user: schemas.UserLogin):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        return None

    if not auth.verify_password(
        user.password,
        db_user.password
    ):
        return None

    token = auth.create_access_token(
        {"sub": db_user.email}
    )

    return token


# -------------------------
# Product CRUD
# -------------------------

def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


def get_products(db: Session):

    return db.query(models.Product).all()


def get_product(db: Session, product_id: int):

    return db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()


def update_product(
    db: Session,
    product_id: int,
    product: schemas.ProductUpdate
):

    db_product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if db_product:

        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price

        db.commit()
        db.refresh(db_product)

    return db_product


def delete_product(db: Session, product_id: int):

    db_product = db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()

    if db_product:

        db.delete(db_product)
        db.commit()

    return db_product