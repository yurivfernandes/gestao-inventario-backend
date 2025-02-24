# Models do Módulo Inventário

## Visão Geral
O módulo de inventário é composto por 5 models principais que representam a estrutura hierárquica do inventário:
- Grupo Econômico
- Cliente
- Site
- Equipamento
- Serviço

## Model Grupo Econômico
Representa os grupos econômicos que agrupam clientes no sistema.

### Definição Django
```python
class GrupoEconomico(models.Model):
    nome = models.CharField(max_length=255)
    codigo = models.CharField(max_length=30)
    status = models.BooleanField()

    class Meta:
        db_table = 'd_grupo_economico'
```

### SQL Equivalente
```sql
CREATE TABLE d_grupo_economico (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL
);
```

### C# Equivalente
```csharp
public class GrupoEconomico
{
    public long Id { get; set; }
    public string Nome { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
}
```

## Model Cliente
Representa os clientes no sistema.

### Definição Django
```python
class Cliente(models.Model):
    grupo_economico = models.ForeignKey(GrupoEconomico, on_delete=models.CASCADE)
    vantive_id = models.IntegerField()
    razao_social = models.CharField(max_length=255)
    codigo = models.CharField(max_length=30)
    status = models.BooleanField()
    cnpj = models.CharField(max_length=18)

    class Meta:
        db_table = 'd_cliente'
```

### SQL Equivalente
```sql
CREATE TABLE d_cliente (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grupo_economico_id BIGINT NOT NULL,
    vantive_id INT NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    FOREIGN KEY (grupo_economico_id) REFERENCES d_grupo_economico(id)
);
```

### C# Equivalente
```csharp
public class Cliente
{
    public long Id { get; set; }
    public long GrupoEconomicoId { get; set; }
    public GrupoEconomico GrupoEconomico { get; set; }
    public int VantiveId { get; set; }
    public string RazaoSocial { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Cnpj { get; set; }
}
```

## Model Site
Representa os locais físicos vinculados a um cliente.

### Definição Django
```python
class Site(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = models.CharField(max_length=10)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, null=True, blank=True)
    codigo_sys_cliente = models.CharField(max_length=30)
    codigo_vivo = models.CharField(max_length=30)
    status = models.BooleanField()
    tipo_site = models.CharField(max_length=50)
    tipo_negocio = models.CharField(max_length=50)

    class Meta:
        db_table = 'd_site'
```

### SQL Equivalente
```sql
CREATE TABLE d_site (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cliente_id BIGINT NOT NULL,
    cep VARCHAR(10) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(255),
    codigo_sys_cliente VARCHAR(30) NOT NULL,
    codigo_vivo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    tipo_site VARCHAR(50) NOT NULL,
    tipo_negocio VARCHAR(50) NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES d_cliente(id)
);
```

### C# Equivalente
```csharp
public class Site
{
    public long Id { get; set; }
    public long ClienteId { get; set; }
    public Cliente Cliente { get; set; }
    public string Cep { get; set; }
    public string Numero { get; set; }
    public string? Complemento { get; set; }
    public string CodigoSysCliente { get; set; }
    public string CodigoVivo { get; set; }
    public bool Status { get; set; }
    public string TipoSite { get; set; }
    public string TipoNegocio { get; set; }
}
```

## Model Equipamento
Representa os equipamentos instalados em um site.

### Definição Django
```python
class Equipamento(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    status = models.BooleanField()
    designador = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = "d_equipamento"
```

### SQL Equivalente
```sql
CREATE TABLE d_equipamento (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    site_id BIGINT NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    designador VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    FOREIGN KEY (site_id) REFERENCES d_site(id)
);
```

### C# Equivalente
```csharp
public class Equipamento
{
    public long Id { get; set; }
    public long SiteId { get; set; }
    public Site Site { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Designador { get; set; }
    public string Tipo { get; set; }
}
```

## Model Serviço
Representa os serviços associados a um equipamento.

### Definição Django
```python
class Servico(models.Model):
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=30)
    status = models.BooleanField()
    designador = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)

    class Meta:
        db_table = "d_servico"
```

### SQL Equivalente
```sql
CREATE TABLE d_servico (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    equipamento_id BIGINT NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    designador VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    FOREIGN KEY (equipamento_id) REFERENCES d_equipamento(id)
);
```

### C# Equivalente
```csharp
public class Servico
{
    public long Id { get; set; }
    public long EquipamentoId { get; set; }
    public Equipamento Equipamento { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Designador { get; set; }
    public string Tipo { get; set; }
}
```

## Relacionamentos

A estrutura do inventário segue uma hierarquia onde:

1. Um **Grupo Econômico** pode ter vários **Clientes**
2. Um **Cliente** pode ter vários **Sites**
3. Um **Site** pode ter vários **Equipamentos**
4. Um **Equipamento** pode ter vários **Serviços**

Todos os relacionamentos são do tipo CASCADE, significando que ao deletar um registro pai, todos os registros filhos serão automaticamente removidos.
