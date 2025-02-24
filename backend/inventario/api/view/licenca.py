from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Contrato, GrupoEconomico, Licenca
from ..serializers import LicencaSerializer


class LicencaListCreate(APIView):
    def get(self, request):
        try:
            # Filtro obrigatório de grupo econômico
            grupo_economico_id = request.query_params.get("grupo_economico")
            grupo_economico = get_object_or_404(
                GrupoEconomico, pk=grupo_economico_id
            )

            licencas = Licenca.objects.select_related(
                "contrato",
                "contrato__equipamento",
                "contrato__equipamento__site",
                "contrato__equipamento__site__cliente",
            ).filter(
                contrato__equipamento__site__cliente__grupo_economico=grupo_economico
            )

            # Filtro de cliente
            cliente_id = request.query_params.get("cliente")
            if cliente_id:
                licencas = licencas.filter(
                    contrato__equipamento__site__cliente_id=cliente_id
                )

            # Filtro de status
            status_param = request.query_params.get("status")
            if status_param is not None:
                status_bool = status_param.lower() == "true"
                licencas = licencas.filter(status=status_bool)

            contrato_id = request.query_params.get("contrato")
            if contrato_id:
                contrato = get_object_or_404(Contrato, pk=contrato_id)
                licencas = licencas.filter(contrato=contrato)

            search = request.query_params.get("search")
            if search:
                licencas = licencas.filter(Q(licenca_numero__icontains=search))

            paginator = Paginator(licencas.distinct(), 50)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)

            serializer = LicencaSerializer(page_obj, many=True)
            return Response(
                {
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": page_obj.number,
                    "results": serializer.data,
                }
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        serializer = LicencaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicencaUpdate(APIView):
    def put(self, request, pk):
        licenca = get_object_or_404(Licenca, pk=pk)

        data = request.data.copy()
        if "contrato" in data:
            del data["contrato"]

        serializer = LicencaSerializer(licenca, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
