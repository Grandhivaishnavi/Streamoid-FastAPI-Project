from pydantic import BaseModel

class ProductResponse(BaseModel):
    sku: str
    name: str
    brand: str | None
    color: str | None
    size: str | None
    mrp: float
    price: float
    quantity: int

    class Config:
        orm_mode = True
