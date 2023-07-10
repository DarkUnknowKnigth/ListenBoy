# import speech_recognition as sr
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
from pydub import AudioSegment
import math
import os
import time
import vosk
import sys
import wave


def audio_a_texto(ruta_archivo):
    # r = sr.Recognizer()
    # with sr.AudioFile(ruta_archivo) as fuente:
    #     audio = r.record(fuente)
    #     texto = r.recognize_google(audio, language='es')
        
    #     return texto
    # Ruta al modelo de reconocimiento de voz
    model_path = "./vosk-model-small-es"

    # Ruta al archivo de audio
    audio_file = ruta_archivo

    # Cargar el modelo
    model = vosk.Model(model_path)

    # Abrir el archivo de audio
    wf = wave.open(audio_file, "rb")

    # Crear el reconocedor de voz
    rec = vosk.KaldiRecognizer(model, wf.getframerate())

    # Leer el audio y realizar el reconocimiento
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    # Obtener el resultado final
    result = rec.FinalResult()
    return result

def guardar_texto_en_archivo(texto, ruta_archivo):
    with open(ruta_archivo, 'w') as archivo:
        archivo.write(texto)

def convertir_m4a_a_wav(ruta_archivo_m4a, ruta_archivo_wav):
    audio = AudioSegment.from_file(ruta_archivo_m4a, format='m4a')
    audio.export(ruta_archivo_wav, format='wav')

def dividir_audio_por_tamaño(input_file, segment_size_mb):
    audio = AudioSegment.from_file(input_file)
    segment_size_bytes = segment_size_mb * 1024 * 1024

    num_segments = math.ceil(len(audio) / segment_size_bytes)

    for i in range(num_segments):
        start = i * segment_size_bytes
        end = start + segment_size_bytes

        segment = audio[start:end]
        output_file = f"segment_{i+1}.wav"
        segment.export(output_file, format="wav")

        print(f"Segmento {i+1} creado: {output_file}")
def main(partes=False):
    if not partes:
        # pedir archivo de audio
        ruta_audio = askopenfilename(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.wav')])
        if not ruta_audio:
            print("No se seleccionó ningún archivo de audio.")
            exit()
        # Crear ventana de diálogo para seleccionar carpeta de destino
        ruta_carpeta_destino = askdirectory(title='Seleccionar carpeta de destino')

        if not ruta_carpeta_destino:
            print("No se seleccionó ninguna carpeta de destino.")
            exit()
        # Llamada a la función para convertir el audio a texto
        texto_convertido = audio_a_texto(ruta_audio)

        # Nombre del archivo de texto de salida
        nombre_archivo = os.path.basename(ruta_audio).split('.')[0]+".txt"
        # Ruta completa al archivo de texto de salida
        ruta_archivo_salida = ruta_carpeta_destino + '/' + nombre_archivo

        # Guardar el texto en un archivo
        guardar_texto_en_archivo(texto_convertido, ruta_archivo_salida)
        print("Texto convertido guardado en el archivo:", ruta_archivo_salida)
    else:
        archivos = askopenfilenames(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.wav')])
        ruta_carpeta_destino = askdirectory(title='Seleccionar carpeta de destino')

        if not ruta_carpeta_destino:
            print("No se seleccionó ninguna carpeta de destino.")
            exit()
        for archivo in archivos:
            texto_convertido = audio_a_texto(archivo)
            # Nombre del archivo de texto de salida
            nombre_archivo = os.path.basename(archivo).split('.')[0]+".txt"
            # Ruta completa al archivo de texto de salida
            ruta_archivo_salida = ruta_carpeta_destino + '/' + nombre_archivo
            # Guardar el texto en un archivo
            guardar_texto_en_archivo(texto_convertido, ruta_archivo_salida)
            print("Texto convertido guardado en el archivo:", ruta_archivo_salida)
            # Detener el tiempo+
            time.sleep(20)
            print("Tiempo 20s")

def preconversor_a_wav(subdividir = True):
    # pedir archivo de audio
    ruta_audio = askopenfilename(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.m4a')])
    if not ruta_audio:
        print("No se seleccionó ningún archivo de audio.")
        exit()
    ruta_archivo_wav =  "./"+os.path.basename(ruta_audio).split('.')[0]+".wav"
    convertir_m4a_a_wav(ruta_audio, ruta_archivo_wav)
    if subdividir:
        tamaño_segmento_mb = 0.1
        dividir_audio_por_tamaño(ruta_archivo_wav,tamaño_segmento_mb)

# Crear ventana de diálogo para seleccionar archivo de audio
Tk().withdraw()
preconversor_a_wav()
main(False)













