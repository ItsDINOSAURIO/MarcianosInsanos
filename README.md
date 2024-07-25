# Proyecto de Control Remoto del Rover

Este proyecto permite controlar un rover de forma remota a través de una interfaz gráfica de usuario (cliente) y un servidor que procesa las solicitudes. La interfaz permite mover el rover utilizando las teclas de flecha y tomar fotos en puntos de interés presionando la tecla Enter.

## Estructura del Proyecto

```
├───client
│   ├───index.html
│   └───client.js
└───server
    └───app.py
```

## Requisitos

- Python 3.7+
- Flask
- Flask-CORS
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
    pip install flask flask-cors
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

## Ejecución del Cliente

1. Navega a la carpeta del cliente:

    ```bash
    cd client
    ```

2. Abre `index.html` en tu navegador web. Puedes hacerlo simplemente haciendo doble clic en el archivo o abriéndolo desde el navegador.

## Uso

- **Mover el Rover**: Usa las teclas de flecha (↑, ↓, ←, →) para mover el rover en la interfaz gráfica.
- **Tomar Foto**: Presiona Enter cuando el rover esté sobre un punto de interés para abrir la cámara y tomar una foto. La foto será enviada y almacenada en el servidor.

## Estructura del Código

### Cliente

- **index.html**: Archivo HTML que contiene la estructura básica de la página y enlaza el archivo JavaScript.
- **client.js**: Archivo JavaScript que maneja la lógica de la interfaz gráfica, captura los eventos del teclado y envía solicitudes al servidor.

### Servidor

- **app.py**: Archivo Python que contiene la aplicación Flask. Maneja las solicitudes de movimiento del rover, toma de fotos y gestión de puntos de interés.

## Notas Adicionales

- Las fotos tomadas se almacenan en una carpeta `photos` en el servidor. El servidor mantiene un máximo de 10 fotos para evitar el uso excesivo de memoria.
- El estado de la cola de fotos se guarda en un archivo `photos_queue.json` para asegurar la persistencia entre reinicios del servidor.

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna mejora, por favor, crea un issue o un pull request en GitHub.

## Integrantes

- Luis Fernando Rodriguez Dominguez.
- Emiliano Delgado Hernandez.
- Angélica Gutiérrez Sánchez.
- Raúl Emiliano Guzmán.
- 
- 
- 