from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, cast, String
from fastapi import HTTPException
from app.models.product_model import Product
from app.models.company_model import Company
from app.models.category_model import Category
from sqlalchemy.orm import joinedload

async def create_product(db: AsyncSession, product_in):
    comp = (await db.execute(select(Company).where(Company.id == product_in.company_id))).scalar_one_or_none()
    if not comp:
        raise HTTPException(status_code=400, detail='company_id is required and must exist')
    cat = (await db.execute(select(Category).where(Category.id == product_in.category_id))).scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=400, detail='category_id is required and must exist')

    exist = (await db.execute(select(Product).where(Product.name == product_in.name, Product.company_id == product_in.company_id))).scalar_one_or_none()
    if exist:
        raise HTTPException(status_code=400, detail='Product with this name already exists for this company')

    obj = Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        company_id=product_in.company_id,
        category_id=product_in.category_id
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(Product)
        .options(joinedload(Product.company), joinedload(Product.category))
        .where(Product.id == product_id)
    )
    prod = result.scalar_one_or_none()
    if prod:
        return {
            "id": prod.id,
            "name": prod.name,
            "description": prod.description,
            "price": prod.price,
            "company_name": prod.company.name,
            "category_name": prod.category.name
        }
    return None

async def list_products(db: AsyncSession, skip: int = 0, limit: int = 50):
    result = await db.execute(
        select(Product)
        .options(joinedload(Product.company), joinedload(Product.category))
        .offset(skip)
        .limit(limit)
    )
    products = result.scalars().all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "company_name": p.company.name,
            "category_name": p.category.name
        } for p in products
    ]

async def update_product(db: AsyncSession, product_obj, updates):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(product_obj, field, value)
    db.add(product_obj)
    await db.commit()
    await db.refresh(product_obj)
    return product_obj

async def delete_product(db: AsyncSession, product_obj):
    await db.delete(product_obj)
    await db.commit()
    return True

async def search_products(db: AsyncSession, q: str = None, company_id: int = None, category_id: int = None, skip: int = 0, limit: int = 10):
    query = select(Product)
    if q:
        like_q = f"%{q}%"
        query = query.where(or_(
            Product.name.ilike(like_q),
            Product.description.ilike(like_q),
            cast(Product.price, String).ilike(like_q)
        ))
    if company_id:
        query = query.where(Product.company_id == company_id)
    if category_id:
        query = query.where(Product.category_id == category_id)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all(), None
