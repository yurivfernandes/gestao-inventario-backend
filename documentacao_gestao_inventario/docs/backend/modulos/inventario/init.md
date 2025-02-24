# Inicialização do Módulo de Inventário

O módulo de inventário utiliza um arquivo `__init__.py` para exportar seus modelos e componentes principais, facilitando a importação em outras partes do sistema.

## Estrutura do __init__.py

### Models

O arquivo `models/__init__.py` exporta os seguintes modelos:

```python
from .cliente import Cliente
from .equipamento import Equipamento
from .servico import Servico
from .site import Site
```

### Views

O arquivo `api/view/__init__.py` exporta as views:

```python
from .cliente import ClienteListCreate, ClienteUpdate
from .equipamento import EquipamentoListCreate, EquipamentoUpdate
from .servico import ServicoListCreate, ServicoUpdate
from .site import SiteListCreate, SiteUpdate
```

### Serializers

O arquivo `api/serializers/__init__.py` exporta os serializers:

```python
from .cliente_serializer import ClienteSerializer
from .equipamento_serializer import EquipamentoSerializer
from .servico_serializer import ServicoSerializer
from .site_serializer import SiteSerializer
```

## Uso

Para importar os componentes em outras partes do projeto, utilize:

```python
from inventario.models import Cliente, Equipamento, Servico, Site
from inventario.api.view import ClienteListCreate, ClienteUpdate
from inventario.api.serializers import ClienteSerializer
```

Esta estrutura de inicialização permite uma organização clara e facilita a manutenção do código.
