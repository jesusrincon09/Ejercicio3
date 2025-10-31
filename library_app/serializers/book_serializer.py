from rest_framework import serializers
from library_app.models.book import Book
from library_app.models.book import Library

class BookSerializer(serializers.ModelSerializer):
    library = serializers.PrimaryKeyRelatedField(
        queryset=Library.objects.all(),
        required=True,
        error_messages={
            'required': 'La biblioteca es obligatoria.',
            'does_not_exist': 'La biblioteca especificada no existe.',
            'incorrect_type': 'El ID de la biblioteca debe ser un número entero.'
        }
    )
    title = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El titulo del libro es obligatorio',
            'blank': 'El titulo del libro no puede estar vacía.'
        }
    )
    author = serializers.CharField(
        required=True,
        error_messages={
            'required': 'El autor es obligatorio.',
            'blank': 'El autor no puede estar vacío.'
        }
    )
    isbn = serializers.CharField(
        max_length=20,
        required=True,
        error_messages={
            'required': 'El ISBN es obligatorio.',
            'blank': 'El campo ISBN no puede estar vacío.',
        }
    )
    stock = serializers.IntegerField(
        min_value=0,
        required=False,
        error_messages={
            'min_value': 'El stock no puede ser negativo.'
        }
    )

    class Meta:
        model = Book
        fields = ['id', 'library', 'title', 'author','isbn','published_year','stock']
        extra_kwargs = {
            'isbn': {'validators': []}
        }
