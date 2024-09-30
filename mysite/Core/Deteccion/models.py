from django.db import models

# Create your models here.

class DeteccionAnimal(models.Model):
    imagen = models.ImageField(upload_to='imagenes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    num_perros = models.IntegerField(default=0)
    num_gatos = models.IntegerField(default=0)

    def __str__(self):
        return f"Detección del {self.fecha_subida}: {self.num_perros} perros, {self.num_gatos} gatos"