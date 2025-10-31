from rest_framework import serializers
from library_app.models.library import Library

class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El nombre de la biblioteca es obligatorio.',
            'blank': 'El nombre no puede estar vacío.'
        }
    )
    address = serializers.CharField(
        required=True,
        error_messages={
            'required': 'La dirección es obligatoria.',
            'blank': 'La dirección no puede estar vacía.'
        }
    )
    phone = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El teléfono es obligatorio.',
            'blank': 'El teléfono no puede estar vacío.'
        }
    )

    class Meta:
        model = Library
        fields = ['id', 'name', 'address', 'phone','email']
    
    def validate_phone(self, value):
        if not (7 <= len(value) <= 10):
            raise serializers.ValidationError("El teléfono debe tener entre 7 y 10 caracteres.")
        return value
