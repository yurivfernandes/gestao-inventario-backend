import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from incidentes.models import Incidente


class Command(BaseCommand):
    help = """
    Cria registros fake de incidentes.
    
    Exemplo de uso:
    python manage.py create_fake_incidentes 100
    
    Isso criará 100 registros de incidentes com dados aleatórios.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="Quantidade de incidentes a serem criados"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]

        CATEGORIAS = [
            "outros",
            "redes wan",
            "redes",
            "sd-wan",
            "security",
            "serviço wan",
            "wireless",
            "operadora",
            "equipamento",
            "devnet",
            "cliente",
        ]

        SUBCATEGORIAS = [
            "access point",
            "acesso",
            "atualização de software e firmware",
            "balanceador",
            "big-ip",
            "cabeamento",
            "call manager",
            "diversos",
            "energia elétrica",
            "equipamento",
            "equipamento sd-wan",
            "falha",
            "firewall",
            "infraestrutura",
            "operadora vivo",
            "operadora terceira",
            "pabx",
            "rede",
            "router",
            "ramal",
            "sd-wan",
            "switch",
            "webex",
            "wifi",
        ]

        STATUS = [
            "Em andamento",
            "Encerrado",
            "Novo",
            "Pendente",
            "Resolvido",
            "Reaberto",
        ]
        ABERTO_POR = ["automação", "analista"]
        TIPO_CONTATO = ["monitoramento", "equipamentos"]

        # Pegar último número de incidente
        ultimo_incidente = Incidente.objects.order_by("-incidente").first()
        if ultimo_incidente:
            ultimo_numero = int(ultimo_incidente.incidente[3:])
        else:
            ultimo_numero = 0

        self.stdout.write(
            self.style.SUCCESS(
                f"\nIniciando criação de {total} incidentes...\n"
            )
        )

        for i in range(total):
            numero_incidente = str(ultimo_numero + i + 1).zfill(9)
            incidente_id = f"INC{numero_incidente}"

            aberto_por = random.choice(ABERTO_POR)
            duracao = timedelta(minutes=3 if aberto_por == "automação" else 20)

            # Gerar datas consistentes
            data_inicio = timezone.datetime(2024, 3, 1, tzinfo=timezone.utc)
            data_fim = timezone.now()
            dias_total = (data_fim - data_inicio).days

            data_abertura = data_inicio + timedelta(
                days=random.randint(0, dias_total)
            )
            data_resolucao = data_abertura + duracao
            data_fechamento = data_resolucao + timedelta(
                minutes=random.randint(1, 10)
            )

            categoria = random.choice(CATEGORIAS)
            subcategoria = random.choice(SUBCATEGORIAS)

            incidente = Incidente(
                incidente=incidente_id,
                aberto_por=aberto_por,
                categoria=categoria,
                codigo_equipamento=f"EQP{random.randint(1000, 9999)}",
                codigo_servico=f"SVC{random.randint(1000, 9999)}",
                data_abertura=data_abertura,
                data_resolucao=data_resolucao,
                data_fechamento=data_fechamento,
                duracao=duracao,
                descricao=f"Descrição do incidente {incidente_id}",
                fila="VITA-AUTOMATION"
                if aberto_por == "automação"
                else "VITA-NOC",
                origem="Vita - IT",
                status=random.choice(STATUS),
                subcategoria=subcategoria,
                subcategoria_detalhe=subcategoria,
                tipo_contato=random.choice(TIPO_CONTATO),
            )

            incidente.save()

            if (i + 1) % 100 == 0 or (i + 1) == total:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Progresso: {i + 1}/{total} incidentes criados"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nProcesso finalizado! {total} incidentes foram criados com sucesso!"
            )
        )
