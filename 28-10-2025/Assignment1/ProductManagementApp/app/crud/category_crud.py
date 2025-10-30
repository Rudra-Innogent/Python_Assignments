from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.category_model import Category
from app.models.company_model import Company

async def create_category(db: AsyncSession, category_in):
    result = await db.execute(select(Company).where(Company.id == category_in.company_id))
    comp = result.scalar_one_or_none()
    if not comp:
        raise HTTPException(status_code=400, detail='company_id is required and must exist')
    obj = Category(name=category_in.name, description=category_in.description, company_id=category_in.company_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()

async def list_categories(db: AsyncSession, skip: int = 0, limit: int = 50):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_category(db: AsyncSession, category_obj):
    await db.delete(category_obj)
    await db.commit()
    return True

async def update_category(db: AsyncSession, category_obj, updates):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(category_obj, field, value)
    db.add(category_obj)
    await db.commit()
    await db.refresh(category_obj)
    return category_obj
