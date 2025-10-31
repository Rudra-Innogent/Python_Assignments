# app/routes/category_routes.py
from fastapi import APIRouter, HTTPException
from typing import List

import logging

from app.core.database import db
from app.schema.category_schema import CategoryRead, CategoryCreate, CategoryUpdate

router = APIRouter(tags=["Category"], prefix="/category")
logger = logging.getLogger("app.category")

@router.post("/", response_model=CategoryRead, status_code=201)
async def create_category(payload: CategoryCreate):
    # verify company exists
    comp = await db.company.find_unique(where={"id": payload.companyId})
    if not comp:
        raise HTTPException(status_code=400, detail="Company does not exist")

    # prevent duplicate category name within the same company
    existing = await db.category.find_first(where={"name": payload.name, "companyId": payload.companyId})
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists for this company")

    created = await db.category.create(data={
        "name": payload.name,
        "companyId": payload.companyId
    })
    logger.info(f"Created category id={created.id} name={created.name} company={payload.companyId}")
    return created

@router.get("/{categoryId}", response_model=CategoryRead)
async def get_category(categoryId: int):
    category = await db.category.find_unique(where={"id": categoryId})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[CategoryRead])
async def get_all_categories():
    return await db.category.find_many()

@router.put("/{categoryId}", response_model=CategoryRead)
async def update_category(categoryId: int, payload: CategoryUpdate):
    category = await db.category.find_unique(where={"id": categoryId})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    data = {}
    if payload.name is not None:
        data["name"] = payload.name

    if not data:
        return category

    # avoid duplicate within same company if name changed
    dup = await db.category.find_first(where={"name": data.get("name"), "companyId": category.company_id})
    if dup and dup.id != categoryId:
        raise HTTPException(status_code=400, detail="Another category with this name exists for this company")

    updated = await db.category.update(where={"id": categoryId}, data=data)
    logger.info(f"Updated category id={categoryId}")
    return updated

@router.delete("/{categoryId}")
async def delete_category(categoryId: int):
    category = await db.category.find_unique(where={"id": categoryId})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.category.delete(where={"id": categoryId})
    logger.info(f"Deleted category id={categoryId}")
    return {"message": "Category deleted successfully"}
