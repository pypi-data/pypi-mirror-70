# Watcher

Nocton oference uma solução simples para um tornar os arquivos executáveis no django. Por padrão, apenas alguns arquivos em específico são executado 100% das vezes, para poder extender esses arquivos, basta adicionar o caminho do arquivo desejado no dicionário ```NOCTON``` presente no ```settings.py``` (caso não exista ainda, é bom criar ;).

```python
#settings.py

...
NOCTON = {
    ...
    "watch": [
        'my_app.singals',
        'my_app.tests.startup_tests'
    ]

}

```