# Proyecto de Control Remoto del Rover

Este proyecto permite controlar un rover de forma remota a través de una interfaz gráfica de usuario (cliente) y un servidor que procesa las solicitudes. La interfaz permite mover el rover utilizando las teclas de flecha y tomar fotos en puntos de interés presionando la tecla Enter.

## Estructura del Proyecto

```
├── client
│   ├── client.js
│   └── index.html
├── proxy
│   ├── api
│   │   └── proxy.js
│   ├── package.json
│   ├── package-lock.json
│   └── vercel.json
├── README.md
└── server
    ├── app.py
    ├── aruco_detector.py
    ├── Dockerfile
    ├── notebookArucos
    │   ├── arucosample.jpg
    │   ├── arucos.ipynb
    │   ├── images.jpeg
    │   ├── InputImage.jpg
    │   ├── marker.png
    │   └── otroaruco.jpeg
    ├── requirements.txt
    └── utils.py
```

## Especificaciones Técnicas del Desarrollo

### Tecnologías Utilizadas

- **Frontend**: HTML, JavaScript
- **Backend**: Python, Flask, Flask-CORS
- **Proxy**: Node.js, Express
- **Despliegue**:
  - Cliente: Vercel
  - Proxy: Vercel
  - Servidor: AWS Elastic Beanstalk
- **Procesamiento de Imágenes**: OpenCV
- **Control de Versiones**: Git, GitHub

### Requisitos

- Python 3.10+
- Node.js 20+
- Navegador web moderno (Chrome, Firefox, etc.)

## Instalación

1. Clona este repositorio:

   ```bash
   git clone https://github.com/luisferdev11/MarcianosInsanos.git
   cd MarcianosInsanos
   ```

2. Navega a la carpeta del servidor e instala las dependencias de Python:

   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. Navega a la carpeta del proxy e instala las dependencias de Node.js:

   ```bash
   cd ../proxy
   npm install
   ```

## Ejecución del Servidor

1. Navega a la carpeta del servidor:

   ```bash
   cd server
   ```

2. Ejecuta la aplicación Flask:

   ```bash
   python app.py
   ```

3. El servidor se ejecutará en `http://127.0.0.1:5000`.

## Ejecución del Proxy

1. Navega a la carpeta del proxy:

   ```bash
   cd ../proxy
   ```

2. Ejecuta el servidor de proxy:

   ```bash
   npm start
   ```

3. El proxy se ejecutará en `http://localhost:3000` y redirigirá las solicitudes a la API del servidor.

## Ejecución del Cliente

1. Navega a la carpeta del cliente:

   ```bash
   cd ../client
   ```

2. Abre `index.html` en tu navegador web. Puedes hacerlo simplemente haciendo doble clic en el archivo o abriéndolo desde el navegador.

## Flujo de Datos

1. **Movimiento del Rover**:

   - El usuario presiona las teclas de flecha en el cliente.
   - `client.js` captura los eventos del teclado y envía una solicitud POST al proxy con las nuevas coordenadas.
   - El proxy reenvía la solicitud al servidor Flask en AWS Elastic Beanstalk.
   - El servidor Flask actualiza la posición del rover y responde al cliente a través del proxy.

2. **Tomar Foto**:
   - El usuario presiona Enter en un punto de interés.
   - `client.js` abre la cámara utilizando `getUserMedia` y toma una foto.
   - La foto se convierte a base64 y se envía como una solicitud POST al proxy.
   - El proxy reenvía la solicitud al servidor Flask en AWS Elastic Beanstalk.
   - El servidor Flask guarda la foto y detecta marcadores ArUco en la imagen utilizando OpenCV.
   - El servidor responde con los datos de los marcadores ArUco detectados a través del proxy.
   - `client.js` muestra la foto y los datos de los marcadores ArUco en la interfaz.

## Estructura del Código

### Cliente

- **index.html**: Archivo HTML que contiene la estructura básica de la página y enlaza el archivo JavaScript.
- **client.js**: Archivo JavaScript que maneja la lógica de la interfaz gráfica, captura los eventos del teclado y envía solicitudes al servidor.

### Proxy

- **api/proxy.js**: Archivo JavaScript que configura el servidor proxy para redirigir las solicitudes a la API del servidor.
- **package.json**: Archivo de configuración de Node.js que incluye las dependencias y scripts necesarios para ejecutar el proxy.
- **vercel.json**: Archivo de configuración de Vercel que define las rutas de proxy.

### Servidor

- **app.py**: Archivo Python que contiene la aplicación Flask. Maneja las solicitudes de movimiento del rover, toma de fotos y gestión de puntos de interés.
- **aruco_detector.py**: Archivo Python que contiene la lógica para detectar marcadores ArUco en las imágenes.
- **utils.py**: Archivo Python que contiene funciones utilitarias, como guardar imágenes.
- **requirements.txt**: Archivo que contiene las dependencias de Python necesarias para ejecutar la aplicación Flask.
- **notebookArucos**: Carpeta que contiene un notebook de Jupyter y ejemplos de imágenes para probar la detección de ArUco.

## Despliegue con Docker

El servidor Flask se despliega utilizando Docker para asegurar la consistencia del entorno de ejecución.

### Dockerfile

```Dockerfile
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx

# By default, listen on port 5000
EXPOSE 5000/tcp

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos requeridos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
```

### Construcción y Ejecución del Contenedor Docker

1. Construir la imagen Docker:

   ```bash
   docker build -t marcianosinsanos .
   ```

2. Ejecutar el contenedor Docker:

   ```bash
   docker run -p 5000:5000 marcianosinsanos
   ```

## Impacto del Proxy en el Rendimiento

El uso del proxy introduce una latencia adicional en las solicitudes, lo que puede hacer que las respuestas sean más lentas. Sin embargo, este enfoque fue necesario para resolver los problemas de "Mixed Content" y asegurar que todas las solicitudes se realicen a través de HTTPS, mejorando la seguridad del proyecto.

## Notas Adicionales

- Las fotos tomadas se almacenan en una carpeta `photos` en el servidor. El servidor mantiene un máximo de 10 fotos para evitar el uso excesivo de memoria.
- El estado de la cola de fotos se mantiene en memoria y se reinicia si el servidor se reinicia.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna mejora, por favor, crea un issue o un pull request en GitHub.

## Integrantes

- Luis Fernando Rodriguez Dominguez.
- Emiliano Delgado Hernandez.
- Angélica Gutiérrez Sánchez.
- Raúl Emiliano Guzmán.
- Ana Fernanda Alejaldre Valdez.
- Diego Sandoval Chavarría.
