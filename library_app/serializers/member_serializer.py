from rest_framework import serializers
from library_app.models.member import Member
from library_app.models.library import Library

class MemberSerializer(serializers.ModelSerializer):
    library = serializers.PrimaryKeyRelatedField(
        queryset=Library.objects.all(),
        required=True,
        error_messages={
            'required': 'La biblioteca es obligatoria.',
            'blank': 'El biblioteca no puede estar vacía.',
            'does_not_exist': 'La biblioteca especificada no existe.',
            'incorrect_type': 'El ID de la biblioteca debe ser un número entero.'
        }
    )
    
    name = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'El nombre es obligatorio.',
            'blank': 'El nombre no puede estar vacío.'
        }
    )
    
    last_name = serializers.CharField(
        required=True,
        max_length=100,
        error_messages={
            'required': 'El apellido es obligatorio.',
            'blank': 'El apellido no puede estar vacío.'
        }
    )

    email = serializers.EmailField(
        required=True,
        max_length=255,
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'blank': 'El correo electrónico no puede estar vacío.',
            'invalid': 'El correo electrónico no tiene un formato válido.'
        }
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=10,
        error_messages={
            'max_length': 'El teléfono no puede tener más de 10 caracteres.'
        }
    )

    address = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=200,
        error_messages={
            'max_length': 'La dirección no puede tener más de 200 caracteres.'
        }
    )

    is_active = serializers.BooleanField(required=False, default=True)

    max_loans = serializers.IntegerField(
        required=False,
        min_value=1,
        error_messages={
            'min_value': 'El número máximo de préstamos debe ser mayor o igual a 1.'
        }
    )

    class Meta:
        model = Member
        fields = ['id', 'library', 'name', 'last_name','email','phone','address','membership_date','is_active','max_loans']
        extra_kwargs = {
            'email': {'validators': []} 
        }
