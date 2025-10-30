import os
from fastapi import FastAPI
from app.db.session import async_engine, Base
from app.utils.logging_config import RequestLoggerMiddleware, logger
from app.routes import company_routes, category_routes, product_routes

app = FastAPI(title="Product Management API (Async SQLAlchemy)")

app.add_middleware(RequestLoggerMiddleware)

app.include_router(company_routes.router)
app.include_router(category_routes.router)
app.include_router(product_routes.router)

@app.on_event("startup")
async def on_startup():
    # Import all models before table creation
    from app.models.company_model import Company
    from app.models.category_model import Category
    from app.models.product_model import Product

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured and app started")


@app.on_event("shutdown")
async def on_shutdown():
    await async_engine.dispose()

@app.get("/health-check")
async def health_check():
    return {"status": "ok"}
