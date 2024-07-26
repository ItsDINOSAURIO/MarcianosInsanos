from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
from collections import deque
import cv2
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

rover_position = {'x': 400, 'y': 300}
points_of_interest = []
photos_queue = deque(maxlen=10)  # Cola con un máximo de 10 fotos

# Asegúrate de que existe el directorio para las fotos
photos_directory = 'photos'
if not os.path.exists(photos_directory):
    os.makedirs(photos_directory)

@app.route('/move', methods=['POST'])
def move_rover():
    global rover_position
    new_position = request.get_json()
    rover_position = new_position
    print(rover_position)
    return jsonify({'status': 'ok', 'position': rover_position})

@app.route('/take-photo', methods=['POST'])
def take_photo():
    data = request.get_json()
    position = data['roverPosition']
    image_data = data['image']
    image_data = image_data.split(",")[1]  # Remover el encabezado de la imagen base64

    print(photos_queue)
    # Guardar la foto en la cola
    if len(photos_queue) > 10:
        # Eliminar la foto más antigua si ya hay 10
        oldest_photo = photos_queue.popleft()
        os.remove(os.path.join(photos_directory, oldest_photo))

    # Guardar la nueva foto
    photo_filename = f"photo_{len(photos_queue) + 1}.png"
    photo_path = os.path.join(photos_directory, photo_filename)
    with open(photo_path, "wb") as fh:
        fh.write(base64.b64decode(image_data))

    # Añadir la nueva foto a la cola
    photos_queue.append(photo_filename)

    for point in points_of_interest:
        if abs(point['x'] - position['x']) < 10 and abs(point['y'] - position['y']) < 10:
            return jsonify({'status': 'photo taken', 'point': point, 'filename': photo_filename})
    return jsonify({'status': 'no point of interest'})

@app.route('/points-of-interest', methods=['POST'])
def set_points_of_interest():
    global points_of_interest
    points_of_interest = request.get_json()
    return jsonify({'status': 'points received'})

if __name__ == '__main__':
    app.run(debug=True)


# Diccionario completo de tipos de ArUco
ARUCO_DICT = {
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL
}

def detect_arucos(image_path):
    # Cargar la imagen
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error al cargar la imagen: {image_path}")
        return None

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Crear el diccionario de resultado
    result = {
        'num_arucos': 0,
        'arucos': []
    }

    # Iterar sobre todos los diccionarios de ArUco
    for dict_name, dict_value in ARUCO_DICT.items():
        # Cargar el diccionario de marcadores ArUco
        dictionary = cv2.aruco.getPredefinedDictionary(dict_value)

        # Detectar los marcadores en la imagen
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, dictionary)

        if ids is not None:
            for i in range(len(ids)):
                aruco_info = {
                    'id': int(ids[i][0]),
                    'coords': {
                        '1': corners[i][0][0].tolist(),
                        '2': corners[i][0][1].tolist(),
                        '3': corners[i][0][2].tolist(),
                        '4': corners[i][0][3].tolist()
                    },
                    
                    'type_aruco': dict_name
                }
                result['arucos'].append(aruco_info)

            # Dibujar los bordes alrededor de los marcadores detectados
            cv2.aruco.drawDetectedMarkers(image, corners, ids, borderColor=(0, 255, 0))

    # Acomodo del diccionario
    result['arucos'] = sorted(result['arucos'], key=lambda x: (x['type_aruco']), reverse=True)
    result['num_arucos'] = len(result['arucos'])

    # Mostrar la imagen con los bordes dibujados
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    return result