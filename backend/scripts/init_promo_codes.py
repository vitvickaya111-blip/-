"""
Script to initialize promo codes in database.

Run with:
docker exec bot python3 scripts/init_promo_codes.py
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.database import setup as db_setup
from infrastructure.database.requests import RequestsRepo
from settings import get_app_settings


async def init_promo_codes():
    """Initialize promo codes in database"""
    settings = get_app_settings()

    # Setup database
    db_setup.main()

    # Create repo
    repo = RequestsRepo(sessionmaker=db_setup.async_session)

    # Define promo codes
    promo_codes = [
        {"code": "VIETNAM15", "discount_percent": 15, "active": True},
        {"code": "DREAMER20", "discount_percent": 20, "active": True},
        {"code": "READY15", "discount_percent": 15, "active": True},
    ]

    # Insert promo codes
    for promo in promo_codes:
        try:
            existing = await repo.promo_codes.get_by_code(promo["code"])
            if existing:
                print(f"✅ Промокод {promo['code']} уже существует (скидка {existing.discount_percent}%)")
            else:
                await repo.promo_codes.create(**promo)
                print(f"✅ Создан промокод {promo['code']} (скидка {promo['discount_percent']}%)")
        except Exception as e:
            print(f"❌ Ошибка при создании промокода {promo['code']}: {e}")

    print("\n🎉 Инициализация промокодов завершена!")


if __name__ == "__main__":
    asyncio.run(init_promo_codes())
