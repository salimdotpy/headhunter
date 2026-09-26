# core/templates.py

from fastapi.templating import Jinja2Templates

from app.core.config import BASE_DIR
from app.core.flash import flash_context


templates = Jinja2Templates(directory=BASE_DIR / "templates", context_processors=[flash_context,],)