# Migrations do Módulo Incidentes

## Estrutura das Migrations

### Django (Python)
```python
# 0001_initial.py
class Migration(migrations.Migration):
    initial = True

    operations = [
        migrations.CreateModel(
            name='Incidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True)),
                ('categoria', models.CharField(max_length=100)),
                # ...outros campos...
            ],
        ),
    ]
```

### Entity Framework (C#)
```csharp
public partial class InitialCreate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Incidentes",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("SqlServer:Identity", "1, 1"),
                Categoria = table.Column<string>(maxLength: 100, nullable: false),
                // ...outros campos...
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Incidentes");
    }
}
```

### SQL Puro
```sql
-- V1__Create_Incidente_Table.sql
CREATE TABLE Incidentes (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    Categoria NVARCHAR(100) NOT NULL,
    -- ...outros campos...
);

-- V1__Rollback.sql
DROP TABLE Incidentes;
```

## Gerenciamento de Migrations

### Django
```bash
# Criar nova migration
python manage.py makemigrations incidentes

# Aplicar migrations
python manage.py migrate incidentes

# Ver SQL que será executado
python manage.py sqlmigrate incidentes 0001
```

### Entity Framework
```powershell
# Criar migration
Add-Migration CreateIncidenteTable -Context IncidenteContext

# Aplicar migration
Update-Database -Context IncidenteContext

# Ver SQL que será executado
Script-Migration
```

### SQL Puro
- Precisa gerenciar manualmente os scripts
- Usar ferramentas como Flyway ou Liquibase
- Manter controle de versão dos scripts

## Boas Práticas

1. **Nomear Migrations**
   ```bash
   # Django
   python manage.py makemigrations incidentes --name create_incidente_table

   # EF
   Add-Migration CreateIncidenteTable
   ```

2. **Dados Iniciais**
   ```python
   # Django - data migration
   from django.db import migrations

   def criar_dados_iniciais(apps, schema_editor):
       Incidente = apps.get_model('incidentes', 'Incidente')
       Incidente.objects.create(
           categoria='Urgente',
           status='Aberto'
       )

   class Migration(migrations.Migration):
       dependencies = [
           ('incidentes', '0001_initial'),
       ]

       operations = [
           migrations.RunPython(criar_dados_iniciais),
       ]
   ```

3. **Reversão de Migrations**
   ```python
   # Django
   python manage.py migrate incidentes 0001

   # EF
   Update-Database -Migration CreateIncidenteTable
   ```
