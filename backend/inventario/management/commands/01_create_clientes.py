from django.core.management.base import BaseCommand
from faker import Faker
from inventario.models import Cliente


class Command(BaseCommand):
    help = "Cria registros fake para o modelo Cliente"

    def add_arguments(self, parser):
        parser.add_argument(
            "quantity",
            type=int,
            help="Quantidade de registros a serem criados",
        )

    def handle(self, *args, **kwargs):
        quantity = kwargs["quantity"]
        fake = Faker("pt_BR")

        for _ in range(quantity):
            Cliente.objects.create(
                vantive_id=fake.random_int(min=1, max=10000),
                razao_social=fake.company(),
                codigo=fake.bothify(text="CLI-########"),
                status=fake.boolean(),
                cnpj=fake.cnpj(),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{quantity} registros de Cliente criados com sucesso!"
            )
        )
