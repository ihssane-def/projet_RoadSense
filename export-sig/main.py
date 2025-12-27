from fastapi import FastAPI
from fastapi.responses import JSONResponse
import mysql.connector
import json

app = FastAPI(title="Export SIG Service")


# =========================
# DB CONNECTION
# =========================
def connect_db():
    return mysql.connector.connect(
        database="roadsense",
        user="root",
        password="root",
        host="localhost",
        port="3306"
    )


# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"status": "export-sig running"}


# =========================
# EXPORT GEOJSON
# =========================
@app.get("/export/geojson")
def export_geojson():
    conn = connect_db()
    cur = conn.cursor()

    # MySQL doesn't have ST_AsGeoJSON built-in easily for returning string directly in same way as PostGIS unless using specific versions/functions.
    # We stored lat/lon in 'damages' table.
    # Note: the original code selected from 'georef' table, but 'georef' service writes to 'damages'.
    # In my migration I unified to use 'damages' table since 'georef' table in init.sql seemed unused by the main logic I saw.
    # Let's select from 'damages'.

    cur.execute("""
        SELECT image_id, latitude, longitude
        FROM damages;
    """)

    features = []

    for (image_id, lat, lon) in cur.fetchall():
        if lat is None or lon is None:
            continue
            
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat] # GeoJSON is [lon, lat]
            },
            "properties": {
                "image_id": image_id
            }
        })

    cur.close()
    conn.close()

    return JSONResponse(
        content={
            "type": "FeatureCollection",
            "features": features
        }
    )
