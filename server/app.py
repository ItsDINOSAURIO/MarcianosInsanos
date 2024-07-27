from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from collections import deque
from aruco_detector import detect_arucos
from utils import save_image

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Habilita CORS para todas las rutas y orígenes

rover_position = {'x': 400, 'y': 300}
points_of_interest = []
photos_queue = deque(maxlen=10)  # Cola con un máximo de 10 fotos

# Asegúrate de que existe el directorio para las fotos
photos_directory = 'photos'
if not os.path.exists(photos_directory):
    os.makedirs(photos_directory)

@app.route('/move', methods=['POST'])
def move_rover() -> jsonify:
    """
    Actualiza la posición del rover.

    Returns:
        jsonify: Un objeto JSON con el estado y la nueva posición del rover.
    """
    global rover_position
    new_position = request.get_json()
    rover_position = new_position
    print(rover_position)
    return jsonify({'status': 'ok', 'position': rover_position})

@app.route('/take-photo', methods=['POST'])
def take_photo() -> jsonify:
    """
    Guarda una foto recibida y detecta marcadores ArUco en ella.

    Returns:
        jsonify: Un objeto JSON con el estado, los puntos de interés y los datos de los marcadores ArUco detectados.
    """
    data = request.get_json()
    position = data['roverPosition']
    image_data = data['image']
    image_data = image_data.split(",")[1]  # Remover el encabezado de la imagen base64

    # Guardar la foto en la cola
    if len(photos_queue) >= 10:
        # Eliminar la foto más antigua si ya hay 10
        oldest_photo = photos_queue.popleft()
        os.remove(os.path.join(photos_directory, oldest_photo))

    # Guardar la nueva foto
    photo_filename = f"photo_{len(photos_queue) + 1}.png"
    photo_path = os.path.join(photos_directory, photo_filename)
    save_image(image_data, photo_path)

    # Añadir la nueva foto a la cola
    photos_queue.append(photo_filename)

    # Detectar ArUcos en la imagen
    aruco_result = detect_arucos(photo_path)

    for point in points_of_interest:
        if abs(point['x'] - position['x']) < 10 and abs(point['y'] - position['y']) < 10:
            return jsonify({'status': 'photo taken', 'point': point, 'filename': photo_filename, 'arucos': aruco_result})
    return jsonify({'status': 'no point of interest', 'arucos': aruco_result})

@app.route('/points-of-interest', methods=['POST'])
def set_points_of_interest() -> jsonify:
    """
    Establece los puntos de interés para el rover.

    Returns:
        jsonify: Un objeto JSON con el estado de la operación.
    """
    global points_of_interest
    points_of_interest = request.get_json()
    return jsonify({'status': 'points received'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
