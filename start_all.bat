@echo off
TITLE RoadSense Launcher
echo ==========================================
echo       Lancement du projet RoadSense
echo ==========================================
echo.
echo [INFO] Assurez-vous que MySQL est bien lance (root/root).
echo.
pause

:: Start Core
echo.
echo [1/4] Lancement roadsense-core (Port 8000)...
start "RoadSense Core" cmd /k "cd roadsense-core && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn app.main:app --port 8000 --reload"

:: Start Georef
echo.
echo [2/4] Lancement Georef (Port 9003)...
start "Georef" cmd /k "cd georef && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn main:app --port 9003 --reload"

:: Start Score Gravite
echo.
echo [Optionnel] Lancement Score Gravite (Port 9004)...
start "Score Gravite" cmd /k "cd score-gravite && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn main:app --port 9004 --reload"

:: Start Prioritisation
echo.
echo [Optionnel] Lancement Prioritisation (Port 9005)...
start "Prioritisation" cmd /k "cd prioritisation && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn main:app --port 9005 --reload"

:: Start Ingestion (Optional - Go)
echo.
echo [Optionnel] Lancement Ingestion Video (Port 8080)...
start "Ingestion Video" cmd /k "cd ingestion-video && go run main.go"

:: Start Export SIG
echo.
echo [Optionnel] Lancement Export SIG (Port 9006)...
start "Export SIG" cmd /k "cd export-sig && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn main:app --port 9006 --reload"

:: Start Detection (Optional)
echo.
echo [Optionnel] Lancement Detection Fissures (Port 8001)...
start "Detection IA" cmd /k "cd detection-fissures && echo Installation des deps... && pip install -r requirements.txt && python -m uvicorn app:app --port 8001 --reload"

:: Start Frontend
echo.
echo [4/4] Lancement Dashboard...
cd dashboard
echo Installation des dependances (si besoin)...
call npm install
echo Lancement du serveur Web...
npm run dev

pause
