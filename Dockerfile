# 1. Usar una imagen base de Python oficial
FROM python:3.12

# 2. Crear una carpeta de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiar el archivo de requerimientos
COPY ./requirements.txt /code/requirements.txt

# 4. Instalar las librerías
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiar todo tu código (la carpeta app) dentro del contenedor
COPY ./app /code/app

# 6. Comando para iniciar el servidor cuando arranque el contenedor
# Nota: Usamos host 0.0.0.0 para que sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]