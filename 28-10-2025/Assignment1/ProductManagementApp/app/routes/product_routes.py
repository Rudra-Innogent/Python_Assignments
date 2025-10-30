from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.session import get_session
from app.schemas.product_schema import ProductCreate, ProductRead
from app.crud.product_crud import create_product, get_product, list_products, update_product, delete_product, search_products

router = APIRouter(prefix='/products', tags=['Products'])

@router.post('/', response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product_endpoint(payload: ProductCreate, db: AsyncSession = Depends(get_session)):
    return await create_product(db, payload)

@router.get('/{product_id}', response_model=ProductRead)
async def get_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    prod = await get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail='Product not found')
    return prod

@router.get('/', response_model=list[ProductRead])
async def list_products_endpoint(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_session)):
    return await list_products(db, skip, limit)

@router.put('/{product_id}', response_model=ProductRead)
async def update_product_endpoint(product_id: int, payload: ProductCreate, db: AsyncSession = Depends(get_session)):
    prod = await get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail='Product not found')
    return await update_product(db, prod, payload)

@router.delete('/{product_id}')
async def delete_product_endpoint(product_id: int, db: AsyncSession = Depends(get_session)):
    prod = await get_product(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail='Product not found')
    await delete_product(db, prod)
    return {'detail': 'Deleted'}

@router.get('/search', response_model=list[ProductRead])
async def search_products_endpoint(q: Optional[str] = Query(None), company_id: Optional[int] = None,
                                  category_id: Optional[int] = None, skip: int = 0, limit: int = 10,
                                  db: AsyncSession = Depends(get_session)):
    results, total = await search_products(db, q, company_id, category_id, skip, limit)
    return results
