import random

from django.core.management.base import BaseCommand
from faker import Faker
from inventario.models import Equipamento, Servico


class Command(BaseCommand):
    help = "Cria registros fake para o modelo Servico"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
        equipamentos = list(Equipamento.objects.all())
        tipos_servico = ["Vivo Gestão de Redes", "Legado", "Projeto especial"]

        # Apagar todos os serviços antes de inserir
        Servico.objects.all().delete()

        for equipamento in equipamentos:
            num_servicos = random.randint(
                1, 3
            )  # Cada equipamento pode ter de 1 a 3 serviços
            for _ in range(num_servicos):
                tipo = (
                    "Vivo Gestão de Redes"
                    if random.random() < 0.8
                    else fake.random_element(tipos_servico[1:])
                )
                codigo = f"vivo_{fake.random_number(digits=6, fix_len=True)}"
                designador = (
                    "VGR"
                    if tipo == "Vivo Gestão de Redes"
                    else ("VGR" if random.random() < 0.5 else "outros")
                )

                Servico.objects.create(
                    equipamento=equipamento,
                    codigo=codigo,
                    status=fake.boolean(),
                    designador=designador,
                    tipo=tipo,
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Serviços criados com sucesso para todos os equipamentos existentes!"
            )
        )
