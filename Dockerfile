# Usa la imagen base de tiangolo/uvicorn-gunicorn-fastapi para Python 3.12
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-2024-05-06


ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"

# Instala Tesseract y sus datos de idioma
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libtesseract-dev

# Establece la variable de entorno TESSDATA_PREFIX
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

# Copiar el archivo requirements.txt y instalar dependencias de Python
COPY requirements.txt .

RUN pip install -r requirements.txt



# Copia el código de la aplicación
COPY . /app

# Exponer el puerto 8000 en el contenedor
EXPOSE 8000

# Comando para ejecutar la aplicación utilizando uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
