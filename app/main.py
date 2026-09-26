from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="Headhunter",
    description=(
        "CV Portfolio Creation, Management, "
        "Presentation and Sharing System"
    ),
    version="0.1.0",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={
            "title": "Headhunter",
        },
    )