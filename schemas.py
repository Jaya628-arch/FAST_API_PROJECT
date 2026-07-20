# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 02:04:10 2026

@author: JAYASAKTHI
"""

from pydantic import BaseModel


# ---------- User Schemas ----------

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


# ---------- Product Schemas ----------

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float


class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True