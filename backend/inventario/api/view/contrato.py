from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Contrato, Equipamento, GrupoEconomico
from ..serializers import ContratoSerializer


class ContratoListCreate(APIView):
    def get(self, request):
        try:
            grupo_economico_id = request.query_params.get("grupo_economico")
            grupo_economico = get_object_or_404(
                GrupoEconomico, pk=grupo_economico_id
            )

            contratos = Contrato.objects.select_related(
                "equipamento", "equipamento__site"
            ).filter(
                equipamento__site__cliente__grupo_economico=grupo_economico
            )

            equipamento_id = request.query_params.get("equipamento")
            if equipamento_id:
                equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
                contratos = contratos.filter(equipamento=equipamento)

            status_param = request.query_params.get("status")
            if status_param is not None:
                if status_param == "true":
                    status_param = True
                else:
                    status_param = False
                contratos = contratos.filter(status=status_param)

            search = request.query_params.get("search")
            if search:
                contratos = contratos.filter(Q(sku__icontains=search))

            paginator = Paginator(contratos.distinct(), 50)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)

            serializer = ContratoSerializer(page_obj, many=True)
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
        serializer = ContratoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContratoUpdate(APIView):
    def put(self, request, pk):
        contrato = get_object_or_404(Contrato, pk=pk)

        data = request.data.copy()
        if "equipamento" in data:
            del data["equipamento"]

        serializer = ContratoSerializer(contrato, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
