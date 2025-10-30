from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.category_schema import CategoryCreate, CategoryRead
from app.crud.category_crud import create_category, get_category, list_categories, delete_category, update_category

router = APIRouter(prefix='/categories', tags=['Categories'])

@router.post('/', response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(payload: CategoryCreate, db: AsyncSession = Depends(get_session)):
    return await create_category(db, payload)

@router.get('/{category_id}', response_model=CategoryRead)
async def get_category_endpoint(category_id: int, db: AsyncSession = Depends(get_session)):
    cat = await get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail='Category not found')
    return cat

@router.get('/', response_model=list[CategoryRead])
async def list_categories_endpoint(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_session)):
    return await list_categories(db, skip, limit)

@router.delete('/{category_id}')
async def delete_category_endpoint(category_id: int, db: AsyncSession = Depends(get_session)):
    cat = await get_category(db, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail='Category not found')
    await delete_category(db, cat)
    return {'detail': 'Deleted'}
@router.put('/{category_id}', response_model=CategoryRead)
async def update_category_endpoint(category_id: int, payload: CategoryCreate, db: AsyncSession = Depends(get_session)):
    category = await get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return await update_category(db, category, payload)
