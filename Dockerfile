# Usa la imagen base de Python
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requerimientos y el código de la app
COPY requirements.txt requirements.txt
COPY . .

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto 5000 y ejecuta la app
EXPOSE 5000
CMD ["python", "app.py"]
