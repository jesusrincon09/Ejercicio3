from rest_framework import serializers
from library_app.models.loan import Loan
from library_app.models.book import Book
from library_app.models.member import Member

class LoanSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        required=True,
        error_messages={
            'required': 'El libro es obligatorio.',
            'does_not_exist': 'El libro especificado no existe.',
            'incorrect_type': 'El ID del libro debe ser un número entero.'
        }
    )

    member = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        required=True,
        error_messages={
            'required': 'El miembro es obligatorio.',
            'does_not_exist': 'El miembro especificado no existe.',
            'incorrect_type': 'El ID del miembro debe ser un número entero.'
        }
    )

    loan_date = serializers.DateTimeField(read_only=True)
    return_date = serializers.DateTimeField(
        required=False,
        allow_null=True,
        error_messages={
            'invalid': 'La fecha de devolución debe tener un formato válido.'
        }
    )
    returned = serializers.BooleanField(default=False)

    class Meta:
        model = Loan
        fields = ['id', 'book', 'member', 'loan_date','return_date','returned']
