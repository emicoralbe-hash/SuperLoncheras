import json
import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Montar estáticos si existen
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, q: str = None):
    db = load_db()
    recetas = db.get("recetas", [])
    if q:
        recetas = [r for r in recetas if q.lower() in r.get("nombre", "").lower()]
    
    # ESTA ES LA FORMA NUEVA Y SEGURA DE ENVIAR DATOS
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "recetas": recetas, 
            "query": q, 
            "user": request.session.get("user")
        }
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = load_db()
    user = next((u for u in db["usuarios"] if u["email"] == email and u["pass"] == password), None)
    if user:
        request.session["user"] = user
        return RedirectResponse(url="/", status_code=303)
    return RedirectResponse(url="/login?error=1", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

@app.get("/planner", response_class=HTMLResponse)
async def get_planner(request: Request):
    db = load_db()
    return templates.TemplateResponse(
        request=request, 
        name="planner.html", 
        context={
            "recetas": db.get("recetas", []), 
            "dias": range(1, 31), 
            "user": request.session.get("user")
        }
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
