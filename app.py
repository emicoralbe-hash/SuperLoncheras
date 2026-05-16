from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()

# Montar archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Datos detallados de recetas
RECETAS = [
    {
        "id": 1, 
        "nombre": "Bowl de Quinoa", 
        "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c", 
        "tag": "⚡ Superfood",
        "ingredientes": [
            {"item": "Quinoa", "cant": "1/2 taza", "cat": "Granos"},
            {"item": "Arándanos", "cant": "1/4 taza", "cat": "Frutas"},
            {"item": "Chía", "cant": "1 cda", "cat": "Superalimentos"}
        ],
        "alergias": [],
        "pasos": [
            "Lavar la quinoa bajo el grifo hasta que el agua salga limpia.",
            "Cocinar la quinoa con el doble de agua por 15 minutos.",
            "Mezclar con los arándanos y las semillas de chía en un bowl.",
            "Acompañar con un poco de miel si se desea."
        ],
        "video_url": "v6YREv0t2rU" # ID de ejemplo de YouTube
    },
    {
        "id": 2, 
        "nombre": "Nuggets de Brócoli", 
        "img": "https://images.unsplash.com/photo-1541832676-9b763b0239ab", 
        "tag": "❄️ Congelable",
        "ingredientes": [
            {"item": "Brócoli", "cant": "1 cabeza", "cat": "Verduras"},
            {"item": "Huevo", "cant": "1 unidad", "cat": "Proteínas"},
            {"item": "Queso Parmesano", "cant": "1/2 taza", "cat": "Lácteos"}
        ],
        "alergias": ["Lácteos", "Huevo"],
        "pasos": [
            "Rallar el brócoli crudo finamente.",
            "Mezclar con el huevo batido y el queso parmesano.",
            "Formar pequeñas bolitas y aplastarlas en una bandeja de horno.",
            "Hornear a 200°C por 15-20 minutos hasta que doren."
        ],
        "video_url": "Y90G7_qC5_k"
    },
    {
        "id": 3, 
        "nombre": "Smoothie Verde", 
        "img": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af", 
        "tag": "🍹 Bebida",
        "ingredientes": [
            {"item": "Espinaca", "cant": "1 puñado", "cat": "Verduras"},
            {"item": "Manzana Verde", "cant": "1 unidad", "cat": "Frutas"},
            {"item": "Spirulina", "cant": "1 cdta", "cat": "Superalimentos"}
        ],
        "alergias": [],
        "pasos": [
            "Lavar bien las espinacas y la manzana.",
            "Cortar la manzana en trozos eliminando el corazón.",
            "Licuar todos los ingredientes con un poco de agua o agua de coco.",
            "Servir inmediatamente para aprovechar los nutrientes."
        ],
        "video_url": "2v1rXvS-8p8"
    },
    {
        "id": 4, 
        "nombre": "Salmón Omega-3", 
        "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd", 
        "tag": "🏠 Familiar",
        "ingredientes": [
            {"item": "Salmón", "cant": "200g", "cat": "Proteínas"},
            {"item": "Espárragos", "cant": "1 manojo", "cat": "Verduras"},
            {"item": "Limón", "cant": "1 unidad", "cat": "Frutas"}
        ],
        "alergias": ["Pescado"],
        "pasos": [
            "Sellar el salmón en una sartén caliente con poco aceite.",
            "Añadir los espárragos a la misma sartén.",
            "Cocinar por 4 minutos de cada lado.",
            "Terminar con jugo de limón fresco y una pizca de sal."
        ],
        "video_url": "b8lXh0m0Lp4"
    },
    {
        "id": 5, 
        "nombre": "Sopa de Lentejas", 
        "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd", 
        "tag": "🍲 Batch Cooking",
        "ingredientes": [
            {"item": "Lentejas", "cant": "1 taza", "cat": "Legumbres"},
            {"item": "Zanahoria", "cant": "2 unidades", "cat": "Verduras"},
            {"item": "Kale", "cant": "1 puñado", "cat": "Verduras"}
        ],
        "congelado_tips": "Dura hasta 3 meses. Descongelar en refrigeración 24h antes.",
        "alergias": [],
        "pasos": [
            "Sofreír la zanahoria picada.",
            "Añadir las lentejas y cubrir con agua o caldo de verduras.",
            "Cocinar a fuego lento por 30 minutos.",
            "Añadir el kale picado al final y dejar reposar 5 minutos."
        ]
    }
]

# Datos del Marketplace
PRODUCTOS = [
    {
        "id": 101,
        "nombre": "Quinoa Orgánica Real",
        "precio": 12.50,
        "vendor": "Tu Cosecha (Productor Directo)",
        "img": "https://images.unsplash.com/photo-1586201375761-83865001e31c",
        "cat": "Granos"
    },
    {
        "id": 102,
        "nombre": "Mix Frutos Secos Premium",
        "precio": 18.00,
        "vendor": "Tu Cosecha (Productor Directo)",
        "img": "https://images.unsplash.com/photo-1596591606975-97ee5cef3a1e",
        "cat": "Frutos Secos"
    },
    {
        "id": 103,
        "nombre": "Miel de Abeja Orgánica",
        "precio": 15.00,
        "vendor": "Apícola Local",
        "img": "https://images.unsplash.com/photo-1587049352846-4a222e784d38",
        "cat": "Endulzantes"
    }
]

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, q: str = None, sin_lacteos: bool = False, sin_huevo: bool = False, sin_pescado: bool = False):
    recetas_filtradas = RECETAS
    
    # Búsqueda por nombre
    if q:
        recetas_filtradas = [r for r in recetas_filtradas if q.lower() in r["nombre"].lower()]
        
    # Filtros de alergias
    if sin_lacteos:
        recetas_filtradas = [r for r in recetas_filtradas if "Lácteos" not in r["alergias"]]
    if sin_huevo:
        recetas_filtradas = [r for r in recetas_filtradas if "Huevo" not in r["alergias"]]
    if sin_pescado:
        recetas_filtradas = [r for r in recetas_filtradas if "Pescado" not in r["alergias"]]
        
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "recetas": recetas_filtradas,
        "filtros": {"lacteos": sin_lacteos, "huevo": sin_huevo, "pescado": sin_pescado},
        "query": q
    })

@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def get_recipe(request: Request, recipe_id: int):
    receta = next((r for r in RECETAS if r["id"] == recipe_id), None)
    return templates.TemplateResponse("recipe_detail.html", {"request": request, "receta": receta})

@app.get("/planner", response_class=HTMLResponse)
async def get_planner(request: Request):
    dias = range(1, 31)
    return templates.TemplateResponse("planner.html", {"request": request, "dias": dias, "recetas": RECETAS})

@app.get("/batch-cooking", response_class=HTMLResponse)
async def get_batch_cooking(request: Request, sin_lacteos: bool = False):
    frozen_recipes = [r for r in RECETAS if "Congelable" in r["tag"] or "Batch Cooking" in r["tag"]]
    if sin_lacteos:
        frozen_recipes = [r for r in frozen_recipes if "Lácteos" not in r["alergias"]]
        
    return templates.TemplateResponse("batch_cooking.html", {
        "request": request, 
        "recetas": frozen_recipes,
        "filtros": {"lacteos": sin_lacteos}
    })

@app.get("/marketplace", response_class=HTMLResponse)
async def get_marketplace(request: Request):
    return templates.TemplateResponse("marketplace.html", {"request": request, "productos": PRODUCTOS})

if __name__ == "__main__":
    print("Iniciando prototipo de SuperLoncheras en http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
