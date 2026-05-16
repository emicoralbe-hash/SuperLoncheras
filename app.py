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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_FILE = "db.json"

def load_db():
    # Si el archivo no existe o está vacío, devolvemos datos básicos
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}
    
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            # Si el JSON está mal escrito, devolvemos datos básicos para que no explote
            return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, q: str = None):
    db = load_db()
    recetas = db.get("recetas", [])
    if q:
        recetas = [r for r in recetas if q.lower() in r["nombre"].lower()]
    return templates.TemplateResponse("index.html", {"request": request, "recetas": recetas, "query": q, "user": request.session.get("user")})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

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
    return templates.TemplateResponse("planner.html", {"request": request, "recetas": db.get("recetas", []), "dias": range(1, 31), "user": request.session.get("user")})

@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def get_recipe(request: Request, recipe_id: int):
    db = load_db()
    receta = next((r for r in db["recetas"] if r["id"] == recipe_id), None)
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "receta": receta, "user": request.session.get("user")})

@app.get("/marketplace", response_class=HTMLResponse)
async def get_marketplace(request: Request):
    db = load_db()
    return templates.TemplateResponse("marketplace.html", {"request": request, "productos": db.get("productos", []), "user": request.session.get("user")})

@app.get("/batch-cooking", response_class=HTMLResponse)
async def get_batch_cooking(request: Request):
    db = load_db()
    recetas = db.get("recetas", [])
    frozen = [r for r in recetas if "Congelable" in r.get("tag", "") or "Batch Cooking" in r.get("tag", "")]
    return templates.TemplateResponse("batch_cooking.html", {"request": request, "recetas": frozen, "user": request.session.get("user")})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
