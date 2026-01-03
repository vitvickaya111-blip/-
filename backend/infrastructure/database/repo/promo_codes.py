from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.models import PromoCode
from infrastructure.database.repo.base import BaseRepo


class PromoCodeRepo(BaseRepo):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker, PromoCode)

    async def get_by_code(self, code: str) -> Optional[PromoCode]:
        """Get promo code by code string"""
        async with self.sessionmaker() as session:
            stmt = select(PromoCode).where(
                PromoCode.code == code.upper(),
                PromoCode.active == True
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_active(self) -> List[PromoCode]:
        """Get all active promo codes"""
        async with self.sessionmaker() as session:
            stmt = select(PromoCode).where(
                PromoCode.active == True
            ).order_by(PromoCode.discount_percent.desc())
            result = await session.execute(stmt)
            return list(result.scalars().all())
