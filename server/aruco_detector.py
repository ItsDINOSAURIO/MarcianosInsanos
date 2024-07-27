import cv2
# import matplotlib.pyplot as plt

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
            # cv2.aruco.drawDetectedMarkers(image, corners, ids, borderColor=(0, 255, 0))

    # Acomodo del diccionario
    result['arucos'] = sorted(result['arucos'], key=lambda x: (x['type_aruco']), reverse=True)
    result['num_arucos'] = len(result['arucos'])

    # Mostrar la imagen con los bordes dibujados
    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    # plt.axis('off')
    # plt.show()

    return result


# print(detect_arucos("notebookArucos/arucosample.jpg"))