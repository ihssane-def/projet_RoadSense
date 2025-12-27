from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import random
from PIL import Image, ImageDraw

# ==========================================
# MODE LITE : MOCK AI (Pas de PyTorch)
# ==========================================

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"

DAMAGE_CLASSES = {
    0: "Pothole",
    1: "Crack",
    2: "Open_Manhole"
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app = FastAPI(title="Detection Fissures API (LITE)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 Mode LITE activé : L'IA est simulée pour économiser de l'espace disque.")

@app.get("/health")
def health():
    return {"status": "detection-fissures (LITE) running"}

@app.get("/results/{filename}")
def get_result(filename: str):
    path = os.path.join(RESULT_FOLDER, filename)
    if not os.path.exists(path):
        # Fallback si l'image n'existe pas, on renvoie une placeholder (ou juste 404)
        raise HTTPException(status_code=404, detail="Image non trouvée")
    return FileResponse(path)

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    try:
        image_id = str(uuid.uuid4())
        filename = f"{image_id}.jpg"
        input_path = os.path.join(UPLOAD_FOLDER, filename)

        # Sauvegarde de l'image reçue
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # Simulation de détection
        # On dessine un carré aléatoire sur l'image pour faire "vrai"
        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        
        # Générer 1 ou 2 dommages aléatoires
        damages = []
        num_damages = random.randint(1, 3)
        
        width, height = img.size
        
        for _ in range(num_damages):
            cls_id = random.choice(list(DAMAGE_CLASSES.keys()))
            x1 = random.randint(0, width // 2)
            y1 = random.randint(0, height // 2)
            x2 = x1 + random.randint(50, 200)
            y2 = y1 + random.randint(50, 200)
            
            # Dessiner la bbox
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
            
            damages.append({
                "class": DAMAGE_CLASSES[cls_id],
                "confidence": round(random.uniform(0.75, 0.99), 3),
                "bbox": [x1, y1, x2, y2]
            })

        output_filename = f"annotated_{filename}"
        output_path = os.path.join(RESULT_FOLDER, output_filename)
        img.save(output_path)

        return {
            "image_id": image_id,
            "total_damages": len(damages),
            "damages": damages,
            "annotated_image_url": f"/results/{output_filename}"
        }

    except Exception as e:
        print(f"Erreur: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def stats():
    return {
        "model": "LITE_MODE_SIMULATION",
        "classes": DAMAGE_CLASSES
    }
