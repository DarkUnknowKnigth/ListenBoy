# import speech_recognition as sr
from tkinter import *
from audio import *
import customtkinter
from customtkinter import CTkButton, CTkLabel, CTkRadioButton

# Opciones
def opciones_multiarchivos(procesador_audio: Audio, opcion):
    if procesador_audio:
        seleccion = opcion.get()
        if seleccion == 1:
            procesador_audio.conversion(True)
        else:
            procesador_audio.conversion(False)
        notification = customtkinter.CTk()
        notification.geometry("200x240")
        notification.title("Mensaje")
        mensaje = CTkLabel(notification, text="Proceso terminado visite la carpeta /output \n Ya puede cerrar la ventana")
        mensaje.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
        notification.mainloop()

# Crear ventana de diálogo para seleccionar archivo de audio
def ui():
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("400x240")
    app.title("Listen Boy")
    # Form multiple
    opcion_multiples_archivos= IntVar()
    etiqueta_multiples_archivos = CTkLabel(app, text="¿Deseas cargar un archivo de audio largo?") 
    etiqueta_multiples_archivos.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)
    opcion_multiple_si = CTkRadioButton(app, text="Cargar múltiples archivos", variable=opcion_multiples_archivos, value=1)
    opcion_multiple_si.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)
    opcion_multiple_no = CTkRadioButton(app, text="Cargar un solo archivo", variable=opcion_multiples_archivos, value=0)
    opcion_multiple_no.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

    # Form comenzar proceso
    boton = CTkButton(app, text="Iniciar", command=lambda: opciones_multiarchivos(Audio(), opcion_multiples_archivos))
    boton.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
    app.mainloop()
ui()













