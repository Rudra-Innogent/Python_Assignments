# app/routes/product_routes.py
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging

from app.core.database import db
from app.schema.product_schema import ProductRead, ProductCreate, ProductUpdate

router = APIRouter(tags=["Product"], prefix="/product")
logger = logging.getLogger("app.product")

def _product_with_names_to_read_obj(prod):
    """
    Convert Prisma product (with included company and category) to ProductRead-compatible dict
    """
    return {
        "id": prod.id,
        "name": prod.name,
        "price": prod.price,
        "description": prod.description,
        "companyId": prod.companyId,
        "categoryId": prod.categoryId,
        "company_name": prod.company.name if getattr(prod, "company", None) else "",
        "category_name": prod.category.name if getattr(prod, "category", None) else ""
    }

@router.post("/", response_model=ProductRead, status_code=201)
async def create_product(payload: ProductCreate):
    # validate company & category exist and category belongs to company
    comp = await db.company.find_unique(where={"id": payload.companyId})
    if not comp:
        raise HTTPException(status_code=400, detail="Company does not exist")

    cat = await db.category.find_unique(where={"id": payload.categoryId})
    if not cat:
        raise HTTPException(status_code=400, detail="Category does not exist")

    if cat.companyId != payload.companyId:
        raise HTTPException(status_code=400, detail="Category does not belong to the specified company")

    # prevent duplicate product entry (same name + company + category)
    existing = await db.product.find_first(where={
        "name": payload.name,
        "companyId": payload.companyId,
        "categoryId": payload.categoryId
    })
    if existing:
        raise HTTPException(status_code=400, detail="Product with same name under this company & category already exists")

    created = await db.product.create(data={
        "name": payload.name,
        "price": payload.price,
        "description": payload.description,
        "companyId": payload.companyId,
        "categoryId": payload.categoryId
    })

    # include related for response
    prod_with_rel = await db.product.find_unique(where={"id": created.id}, include={"company": True, "category": True})
    logger.info(f"Created product id={created.id} name={created.name}")
    return _product_with_names_to_read_obj(prod_with_rel)

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int):
    prod = await db.product.find_unique(where={"id": product_id}, include={"company": True, "category": True})
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return _product_with_names_to_read_obj(prod)

@router.get("/", response_model=List[ProductRead])
async def get_all_products(skip: int = 0, limit: int = 50):
    prods = await db.product.find_many(skip=skip, take=limit, include={"company": True, "category": True})
    return [_product_with_names_to_read_obj(p) for p in prods]

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, payload: ProductUpdate):
    prod = await db.product.find_unique(where={"id": product_id})
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    data = {}
    if payload.name is not None:
        data["name"] = payload.name
    if payload.price is not None:
        data["price"] = payload.price
    if payload.description is not None:
        data["description"] = payload.description
    if payload.companyId is not None:
        comp = await db.company.find_unique(where={"id": payload.companyId})
        if not comp:
            raise HTTPException(status_code=400, detail="Company does not exist")
        data["companyId"] = payload.companyId
    if payload.categoryId is not None:
        cat = await db.category.find_unique(where={"id": payload.categoryId})
        if not cat:
            raise HTTPException(status_code=400, detail="Category does not exist")
        data["categoryId"] = payload.categoryId

    if not data:
        prod_with_rel = await db.product.find_unique(where={"id": product_id}, include={"company": True, "category": True})
        return _product_with_names_to_read_obj(prod_with_rel)

    # If both companyId and categoryId are set, ensure category belongs to company
    companyId_to_check = data.get("companyId", prod.companyId)
    categoryId_to_check = data.get("categoryId", prod.categoryId)
    cat_check = await db.category.find_unique(where={"id": categoryId_to_check})
    if cat_check.companyId != companyId_to_check:
        raise HTTPException(status_code=400, detail="Category does not belong to the specified company")

    updated = await db.product.update(where={"id": product_id}, data=data)
    updated_with_rel = await db.product.find_unique(where={"id": updated.id}, include={"company": True, "category": True})
    logger.info(f"Updated product id={product_id}")
    return _product_with_names_to_read_obj(updated_with_rel)

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    prod = await db.product.find_unique(where={"id": product_id})
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.product.delete(where={"id": product_id})
    logger.info(f"Deleted product id={product_id}")
    return {"message": "Product deleted successfully"}

# Search endpoint: search q across product.name, product.description, company.name, category.name
@router.get("/search", response_model=List[ProductRead])
async def search_products(
    q: Optional[str] = Query(None, min_length=1),
    companyId: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(25, ge=1, le=100)
):
    where = {}

    # add company filter if provided
    if companyId is not None:
        where["companyId"] = companyId

    # if q is present, build OR across fields
    if q:
        # Prisma nested filters allow relational search using dicts
        where["OR"] = [
            {"name": {"contains": q, "mode": "insensitive"}},
            {"description": {"contains": q, "mode": "insensitive"}},
            {"company": {"name": {"contains": q, "mode": "insensitive"}}},
            {"category": {"name": {"contains": q, "mode": "insensitive"}}}
        ]

    prods = await db.product.find_many(where=where, skip=skip, take=limit, include={"company": True, "category": True})
    return [_product_with_names_to_read_obj(p) for p in prods]
