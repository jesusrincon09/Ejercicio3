from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import Http404

from library_app.serializers.member_serializer import MemberSerializer
from library_app.repositories.member_repository import MemberRepository
from library_app.services.member_service import MemberService
from drf_spectacular.utils import extend_schema, OpenApiResponse,extend_schema_view
from rest_framework.exceptions import NotFound

@extend_schema_view(partial_update=extend_schema(exclude=True),)
@extend_schema(tags=["Miembros"])
class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = MemberService(MemberRepository())
    
    def get_object(self):
        member_id = self.kwargs.get("pk")
        try:
            return self.service.get_member_by_id(member_id)
        except NotFound:
            raise NotFound("No existe.")

    @extend_schema(
        summary="Listar todos los miembros",
        description="Obtiene una lista paginada de todos los miembros registrados en el sistema.",
        responses={
            200: OpenApiResponse(
                response=MemberSerializer,
                description="Lista de miembros obtenida correctamente."
            ),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def list(self, request):
        try:
            filters = {
                'name': request.query_params.get('name'),
                'email': request.query_params.get('email'),
                'last_name': request.query_params.get('last_name'),
                'library': request.query_params.get('library'),
                'max_loans': request.query_params.get('max_loans'),
            }
            members = self.service.list_members(filters)
            paginator = PageNumberPagination()
            paginator.page_size = 5
            result_page = paginator.paginate_queryset(members, request)
            serializer = self.get_serializer(result_page, many=True)
            return paginator.get_paginated_response({
                "code": 200,
                "msg": "Lista de miembros obtenida correctamente.",
                "data": serializer.data
            })
        except Exception as e:
            return Response(
                {"code": 500, "msg": f"Ocurrió un error al obtener los miembros: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Obtener miembro por ID",
        description="Devuelve la información de un miembro específico según su ID.",
        responses={
            200: OpenApiResponse(response=MemberSerializer, description="Miembro obtenido correctamente."),
            401: OpenApiResponse(description="El miembro no existe."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(
                {"code": 200, "msg": "Miembro obtenido correctamente.", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response(
                {"code": 401, "msg": "El miembro no existe."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"code": 500, "msg": f"Ocurrió un error al obtener el miembro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Crear un nuevo miembro",
        description="Registra un nuevo miembro en el sistema.",
        request=MemberSerializer,
        responses={
            201: OpenApiResponse(response=MemberSerializer, description="Miembro creado correctamente."),
            400: OpenApiResponse(description="Datos inválidos o error de validación."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=status.HTTP_400_BAD_REQUEST)
        
            result = self.service.create_member(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Actualizar un miembro existente",
        description="Actualiza los datos de un miembro según su ID.",
        request=MemberSerializer,
        responses={
            200: OpenApiResponse(description="Miembro actualizado correctamente."),
            400: OpenApiResponse(description="Datos inválidos o error de validación."),
            404: OpenApiResponse(description="El miembro no existe."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(data=request.data, partial=True)
            if not serializer.is_valid():
                msg = next(iter(serializer.errors.values()))[0]
                return Response({"code": 400, "msg": msg}, status=status.HTTP_400_BAD_REQUEST)
            result = self.service.update_member(instance, serializer.validated_data)
            return Response(result, status=status.HTTP_200_OK)
        except Http404:
            return Response({"code": 404, "msg": "El miembro no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        summary="Eliminar miembro",
        description="Elimina un miembro existente según su ID.",
        responses={
            204: OpenApiResponse(description="Miembro eliminado correctamente."),
            404: OpenApiResponse(description="El miembro no existe."),
            500: OpenApiResponse(description="Error interno del servidor."),
        },
    )
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.service.delete_member(instance)
            return Response({"code": 204, "msg": "Miembro eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({"code": 404, "msg": "El miembro no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"code": 500, "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
