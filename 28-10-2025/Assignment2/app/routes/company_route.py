# app/routes/company_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
import logging

from app.core.database import db
from app.schema.company_schema import CompanyRead, CompanyCreate, CompanyUpdate

router = APIRouter(tags=["Company"], prefix="/company")
logger = logging.getLogger("app.company")

@router.post("/create", response_model=CompanyRead, status_code=201)
async def create_company(payload: CompanyCreate):
    # prevent duplicate names
    existing = await db.company.find_first(where={"name": payload.name})
    if existing:
        raise HTTPException(status_code=400, detail="Company with this name already exists")
    try:
        created = await db.company.create(data={"name": payload.name})
        logger.info(f"Created company id={created.id} name={created.name}")
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/getById/{companyId}", response_model=CompanyRead)
async def get_company(companyId: int):
    company = await db.company.find_unique(where={"id": companyId})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.get("/getAll", response_model=List[CompanyRead])
async def get_all_companies():
    return await db.company.find_many()

@router.put("/updateById/{companyId}", response_model=CompanyRead)
async def update_company(companyId: int, payload: CompanyUpdate):
    company = await db.company.find_unique(where={"id": companyId})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    data = {}
    if payload.name is not None:
        data["name"] = payload.name

    if not data:
        return company

    # prevent duplicates if updating name
    if "name" in data:
        dup = await db.company.find_first(where={"name": data["name"]})
        if dup and dup.id != companyId:
            raise HTTPException(status_code=400, detail="Another company with this name exists")
    updated = await db.company.update(where={"id": companyId}, data=data)
    logger.info(f"Updated company id={companyId}")
    return updated

@router.delete("/deleteById/{companyId}")
async def delete_company(companyId: int):
    # Will raise Prisma error if not found; catch it if you want explicit 404
    company = await db.company.find_unique(where={"id": companyId})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    # optionally: check related products/categories before delete
    await db.company.delete(where={"id": companyId})
    logger.info(f"Deleted company id={companyId}")
    return {"message": "Company deleted successfully"}
