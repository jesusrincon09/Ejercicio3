from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

from library_app.models.book import Book
from library_app.serializers.book_serializer import BookSerializer
from library_app.repositories.book_repository import BookRepository
from library_app.services.book_service import BookService
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema, OpenApiResponse,extend_schema_view
from rest_framework.exceptions import NotFound

@extend_schema_view(partial_update=extend_schema(exclude=True),)
@extend_schema(tags=["Libros"])
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BookService(BookRepository())
    
    def get_object(self):
        book_id = self.kwargs.get("pk")
        try:
            return self.service.get_book_by_id(book_id)
        except NotFound:
            raise NotFound("El libro no existe.")


    @extend_schema(
        summary="Listar todos los libros",
        description="Obtiene una lista paginada de todos los libros registrados en el sistema.",
        responses={
            200: OpenApiResponse(
                response=BookSerializer,
                description="Lista de libros obtenida correctamente."
            ),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def list(self, request):
        try:
            filters = {
                'title': request.query_params.get('title'),
                'author': request.query_params.get('author'),
                'isbn': request.query_params.get('isbn'),
                'library_id': request.query_params.get('library'),
                'published_year': request.query_params.get('published_year')
            }
            books = self.service.list_books(filters)
            paginator = PageNumberPagination()
            paginator.page_size = 5
            result_page = paginator.paginate_queryset(books, request)
            serializer = self.get_serializer(result_page, many=True)
            return paginator.get_paginated_response({
                "code": 200,
                "msg": "Lista de libros obtenida correctamente.",
                "data": serializer.data
            })
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Obtener libro por ID",
        description="Devuelve la información detallada de un libro específico según su ID.",
        responses={
            200: OpenApiResponse(response=BookSerializer, description="Libro obtenido correctamente."),
            404: OpenApiResponse(description="El libro no existe."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"code": 200, "msg": "Libro obtenido correctamente.", "data": serializer.data}, status=200)
        except Http404:
            return Response({"code": 404, "msg": "El libro no existe."}, status=404)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Crear un nuevo libro",
        description="Registra un nuevo libro en la base de datos.",
        request=BookSerializer,
        responses={
            201: OpenApiResponse(description="Libro creado correctamente."),
            400: OpenApiResponse(description="Datos inválidos o error de validación."),
        },
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=400)
            self.service.create_book(serializer.validated_data)
            return Response({"code": 201, "msg": "Libro creado correctamente."}, status=201)
        except Exception as e:
            return Response({"code": 400, "msg": str(e)}, status=400)

    @extend_schema(
        summary="Actualizar un libro",
        description="Actualiza la información de un libro según su ID.",
        request=BookSerializer,
        responses={
            200: OpenApiResponse(description="Libro actualizado correctamente."),
            400: OpenApiResponse(description="Datos inválidos o error de validación."),
        },
    )
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=400)
            self.service.update_book(instance, serializer.validated_data)
            return Response({"code": 200, "msg": "Libro actualizado correctamente."}, status=200)
        except Exception as e:
            return Response({"code": 400, "msg": str(e)}, status=400)

    @extend_schema(
        summary="Eliminar un libro",
        description="Elimina un libro existente según su ID.",
        responses={
            204: OpenApiResponse(description="Libro eliminado correctamente."),
            404: OpenApiResponse(description="El libro no existe."),
            400: OpenApiResponse(description="Error al eliminar el libro."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.service.delete_book(instance)
            return Response({"code": 204, "msg": "Libro eliminado correctamente."}, status=204)
        except Http404:
            return Response({"code": 404, "msg": "El libro no existe."}, status=404)
        except Exception as e:
            return Response({"code": 400, "msg": str(e)}, status=400)
