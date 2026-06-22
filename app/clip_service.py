from pathlib import Path
from PIL import Image
from sentence_transformers import SentenceTransformer, util
import json

REFERENCES_DIR = Path("references")

print("Carregando CLIP...")
model = SentenceTransformer("clip-ViT-B-32")
print("CLIP carregado.")

reference_data = []


def load_animal_metadata(animal_folder: Path):
    metadata = {
        "animal": animal_folder.name,
        "display_name": animal_folder.name.replace("-", " ").replace("_", " ").title(),
        "scientific_name": animal_folder.name.replace("-", " ").replace("_", " ").title(),
    }

    metadata_file = animal_folder / "metadata.json"

    if metadata_file.exists():
        with open(metadata_file, "r", encoding="utf-8") as file:
            custom_metadata = json.load(file)
            metadata.update(custom_metadata)

    return metadata


def load_references():
    reference_data.clear()

    for animal_folder in REFERENCES_DIR.iterdir():
        if not animal_folder.is_dir():
            continue

        metadata = load_animal_metadata(animal_folder)

        for image_path in animal_folder.iterdir():
            if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue

            image = Image.open(image_path).convert("RGB")
            embedding = model.encode(image, convert_to_tensor=True)

            reference_data.append({
                "animal": metadata["animal"],
                "display_name": metadata["display_name"],
                "scientific_name": metadata["scientific_name"],
                "image": image_path.name,
                "embedding": embedding
            })

    print(f"{len(reference_data)} imagens de referência carregadas.")


def predict_animal(image: Image.Image):
    if not reference_data:
        raise Exception("Nenhuma imagem de referência carregada.")

    query_embedding = model.encode(image.convert("RGB"), convert_to_tensor=True)

    results = []

    for item in reference_data:
        score = util.cos_sim(query_embedding, item["embedding"]).item()

        results.append({
            "animal": item["animal"],
            "display_name": item["display_name"],
            "scientific_name": item["scientific_name"],
            "reference_image": item["image"],
            "score": score
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    grouped = {}

    for result in results:
        animal = result["animal"]

        if animal not in grouped:
            grouped[animal] = {
                "animal": animal,
                "display_name": result["display_name"],
                "scientific_name": result["scientific_name"],
                "confidence": result["score"],
                "best_reference": result["reference_image"]
            }

    final_results = list(grouped.values())
    final_results.sort(key=lambda item: item["confidence"], reverse=True)

    return final_results[:5]