import random

from django.core.management.base import BaseCommand
from faker import Faker
from inventario.models import Equipamento, Site


class Command(BaseCommand):
    help = "Cria registros fake para o modelo Equipamento"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
        sites = list(Site.objects.all())
        tipos_equipamento = [
            "sd-wan",
            "sd-lan",
            "sd-wifi",
            "router",
            "switch",
            "firewall",
            "sbc",
            "access point",
            "controller",
            "pabx ip",
            "media gateway",
            "outros",
        ]

        # Apagar todos os equipamentos antes de inserir
        Equipamento.objects.all().delete()

        for site in sites:
            num_equipamentos = random.randint(
                1, 10
            )  # Cada site pode ter de 1 a 10 equipamentos
            for _ in range(num_equipamentos):
                tipo = fake.random_element(tipos_equipamento)
                codigo = f"vivo_{fake.random_number(digits=4, fix_len=True)}_{site.id}"
                designador = "VGR" if random.random() < 0.8 else "outros"

                Equipamento.objects.create(
                    site=site,
                    codigo=codigo,
                    status=fake.boolean(),
                    designador=designador,
                    tipo=tipo,
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Equipamentos criados com sucesso para todos os sites existentes!"
            )
        )
