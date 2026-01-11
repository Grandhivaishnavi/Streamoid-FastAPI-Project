# Product Catalog Service

Simple FastAPI service to upload product CSVs and query products.

**Files in this project**
- `main.py`: FastAPI app.This handles CSV upload and product endpoints.
- `models.py`: This has models for the `products` table.
- `schemas.py`: It uses Pydantic response model which is used by the API.
- `database.py`: DB setup (engine, Base, SessionLocal). Configure your DB here.
- `requirements.txt`:It has all the Python dependencies for this project.

**Overview**
This service lets you upload a CSV of products using a particular key word and stores valid rows in a SQL database. It also has endpoints to list and search products.

CSV requirements (column names):
- `sku`, `name`, `brand`, `color`, `size`, `mrp`, `price`, `quantity`

CSV format and validation
- Required columns (case-insensitive): `sku`, `name`, `brand`, `mrp`, `price`, `quantity`.
- Optional columns: `color`, `size`.
- Validation rules applied on upload:
  - `sku`, `name`, `brand`, `mrp`, and `price` must be present.
  - `price` must be less than or equal to `mrp`.
  - `quantity` must be a non-negative integer.
  - `sku` must be unique (duplicate SKUs in the DB are rejected).

API Documentation

1) POST /upload-csv
- Description: Upload a CSV file (multipart form). Field name: `file`.
- Request example (curl):

```bash
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@products.csv"
```

- Successful response example:

```json
{
  "totalRows": 10,
  "validRows": 8,
  "invalidRows": 2,
  "errors": [
    {"row": 3, "error": "Price cannot be greater than MRP"},
    {"row": 7, "error": "Duplicate sku"}
  ]
}
```

2) GET /products
- Description: Returns a paginated list of products.
- Query params:
  - `page` (int, default 1)
  - `limit` (int, default 10)
- Request example:

```bash
curl "http://localhost:8000/products?page=1&limit=10"
```

- Response example (array of products):

```json
[
  {
    "sku": "SKU123",
    "name": "T-Shirt",
    "brand": "Acme",
    "color": "Red",
    "size": "M",
    "mrp": 29.99,
    "price": 19.99,
    "quantity": 100
  }
]
```

3) GET /products/search
- Description: Search or filter products.
- Query params (all optional): `brand`, `color`, `minPrice`, `maxPrice`.
- Request example:

```bash
curl "http://localhost:8000/products/search?brand=Acme&minPrice=10&maxPrice=50"
```

- Response: same product object structure as `/products`.

Setup Instructions

1. Create and activate a virtual environment (example):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your database in `database.py`:
- Provide SQLAlchemy connection string and make sure the DB is reachable. The project expects an engine, `Base`, and `SessionLocal` exported from `database.py`.

4. Start the server:

```bash
uvicorn main:app --reload 
```

Testing the API

- Use the included Swagger UI at `http://localhost:8000/docs` for interactive testing.
- Example `products.csv` header (first line):

```
sku,name,brand,color,size,mrp,price,quantity
```

- Example `curl` upload (see above). Inspect the JSON response to see which rows failed and why.

Common issues & troubleshooting
- If you see DB connection errors, check credentials and network access in `database.py`.
- If rows are rejected as duplicates, check the `sku` column values and ensure you don't re-upload the same items.
