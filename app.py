import json
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {"recetas": [], "productos": [], "usuarios": []}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- RUTAS DE AUTENTICACIÓN ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    db = load_db()
    user = next((u for u in db["usuarios"] if u["email"] == email and u["pass"] == password), None)
    if user:
        request.session["user"] = user
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse(url="/login?error=1", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

# --- RUTAS PRINCIPALES ---

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, q: str = None):
    db = load_db()
    recetas = db["recetas"]
    if q:
        recetas = [r for r in recetas if q.lower() in r["nombre"].lower()]
    return templates.TemplateResponse("index.html", {"request": request, "recetas": recetas, "query": q, "user": request.session.get("user")})

@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def get_recipe(request: Request, recipe_id: int):
    db = load_db()
    receta = next((r for r in db["recetas"] if r["id"] == recipe_id), None)
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "receta": receta, "user": request.session.get("user")})

# --- PANEL DE ADMINISTRADOR ---

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    user = request.session.get("user")
    if not user or user["role"] != "admin":
        return RedirectResponse(url="/")
    db = load_db()
    return templates.TemplateResponse("admin.html", {"request": request, "db": db, "user": user})

@app.post("/admin/add-recipe")
async def add_recipe(request: Request, nombre: str = Form(...), tag: str = Form(...), img: str = Form(...), steps: str = Form(...), video: str = Form(...)):
    db = load_db()
    new_id = max([r["id"] for r in db["recetas"]]) + 1 if db["recetas"] else 1
    new_recipe = {
        "id": new_id,
        "nombre": nombre,
        "tag": tag,
        "img": img,
        "ingredientes": [],
        "alergias": [],
        "pasos": steps.split("\n"),
        "video_url": video
    }
    db["recetas"].append(new_recipe)
    save_db(db)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/admin/delete-recipe/{rid}")
async def delete_recipe(request: Request, rid: int):
    db = load_db()
    db["recetas"] = [r for r in db["recetas"] if r["id"] != rid]
    save_db(db)
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/marketplace", response_class=HTMLResponse)
async def get_marketplace(request: Request):
    db = load_db()
    return templates.TemplateResponse("marketplace.html", {"request": request, "productos": db["productos"], "user": request.session.get("user")})

@app.get("/planner", response_class=HTMLResponse)
async def get_planner(request: Request):
    db = load_db()
    return templates.TemplateResponse("planner.html", {"request": request, "recetas": db["recetas"], "dias": range(1, 31), "user": request.session.get("user")})

@app.get("/batch-cooking", response_class=HTMLResponse)
async def get_batch_cooking(request: Request):
    db = load_db()
    frozen = [r for r in db["recetas"] if "Congelable" in r["tag"] or "Batch Cooking" in r["tag"]]
    return templates.TemplateResponse("batch_cooking.html", {"request": request, "recetas": frozen, "user": request.session.get("user")})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
