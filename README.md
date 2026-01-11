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

Validation rules when uploading:
- `sku`, `name`, `brand`, `mrp`, `price` are required.
- `price` must be <= `mrp`.
- `quantity` must be a non-negative integer.
- `sku` must be unique (duplicate SKUs are rejected).

API endpoints
- POST `/upload-csv` — form multipart upload. Field name: `file`.
  - Accepts a CSV file. Returns counts and a list of row errors.
- GET `/products` — paginated list of products.
  - Query params: `page` (default 1), `limit` (default 10).
- GET `/products/search` — filter products.
  - Query params: `brand`, `color`, `minPrice`, `maxPrice` (Any one of these are fine).

Quick setup
1. Create a virtual environment and activate it (example using `venv`):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the database connection inside `database.py`.
   - The project expects a SQLAlchemy engine and `SessionLocal` to be available from `database.py`.
   - If you use MySQL, ensure `mysql-connector-python` is installed (listed in `requirements.txt`).

Run the app

```bash
uvicorn main:app --reload
```

Notes & next steps
- Make sure `database.py` is configured with correct credentials and the DB is reachable.
- You can open the automatic API docs at `http://localhost:8000/docs` once the app is running.
- Consider adding tests or a sample `products.csv` for manual testing.
