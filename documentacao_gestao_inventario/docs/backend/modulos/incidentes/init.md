# Inicialização do Módulo Incidentes

## Arquivos __init__.py

Os arquivos `__init__.py` no Python são similares aos `namespace` em C#. Eles marcam um diretório como um pacote Python.

### Estrutura

```
incidentes/
├── __init__.py                  # Marca o módulo principal
├── api/
│   ├── __init__.py             # Inicialização da API
│   ├── serializers/
│   │   └── __init__.py         # Exporta serializers
│   └── view/
│       └── __init__.py         # Exporta views
└── models/
    └── __init__.py             # Exporta models
```

### Implementação

#### Models __init__.py
```python
from .incidente import Incidente

__all__ = ['Incidente']
```

#### Equivalente em C# (conceitual)
```csharp
namespace Incidentes.Models
{
    public class Incidente { }
}
```

## Registro do App

### Django (apps.py)
```python
from django.apps import AppConfig

class IncidentesConfig(AppConfig):
    name = 'incidentes'
```

### Equivalente em C# (Startup.cs)
```csharp
public void ConfigureServices(IServiceCollection services)
{
    services.AddDbContext<IncidentesContext>();
    services.AddScoped<IIncidenteService, IncidenteService>();
}
```

## Inicialização Automática

### Django (settings.py)
```python
INSTALLED_APPS = [
    # ...
    'incidentes',
]
```

### C# (Program.cs ou Startup.cs)
```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers()
    .AddApplicationPart(typeof(IncidentesController).Assembly);
```

## Diferenças Principais

1. **Organização de Módulos**
   - Python: Usa `__init__.py` para marcar pacotes
   - C#: Usa namespaces e assembly references

2. **Registro de Componentes**
   - Django: Lista em INSTALLED_APPS
   - C#: Registro via DI container

3. **Importação**
   - Python: `from module import Class`
   - C#: `using Namespace;`
