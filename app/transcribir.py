import speech_recognition as sr
import pyaudio
import wave

class Transcribir:
    def __init__(
        self,
        formato: pyaudio.paInt16,
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

        self.escuchando = False
        self.texto_transcrito = ""

    def iniciar_escucha(self):
        if not self.escuchando:
            self.escuchando = True
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

                # Grabacion de audio
                while self.escuchando:
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

                self.escuchando = False

                # Transcripcion del audio
                self.texto_transcrito = self.transcribir_audio(self.ruta_archivo)

            except Exception as exception:
                raise NameError(
                    f"Ha ocurrido un error al grabar el audio, revisa {exception}"
                )

    def recibir_texto_transcrito(self):
        if self.texto_transcrito:
            return {
                "estado": "success",
                "mensaje": "Audio transcrito de manera exitosa",
                "texto": self.texto_transcrito,
            }
        else:
            return {
                "estado": "failed",
                "mensaje": "No se ha transcrito audio aún",
            }

    def parar_escucha(self):
        self.escuchando = False

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
            else:
                return {
                    "estado": "failed",
                    "mensaje": "No se pudo transcribir el audio",
                }

        except Exception as exception:
            raise NameError(
                f"Ha ocurrido un error al transcribir el audio, revisa {exception}"
            )

# Ejemplo de uso
formato = pyaudio.paInt16
canales = 2
tasa_muestreo = 44100
tamanio_bufer = 1024
duracion_grabacion = 15
ruta_archivo = "audio_grabacion.wav"

transcribir = Transcribir(
    formato, canales, tasa_muestreo, tamanio_bufer, duracion_grabacion, ruta_archivo
)

# Iniciar escucha
transcribir.iniciar_escucha()

# Recibir texto transcrito (mientras se graba)
texto_transcrito = transcribir.recibir_texto_transcrito()
print(texto_transcrito)

# Parar escucha
transcribir.parar_escucha
