"""
Companies API endpoints

FR-1.2: Профиль компании
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создать новую компанию
    
    FR-1.2: Пользователь может создать профиль компании
    """
    
    # Проверяем что компания с таким ИНН уже не зарегистрирована этим пользователем
    existing = db.query(Company).filter(
        Company.owner_id == current_user.id,
        Company.inn == company_in.inn
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this INN already exists"
        )
    
    # Создаем компанию
    company = Company(
        owner_id=current_user.id,
        **company_in.model_dump()
    )
    
    # Валидируем ИНН
    if not company.validate_inn():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid INN format"
        )
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse.model_validate(company)


@router.get("/me", response_model=List[CompanyResponse])
async def get_my_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все компании текущего пользователя
    """
    companies = db.query(Company).filter(
        Company.owner_id == current_user.id
    ).order_by(Company.created_at.desc()).all()
    
    return [CompanyResponse.model_validate(c) for c in companies]


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить конкретную компанию по ID
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return CompanyResponse.model_validate(company)


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: UUID,
    company_update: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить данные компании
    
    FR-1.2: Редактирование в любое время
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Обновляем только переданные поля
    update_data = company_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(company, field, value)
    
    # Валидируем ИНН если он был обновлен
    if 'inn' in update_data and not company.validate_inn():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid INN format"
        )
    
    db.commit()
    db.refresh(company)
    
    return CompanyResponse.model_validate(company)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить компанию
    
    Осторожно: Удаляются также все финансовые данные и метрики (CASCADE)
    """
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.owner_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    
    return None

