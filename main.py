from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Catalog Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload-csv")
def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    file.file.seek(0)
    df = pd.read_csv(file.file, encoding="utf-8-sig", sep=",")
    df.columns = df.columns.str.strip().str.lower()
    print(df.columns.tolist())


    total_rows = len(df)
    valid_rows = 0
    errors = []

    for index, row in df.iterrows():
        try:
            if pd.isna(row["sku"]) or pd.isna(row["name"]) or pd.isna(row["brand"]) or pd.isna(row["mrp"]) or pd.isna(row["price"]):
                raise ValueError("sku or Name or Brand or MRP or Price missing")

            if float(row["price"]) > float(row["mrp"]):
                raise ValueError("Price cannot be greater than MRP")

            if int(row["quantity"]) < 0:
                raise ValueError("Quantity cannot be negative")

            existing = db.query(models.Product).filter_by(sku=row["sku"]).first()
            if existing:
                raise ValueError("Duplicate sku")

            product = models.Product(
                sku=str(row["sku"]),
                name=row["name"],
                brand=row.get("brand"),
                color=row.get("color"),
                size=row.get("size"),
                mrp=float(row["mrp"]),
                price=float(row["price"]),
                quantity=int(row["quantity"])
            )

            db.add(product)
            db.commit()
            valid_rows += 1

        except Exception as e:
            db.rollback()
            errors.append({
                "row": index + 1,
                "error": str(e)
            })

    return {
        "totalRows": total_rows,
        "validRows": valid_rows,
        "invalidRows": total_rows - valid_rows,
        "errors": errors
    }



@app.get("/products", response_model=list[schemas.ProductResponse])
def list_products(
    page: int = 1,        
    limit: int = 10,      
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    products = db.query(models.Product).offset(offset).limit(limit).all()
    return products


@app.get("/products/search", response_model=list[schemas.ProductResponse])
def search_products(
    brand: str | None = None,
    color: str | None = None,
    minPrice: float | None = None,
    maxPrice: float | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if brand:
        query = query.filter(models.Product.brand == brand)
    if color:
        query = query.filter(models.Product.color == color)
    if minPrice is not None:
        query = query.filter(models.Product.price >= minPrice)
    if maxPrice is not None:
        query = query.filter(models.Product.price <= maxPrice)

    return query.all()
