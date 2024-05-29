import cv2
import pytesseract

def scanTexto_func(imagePath):
    """
    Extrae texto de una imagen y lo devuelve como cadena.

    Argumentos:
        imagePath (str): Ruta al archivo de imagen a escanear.

    Retorno:
        str: El texto extraído de la imagen.
    """

    # Cargar la imagen
    img = cv2.imread(imagePath)

    # Compruebe si la imagen se leyó correctamente.
    if img is None:
        raise Exception("Error loading image: {}".format(imagePath))

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar umbrales para convertir a una imagen binaria
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Establecer la ruta de Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:/Archivos de programa/Tesseract-OCR/tesseract.exe'

    # Establecer el idioma del texto
    text = pytesseract.image_to_string(img, config='--psm 10 lang=es')

    # Extraer texto usando pytesseract
    text = pytesseract.image_to_string(threshold_img)

    # Devolver el texto extraído
    return text



