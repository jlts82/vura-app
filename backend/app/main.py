from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import base64
from PIL import Image
import io
import random

app = FastAPI(title="Vura API", version="0.1.0")

# Base de datos temporal de comidas mexicanas
FOOD_DB = {
    "tacos_al_pastor": {
        "name_es": "Tacos al pastor",
        "name_en": "Al pastor tacos",
        "calories_per_100g": 226,
        "protein": 12,
        "carbs": 28,
        "fat": 8
    },
    "tacos_barbacoa": {
        "name_es": "Tacos de barbacoa",
        "name_en": "Barbacoa tacos",
        "calories_per_100g": 245,
        "protein": 15,
        "carbs": 25,
        "fat": 10
    },
    "enchiladas_verdes": {
        "name_es": "Enchiladas verdes",
        "name_en": "Green enchiladas",
        "calories_per_100g": 168,
        "protein": 8,
        "carbs": 22,
        "fat": 6
    },
    "chilaquiles": {
        "name_es": "Chilaquiles",
        "name_en": "Chilaquiles",
        "calories_per_100g": 141,
        "protein": 6,
        "carbs": 20,
        "fat": 5
    },
    "pozole": {
        "name_es": "Pozole",
        "name_en": "Pozole",
        "calories_per_100g": 120,
        "protein": 8,
        "carbs": 15,
        "fat": 3
    }
}

@app.get("/")
def root():
    return {
        "message": "Vura API - Tu plato, sin secretos",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model": "mock-v1"}

@app.post("/api/v1/analyze")
async def analyze_food(file: UploadFile = File(...)):
    """
    Analiza una imagen de comida y retorna información nutricional.
    Versión mock: simula análisis con datos realistas.
    """
    try:
        # Leer imagen
        contents = await file.read()
        
        # Simular procesamiento (en versión real aquí iría el modelo IA)
        # Por ahora seleccionamos aleatoriamente para demo
        food_key = random.choice(list(FOOD_DB.keys()))
        food = FOOD_DB[food_key]
        
        # Simular peso detectado (en realidad se calcularía de la imagen)
        weight_g = random.randint(250, 400)
        
        # Calcular totales
        calories = int((weight_g / 100) * food["calories_per_100g"])
        
        return {
            "success": True,
            "food_class": food_key,
            "food_name_es": food["name_es"],
            "food_name_en": food["name_en"],
            "confidence": round(random.uniform(0.75, 0.95), 2),
            "estimated_weight_g": weight_g,
            "calories_total": calories,
            "calories_per_100g": food["calories_per_100g"],
            "macros": {
                "protein_g": round((weight_g / 100) * food["protein"], 1),
                "carbs_g": round((weight_g / 100) * food["carbs"], 1),
                "fat_g": round((weight_g / 100) * food["fat"], 1)
            },
            "has_reference_object": random.choice([True, False]),
            "model_version": "vura-mock-v0.1.0"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/v1/analyze-base64")
async def analyze_base64(image_base64: str):
    """
    Versión alternativa: recibe imagen en base64 (para app móvil).
    """
    try:
        # Decodificar base64
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Mismo análisis mock
        food_key = random.choice(list(FOOD_DB.keys()))
        food = FOOD_DB[food_key]
        weight_g = random.randint(250, 400)
        calories = int((weight_g / 100) * food["calories_per_100g"])
        
        return {
            "success": True,
            "food_class": food_key,
            "food_name_es": food["name_es"],
            "food_name_en": food["name_en"],
            "confidence": round(random.uniform(0.75, 0.95), 2),
            "estimated_weight_g": weight_g,
            "calories_total": calories,
            "macros": {
                "protein_g": round((weight_g / 100) * food["protein"], 1),
                "carbs_g": round((weight_g / 100) * food["carbs"], 1),
                "fat_g": round((weight_g / 100) * food["fat"], 1)
            },
            "image_size": image.size,
            "model_version": "vura-mock-v0.1.0"
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Invalid image data"}
        )