# Guide d'Installation Manuelle (Sans Docker)

Ce guide vous explique comment lancer le projet RoadSense sur Windows sans utiliser Docker.

## Prérequis

Vous devez installer les logiciels suivants sur votre machine :

1.  **MySQL Server** (8.0 ou plus récent)
    *   Lors de l'installation, notez bien le mot de passe `root`.
    *   Assurez-vous que le service MySQL est lancé.
2.  **Python 3.10+**
    *   Cochez "Add Python to PATH" lors de l'installation.
3.  **Node.js 18+** (LTS recommandé)
    *   Vérifiez avec `node -v` et `npm -v`.

Optionnel mais recommandé :
*   **Git Bash** ou un termina Powershell confortable.
*   **MinIO** (Serveur autonome) `minio.exe` si vous voulez stocker les vidéos localement, ou désactivez la partie stockage vidéo si vous testez juste l'IA. Pour ce guide, nous supposerons que vous avez un exécutable `minio.exe` ou que vous ignorez cette partie pour l'instant.

## Étape 1 : Base de Données (MySQL)

1.  Ouvrez une ligne de commande ou MySQL Workbench.
2.  Connectez-vous à MySQL : `mysql -u root -p`
3.  Créez la base de données et les tables en copiant le contenu du fichier `infra/db/init_mysql.sql`.

```sql
SOURCE infra/db/init_mysql.sql;
-- Ou copiez-collez le contenu SQL ici
```

Assurez-vous que l'utilisateur `root` avec le mot de passe `root` a accès (ou modifiez les fichiers de config Python).

## Étape 2 : Services Python (Backend)

Nous allons lancer les services principaux.

### 2.1 RoadSense Core
Ce service gère l'API principale.

1.  Ouvrez un terminal dans `roadsense-core`.
2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3.  Lancez le serveur :
    ```bash
    uvicorn app.main:app --port 8000 --reload
    ```
    *Il devrait se connecter à MySQL sur localhost:3306.*

### 2.2 Detection Fissures
Service d'IA (si vous voulez tester la détection).

1.  Ouvrez un **nouveau terminal** dans `detection-fissures`.
2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3.  Lancez le service :
    ```bash
    uvicorn app:app --port 8001 --reload
    ```

### 2.3 Georef
Service de géoréférencement.

1.  Ouvrez un **nouveau terminal** dans `georef`.
2.  Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
3.  Lancez le service :
    ```bash
    uvicorn main:app --port 9003 --reload
    ```

## Étape 3 : Frontend (Dashboard)

1.  Ouvrez un **nouveau terminal** dans `dashboard`.
2.  Installez les dépendances :
    ```bash
    npm install
    ```
3.  Lancez le site :
    ```bash
    npm run dev
    ```
4.  Ouvrez le lien affiché (ex: http://localhost:5173).

## Script Automatique (start_all.bat)

Un script `start_all.bat` a été créé à la racine.
Double-cliquez dessus pour tenter de lancer tous les services d'un coup (nécessite que Python et npm soient dans le PATH).
**Attention** : Vous devez avoir installé les dépendances (`pip install ...` et `npm install`) au moins une fois manuellement avant d'utiliser le script.
