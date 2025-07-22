from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from server.routes.auth import router as auth_router
from server.routes.content import router as content_router
from server.config.settings import settings
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(
    title="AI Social Content Generator",
    description="API para generar contenido de redes sociales con IA",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (CSS, JS, images)
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "client"))
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

# Templates
templates = Jinja2Templates(directory=os.path.join(frontend_path, "templates"))


# Routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})