from pydantic import Field
from pydantic_settings import BaseSettings


class MiscellaneousSettings(BaseSettings):
    # Paid products settings
    community_chat_id: str = Field(default="")  # ID закрытого чата сообщества (будет установлено позже)
    paid_pdf_url: str = Field(default="")  # URL платного PDF гайда (будет установлено позже)
