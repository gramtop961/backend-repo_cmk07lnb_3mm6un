"""
Database Schemas for Tutti Amici

Each Pydantic model maps to a MongoDB collection (name is the lowercase of the class name).
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    """Menu items available for ordering"""
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Category (e.g., Pizza, Pasta, Sides, Drinks, Dessert)")
    image: Optional[str] = Field(None, description="Image URL")
    is_available: bool = Field(True, description="Whether the item is available")


class OrderItem(BaseModel):
    """One line item in an order"""
    menu_item_id: str = Field(..., description="ID of the menu item")
    name: str = Field(..., description="Name at time of order")
    price: float = Field(..., ge=0, description="Unit price at time of order")
    quantity: int = Field(..., ge=1, description="Quantity ordered")
    notes: Optional[str] = Field(None, description="Special instructions for this item")


class Customer(BaseModel):
    """Customer information for delivery/contact"""
    name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="Contact phone number")
    address: Optional[str] = Field(None, description="Delivery address if applicable")


class Order(BaseModel):
    """Orders placed by customers"""
    items: List[OrderItem] = Field(..., description="Ordered items")
    subtotal: float = Field(..., ge=0, description="Subtotal before fees")
    tax: float = Field(..., ge=0, description="Tax amount")
    total: float = Field(..., ge=0, description="Final total amount")
    status: str = Field("pending", description="Order status: pending, confirmed, preparing, ready, delivered, cancelled")
    customer: Customer
    notes: Optional[str] = Field(None, description="Special instructions for the order")
