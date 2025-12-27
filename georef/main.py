from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from datetime import datetime

app = FastAPI(title="Georef Microservice")

# ==============================
# DATABASE CONFIG (Manual/Local)
# ==============================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root", # Default for many local setups, user should verify
    "database": "roadsense",
    "port": 3306,
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ==============================
# HEALTH
# ==============================
@app.get("/")
def root():
    return {"message": "Georef microservice OK"}

@app.get("/health")
def health():
    return {"status": "georef running"}

# ==============================
# DATA MODEL
# ==============================
class GeoRequest(BaseModel):
    image_id: str
    lon: float
    lat: float
    score: float | None = None
    priorite: str | None = None

# ==============================
# INSERT DAMAGE
# ==============================
@app.post("/georef")
def georef(data: GeoRequest):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO damages (image_id, score, priorite, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            data.image_id,
            data.score,
            data.priorite,
            data.lat,
            data.lon,
        )
    )

    damage_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "saved",
        "id": damage_id,
        "image_id": data.image_id,
        "latitude": data.lat,
        "longitude": data.lon,
    }

# ==============================
# GET ALL DAMAGES (CARTE)
# ==============================
@app.get("/damages")
def get_all_damages():
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        """
        SELECT
            id,
            image_id,
            score,
            priorite,
            latitude,
            longitude,
            created_at
        FROM damages
        ORDER BY created_at DESC
        """
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return {
        "count": len(rows),
        "damages": rows
    }
