# Migrations do Módulo Inventário

## Migration Inicial (0001_initial)

A migration inicial cria a estrutura base do banco de dados para o módulo de inventário.

### Estrutura Criada

1. **Tabela Cliente (d_cliente)**
```sql
CREATE TABLE d_cliente (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    vantive_id INTEGER NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    cnpj VARCHAR(18) NOT NULL
);
```

2. **Tabela Site (d_site)**
```sql
CREATE TABLE d_site (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cep VARCHAR(10) NOT NULL,
    numero VARCHAR(10) NOT NULL,
    complemento VARCHAR(255) NULL,
    codigo_sys_cliente VARCHAR(30) NOT NULL,
    codigo_vivo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    tipo_site VARCHAR(50) NOT NULL,
    tipo_negocio VARCHAR(50) NOT NULL,
    cliente_id BIGINT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES d_cliente(id)
);
```

3. **Tabela Equipamento (d_equipamento)**
```sql
CREATE TABLE d_equipamento (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    designador VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    site_id BIGINT NOT NULL,
    FOREIGN KEY (site_id) REFERENCES d_site(id)
);
```

4. **Tabela Serviço (d_servico)**
```sql
CREATE TABLE d_servico (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(30) NOT NULL,
    status BOOLEAN NOT NULL,
    designador VARCHAR(50) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    equipamento_id BIGINT NOT NULL,
    FOREIGN KEY (equipamento_id) REFERENCES d_equipamento(id)
);
```

5. **Tabela Grupo Econômico (d_grupo_economico)**
```sql
CREATE TABLE d_grupo_economico (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    status BOOLEAN NOT NULL
);
```

### Equivalente C# (Entity Framework)

```csharp
public class InventarioDbContext : DbContext
{
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Cliente>(entity =>
        {
            entity.ToTable("d_cliente");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.VantiveId).IsRequired();
            entity.Property(e => e.RazaoSocial).HasMaxLength(255).IsRequired();
            entity.Property(e => e.Codigo).HasMaxLength(30).IsRequired();
            entity.Property(e => e.Status).IsRequired();
            entity.Property(e => e.Cnpj).HasMaxLength(18).IsRequired();
        });

        modelBuilder.Entity<Site>(entity =>
        {
            entity.ToTable("d_site");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Cep).HasMaxLength(10).IsRequired();
            entity.Property(e => e.Numero).HasMaxLength(10).IsRequired();
            entity.Property(e => e.Complemento).HasMaxLength(255);
            entity.Property(e => e.CodigoSysCliente).HasMaxLength(30).IsRequired();
            entity.Property(e => e.CodigoVivo).HasMaxLength(30).IsRequired();
            entity.Property(e => e.Status).IsRequired();
            entity.Property(e => e.TipoSite).HasMaxLength(50).IsRequired();
            entity.Property(e => e.TipoNegocio).HasMaxLength(50).IsRequired();
            
            entity.HasOne(e => e.Cliente)
                  .WithMany(c => c.Sites)
                  .HasForeignKey(e => e.ClienteId)
                  .OnDelete(DeleteBehavior.Cascade);
        });

        modelBuilder.Entity<GrupoEconomico>(entity =>
        {
            entity.ToTable("d_grupo_economico");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Nome).HasMaxLength(255).IsRequired();
            entity.Property(e => e.Status).IsRequired();
        });

        // Configurações similares para Equipamento e Serviço
    }
}
```

### Processo de Aplicação

1. **Geração da Migration**
```bash
python manage.py makemigrations inventario
```

2. **Aplicação da Migration**
```bash
python manage.py migrate inventario
```

### Reversão (Rollback)

Para reverter esta migration:

```bash
python manage.py migrate inventario zero
```

### Dependências

Esta migration é independente e não possui dependências de outras migrations.

### Considerações

1. **Cascading Deletes**: Todas as foreign keys estão configuradas com CASCADE
2. **Campos Obrigatórios**: Apenas o campo 'complemento' do Site permite NULL
3. **Índices**: Criados automaticamente para as chaves primárias e foreign keys
4. **Convenção de Nomes**: Prefixo 'd_' usado nas tabelas para indicar domínio
