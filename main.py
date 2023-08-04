from pytube import YouTube
import os

def descargar_todas_resoluciones(url):
    try:
        video = YouTube(url)
        print("Título:", video.title)
        print("Duración:", video.length, "segundos")
        print("Resoluciones disponibles:")
        resoluciones_descargadas = set()

        for stream in video.streams.filter(file_extension="mp4"):
            if stream.resolution:
                calidad = stream.resolution
                print(calidad)
                file_name = f"{video.title}_{calidad}.mp4".replace(" ", "_")

                # Evitar duplicados en nombres de archivo
                num = 1
                while file_name in resoluciones_descargadas:
                    num += 1
                    file_name = f"{video.title}_{calidad}_{num}.mp4".replace(" ", "_")

                resoluciones_descargadas.add(file_name)

                print(f"Descargando video en {calidad}...")
                stream.download(filename=file_name)
                print("Descarga completada.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    url = input("Ingresa la URL del video de YouTube: ")
    descargar_todas_resoluciones(url)
