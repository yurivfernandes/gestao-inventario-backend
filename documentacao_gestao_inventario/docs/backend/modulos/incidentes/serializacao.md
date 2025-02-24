# Serialização de Incidentes

## Implementação Django
Usamos serializers do DRF para converter modelos em JSON.

```python
class IncidenteSerializer(serializers.ModelSerializer):
    data_abertura = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    
    class Meta:
        model = Incidente
        fields = "__all__"
```

## Equivalente em C#

### DTO
```csharp
public class IncidenteDTO
{
    public string AbertoPor { get; set; }
    public string Categoria { get; set; }
    public string CodigoEquipamento { get; set; }
    public string CodigoServico { get; set; }
    
    [JsonConverter(typeof(CustomDateTimeConverter))]
    public DateTime DataAbertura { get; set; }
    
    [JsonConverter(typeof(CustomDateTimeConverter))]
    public DateTime? DataFechamento { get; set; }
    
    // ... outros campos ...
}

public class CustomDateTimeConverter : JsonConverter<DateTime>
{
    public override DateTime Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        return DateTime.Parse(reader.GetString());
    }

    public override void Write(Utf8JsonWriter writer, DateTime value, JsonSerializerOptions options)
    {
        writer.WriteStringValue(value.ToString("yyyy-MM-dd HH:mm:ss"));
    }
}
```

### AutoMapper (opcional)
```csharp
public class IncidenteMappingProfile : Profile
{
    public IncidenteMappingProfile()
    {
        CreateMap<Incidente, IncidenteDTO>();
        CreateMap<IncidenteDTO, Incidente>();
    }
}
```

## Principais Diferenças

1. **Serialização**
   - Django: Automática via ModelSerializer
   - C#: DTOs + JsonConverter ou AutoMapper

2. **Formatação de Data**
   - Django: Definido no serializer
   - C#: JsonConverter customizado

3. **Campos**
   - Django: Todos os campos via `fields = "__all__"`
   - C#: Precisa definir explicitamente

4. **Validação**
   - Django: Integrada no serializer
   - C#: DataAnnotations ou FluentValidation
