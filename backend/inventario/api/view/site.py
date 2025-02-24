from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Cliente, GrupoEconomico, Site
from ..serializers import SiteSerializer


class SiteListCreate(APIView):
    def get(self, request):
        try:
            grupo_economico_id = request.query_params.get("grupo_economico")
            grupo_economico = get_object_or_404(
                GrupoEconomico, pk=grupo_economico_id
            )

            sites = Site.objects.filter(
                cliente__grupo_economico=grupo_economico
            )

            cliente_id = request.query_params.get("cliente")
            if cliente_id:
                cliente = get_object_or_404(
                    Cliente, pk=cliente_id, grupo_economico=grupo_economico
                )
                sites = sites.filter(cliente=cliente)

            search = request.query_params.get("search")
            if search:
                sites = sites.filter(
                    Q(razao_social__icontains=search)
                    | Q(cnpj__icontains=search)
                    | Q(codigo_vivo__icontains=search)
                )

            paginator = Paginator(sites, 50)  # 50 registros por página
            page_number = request.query_params.get("page")
            page_obj = paginator.get_page(page_number)

            serializer = SiteSerializer(page_obj, many=True)
            return Response(
                {
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": page_obj.number,
                    "results": serializer.data,
                }
            )
        except ValidationError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Erro ao buscar sites"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteUpdate(APIView):
    def put(self, request, pk):
        site = get_object_or_404(Site, pk=pk)

        # Remove o cliente do request.data se presente
        data = request.data.copy()
        if "cliente" in data:
            del data["cliente"]

        serializer = SiteSerializer(site, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
