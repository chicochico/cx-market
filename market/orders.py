import time
from enum import Enum
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel, Field, validator

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


class Side(str, Enum):
    buy = "buy"
    sell = "sell"

    @classmethod
    def _missing_(cls, side):
        "case insensitive side"
        side = side.lower()
        if side in ["buy", "sell"]:
            return getattr(cls, side)


class Order(BaseModel):
    isin: str = Field(regex="^([A-Z]{2})([A-Z0-9]{9})([0-9]{1})$")
    limit_price: float = Field(gt=0)
    side: Side
    valid_until: int
    quantity: int = Field(gt=0)

    @validator("valid_until")
    def valid_until_in_future(cls, v):
        if v < time.time():
            raise ValueError("valid_until cannot be in the past")
        return v


class OrderResponse(BaseModel):
    msg: str


orders = []


@router.post("/order", response_model=OrderResponse)
async def submit_order(order: Order):
    # "process" the order here the order can be
    # sent for execution and saved into DB
    orders.append(order)
    return OrderResponse(msg="success")


@router.get("/", response_model=List[Order])
async def get_orders():
    return orders
