import base64, os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    github_app_id: str = os.getenv("GITHUB_APP_ID", "")
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    github_private_key_b64: str = os.getenv("GITHUB_PRIVATE_KEY_BASE64", "")
    bot_comment_tag: str = os.getenv("BOT_COMMENT_TAG", "ai-review-bot")
    max_patch_chars: int = int(os.getenv("MAX_PATCH_CHARS", "12000"))

    @property
    def github_private_key_pem(self) -> bytes:
        if not self.github_private_key_b64:
            raise ValueError("GITHUB_PRIVATE_KEY_BASE64 environment variable not set")
        return base64.b64decode(self.github_private_key_b64)

settings = Settings()
