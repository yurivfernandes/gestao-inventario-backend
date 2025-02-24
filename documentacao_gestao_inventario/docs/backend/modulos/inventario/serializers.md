# Serializers do Módulo Inventário

## ClienteSerializer

Responsável pela serialização do modelo Cliente.

```python
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"
```
 
### Equivalente C#
```csharp
public class ClienteDto
{
    public long Id { get; set; }
    public int VantiveId { get; set; }
    public string RazaoSocial { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Cnpj { get; set; }
}

public class ClienteProfile : Profile
{
    public ClienteProfile()
    {
        CreateMap<Cliente, ClienteDto>();
        CreateMap<ClienteDto, Cliente>();
    }
}
```

## SiteSerializer

Responsável pela serialização do modelo Site.

```python
class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = "__all__"
```

### Equivalente C#
```csharp
public class SiteDto
{
    public long Id { get; set; }
    public long ClienteId { get; set; }
    public string Cep { get; set; }
    public string Numero { get; set; }
    public string Complemento { get; set; }
    public string CodigoSysCliente { get; set; }
    public string CodigoVivo { get; set; }
    public bool Status { get; set; }
    public string TipoSite { get; set; }
    public string TipoNegocio { get; set; }
}

public class SiteProfile : Profile
{
    public SiteProfile()
    {
        CreateMap<Site, SiteDto>();
        CreateMap<SiteDto, Site>();
    }
}
```

## EquipamentoSerializer

Responsável pela serialização do modelo Equipamento, incluindo dados relacionados do Site.

```python
class EquipamentoSerializer(serializers.ModelSerializer):
    site_codigo_vivo = serializers.CharField(
        source="site.codigo_vivo", 
        read_only=True
    )

    class Meta:
        model = Equipamento
        fields = [
            "id", "site", "codigo", "status",
            "designador", "tipo", "site_codigo_vivo"
        ]
```

### Equivalente C#
```csharp
public class EquipamentoDto
{
    public long Id { get; set; }
    public long SiteId { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Designador { get; set; }
    public string Tipo { get; set; }
    public string SiteCodigoVivo { get; set; }
}

public class EquipamentoProfile : Profile
{
    public EquipamentoProfile()
    {
        CreateMap<Equipamento, EquipamentoDto>()
            .ForMember(dest => dest.SiteCodigoVivo, 
                      opt => opt.MapFrom(src => src.Site.CodigoVivo));
    }
}
```

## ServicoSerializer

Responsável pela serialização do modelo Serviço, incluindo dados relacionados do Equipamento e Site.

```python
class ServicoSerializer(serializers.ModelSerializer):
    equipamento_codigo = serializers.CharField(
        source="equipamento.codigo",
        read_only=True
    )
    site_codigo_vivo = serializers.CharField(
        source="equipamento.site.codigo_vivo",
        read_only=True
    )

    class Meta:
        model = Servico
        fields = [
            "id", "equipamento", "codigo", "status",
            "designador", "tipo", "equipamento_codigo",
            "site_codigo_vivo"
        ]
```

### Equivalente C#
```csharp
public class ServicoDto
{
    public long Id { get; set; }
    public long EquipamentoId { get; set; }
    public string Codigo { get; set; }
    public bool Status { get; set; }
    public string Designador { get; set; }
    public string Tipo { get; set; }
    public string EquipamentoCodigo { get; set; }
    public string SiteCodigoVivo { get; set; }
}

public class ServicoProfile : Profile
{
    public ServicoProfile()
    {
        CreateMap<Servico, ServicoDto>()
            .ForMember(dest => dest.EquipamentoCodigo, 
                      opt => opt.MapFrom(src => src.Equipamento.Codigo))
            .ForMember(dest => dest.SiteCodigoVivo, 
                      opt => opt.MapFrom(src => src.Equipamento.Site.CodigoVivo));
    }
}
```

## Características Principais

1. **Serialização Automática**
   - Uso do ModelSerializer para mapeamento automático
   - Campos relacionados são incluídos quando necessário
   
2. **Campos Somente Leitura**
   - Campos calculados são marcados como read_only
   - Dados relacionados são expostos de forma segura

3. **Validação Integrada**
   - Validação automática baseada no modelo
   - Relacionamentos são validados automaticamente

4. **Aninhamento de Dados**
   - Acesso a dados de modelos relacionados
   - Campos calculados baseados em relacionamentos
