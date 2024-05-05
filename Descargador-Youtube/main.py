import tkinter
import customtkinter
import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable
from moviepy.editor import VideoFileClip
from tkinter import filedialog




def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        
        download_folder = folder_path_var.get()  # Get the selected download folder

        if download_folder:
            if download_choice.get() == "Video MP4":
                video = ytObject.streams.get_highest_resolution()
                file_extension = video.mime_type.split("/")[-1]
                filename = os.path.join(download_folder, video.default_filename)
            else:
                video = ytObject.streams.filter(only_audio=True).first()
                file_extension = "mp3"
                filename = os.path.join(download_folder, ytObject.title + ".mp3")

            if video:
                title_label.configure(text=ytObject.title, text_color="white")
                finishLabel.configure(text="")
                
                video.download(output_path=download_folder, filename=(video.default_filename.replace(".mp4", "") + "." + file_extension))

                if download_choice.get() == "Audio MP3":
                    if convert_to_mp3(os.path.join(download_folder, "temp." + file_extension), filename):
                        os.remove(os.path.join(download_folder, "temp." + file_extension))
                        print("Descarga Completada")
                        finishLabel.configure(text="Descargado!")
                else:
                    os.rename(os.path.join(download_folder, "temp." + file_extension), filename)
                    print("Descarga Completada")
                    finishLabel.configure(text="Descargado!")
            else:
                print("no tiene resolucion adecuada")
                finishLabel.configure(text="No tiene resolucion adecuada", text_color="red")  
        else:
            print("Seleccione una carpeta de descarga")
            finishLabel.configure(text="Seleccione una carpeta de descarga", text_color="red")
                                
    except RegexMatchError:
        print("enlace no es valido")
        finishLabel.configure(text="Error al descargar, Link invalido", text_color="red")
    except VideoUnavailable:
        print("video no disponible o enlace incorrecto")
        finishLabel.configure(text="video no disponible o enlace incorrecto", text_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize 
    bytes_download = total_size - bytes_remaining
    percentage_of_compeletion = int(bytes_download/total_size * 100)

    per = str(int(percentage_of_compeletion))
    pPercentaje.configure(text=per + '%')
    pPercentaje.update()

    progressBar.set(float(percentage_of_compeletion)/100)

def convert_to_mp3(input_file, output_file):
    video = VideoFileClip(input_file)
    video.audio.write_audiofile(output_file)
    video.close()

def choose_folder():
     folder_selected = filedialog.askdirectory()
     folder_path_var.set(folder_selected)

#def choose_resolution():
#    resolution_selected = resolutions_choice.get()
#    print("resolution selected:", resolution_selected)



# configuracion 
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")



# frame de la aplicacion
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Descargador de Youtube")

link_frame = customtkinter.CTkFrame(app)
link_frame.pack(padx=10, pady=10)


# añado la interfaz 
title_label = customtkinter.CTkLabel(link_frame, text="Inserte link de YouTube")
title_label.pack(side="left") # tamaño


#barra de progresso
pPercentaje = customtkinter.CTkLabel(app, text="0%")
pPercentaje.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)


# input para el link 
url_var = tkinter.StringVar() # hago una variable url var para tener la ultima info de que es lo que hay en el link y usarlo en cualquier lado
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()


# menu desplegable
download_choice = customtkinter.StringVar(app)
download_choice.set("Video MP4")

download_menu = customtkinter.CTkOptionMenu(app, values=["Video MP4" , "Audio MP3"], command=lambda value: download_choice.set(value)) 
#download_menu.config(bg="gray", fg="white")
download_menu.pack(padx=10, pady=10)

#download_menu.place(relx=0.76, rely=0.26, anchor=tkinter.W)
#relx= costado; rely= altura

folder_path_var = tkinter.StringVar() # defino una variable para guardar la ruta elejida
folder_label = customtkinter.CTkLabel(app, text="Carpeta de destino") #creo que prompt para que el usuario elija la ruta
folder_label.pack()

folder_path_entry = customtkinter.CTkEntry(app, textvariable=folder_path_var, state="readonly", width=100) 
folder_path_entry.pack()

#creo el boton 
browse_button = customtkinter.CTkButton(app, text="Buscar", command=choose_folder)
browse_button.pack(padx=10, pady=10)

# termino la descarga 
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# selector de resolucion
resolutions = ["720p", "480p", "360p"]

resolutions_var = tkinter.StringVar(app)
resolutions_combobox = tkinter.Combobox(link_frame, values= resolutions, text_variable=resolutions_var )
resolutions_combobox.pack(pady=("10p" , "5p"))
resolutions_combobox.set("720px")

# botton de descarga 
download = customtkinter.CTkButton(app, text="Descargar", command=startDownload) 
download.pack(padx=5, pady=5)




# corro la app
app.mainloop()
