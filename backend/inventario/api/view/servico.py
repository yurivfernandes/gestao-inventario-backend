from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Cliente, Equipamento, GrupoEconomico, Servico, Site
from ..serializers import ServicoSerializer


class ServicoListCreate(APIView):
    def get(self, request):
        try:
            grupo_economico_id = request.query_params.get("grupo_economico")
            grupo_economico = get_object_or_404(
                GrupoEconomico, pk=grupo_economico_id
            )

            servicos = Servico.objects.select_related(
                "equipamento", "equipamento__site"
            ).filter(
                equipamento__site__cliente__grupo_economico=grupo_economico
            )

            cliente_id = request.query_params.get("cliente")
            if cliente_id:
                cliente = get_object_or_404(
                    Cliente, pk=cliente_id, grupo_economico=grupo_economico
                )
                servicos = servicos.filter(equipamento__site__cliente=cliente)

            site_id = request.query_params.get("site")
            if site_id:
                site = get_object_or_404(
                    Site, pk=site_id, cliente__grupo_economico=grupo_economico
                )
                servicos = servicos.filter(equipamento__site=site)

            equipamento_id = request.query_params.get("equipamento")
            if equipamento_id:
                equipamento = get_object_or_404(
                    Equipamento,
                    pk=equipamento_id,
                    site__cliente__grupo_economico=grupo_economico,
                )
                servicos = servicos.filter(equipamento=equipamento)

            # Debug para verificar os parâmetros recebidos
            print(f"Parâmetros recebidos na API: {request.query_params}")

            # Aplicar filtros em sequência
            if site_id:
                servicos = servicos.filter(equipamento__site_id=site_id)

            if equipamento_id:
                servicos = servicos.filter(equipamento_id=equipamento_id)

            # Aplicar busca se houver
            search = request.query_params.get("search")
            if search:
                servicos = servicos.filter(
                    Q(designador__icontains=search)
                    | Q(servico_num__icontains=search)
                    | Q(oferta__icontains=search)
                    | Q(operadora__icontains=search)
                    | Q(ip__icontains=search)
                )

            # Paginação dos resultados
            paginator = Paginator(servicos.distinct(), 50)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)

            serializer = ServicoSerializer(page_obj, many=True)
            return Response(
                {
                    "count": paginator.count,
                    "num_pages": paginator.num_pages,
                    "current_page": page_obj.number,
                    "results": serializer.data,
                    "filters_applied": {
                        "grupo_economico": grupo_economico_id,
                        "cliente": cliente_id,
                        "site": site_id,
                        "equipamento": equipamento_id,
                        "search": search,
                    },
                }
            )

        except ValidationError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print(f"Erro ao buscar serviços: {str(e)}")  # Debug
            return Response(
                {"error": "Erro ao buscar serviços"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        serializer = ServicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicoUpdate(APIView):
    def put(self, request, pk):
        servico = get_object_or_404(Servico, pk=pk)

        data = request.data.copy()
        if "equipamento" in data:
            del data["equipamento"]

        serializer = ServicoSerializer(servico, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
