FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx libglib2.0-0

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos requeridos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Exponer el puerto que usará Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
