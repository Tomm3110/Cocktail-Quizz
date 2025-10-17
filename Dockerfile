# ===========================
# Dockerfile - Flask App
# ===========================

# Étape 1 : Choisir une image de base Python légère
FROM python:3.12-slim

# Étape 2 : Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Étape 3 : Copier les fichiers de dépendances
COPY requirements.txt .

# Étape 4 : Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le code source de l'application
COPY . .

# Étape 6 : Exposer le port Flask (5000 par défaut)
EXPOSE 5000

# Étape 7 : Définir la commande de lancement
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
