# Modelo de Incidentes

## Implementação Django
O modelo de incidentes é implementado usando o ORM do Django.

```python
class Incidente(models.Model):
    aberto_por = models.CharField(max_length=50)
    categoria = models.CharField(max_length=100)
    # ...outros campos...

    class Meta:
        db_table = "f_incidente"
```

## Equivalente em C#

### Modelo em C# (Entity Framework)
```csharp
public class Incidente
{
    public int Id { get; set; }
    public string AbertoPor { get; set; }
    public string Categoria { get; set; }
    public string CodigoEquipamento { get; set; }
    public string CodigoServico { get; set; }
    public DateTime DataAbertura { get; set; }
    public DateTime? DataFechamento { get; set; }
    public DateTime? DataResolucao { get; set; }
    public TimeSpan Duracao { get; set; }
    public string Descricao { get; set; }
    public string Fila { get; set; }
    public string IncidenteNumero { get; set; }
    public string Origem { get; set; }
    public string Status { get; set; }
    public string Subcategoria { get; set; }
    public string SubcategoriaDetalhe { get; set; }
    public string TipoContato { get; set; }
    
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
```

### SQL Puro
```sql
CREATE TABLE f_incidente (
    id INT IDENTITY(1,1) PRIMARY KEY,
    aberto_por NVARCHAR(50) NOT NULL,
    categoria NVARCHAR(100) NOT NULL,
    codigo_equipamento NVARCHAR(50) NOT NULL,
    codigo_servico NVARCHAR(50) NOT NULL,
    data_abertura DATETIME NOT NULL,
    data_fechamento DATETIME NULL,
    data_resolucao DATETIME NULL,
    duracao TIME NOT NULL,
    descricao NTEXT NOT NULL,
    fila NVARCHAR(50) NOT NULL,
    incidente NVARCHAR(50) NOT NULL,
    origem NVARCHAR(100) NOT NULL,
    status NVARCHAR(20) NOT NULL,
    subcategoria NVARCHAR(100) NOT NULL,
    subcategoria_detalhe NVARCHAR(200) NOT NULL,
    tipo_contato NVARCHAR(50) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE()
)
```

## Principais Diferenças

1. **Definição de Campo**
   - Django: Usa classes do models para definir campos
   - C#/EF: Usa propriedades com DataAnnotations
   - SQL: Definição direta dos tipos de dados

2. **Nomenclatura**
   - Django: snake_case (padrão Python)
   - C#: PascalCase
   - SQL: Geralmente snake_case

3. **Timestamps Automáticos**
   - Django: `auto_now_add` e `auto_now`
   - C#/EF: Precisa implementar manualmente
   - SQL: Usa DEFAULT GETDATE()

4. **Campos Nulos**
   - Django: `null=True, blank=True`
   - C#: Tipo nullable (`DateTime?`)
   - SQL: NULL/NOT NULL
