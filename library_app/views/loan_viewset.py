from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound, ValidationError
from django.http import Http404
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse,extend_schema_view

from library_app.models.loan import Loan
from library_app.serializers.loan_serializer import LoanSerializer
from library_app.repositories.loan_repository import LoanRepository
from library_app.repositories.book_repository import BookRepository
from library_app.repositories.member_repository import MemberRepository
from library_app.services.loan_service import LoanService

@extend_schema_view(partial_update=extend_schema(exclude=True),)
@extend_schema(tags=["Préstamos"])
class LoanViewSet(viewsets.ModelViewSet):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LoanService(
            repository=LoanRepository(),
            book_repository=BookRepository(),
            member_repository=MemberRepository()
        )

    def get_object(self):
        loan_id = self.kwargs.get("pk")
        try:
            return self.service.get_loan_by_id(loan_id)
        except NotFound:
            raise NotFound("El préstamo no existe.")

    @extend_schema(
        summary="Listar préstamos",
        description="Obtiene una lista paginada de todos los préstamos.",
        responses={
            200: OpenApiResponse(response=LoanSerializer, description="Lista de préstamos obtenida."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def list(self, request):
        try:
            filters = {
                'book': request.query_params.get('book'),
                'member': request.query_params.get('member'),
                'returned': request.query_params.get('returned'),
                'loan_date': request.query_params.get('loan_date'),
            }
            loans = self.service.list_loans(filters)
            paginator = PageNumberPagination()
            paginator.page_size = 5
            result_page = paginator.paginate_queryset(loans, request)
            serializer = self.get_serializer(result_page, many=True)
            return paginator.get_paginated_response({
                "code": 200,
                "msg": "Lista de préstamos obtenida correctamente.",
                "data": serializer.data
            })
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Obtener préstamo por ID",
        description="Devuelve los detalles de un préstamo específico según su ID.",
        responses={
            200: OpenApiResponse(response=LoanSerializer, description="Préstamo obtenido correctamente."),
            404: OpenApiResponse(description="El préstamo no existe."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"code": 200, "msg": "Préstamo obtenido correctamente.", "data": serializer.data}, status=200)
        except Http404:
            return Response({"code": 404, "msg": "El préstamo no existe."}, status=404)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Crear préstamo",
        description="Registra un nuevo préstamo de libro.",
        request=LoanSerializer,
        responses={
            201: OpenApiResponse(description="Préstamo creado correctamente."),
            400: OpenApiResponse(description="Datos inválidos o error de validación."),
        },
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=400)
            self.service.create_loan(serializer.validated_data)
            return Response({"code": 201, "msg": "Préstamo creado correctamente."}, status=201)
        except ValidationError as ve:
            return Response({"code": 400, "msg": str(ve.detail[0])}, status=400)
        except Exception as e:
            return Response({"code": 400, "msg": str(e)}, status=400)

    
    @extend_schema(
        summary="Devolver un libro",
        description="Marca un préstamo como devuelto y aumenta el stock del libro.",
        responses={
            200: OpenApiResponse(description="Libro devuelto correctamente."),
            400: OpenApiResponse(description="Error al devolver el libro."),
            404: OpenApiResponse(description="Préstamo no encontrado.")
        },
    )
    @action(detail=True, methods=["post"], url_path="return")
    def return_book(self, request, pk=None):
        try:
            loan = self.service.get_loan_by_id(pk)
            result = self.service.return_book(loan)
            return Response(result, status=200)
        except NotFound:
            return Response({"code": 404, "msg": "El préstamo no existe."}, status=404)
        except ValidationError as e:
            return Response({"code": 400, "msg": str(e)}, status=400)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)
        
    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(
            {"error": "Esta acción no está permitida."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"error": "Esta acción no está permitida."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"error": "Esta acción no está permitida."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

