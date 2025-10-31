from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

from library_app.serializers.library_serializer import LibrarySerializer
from library_app.repositories.library_repository import LibraryRepository
from library_app.services.library_service import LibraryService
from drf_spectacular.utils import extend_schema, OpenApiResponse,extend_schema_view
from rest_framework.exceptions import NotFound

@extend_schema_view(partial_update=extend_schema(exclude=True),)
@extend_schema(tags=["Bibliotecas"])
class LibraryViewSet(viewsets.ModelViewSet):
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LibraryService(LibraryRepository())

    def get_object(self):
        library_id = self.kwargs.get("pk")
        try:
            return self.service.get_library_by_id(library_id)
        except NotFound:
            raise NotFound("La biblioteca no existe.")


    @extend_schema(
        summary="Listar todas las bibliotecas",
        description="Retorna una lista con todas las bibliotecas registradas en el sistema.",
        responses={
            200: OpenApiResponse(
                response=LibrarySerializer,
                description="Lista de bibliotecas obtenida correctamente"
            ),
            500: OpenApiResponse(
                description="Error interno del servidor."
            ),
        },
    )
    def list(self, request):
        filters = {
            'name': request.query_params.get('name'),
            'address': request.query_params.get('address'),
            'phone': request.query_params.get('phone'),
        }
        try:
            libraries = self.service.list_libraries(filters)
            paginator = PageNumberPagination()
            paginator.page_size = 5
            result_page = paginator.paginate_queryset(libraries, request)
            serializer = self.get_serializer(result_page, many=True)
            return paginator.get_paginated_response({
                "code": 200,
                "msg": "Lista de bibliotecas obtenida correctamente.",
                "data": serializer.data
            })
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Obtener biblioteca por ID",
        description="Retorna la biblioteca según el ID ingresado.",
        responses={
            200: OpenApiResponse(
                response=LibrarySerializer,
                description="Biblioteca obtenida correctamente."
            ),
            404: OpenApiResponse(
                description="La biblioteca no existe."
            ),
            500: OpenApiResponse(
                description="Error interno del servidor."
            ),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  
            serializer = LibrarySerializer(instance)
            return Response({
                "code": 200,
                "msg": "Biblioteca obtenida correctamente.",
                "data": serializer.data
            }, status=200)
        except NotFound:
            return Response({"code": 404, "msg": "La biblioteca no existe."}, status=404)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)


    @extend_schema(
        summary="Crear una nueva biblioteca",
        description="Registra una nueva biblioteca en el sistema.",
        request=LibrarySerializer,
        responses={
            201: OpenApiResponse(
                response=LibrarySerializer,
                description="Biblioteca creada correctamente."
            ),
            500: OpenApiResponse(description="Datos inválidos o error de validación."),
        },
    )
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=400)

            self.service.create_library(serializer.validated_data)
            return Response({"code": 201, "msg": "Biblioteca creada correctamente."}, status=201)

        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)

    @extend_schema(
        summary="Actualizar una biblioteca existente",
        description="Actualiza parcialmente o completamente una biblioteca según el ID proporcionado.",
        request=LibrarySerializer,
        responses={
            200: OpenApiResponse(description="Biblioteca actualizada correctamente."),
            500: OpenApiResponse(description="Datos inválidos o error de validación."),
        },
    )
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=400)

            self.service.update_library(instance, serializer.validated_data)
            return Response({"code": 200, "msg": "Biblioteca actualizada correctamente."}, status=200)

        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)


    @extend_schema(
        summary="Eliminar biblioteca",
        description="Elimina una biblioteca existente según su ID.",
        responses={
            204: OpenApiResponse(description="Biblioteca eliminada correctamente."),
            404: OpenApiResponse(description="La biblioteca no existe."),
            500: OpenApiResponse(description="Error al eliminar la biblioteca."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.service.delete_library(instance)
            return Response({"code": 204, "msg": "Biblioteca eliminada correctamente."}, status=204)
        except Http404:
            return Response({"code": 404, "msg": "La biblioteca no existe."}, status=404)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=500)
