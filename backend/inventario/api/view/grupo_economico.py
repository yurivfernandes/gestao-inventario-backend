from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import GrupoEconomico
from ..serializers import GrupoEconomicoSerializer


class GrupoEconomicoListCreate(APIView):
    def get(self, request):
        try:
            grupos = GrupoEconomico.objects.all()

            search = request.query_params.get("search")
            if search:
                grupos = grupos.filter(
                    Q(nome__icontains=search) | Q(codigo__icontains=search)
                )

            paginator = Paginator(grupos, 50)
            page_number = request.query_params.get("page", 1)
            page_obj = paginator.get_page(page_number)

            serializer = GrupoEconomicoSerializer(page_obj, many=True)
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
                {"error": "Erro ao buscar grupos econômicos"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request):
        serializer = GrupoEconomicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GrupoEconomicoUpdate(APIView):
    def put(self, request, pk):
        grupo_economico = get_object_or_404(GrupoEconomico, pk=pk)

        serializer = GrupoEconomicoSerializer(
            grupo_economico, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
