from datetime import datetime
from typing import Optional
from sqlalchemy import BIGINT, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class User(Base, TableNameMixin, TimestampMixin):
    id: Mapped[int_pk] = mapped_column(BIGINT)
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]
    language: Mapped[str] = mapped_column(String, server_default="en")

    # Tracking fields according to instructions
    source: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # Instagram, direct link, recommendation
    downloaded_pdf: Mapped[bool] = mapped_column(Boolean, server_default="false")
    pdf_downloaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # When PDF was downloaded
    subscribed_to_channel: Mapped[bool] = mapped_column(Boolean, server_default="false")
    consultation_requested: Mapped[bool] = mapped_column(Boolean, server_default="false")
    consultation_declined: Mapped[bool] = mapped_column(Boolean, server_default="false")
    consultation_paid: Mapped[bool] = mapped_column(Boolean, server_default="false")
    last_message_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    autoresponder_day: Mapped[int] = mapped_column(BIGINT, server_default="0")  # 0-7 for auto-funnel

    # Consultation form data
    consultation_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    consultation_situation: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    consultation_concern: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Paid products access
    has_paid_pdf: Mapped[bool] = mapped_column(Boolean, server_default="false")  # Платный PDF гайд
    has_community_access: Mapped[bool] = mapped_column(Boolean, server_default="false")  # Доступ к сообществу
    community_paid_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Подписка до
    has_paid_consultation_300: Mapped[bool] = mapped_column(Boolean, server_default="false")  # Консультация $300

    #  joinedload - для m2o и o2o связей
    #  selectinload - для o2m и m2m связей
