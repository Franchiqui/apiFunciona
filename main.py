from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.traductor import traductor_func
from app.video import video_func
from app.scanTexto import scanTexto_func
from app.transcribir import transcribir_func
import os

app = FastAPI()

class Libro(BaseModel):
    titulo: str
    autor: str
    paginas: int
    editorial: str

@app.get("/")
def index():
    return {"message": "Hola, Pythonianos"}

@app.get("/libros/{id}")
def mostrar_libro(id: int):
    return {"data": id}

@app.get("/libros")
def mostrar_libros():
    return {"data": "Lista de libros"}

@app.post("/libros")
def insertar_libro(libro: Libro):
    return {"message": f"Libro {libro.titulo} insertado"}

@app.put("/libros/{id}")
def actualizar_libro(id: int, libro: Libro):
    return {"message": f"Libro {libro.titulo} actualizado"}

@app.delete("/libros/{id}")
def eliminar_libro(id: int):
    return {"message": f"Libro {id} eliminado"}

@app.post("/scanTexto")
async def scanTexto_endpoint(file: UploadFile = File(...)):
    try:
        # Guardar el archivo subido
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Escanear el texto
        escaner = scanTexto_func(file_location)

        # Eliminar el archivo después de procesarlo
        os.remove(file_location)

        return {"data": escaner}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

class TraductorRequest(BaseModel):
    translate_text: str
    target_lang: str

@app.get("/video")
def video():
    return video_func()

@app.post("/traductor")
async def traductor_endpoint(traductor_data: TraductorRequest):
    translate_text = traductor_data.translate_text
    target_lang = traductor_data.target_lang
    traduccion = traductor_func(translate_text, target_lang)
    return {"data": traduccion}

class TranscribirRequest(BaseModel):
    iniciar_escucha: str
    recibir_texto_transcrito: str
    parar_escucha: str


@app.post("/transcribir")
async def transcribir_endpoint(transcribir_data: TranscribirRequest):
    iniciar_escucha = transcribir_data.iniciar_escucha
    recibir_texto_transcrito = transcribir_data.recibir_texto_transcrito
    parar_escucha = transcribir_data.parar_escucha
    transcripcion = transcribir_func(iniciar_escucha, recibir_texto_transcrito, parar_escucha)
    return {"data": transcripcion}

