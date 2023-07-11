from pydub import AudioSegment
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
import vosk
import wave
import math
import os

class Audio:
    # Ruta al modelo de reconocimiento de voz
    model_path = ""

    ruta_carpeta_destino = ""
    # Ruta al archivo de audio
    ruta_audio = None
    output_path ='./output/'
    # Cargar el modelo
    model = None
    def __init__(audio) -> None:
        pass
    def audio_a_texto(self, ruta_archivo):
        # r = sr.Recognizer()
        # with sr.AudioFile(ruta_archivo) as fuente:
        #     audio = r.record(fuente)
        #     texto = r.recognize_google(audio, language='es')
            
        #     return texto
        # Ruta al modelo de reconocimiento de voz
        self.model_path = "./vosk-model-small-es"

        # Cargar el modelo
        model = vosk.Model(self.model_path)

        # Abrir el archivo de audio
        wf = wave.open(ruta_archivo, "rb")

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
    def dividir_audio_por_tamaño(self, ruta_archivo, segment_size_mb):
        audio = AudioSegment.from_file(ruta_archivo)
        segment_size_bytes = segment_size_mb * 1024 * 1024

        num_segments = math.ceil(len(audio) / segment_size_bytes)

        for i in range(num_segments):
            start = i * segment_size_bytes
            end = start + segment_size_bytes

            segment = audio[start:end]
            output_file = f"segment_{i+1}.wav"
            segment.export(self.output_path + output_file, format="wav")

            print(f"Segmento {i+1} creado: {output_file}")
    def convertir_m4a_a_wav(self, ruta_archivo_m4a, ruta_archivo_wav):
        extension = self.obtener_extension(ruta_archivo_m4a)
        audio = AudioSegment.from_file(ruta_archivo_m4a, format=extension)
        if audio:
            audio.export(ruta_archivo_wav, format='wav')
        else:
            print("No podemos convertir el archivo")
    def preconversor_a_wav(self, subdividir = True, tamaño_segmento_mb= 0.1):
        # pedir archivo de audio
        self.ruta_audio = askopenfilename(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.mp3;*.m4a;*.acc')])
        if not self.ruta_audio:
            print("No se seleccionó ningún archivo de audio.")
            exit()
        ruta_archivo_wav =  self.output_path + self.obtener_nombre(self.ruta_audio)+".wav"
        self.convertir_m4a_a_wav(self.ruta_audio, ruta_archivo_wav)
        if subdividir:
            self.dividir_audio_por_tamaño(ruta_archivo_wav,tamaño_segmento_mb)
    def conversion(self, partes=False):
        self.preconversor_a_wav(subdividir=False,tamaño_segmento_mb=0.1)
        if not partes:
            # pedir archivo de audio
            self.ruta_audio = askopenfilename(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.wav')])
            if not self.ruta_audio:
                print("No se seleccionó ningún archivo de audio.")
                exit()
            # Crear ventana de diálogo para seleccionar carpeta de destino
            self.ruta_carpeta_destino = askdirectory(title='Seleccionar carpeta de destino')
            if not self.ruta_carpeta_destino:
                print("No se seleccionó ninguna carpeta de destino.")
                exit()
            # Llamada a la función para convertir el audio a texto
            texto_convertido = self.audio_a_texto(self.ruta_audio)

            # Nombre del archivo de texto de salida
            nombre_archivo = self.obtener_nombre(self.ruta_audio)+".txt"
            # Ruta completa al archivo de texto de salida
            ruta_archivo_salida = self.ruta_carpeta_destino + '/' + self.output_path +nombre_archivo

            # Guardar el texto en un archivo
            self.guardar_texto_en_archivo(texto_convertido, ruta_archivo_salida)
            print("Texto convertido guardado en el archivo:", ruta_archivo_salida)
        else:
            archivos = askopenfilenames(title='Seleccionar archivo de audio', filetypes=[('Archivos de audio', '*.mp3;*.m4a;*.acc')])
            self.ruta_carpeta_destino = askdirectory(title='Seleccionar carpeta de destino')

            if not self.ruta_carpeta_destino:
                print("No se seleccionó ninguna carpeta de destino.")
                exit()
            for archivo in archivos:
                texto_convertido = self.audio_a_texto(archivo)
                # Nombre del archivo de texto de salida
                nombre_archivo = self.obtener_nombre(archivo)+".txt"
                # Ruta completa al archivo de texto de salida
                ruta_archivo_salida = self.ruta_carpeta_destino + '/' + self.output_path +nombre_archivo
                # Guardar el texto en un archivo
                self.guardar_texto_en_archivo(texto_convertido, ruta_archivo_salida)
                print("Texto convertido guardado en el archivo:", ruta_archivo_salida)
    def guardar_texto_en_archivo(self, texto, ruta_archivo):
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(texto)

    def obtener_nombre(self, ruta_archivo):
        nombre = os.path.basename(ruta_archivo).split('.')[0]
        return nombre

    def obtener_extension(self, ruta_archivo):
        extension = os.path.basename(ruta_archivo).split('.')[1]
        return extension