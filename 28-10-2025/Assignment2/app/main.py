# app/main.py

from fastapi import FastAPI
from app.core.database import db, connect_db, disconnect_db
from app.routes import company_route, category_route, product_route

app = FastAPI(
    title="Assignment 2 - Product Management API"
)

# ---------- Database Events ----------
@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# ---------- Routers ----------
app.include_router(company_route.router, prefix="/api/company", tags=["Company"])
app.include_router(category_route.router, prefix="/api/category", tags=["Category"])
app.include_router(product_route.router, prefix="/api/product", tags=["Product"])

# ---------- Root Route ----------
@app.get("/")
async def root():
    return {"message": " FastAPI Prisma Product Management API is running successfully!"}
