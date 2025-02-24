# API de Incidentes

## Implementação Django

### View de Listagem
```python
class IncidenteListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        queryset = Incidente.objects.all()
        # ...lógica de filtros...
```

## Equivalente em C#

### Controller
```csharp
[ApiController]
[Route("api/[controller]")]
public class IncidentesController : ControllerBase
{
    private readonly ApplicationDbContext _context;
    
    public IncidentesController(ApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    [Authorize]
    public async Task<ActionResult<IEnumerable<Incidente>>> GetIncidentes([FromQuery] IncidenteFilter filter)
    {
        var query = _context.Incidentes.AsQueryable();

        // Filtros de data
        if (filter.DataAberturaInicio.HasValue)
            query = query.Where(i => i.DataAbertura >= filter.DataAberturaInicio);
        
        if (filter.DataAberturaFim.HasValue)
            query = query.Where(i => i.DataAbertura <= filter.DataAberturaFim);

        // Busca em texto
        if (!string.IsNullOrEmpty(filter.Search))
        {
            query = query.Where(i => 
                i.Origem.Contains(filter.Search) ||
                i.Categoria.Contains(filter.Search) ||
                i.Subcategoria.Contains(filter.Search) ||
                i.Descricao.Contains(filter.Search)
            );
        }

        // Paginação
        var pageSize = 10;
        var page = await query
            .Skip((filter.Page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return Ok(new {
            Items = page,
            TotalCount = await query.CountAsync()
        });
    }
}
```

### SQL Equivalente
```sql
-- Exemplo de consulta com filtros
DECLARE @search NVARCHAR(100) = '%termo%'
DECLARE @dataInicio DATETIME = '2024-01-01'
DECLARE @dataFim DATETIME = '2024-12-31'

SELECT *
FROM f_incidente
WHERE 
    (data_abertura BETWEEN @dataInicio AND @dataFim)
    AND (
        origem LIKE @search OR
        categoria LIKE @search OR
        subcategoria LIKE @search OR
        descricao LIKE @search
    )
ORDER BY data_abertura DESC
OFFSET 0 ROWS
FETCH NEXT 10 ROWS ONLY
```

## Principais Diferenças

1. **Roteamento**
   - Django: Definido em urls.py
   - C#: Atributos no controller

2. **Autenticação**
   - Django: `permission_classes`
   - C#: Atributo `[Authorize]`

3. **Paginação**
   - Django: Classe customizada de paginação
   - C#: Skip/Take manualmente
   - SQL: OFFSET/FETCH

4. **Filtros**
   - Django: Q objects para queries complexas
   - C#: LINQ
   - SQL: WHERE clauses
