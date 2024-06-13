import speech_recognition as sr
import pyaudio
import wave

class Transcribir:
    def __init__(
        self,
        formato: pyaudio,
        canales: int,
        tasa_muestreo: int,
        tamanio_bufer: int,
        duracion_grabacion: int,
        ruta_archivo: str,
    ):    

        self.formato = formato
        self.canales = canales
        self.tasa_muestreo = tasa_muestreo
        self.tamanio_bufer = tamanio_bufer
        self.duracion_grabacion = duracion_grabacion
        self.ruta_archivo = ruta_archivo

    def grabacion_de_audio(self):
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=self.formato,
                channels=self.canales,
                rate=self.tasa_muestreo,
                input=True,
                frames_per_buffer=self.tamanio_bufer,
            ) 
            print("Grabacion empezada.........")
            
            frames = []
            
            #Grabacion de audio
            for i in range(0, int(self.tasa_muestreo / self.tamanio_bufer * self.duracion_grabacion)):
                data = stream.read(self.tamanio_bufer)
                frames.append(data)
                
            print("Grabacion finalizada")
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            
            wf = wave.open(self.ruta_archivo, "wb")
            wf.setnchannels(self.canales)
            wf.setsampwidth(audio.get_sample_size(self.formato))
            wf.setframerate(self.tasa_muestreo)
            wf.writeframes(b"".join(frames))  
            wf.close()
            
            resultado = self.transcribir_audio(self.ruta_archivo)
            
            if resultado["estado"] == "success":
                return {
                    "estado": "success",
                    "mensaje": "Proceso culminado con exito",
                    "texto": resultado["texto"],
                }
            return {
                "estado": "failed",
                "mensaje": "No se pudo culminar con exito el proceso",
            }             
        except Exception as exception:
            raise NameError(
                f"Ha ocurrido un error al grabar el audio, revisa {exception}"
            ) 
    def transcribir_audio(self, ruta_audio):
        try:
            r = sr.Recognizer()
            audio_file = sr.AudioFile(ruta_audio)
            
            with audio_file as source:
                audio = r.record(source)
                
            texto = r.recognize_google(audio, language="es-ES")
            
            if texto:
                return {
                    "estado": "success",
                    "mensaje": "Audio transcrito de manera exitosa",
                    "texto": texto,
                } 
            return {
                "estado": "failed",
                "mensaje": "No se pudo transcribir el audio",
            }       
          
        except Exception as exception:
            raise NameError(
                f"Ha ocurrido un error al grabar el audio, revisa {exception}"
            ) 
            
formato = pyaudio.paInt16
canales = 2
tasa_muestreo = 44100
tamanio_bufer = 1024
duracion_grabacion = 15
ruta_archivo = "audio_grabacion.wav"   

transcribir = Transcribir(
    formato, canales, tasa_muestreo, tamanio_bufer, duracion_grabacion, ruta_archivo
)    

print(transcribir.grabacion_de_audio())                         
