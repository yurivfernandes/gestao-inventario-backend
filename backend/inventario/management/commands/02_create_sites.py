import random

from django.core.management.base import BaseCommand
from faker import Faker
from inventario.models import Cliente, Site


class Command(BaseCommand):
    help = "Cria registros fake para o modelo Site"

    def handle(self, *args, **kwargs):
        fake = Faker("pt_BR")
        cliente_arcos_dourados = Cliente.objects.get(id=31)
        cliente_drogas_raia = Cliente.objects.get(id=32)
        tipos_negocio_arcos = ["restaurante", "quiosque"]
        tipos_negocio_raia = ["farmácia", "franquia"]
        complementos = ["shopping", "bairro"]

        # Apagar todos os dados antes de inserir
        Site.objects.filter().delete()

        # Criar sites para Arcos Dourados
        for _ in range(3500):
            tipo_negocio = fake.random_element(tipos_negocio_arcos)
            codigo_sys_cliente = (
                "RST" if tipo_negocio == "restaurante" else "KSK"
            )
            codigo_vivo = f"{codigo_sys_cliente}_{fake.random_number(digits=6, fix_len=True)}"
            status = random.random() > 0.1  # 10% inativos

            Site.objects.create(
                cliente=cliente_arcos_dourados,
                cep=fake.postcode(),
                numero=fake.building_number(),
                complemento=fake.random_element(complementos),
                codigo_sys_cliente=codigo_sys_cliente,
                codigo_vivo=codigo_vivo,
                status=status,
                tipo_site="estabelecimento",
                tipo_negocio=tipo_negocio,
            )

        # Criar sites para Drogas Raia
        for _ in range(1500):
            tipo_negocio = fake.random_element(tipos_negocio_raia)
            codigo_sys_cliente = "FMC" if tipo_negocio == "farmácia" else "FRQ"
            codigo_vivo = f"{codigo_sys_cliente}_{fake.random_number(digits=6, fix_len=True)}"
            status = random.random() > 0.15  # 15% inativos

            Site.objects.create(
                cliente=cliente_drogas_raia,
                cep=fake.postcode(),
                numero=fake.building_number(),
                complemento=fake.random_element(complementos),
                codigo_sys_cliente=codigo_sys_cliente,
                codigo_vivo=codigo_vivo,
                status=status,
                tipo_site="estabelecimento",
                tipo_negocio=tipo_negocio,
            )

        self.stdout.write(
            self.style.SUCCESS(
                "3500 registros de Site para Arcos Dourados e 1500 registros de Site para Drogas Raia criados com sucesso!"
            )
        )
