from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from app.models.company_model import Company

async def create_company(db: AsyncSession, company_in):
    result = await db.execute(select(Company).where(Company.name == company_in.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail='Company already exists')
    obj = Company(name=company_in.name, description=company_in.description)
    db.add(obj)
    await db.flush()
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_company(db: AsyncSession, company_id: int):
    result = await db.execute(select(Company).where(Company.id == company_id))
    return result.scalar_one_or_none()

async def list_companies(db: AsyncSession, skip: int = 0, limit: int = 50):
    result = await db.execute(select(Company).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_company(db: AsyncSession, company_obj):
    await db.delete(company_obj)
    await db.flush()
    await db.commit()
    return True

async def update_company(db: AsyncSession, company_obj, updates):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(company_obj, field, value)
    db.add(company_obj)
    await db.commit()
    await db.refresh(company_obj)
    return company_obj

