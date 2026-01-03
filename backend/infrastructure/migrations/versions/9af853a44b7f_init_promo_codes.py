"""init_promo_codes

Revision ID: 9af853a44b7f
Revises: cf23380eef77
Create Date: 2026-01-03 22:14:37.124758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9af853a44b7f'
down_revision: Union[str, None] = 'cf23380eef77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Initialize promo codes"""
    from sqlalchemy import table, column, String, Integer, Boolean
    from datetime import datetime

    promo_codes_table = table('promo_codes',
        column('code', String),
        column('discount_percent', Integer),
        column('active', Boolean),
        column('created_at', sa.DateTime),
        column('updated_at', sa.DateTime),
    )

    now = datetime.utcnow()

    op.bulk_insert(promo_codes_table, [
        {'code': 'VIETNAM15', 'discount_percent': 15, 'active': True, 'created_at': now, 'updated_at': now},
        {'code': 'DREAMER20', 'discount_percent': 20, 'active': True, 'created_at': now, 'updated_at': now},
        {'code': 'READY15', 'discount_percent': 15, 'active': True, 'created_at': now, 'updated_at': now},
    ])


def downgrade() -> None:
    """Remove promo codes"""
    op.execute("DELETE FROM promo_codes WHERE code IN ('VIETNAM15', 'DREAMER20', 'READY15')")
