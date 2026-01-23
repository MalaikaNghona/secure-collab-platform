import os
from typing import Optional

# JWT Configuration
SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
