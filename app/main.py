from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO

from app.clip_service import load_references, predict_animal
from app.animal_service import get_animal_data

app = FastAPI(title="Animal Recognition API")


@app.on_event("startup")
def startup_event():
    load_references()


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "API FaunaLog funcionando"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Envie uma imagem válida."
        )

    image_bytes = await file.read()

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível abrir a imagem."
        )

    try:
        results = predict_animal(image)
        best = results[0]

        animal_data = get_animal_data(best["display_name"])

        return {
            "animal": best["animal"],
            "display_name": best["display_name"],
            "scientific_name": best["scientific_name"],
            "confidence": round(best["confidence"], 4),
            "best_reference": best["best_reference"],
            "data": animal_data,
            "top_results": results,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )