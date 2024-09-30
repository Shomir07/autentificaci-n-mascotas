from django import forms

class DImageForm(forms.Form):
    image = forms.ImageField(label="Subir una imagen de perro o gato")