import json
import os
import sys
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Intentar montar estáticos
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

templates = Jinja2Templates(directory="templates")

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {"recetas": [], "productos": [], "usuarios": [{"email": "admin@superloncheras.com", "pass": "admin123", "role": "admin"}]}

@app.get("/")
async def read_item(request: Request):
    try:
        db = load_db()
        return templates.TemplateResponse("index.html", {
            "request": request, 
            "recetas": db.get("recetas", []), 
            "query": None, 
            "user": request.session.get("user")
        })
    except Exception as e:
        # SI FALLA, NOS DIRÁ EL ERROR EN LA WEB DIRECTAMENTE
        return PlainTextResponse(f"ERROR DETECTADO: {str(e)}")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
