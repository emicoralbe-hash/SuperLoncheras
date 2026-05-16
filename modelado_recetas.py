import json

class Receta:
    def __init__(self, nombre, ingredientes, pasos, es_congelable=False, superalimentos=None, alergias=None):
        self.nombre = nombre
        self.ingredientes = ingredientes  # Lista de dicts: {"item": "Quinoa", "cantidad": "100g"}
        self.pasos = pasos  # Lista de strings
        self.es_congelable = es_congelable
        self.superalimentos = superalimentos or []
        self.alergias = alergias or []

    def to_dict(self):
        return self.__dict__

# Ejemplo de base de datos inicial
base_datos_ejemplo = [
    Receta(
        nombre="Bowl de Quinoa y Arándanos",
        ingredientes=[
            {"item": "Quinoa cocida", "cantidad": "1 taza"},
            {"item": "Arándanos frescos", "cantidad": "1/2 taza"},
            {"item": "Semillas de Chía", "cantidad": "1 cda"},
            {"item": "Yogurt griego natural", "cantidad": "1/2 taza"}
        ],
        pasos=[
            "Lavar bien la quinoa y cocinarla según instrucciones.",
            "Mezclar la quinoa con el yogurt en un bowl.",
            "Añadir los arándanos y las semillas de chía por encima.",
            "Servir frío o a temperatura ambiente."
        ],
        es_congelable=False,
        superalimentos=["Quinoa", "Arándanos", "Chía"],
        alergias=["Lácteos"]
    ),
    Receta(
        nombre="Lonchera de Nuggets de Brócoli (Batch Cooking)",
        ingredientes=[
            {"item": "Brócoli rallado", "cantidad": "2 tazas"},
            {"item": "Huevo", "cantidad": "1 unidad"},
            {"item": "Queso parmesano", "cantidad": "1/2 taza"},
            {"item": "Harina de almendras", "cantidad": "1/2 taza"}
        ],
        pasos=[
            "Mezclar todos los ingredientes en un bowl hasta formar una masa.",
            "Formar pequeños nuggets con las manos.",
            "Hornear a 180°C por 20 minutos o hasta que doren.",
            "Para congelar: Dejar enfriar totalmente y guardar en bolsas herméticas."
        ],
        es_congelable=True,
        superalimentos=["Brócoli", "Almendras"],
        alergias=["Huevo", "Frutos secos"]
    ),
    Receta(
        nombre="Mini Pizza Pockets de Vegetales",
        ingredientes=[
            {"item": "Harina de trigo integral", "cantidad": "500g"},
            {"item": "Espinaca picada", "cantidad": "1 taza"},
            {"item": "Champiñones picados", "cantidad": "1/2 taza"},
            {"item": "Salsa de tomate casera", "cantidad": "1 taza"},
            {"item": "Queso mozzarella rallado", "cantidad": "200g"}
        ],
        pasos=[
            "Preparar la masa integral y dejar leudar.",
            "Estirar la masa y cortar círculos de 10cm.",
            "Rellenar con salsa, vegetales salteados y queso.",
            "Cerrar como una empanada y sellar bordes con tenedor.",
            "Hornear a 200°C por 15 min hasta que doren.",
            "Dejar enfriar completamente antes de congelar."
        ],
        es_congelable=True,
        superalimentos=["Espinaca", "Champiñones", "Harina Integral"],
        alergias=["Gluten", "Lácteos"]
    )
]

def guardar_recetas(recetas, filename="recetas_base.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([r.to_dict() for r in recetas], f, indent=4, ensure_ascii=False)
    print(f"Base de datos guardada en {filename}")

if __name__ == "__main__":
    guardar_recetas(base_datos_ejemplo)
