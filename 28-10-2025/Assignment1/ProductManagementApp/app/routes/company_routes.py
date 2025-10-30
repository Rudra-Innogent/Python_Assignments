from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.company_schema import CompanyCreate, CompanyRead
from app.crud.company_crud import create_company, get_company, list_companies, delete_company, update_company

router = APIRouter(prefix='/companies', tags=['Companies'])

@router.post('/', response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
async def create_company_endpoint(payload: CompanyCreate, db: AsyncSession = Depends(get_session)):
    return await create_company(db, payload)

@router.get('/{company_id}', response_model=CompanyRead)
async def get_company_endpoint(company_id: int, db: AsyncSession = Depends(get_session)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    return company

@router.get('/', response_model=list[CompanyRead])
async def list_companies_endpoint(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_session)):
    return await list_companies(db, skip, limit)

@router.delete('/{company_id}')
async def delete_company_endpoint(company_id: int, db: AsyncSession = Depends(get_session)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    await delete_company(db, company)
    return {'detail': 'Deleted'}

@router.put('/{company_id}', response_model=CompanyRead)
async def update_company_endpoint(company_id: int, payload: CompanyCreate, db: AsyncSession = Depends(get_session)):
    company = await get_company(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    return await update_company(db, company, payload)
