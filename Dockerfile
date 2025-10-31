# Imagen base de Python
FROM python:3.11-slim

# Evitar que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    pip install --upgrade pip

# Copiar archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
