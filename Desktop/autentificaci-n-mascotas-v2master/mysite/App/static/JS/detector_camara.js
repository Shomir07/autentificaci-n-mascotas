const camera = document.getElementById('camera');
const photo = document.getElementById('photo');
const toggleCameraBtn = document.getElementById('toggleCameraBtn');
const takePhotoBtn = document.getElementById('takePhotoBtn');
const closeCameraBtn = document.getElementById('closeCameraBtn');
const flipCameraBtn = document.getElementById('flipCameraBtn'); // Botón para voltear la cámara

let stream;
let isFrontCamera = true; // Usamos esta variable para controlar la cámara frontal o trasera

toggleCameraBtn.addEventListener('click', toggleCamera);
takePhotoBtn.addEventListener('click', takePhoto);
closeCameraBtn.addEventListener('click', closeCamera);
flipCameraBtn.addEventListener('click', flipCamera); // Listener para voltear la cámara

// Función para encender/apagar la cámara
function toggleCamera() {
    if (camera.style.display === 'none') {
        openCamera();
    } else {
        closeCamera();
    }
}

// Función para abrir la cámara con el modo seleccionado
async function openCamera() {
    try {
        // Detener el stream anterior si existe
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }

        // Configuración de la cámara según el modo (frontal o trasera)
        stream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: isFrontCamera ? 'user' : 'environment' // 'user' es para la cámara frontal, 'environment' es para la trasera
            },
            audio: false
        });

        // Mostrar el video en el elemento <video>
        camera.srcObject = stream;
        camera.style.display = 'block';
        photo.style.display = 'none';
        toggleCameraBtn.textContent = '👁️';

        // Aseguramos que el botón de voltear cámara siempre sea visible
        flipCameraBtn.style.visibility = 'visible'; // Cambiar 'display' a 'visibility'

    } catch (err) {
        console.error("Error accediendo a la cámara:", err);
    }
}

// Función para cerrar la cámara
function closeCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    camera.style.display = 'none';
    photo.style.display = 'none';
    toggleCameraBtn.textContent = '👁️‍🗨️';

    // Aseguramos que el botón de voltear cámara siempre sea visible
    flipCameraBtn.style.visibility = 'visible'; // Cambiar 'display' a 'visibility'
}

// Función para capturar la foto
function takePhoto() {
    if (camera.style.display === 'block') {
        const context = photo.getContext('2d');
        photo.width = camera.videoWidth;
        photo.height = camera.videoHeight;
        context.drawImage(camera, 0, 0, photo.width, photo.height);
        camera.style.display = 'none';
        photo.style.display = 'block';
    }
}

// Función para alternar entre la cámara delantera y trasera SIN encender la cámara automáticamente
function flipCamera() {
    isFrontCamera = !isFrontCamera; // Cambiar entre frontal y trasera
    // No se llama a openCamera() aquí, así que la cámara no se enciende automáticamente
    console.log(isFrontCamera ? 'Cámara frontal seleccionada' : 'Cámara trasera seleccionada');
}
