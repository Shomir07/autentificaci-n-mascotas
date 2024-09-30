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

        flipCameraBtn.style.visibility = 'visible';

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
    flipCameraBtn.style.visibility = 'visible';
}

// Función para capturar la foto y enviarla al servidor
function takePhoto() {
    if (camera.style.display === 'block') {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = camera.videoWidth;
        canvas.height = camera.videoHeight;
        context.drawImage(camera, 0, 0, canvas.width, canvas.height);

        // Convertir la imagen a un blob y enviar al servidor
        canvas.toBlob(function(blob) {
            const formData = new FormData();
            formData.append('image', blob, 'captured_image.jpg');

            // Enviar la imagen al servidor
            fetch('/procesar-imagen/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);
                // Mostrar la imagen procesada y los resultados
                const processedImageUrl = data.processed_image_url;
                const numPerros = data.num_perros;
                const numGatos = data.num_gatos;

                photo.src = processedImageUrl;
                photo.style.display = 'block';
                camera.style.display = 'none';

                alert(`Perros detectados: ${numPerros}\nGatos detectados: ${numGatos}`);
            })
            .catch(error => {
                console.error('Error al enviar la imagen:', error);
            });
        }, 'image/jpeg');
    }
}

// Función para alternar entre la cámara delantera y trasera
function flipCamera() {
    isFrontCamera = !isFrontCamera;
    console.log(isFrontCamera ? 'Cámara frontal seleccionada' : 'Cámara trasera seleccionada');
}
