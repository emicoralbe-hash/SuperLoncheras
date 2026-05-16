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
        "nombre": "Bowl de Quinoa y Aguacate Hass", 
        "img": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c", 
        "tag": "⚡ Superfood",
        "ingredientes": [
            {"item": "Quinoa de Boyacá", "cant": "1/2 taza", "cat": "Granos"},
            {"item": "Aguacate Hass", "cant": "1/2 unidad", "cat": "Frutas"},
            {"item": "Chía", "cant": "1 cda", "cat": "Superalimentos"}
        ],
        "alergias": [],
        "pasos": ["Cocinar la quinoa", "Picar el aguacate en cubos", "Mezclar todo en un bowl"],
        "video_url": "v6YREv0t2rU"
    },
    {
        "id": 2, 
        "nombre": "Nuggets de Brócoli y Queso Campesino", 
        "img": "https://images.unsplash.com/photo-1541832676-9b763b0239ab", 
        "tag": "❄️ Congelable",
        "ingredientes": [
            {"item": "Brócoli fresco", "cant": "1 cabeza", "cat": "Verduras"},
            {"item": "Queso Campesino", "cant": "100g", "cat": "Lácteos"},
            {"item": "Huevo", "cant": "1 unidad", "cat": "Proteínas"}
        ],
        "alergias": ["Lácteos", "Huevo"],
        "pasos": ["Rallar el brócoli", "Mezclar con queso y huevo", "Hornear por 15 min"],
        "video_url": "Y90G7_qC5_k"
    },
    {
        "id": 3, 
        "nombre": "Batido de Lulo y Spirulina", 
        "img": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af", 
        "tag": "🍹 Bebida",
        "ingredientes": [
            {"item": "Lulo maduro", "cant": "2 unidades", "cat": "Frutas"},
            {"item": "Spirulina", "cant": "1 cdta", "cat": "Superalimentos"},
            {"item": "Agua de Coco", "cant": "1 taza", "cat": "Bebidas"}
        ],
        "alergias": [],
        "pasos": ["Licuar el lulo con agua de coco", "Añadir spirulina", "Servir frío"],
        "video_url": "2v1rXvS-8p8"
    },
    {
        "id": 4, 
        "nombre": "Arepitas de Yuca y Chía", 
        "img": "https://images.unsplash.com/photo-1599121174707-1304977123a0", 
        "tag": "🏠 Familiar",
        "ingredientes": [
            {"item": "Yuca cocida", "cant": "2 tazas", "cat": "Tubérculos"},
            {"item": "Semillas de Chía", "cant": "1 cda", "cat": "Superalimentos"},
            {"item": "Sal rosada", "cant": "al gusto", "cat": "Especias"}
        ],
        "alergias": [],
        "pasos": ["Masar la yuca cocida", "Agregar chía", "Asar en sartén hasta dorar"],
        "video_url": "v_KjT-vP0lE"
    },
    {
        "id": 5, 
        "nombre": "Patacones al Horno con Atún", 
        "img": "https://images.unsplash.com/photo-1626074353765-517a681e40be", 
        "tag": "🏠 Familiar",
        "ingredientes": [
            {"item": "Plátano Verde", "cant": "2 unidades", "cat": "Frutas"},
            {"item": "Atún en agua", "cant": "1 lata", "cat": "Proteínas"},
            {"item": "Tomate y Cebolla", "cant": "para el hogao", "cat": "Verduras"}
        ],
        "alergias": ["Pescado"],
        "pasos": ["Hacer patacones", "Hornear para que queden crocantes", "Poner atún encima"],
        "video_url": "H4Ym_M7H-4M"
    },
    {
        "id": 6, 
        "nombre": "Crema de Auyama y Jengibre", 
        "img": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a", 
        "tag": "🍲 Batch Cooking",
        "ingredientes": [
            {"item": "Auyama picada", "cant": "500g", "cat": "Verduras"},
            {"item": "Jengibre rallado", "cant": "1 cdta", "cat": "Especias"},
            {"item": "Leche de Coco", "cant": "1/2 taza", "cat": "Bebidas"}
        ],
        "alergias": [],
        "pasos": ["Cocinar auyama con jengibre", "Licuar con leche de coco", "Salpimentar"],
        "video_url": "K8_wWp3vC0E"
    },
    {
        "id": 7, 
        "nombre": "Muffins de Banano y Avena", 
        "img": "https://images.unsplash.com/photo-1558961359-1d99283f085c", 
        "tag": "❄️ Congelable",
        "ingredientes": [
            {"item": "Banano maduro", "cant": "3 unidades", "cat": "Frutas"},
            {"item": "Avena en hojuelas", "cant": "2 tazas", "cat": "Granos"},
            {"item": "Canela", "cant": "1 cdta", "cat": "Especias"}
        ],
        "alergias": [],
        "pasos": ["Aplastar bananos", "Mezclar con avena", "Hornear 20 min"],
        "video_url": "fL-z7_x_O-I"
    },
    {
        "id": 8, 
        "nombre": "Ensalada de Frijol Negro y Maíz", 
        "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd", 
        "tag": "🥗 Saludable",
        "ingredientes": [
            {"item": "Frijol Negro cocido", "cant": "1 taza", "cat": "Legumbres"},
            {"item": "Maíz tierno", "cant": "1/2 taza", "cat": "Granos"},
            {"item": "Cilantro", "cant": "un manojo", "cat": "Verduras"}
        ],
        "alergias": [],
        "pasos": ["Mezclar frijoles y maíz", "Añadir limón y cilantro", "Refrigerar antes de servir"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 9,
        "nombre": "Arroz con Pollo y Verduras",
        "img": "https://images.unsplash.com/photo-1512058560366-cd24295980c7",
        "tag": "🏠 Familiar",
        "ingredientes": [
            {"item": "Arroz blanco", "cant": "1 taza", "cat": "Granos"},
            {"item": "Pollo desmechado", "cant": "1 pechuga", "cat": "Proteínas"},
            {"item": "Arveja y Zanahoria", "cant": "1/2 taza", "cat": "Verduras"}
        ],
        "alergias": [],
        "pasos": ["Cocinar arroz con verduras", "Añadir pollo", "Mezclar bien"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 10,
        "nombre": "Sopa de Guineo (Banano Verde)",
        "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
        "tag": "🍲 Tradicional",
        "ingredientes": [
            {"item": "Guineo verde", "cant": "4 unidades", "cat": "Frutas"},
            {"item": "Carne de res para sopa", "cant": "250g", "cat": "Proteínas"},
            {"item": "Cilantro y Cebolla", "cant": "al gusto", "cat": "Verduras"}
        ],
        "alergias": [],
        "pasos": ["Picar guineo en cuadritos", "Cocinar con carne y aliños", "Servir caliente"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 11,
        "nombre": "Jugo de Guayaba y Avena",
        "img": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b",
        "tag": "🍹 Bebida",
        "ingredientes": [
            {"item": "Guayaba madura", "cant": "3 unidades", "cat": "Frutas"},
            {"item": "Avena en polvo", "cant": "2 cdas", "cat": "Granos"},
            {"item": "Panela rallada", "cant": "1 cda", "cat": "Endulzantes"}
        ],
        "alergias": [],
        "pasos": ["Licuar guayaba con avena", "Colar si se desea", "Endulzar con panela"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 12,
        "nombre": "Tortilla de Espinaca y Champiñones",
        "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
        "tag": "🍳 Desayuno",
        "ingredientes": [
            {"item": "Huevo", "cant": "2 unidades", "cat": "Proteínas"},
            {"item": "Espinaca baby", "cant": "1 taza", "cat": "Verduras"},
            {"item": "Champiñones", "cant": "1/2 taza", "cat": "Verduras"}
        ],
        "alergias": ["Huevo"],
        "pasos": ["Batir huevos", "Añadir espinaca y champiñones", "Cocinar en sartén"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 13,
        "nombre": "Lentejas con Chorizo de Ternera",
        "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
        "tag": "🍲 Familiar",
        "ingredientes": [
            {"item": "Lentejas Pardinas", "cant": "1 taza", "cat": "Legumbres"},
            {"item": "Chorizo de Ternera", "cant": "2 unidades", "cat": "Proteínas"},
            {"item": "Papa picada", "cant": "1 unidad", "cat": "Tubérculos"}
        ],
        "alergias": [],
        "pasos": ["Cocinar lentejas con papa", "Añadir chorizo picado", "Hacer un buen hogao"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 14,
        "nombre": "Salpicón de Frutas Tropicales",
        "img": "https://images.unsplash.com/photo-1490818387583-1baba5e638af",
        "tag": "🍹 Bebida",
        "ingredientes": [
            {"item": "Papaya y Melón", "cant": "1 taza", "cat": "Frutas"},
            {"item": "Banano", "cant": "1 unidad", "cat": "Frutas"},
            {"item": "Jugo de Naranja", "cant": "2 tazas", "cat": "Frutas"}
        ],
        "alergias": [],
        "pasos": ["Picar frutas en cubos", "Mezclar con jugo de naranja", "Servir bien frío"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 15,
        "nombre": "Tostadas de Masa Madre con Tomate",
        "img": "https://images.unsplash.com/photo-1525351484163-7529414344d8",
        "tag": "🍳 Desayuno",
        "ingredientes": [
            {"item": "Pan de Masa Madre", "cant": "2 tajadas", "cat": "Granos"},
            {"item": "Tomate cherry", "cant": "1/2 taza", "cat": "Verduras"},
            {"item": "Aceite de Oliva", "cant": "1 cda", "cat": "Grasas"}
        ],
        "alergias": ["Gluten"],
        "pasos": ["Tostar el pan", "Poner tomate y aceite encima", "Salpimentar"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 16,
        "nombre": "Pancakes de Avena y Arándanos",
        "img": "https://images.unsplash.com/photo-1528452632967-2d43a6d599a7",
        "tag": "🍳 Desayuno",
        "ingredientes": [
            {"item": "Avena molida", "cant": "1 taza", "cat": "Granos"},
            {"item": "Huevo", "cant": "1 unidad", "cat": "Proteínas"},
            {"item": "Arándanos frescos", "cant": "1/4 taza", "cat": "Frutas"}
        ],
        "alergias": ["Huevo"],
        "pasos": ["Licuar ingredientes", "Cocinar en sartén", "Servir con miel"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 17,
        "nombre": "Caldo de Costilla Levanta Muertos",
        "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd",
        "tag": "🍲 Tradicional",
        "ingredientes": [
            {"item": "Costilla de res", "cant": "500g", "cat": "Proteínas"},
            {"item": "Papa Sabanera", "cant": "3 unidades", "cat": "Tubérculos"},
            {"item": "Cilantro", "cant": "al gusto", "cat": "Verduras"}
        ],
        "alergias": [],
        "pasos": ["Pitar la costilla", "Añadir papa y cilantro", "Servir con arepa"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 18,
        "nombre": "Arepa de Choclo con Queso",
        "img": "https://images.unsplash.com/photo-1599121174707-1304977123a0",
        "tag": "🌽 Típico",
        "ingredientes": [
            {"item": "Masa de choclo", "cant": "2 tazas", "cat": "Granos"},
            {"item": "Queso Cuajada", "cant": "100g", "cat": "Lácteos"},
            {"item": "Mantequilla", "cant": "1 cda", "cat": "Grasas"}
        ],
        "alergias": ["Lácteos"],
        "pasos": ["Asar arepa", "Poner queso encima", "Doblar y calentar"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 19,
        "nombre": "Salpicón de Pollo (Lonchera)",
        "img": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
        "tag": "🍱 Lonchera",
        "ingredientes": [
            {"item": "Pollo cocido", "cant": "1/2 pechuga", "cat": "Proteínas"},
            {"item": "Papa picada", "cant": "1 unidad", "cat": "Tubérculos"},
            {"item": "Mayonesa casera", "cant": "1 cda", "cat": "Salsas"}
        ],
        "alergias": ["Huevo"],
        "pasos": ["Mezclar pollo y papa", "Añadir mayonesa", "Refrigerar"],
        "video_url": "vY_KjT-vP0lE"
    },
    {
        "id": 20,
        "nombre": "Smoothie de Mango y Chía",
        "img": "https://images.unsplash.com/photo-1505253716362-afaea1d3d1af",
        "tag": "🍹 Bebida",
        "ingredientes": [
            {"item": "Mango de azúcar", "cant": "2 unidades", "cat": "Frutas"},
            {"item": "Semillas de Chía", "cant": "1 cda", "cat": "Superalimentos"},
            {"item": "Leche de Almendras", "cant": "1 taza", "cat": "Bebidas"}
        ],
        "alergias": [],
        "pasos": ["Licuar mango con leche", "Añadir chía", "Dejar reposar 5 min"],
        "video_url": "vY_KjT-vP0lE"
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
