import torch
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Deteccion.models import DeteccionAnimal

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'custom', path="C:\\yolov5s.pt", force_reload=True)

# Procesar la imagen y detectar animales
def procesar(imagen_path):
    results = model(imagen_path)
    detecciones = results.xyxy[0].cpu().numpy()

    dog_count = 0
    cat_count = 0
    detecciones_filtradas = []

    for box in detecciones:
        x1, y1, x2, y2, confianza, clase = box[:6]
        label = model.names[int(clase)]

        if label == "dog":
            dog_count += 1
            detecciones_filtradas.append((x1, y1, x2, y2, "Perro"))
        elif label == "cat":
            cat_count += 1
            detecciones_filtradas.append((x1, y1, x2, y2, "Gato"))

    img = cv2.imread(imagen_path)
    for (x1, y1, x2, y2, label) in detecciones_filtradas:
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(img, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    processed_image_path = imagen_path.replace(".jpg", "_procesada.jpg")
    cv2.imwrite(processed_image_path, img)

    return processed_image_path, dog_count, cat_count

# Vista para procesar la imagen enviada desde JavaScript
@csrf_exempt
def procesar_img(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.path(filename)

        # Procesar la imagen
        processed_image_path, num_perros, num_gatos = procesar(image_path)

        # Devolver los resultados como JSON
        response_data = {
            'processed_image_url': fs.url(processed_image_path),
            'num_perros': num_perros,
            'num_gatos': num_gatos,
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'No se envió ninguna imagen'}, status=400)