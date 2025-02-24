from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Cliente, GrupoEconomico
from ..serializers import ClienteSerializer


class ClienteListCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        grupo_economico_id = request.query_params.get("grupo_economico")
        grupo_economico = get_object_or_404(
            GrupoEconomico, pk=grupo_economico_id
        )

        # Inicia com clientes filtrados por grupo econômico
        clientes = Cliente.objects.filter(grupo_economico=grupo_economico)

        # Aplica os filtros se fornecidos
        razao_social = request.query_params.get("razao_social")
        cnpj = request.query_params.get("cnpj")
        vantive_id = request.query_params.get("vantive_id")
        codigo = request.query_params.get("codigo")
        status_param = request.query_params.get("status")

        if razao_social:
            clientes = clientes.filter(razao_social__icontains=razao_social)
        if cnpj:
            clientes = clientes.filter(cnpj__icontains=cnpj)
        if codigo:
            clientes = clientes.filter(codigo__icontains=codigo)
        if vantive_id:
            clientes = clientes.filter(vantive_id=vantive_id)
        if (
            status_param is not None
        ):  # Precisa checar None porque status pode ser False
            clientes = clientes.filter(status=status_param.lower() == "true")

        paginator = Paginator(clientes, 50)
        page_number = request.query_params.get("page", 1)
        page_obj = paginator.get_page(page_number)

        serializer = ClienteSerializer(page_obj, many=True)
        return Response(
            {
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page_obj.number,
                "results": serializer.data,
            }
        )

    def post(self, request):
        grupo_economico_id = request.data.get("grupo_economico")
        grupo_economico = get_object_or_404(
            GrupoEconomico, pk=grupo_economico_id
        )

        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(grupo_economico=grupo_economico)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClienteUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        cliente = get_object_or_404(Cliente, pk=pk)

        # Remove o grupo_economico do request.data se presente
        data = request.data.copy()
        if "grupo_economico" in data:
            del data["grupo_economico"]

        serializer = ClienteSerializer(cliente, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
