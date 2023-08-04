import os
import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)
app.static_folder = 'data'  # Cambiar el nombre de la carpeta a "data"

port = int(os.environ.get('PORT', 5000))

scheduler = BackgroundScheduler()
scheduler.start()


# Ruta para recibir las solicitudes de descarga
@app.route('/download', methods=['POST'])
def descargar_video():
    url = request.json['url']
    # Llamar a la función para descargar el video
    videos_descargados = descargar_todas_resoluciones(url)

    return jsonify(videos_descargados)

# Tu función para descargar videos de YouTube
def descargar_todas_resoluciones(url):
    videos_descargados = []
    try:
        video = YouTube(url)
        print("Título:", video.title)
        print("Duración:", video.length, "segundos")
        print("Resoluciones disponibles:")

        for stream in video.streams.filter(file_extension="mp4"):
            if stream.resolution:
                calidad = stream.resolution
                print(calidad)

                # Crear una carpeta con el nombre del video
                video_folder = f"data/{video.title}"
                os.makedirs(video_folder, exist_ok=True)

                file_name = f"{video.title}_{calidad}.mp4".replace(" ", "_")
                # Agregar el nombre de la carpeta al file_path
                file_path = os.path.join(video_folder, file_name)

                print(f"Descargando video en {calidad}...")
                # Guardar el archivo en la carpeta correspondiente
                stream.download(output_path=video_folder, filename=file_name)
                print("Descarga completada.")

                # Agregar información del video descargado a la lista
                videos_descargados.append({
                    'title': video.title,
                    'resolution': calidad,
                    'downloadUrl': f"http://127.0.0.1:5000/download/{video.title}/{file_name}"
                })

    except Exception as e:
        print("Error:", e)

    return videos_descargados


def limpiar_archivos_antiguos():
    max_antiguedad_dias = 10  # Establecer la máxima antigüedad en días para los archivos

    # Obtener la fecha actual
    fecha_actual = datetime.datetime.now()

    # Recorrer los archivos en la carpeta "data"
    carpeta_data = "data"
    for root, _, files in os.walk(carpeta_data):
        for archivo in files:
            archivo_path = os.path.join(root, archivo)

            # Obtener la fecha de modificación del archivo
            fecha_modificacion = datetime.datetime.fromtimestamp(os.path.getmtime(archivo_path))

            # Calcular la diferencia de tiempo entre la fecha actual y la fecha de modificación
            diferencia_tiempo = fecha_actual - fecha_modificacion

            # Verificar si el archivo es más antiguo que el límite establecido
            if diferencia_tiempo.days > max_antiguedad_dias:
                # Eliminar el archivo
                os.remove(archivo_path)
                print(f"Archivo {archivo_path} eliminado por ser antiguo.")

# Nueva ruta para servir los archivos descargados
@app.route('/download/<path:video_title>/<path:filename>', methods=['GET'])
def descargar_archivo(video_title, filename):
    return send_file(f"data/{video_title}/{filename}", as_attachment=True)  # Cambiar la ruta a "data"

if __name__ == "__main__":
    scheduler.add_job(limpiar_archivos_antiguos, trigger='interval', weeks=1)

    app.run(host='0.0.0.0', port=port)
