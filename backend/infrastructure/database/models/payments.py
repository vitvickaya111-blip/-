from datetime import datetime
from typing import Optional
from decimal import Decimal

from sqlalchemy import BIGINT, String, Boolean, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class PendingPayment(Base, TimestampMixin):
    """
    Pending payments awaiting admin approval.

    Status flow: pending -> approved/rejected
    """
    __tablename__ = "pending_payments"

    id: Mapped[int_pk] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT)

    # Product information
    product_type: Mapped[str] = mapped_column(String)  # 'paid_pdf', 'community', 'consultation_300'

    # Pricing
    amount_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # Original price
    promo_code: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    discount_percent: Mapped[int] = mapped_column(Integer, server_default="0")
    final_amount_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2))  # After discount

    # Payment proof
    screenshot_file_id: Mapped[str] = mapped_column(String)

    # Status
    status: Mapped[str] = mapped_column(String, server_default="pending")  # 'pending', 'approved', 'rejected'


class PromoCode(Base, TimestampMixin):
    """
    Promotional codes for discounts.
    """
    __tablename__ = "promo_codes"

    id: Mapped[int_pk] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String, unique=True)
    discount_percent: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean, server_default="true")
