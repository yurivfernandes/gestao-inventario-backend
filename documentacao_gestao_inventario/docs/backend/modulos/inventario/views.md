# Views do Módulo Inventário

## Cliente Views

### ClienteListCreate
Endpoint para listar e criar clientes.

#### GET /api/inventario/clientes/
- **Permissões**: Requer autenticação
- **Filtros**:
  - razao_social
  - cnpj
  - vantive_id
  - codigo
  - status

##### Exemplo SQL Equivalente
```sql
SELECT * FROM d_cliente 
WHERE razao_social LIKE %?% 
  AND cnpj LIKE %?% 
  AND codigo LIKE %?% 
  AND vantive_id = ? 
  AND status = ?
LIMIT 50 OFFSET ?;
```

##### Exemplo C# Equivalente
```csharp
public class ClienteController : ControllerBase
{
    [HttpGet]
    [Authorize]
    public async Task<ActionResult<PagedResult<Cliente>>> GetClientes(
        [FromQuery] string razaoSocial,
        [FromQuery] string cnpj,
        [FromQuery] int? vantiveId,
        [FromQuery] string codigo,
        [FromQuery] bool? status,
        [FromQuery] int page = 1)
    {
        var query = _context.Clientes.AsQueryable();
        
        if (!string.IsNullOrEmpty(razaoSocial))
            query = query.Where(c => c.RazaoSocial.Contains(razaoSocial));
            
        if (!string.IsNullOrEmpty(cnpj))
            query = query.Where(c => c.Cnpj.Contains(cnpj));
            
        // ... outros filtros

        return Ok(await query.ToPagedResultAsync(page, 50));
    }
}
```

## Site Views

### SiteListCreate
Endpoint para listar e criar sites.

#### GET /api/inventario/sites/
- **Filtros Obrigatórios**: cliente_id
- **Filtros Opcionais**: search (busca em codigo_vivo e tipo_negocio)

##### Exemplo SQL Equivalente
```sql
SELECT s.* 
FROM d_site s
WHERE s.cliente_id = ?
  AND (s.codigo_vivo LIKE %?% OR s.tipo_negocio LIKE %?%)
LIMIT 50 OFFSET ?;
```

##### Exemplo C# Equivalente
```csharp
[HttpGet]
public async Task<ActionResult<PagedResult<Site>>> GetSites(
    [FromQuery] int clienteId,
    [FromQuery] string search,
    [FromQuery] int page = 1)
{ 
    if (clienteId == 0)
        return BadRequest(new { error = "Cliente é obrigatório" });

    var query = _context.Sites
        .Where(s => s.ClienteId == clienteId);

    if (!string.IsNullOrEmpty(search))
    {
        query = query.Where(s => 
            s.CodigoVivo.Contains(search) || 
            s.TipoNegocio.Contains(search));
    }

    return Ok(await query.ToPagedResultAsync(page, 50));
}
```

## Equipamento Views

### EquipamentoListCreate
Endpoint para listar e criar equipamentos.

#### GET /api/inventario/equipamentos/
- **Filtros Obrigatórios**: cliente_id
- **Filtros Opcionais**: 
  - site_id
  - search (busca em designador e codigo)

##### Exemplo SQL Equivalente
```sql
SELECT e.* 
FROM d_equipamento e
INNER JOIN d_site s ON e.site_id = s.id
WHERE s.cliente_id = ?
  AND (e.site_id = ? OR ? IS NULL)
  AND (e.designador LIKE %?% OR e.codigo LIKE %?%)
LIMIT 50 OFFSET ?;
```

##### Exemplo C# Equivalente
```csharp
[HttpGet]
public async Task<ActionResult<PagedResult<Equipamento>>> GetEquipamentos(
    [FromQuery] int clienteId,
    [FromQuery] int? siteId,
    [FromQuery] string search,
    [FromQuery] int page = 1)
{
    if (clienteId == 0)
        return BadRequest(new { error = "Cliente é obrigatório" });

    var query = _context.Equipamentos
        .Include(e => e.Site)
        .Where(e => e.Site.ClienteId == clienteId);

    if (siteId.HasValue)
        query = query.Where(e => e.SiteId == siteId);

    if (!string.IsNullOrEmpty(search))
    {
        query = query.Where(e => 
            e.Designador.Contains(search) || 
            e.Codigo.Contains(search));
    }

    return Ok(await query.ToPagedResultAsync(page, 50));
}
```

## Serviço Views

### ServicoListCreate
Endpoint para listar e criar serviços.

#### GET /api/inventario/servicos/
- **Filtros Obrigatórios**: cliente_id
- **Filtros Opcionais**: 
  - site_id
  - equipamento_id
  - search (busca em designador e codigo)

##### Exemplo SQL Equivalente
```sql
SELECT sv.* 
FROM d_servico sv
INNER JOIN d_equipamento e ON sv.equipamento_id = e.id
INNER JOIN d_site s ON e.site_id = s.id
WHERE s.cliente_id = ?
  AND (e.site_id = ? OR ? IS NULL)
  AND (sv.equipamento_id = ? OR ? IS NULL)
  AND (sv.designador LIKE %?% OR sv.codigo LIKE %?%)
LIMIT 50 OFFSET ?;
```

##### Exemplo C# Equivalente
```csharp
[HttpGet]
public async Task<ActionResult<PagedResult<Servico>>> GetServicos(
    [FromQuery] int clienteId,
    [FromQuery] int? siteId,
    [FromQuery] int? equipamentoId,
    [FromQuery] string search,
    [FromQuery] int page = 1)
{
    if (clienteId == 0)
        return BadRequest(new { error = "Cliente é obrigatório" });

    var query = _context.Servicos
        .Include(s => s.Equipamento)
        .ThenInclude(e => e.Site)
        .Where(s => s.Equipamento.Site.ClienteId == clienteId);

    if (siteId.HasValue)
        query = query.Where(s => s.Equipamento.SiteId == siteId);

    if (equipamentoId.HasValue)
        query = query.Where(s => s.EquipamentoId == equipamentoId);

    if (!string.IsNullOrEmpty(search))
    {
        query = query.Where(s => 
            s.Designador.Contains(search) || 
            s.Codigo.Contains(search));
    }

    return Ok(await query.ToPagedResultAsync(page, 50));
}
```
