const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let roverPosition = { x: 400, y: 300 };
const pointsOfInterest = [
  { x: 200, y: 150 },
  { x: 600, y: 450 },
  { x: 300, y: 300 },
];

const roverWidth = 20;
const roverHeight = 20;

// Límite del canvas
const canvasWidth = canvas.width;
const canvasHeight = canvas.height;

document.addEventListener("keydown", function (event) {
  let move = { x: 0, y: 0 };
  switch (event.key) {
    case "ArrowUp":
      move.y = -10;
      break;
    case "ArrowDown":
      move.y = 10;
      break;
    case "ArrowLeft":
      move.x = -10;
      break;
    case "ArrowRight":
      move.x = 10;
      break;
    case "Enter":
      if (isOnPointOfInterest(roverPosition, pointsOfInterest)) {
        openCamera();
      }
      return;
    default:
      return; // Quit when this doesn't handle the key event.
  }
  // Update rover position
  let newX = roverPosition.x + move.x;
  let newY = roverPosition.y + move.y;
  // Limit rover position to canvas
  newX = Math.max(0, Math.min(canvasWidth - roverWidth, newX));
  newY = Math.max(0, Math.min(canvasHeight - roverHeight, newY));

  roverPosition = { x: newX, y: newY };

  // Send move request to server
  fetch("http://127.0.0.1:5000/move", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(roverPosition),
  })
    .then((response) => response.json())
    .then((data) => {
      roverPosition = data.position;
      draw();
    });
});

// Considering the exact collision with a point of interest
function isOnPointOfInterest(rover, points) {
  return points.some((point) => point.x == rover.x && point.y == rover.y);
}

function openCamera() {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      const video = document.createElement("video");
      video.srcObject = stream;
      video.play();

      const takePhotoButton = document.createElement("button");
      takePhotoButton.innerText = "Toma la foto";
      takePhotoButton.onclick = () => {
        const photoCanvas = document.createElement("canvas");
        photoCanvas.width = 640;
        photoCanvas.height = 480;
        const context = photoCanvas.getContext("2d");
        context.drawImage(video, 0, 0, photoCanvas.width, photoCanvas.height);
        const imageData = photoCanvas.toDataURL("image/png");

        // Send photo to server
        fetch("http://127.0.0.1:5000/take-photo", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ roverPosition, image: imageData }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            displayPhotoAndArucos(imageData, data.arucos.arucos);
          });

        // Stop the video stream
        stream.getTracks().forEach((track) => track.stop());
        document.body.removeChild(video);
        document.body.removeChild(takePhotoButton);
      };

      document.body.appendChild(video);
      document.body.appendChild(takePhotoButton);
    })
    .catch((err) => console.error("Error accessing the camera: ", err));
}

function displayPhotoAndArucos(imageData, arucos) {
  // Clear previous results
  const resultsDiv = document.getElementById("results");
  if (resultsDiv) {
    resultsDiv.remove();
  }

  const newResultsDiv = document.createElement("div");
  newResultsDiv.id = "results";

  // Display the photo
  const img = document.createElement("img");
  img.src = imageData;
  img.width = 640;
  img.height = 480;
  newResultsDiv.appendChild(img);

  // Display ArUco information
  const arucoInfo = document.createElement("div");
  arucoInfo.innerHTML = `<h3>Información de los ArUcos detectados:</h3>`;
  arucos.forEach((aruco) => {
    const arucoDiv = document.createElement("div");
    arucoDiv.innerHTML = `
      <p><strong>ID:</strong> ${aruco.id}</p>
      <p><strong>Tipo:</strong> ${aruco.type_aruco}</p>
      <p><strong>Coordenadas:</strong></p>
      <ul>
        <li>1: (${aruco.coords[1][0]}, ${aruco.coords[1][1]})</li>
        <li>2: (${aruco.coords[2][0]}, ${aruco.coords[2][1]})</li>
        <li>3: (${aruco.coords[3][0]}, ${aruco.coords[3][1]})</li>
        <li>4: (${aruco.coords[4][0]}, ${aruco.coords[4][1]})</li>
      </ul>
    `;
    arucoInfo.appendChild(arucoDiv);
  });
  newResultsDiv.appendChild(arucoInfo);

  document.body.appendChild(newResultsDiv);
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "seashell";
  ctx.fillRect(roverPosition.x, roverPosition.y, roverWidth, roverHeight);

  pointsOfInterest.forEach((point) => {
    ctx.beginPath();
    ctx.arc(point.x + 10, point.y + 10, 10, 0, 2 * Math.PI, false);
    ctx.fillStyle = "gold";
    ctx.fill();
    ctx.lineWidth = 2;
    ctx.strokeStyle = "black";
    ctx.stroke();
  });
}

draw();

// Send points of interest to server on load
fetch("http://127.0.0.1:5000/points-of-interest", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify(pointsOfInterest),
});
