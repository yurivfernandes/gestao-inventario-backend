from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Incidente
from ..serializers import IncidenteSerializer


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class IncidenteListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        # Criar query base
        queryset = Incidente.objects.all()

        # Aplicar filtros baseados nos parâmetros da URL
        filters = {}
        date_filters = {}

        # Campos de data com tratamento para período
        date_ranges = {
            "data_abertura": ["data_abertura_inicio", "data_abertura_fim"],
            "data_fechamento": [
                "data_fechamento_inicio",
                "data_fechamento_fim",
            ],
            "data_resolucao": ["data_resolucao_inicio", "data_resolucao_fim"],
        }

        # Processar filtros de período de data
        for field, range_fields in date_ranges.items():
            inicio = request.query_params.get(range_fields[0])
            fim = request.query_params.get(range_fields[1])

            if inicio:
                date_filters[f"{field}__gte"] = inicio
            if fim:
                date_filters[f"{field}__lte"] = fim

        # Campos de data com tratamento especial
        date_fields = ["data_abertura", "data_fechamento", "data_resolucao"]

        for field in Incidente._meta.fields:
            field_name = field.name
            if field_name in request.query_params:
                if field_name in date_fields:
                    date_filters[f"{field_name}__date"] = request.query_params[
                        field_name
                    ]
                else:
                    filters[field_name] = request.query_params[field_name]

        # Aplicar busca em campos de texto
        search = request.query_params.get("search", "")
        if search:
            text_query = (
                Q(origem__icontains=search)
                | Q(categoria__icontains=search)
                | Q(subcategoria__icontains=search)
                | Q(detalhe_subcategoria__icontains=search)
                | Q(descricao__icontains=search)
                | Q(incidente__icontains=search)
            )
            queryset = queryset.filter(text_query)

        # Aplicar os filtros
        queryset = queryset.filter(**filters).filter(**date_filters)

        # Paginação
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = IncidenteSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = IncidenteSerializer(queryset, many=True)
        return Response(serializer.data)
