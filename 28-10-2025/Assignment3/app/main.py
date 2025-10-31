from fastapi import FastAPI
from app.routes import employee_route
from app.database.database import lifespan

app = FastAPI(
    title="File Handling API with Prisma",
    lifespan=lifespan
)

app.include_router(employee_route.router)
