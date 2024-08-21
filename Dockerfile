# Basis-Image mit Python
FROM python:3.11-slim

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere die app.py in das Arbeitsverzeichnis
COPY app.py .

# Installiere Flask
RUN pip install flask

# Exponiere den Port, auf dem die Flask-App läuft
EXPOSE 5000

# Starte die Flask-App
CMD ["python", "app.py"]
