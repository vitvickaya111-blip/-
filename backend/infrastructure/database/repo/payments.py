from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from infrastructure.database.models import PendingPayment
from infrastructure.database.repo.base import BaseRepo


class PaymentRepo(BaseRepo):
    def __init__(self, sessionmaker: async_sessionmaker):
        super().__init__(sessionmaker, PendingPayment)

    async def get_payment_by_id(self, payment_id: int) -> Optional[PendingPayment]:
        """Get payment by ID"""
        return await self.get(payment_id)

    async def get_pending_by_user(self, user_id: int) -> Optional[PendingPayment]:
        """Get pending payment for user"""
        async with self.sessionmaker() as session:
            stmt = select(PendingPayment).where(
                PendingPayment.user_id == user_id,
                PendingPayment.status == "pending"
            ).order_by(PendingPayment.created_at.desc())
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_all_pending(self) -> List[PendingPayment]:
        """Get all pending payments"""
        async with self.sessionmaker() as session:
            stmt = select(PendingPayment).where(
                PendingPayment.status == "pending"
            ).order_by(PendingPayment.created_at.desc())
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def approve_payment(self, payment_id: int) -> Optional[PendingPayment]:
        """Approve payment"""
        return await self.update(payment_id, status="approved")

    async def reject_payment(self, payment_id: int) -> Optional[PendingPayment]:
        """Reject payment"""
        return await self.update(payment_id, status="rejected")
