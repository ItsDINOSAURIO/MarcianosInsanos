const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

let roverPosition = { x: 400, y: 300 };
const pointsOfInterest = [
    { x: 200, y: 150 },
    { x: 600, y: 450 },
    { x: 300, y: 300 }
];

document.addEventListener('keydown', function(event) {
    let move = { x: 0, y: 0 };
    switch (event.key) {
        case 'ArrowUp':
            move.y = -10;
            break;
        case 'ArrowDown':
            move.y = 10;
            break;
        case 'ArrowLeft':
            move.x = -10;
            break;
        case 'ArrowRight':
            move.x = 10;
            break;
        case 'Enter':
            if (isOnPointOfInterest(roverPosition, pointsOfInterest)) {
                // alert("Esta en punto de interes")
                openCamera();
            }
            return;
        default:
            return; // Quit when this doesn't handle the key event.
    }

    // Update rover position
    roverPosition.x += move.x;
    roverPosition.y += move.y;

    // Send move request to server
    fetch('http://127.0.0.1:5000/move', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(roverPosition)
    })
    .then(response => response.json())
    .then(data => {
        roverPosition = data.position;
        draw();
    });
});

function isOnPointOfInterest(rover, points) {
    return points.some(point => point.x == rover.x && point.y == rover.y);
}

function openCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();

            const takePhotoButton = document.createElement('button');
            takePhotoButton.innerText = "Toma la foto";
            takePhotoButton.onclick = () => {
                const canvas = document.createElement('canvas');
                canvas.width = 640;
                canvas.height = 480;
                const context = canvas.getContext('2d');
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL('image/png');

                // Send photo to server
                fetch('http://127.0.0.1:5000/take-photo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ roverPosition, image: imageData })
                })
                .then(response => response.json())
                .then(data => console.log(data));

                // Stop the video stream
                stream.getTracks().forEach(track => track.stop());
                document.body.removeChild(video);
                document.body.removeChild(takePhotoButton);
            };

            document.body.appendChild(video);
            document.body.appendChild(takePhotoButton);
        })
        .catch(err => console.error('Error accessing the camera: ', err));
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'seashell';
    ctx.fillRect(roverPosition.x, roverPosition.y, 20, 20);
    

    pointsOfInterest.forEach(point => {
        ctx.beginPath();
        ctx.arc(point.x + 10, point.y + 10, 10, 0, 2 * Math.PI, false);
        ctx.fillStyle = 'gold';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = 'black';
        ctx.stroke();
    });
}

draw();

// Send points of interest to server on load
fetch('http://127.0.0.1:5000/points-of-interest', { 
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(pointsOfInterest)
});
