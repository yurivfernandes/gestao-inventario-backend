from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Equipamento, GrupoEconomico, Link
from ..serializers import LinkSerializer


class LinkListCreate(APIView):
    def get(self, request):
        try:
            grupo_economico_id = request.query_params.get("grupo_economico")
            grupo_economico = get_object_or_404(
                GrupoEconomico, pk=grupo_economico_id
            )

            links = Link.objects.select_related(
                "equipamento",
                "equipamento__site",
                "equipamento__site__cliente",
            ).filter(
                equipamento__site__cliente__grupo_economico=grupo_economico
            )

            cliente_id = request.query_params.get("cliente")
            if cliente_id:
                links = links.filter(equipamento__site__cliente_id=cliente_id)

            status_param = request.query_params.get("status")
            if status_param is not None:
                status_bool = status_param.lower() == "true"
                links = links.filter(status=status_bool)

            equipamento_id = request.query_params.get("equipamento")
            if equipamento_id:
                equipamento = get_object_or_404(Equipamento, pk=equipamento_id)
                links = links.filter(equipamento=equipamento)

            search = request.query_params.get("search")
            if search:
                links = links.filter(
                    Q(operadora__icontains=search)
                    | Q(designador__icontains=search)
                )

            paginator = Paginator(links.distinct(), 50)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)

            serializer = LinkSerializer(page_obj, many=True)
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
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinkUpdate(APIView):
    def put(self, request, pk):
        link = get_object_or_404(Link, pk=pk)

        data = request.data.copy()
        if "equipamento" in data:
            del data["equipamento"]

        serializer = LinkSerializer(link, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
