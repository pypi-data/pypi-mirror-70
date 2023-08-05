# **NOCTON**

Nocton é uma extensão que reúne alguns problemas recorrentes nas aplicações django que usam a lógica rest.

Ele foi criado para acelerar o processo de criação de API's utilizando [django-rest-framework](https://github.com/encode/django-rest-framework).


Para utilizá-lo, basta instalá-lo na sua venv através do comando ```pip install nocton```.

Feito isso, é necessário adicioná-lo aos ```INSTALLED_APPS``` no arquivo ```settings.py```. Além disso, crie um dicionário em branco com o nome ```NOCTON``` no mesmo arquivo. É nesse dicionário que as configurações das funcionalidades do nocton serão feitas, conforme será explicado melhor na documentação.

```python
INSTALLED_APPS = [
    ...
    "nocton",
]
...

NOCTON = {

}
```




Segue a documentação das features do nocton:

- [Validação de conta](https://github.com/PauloE314/nocton/blob/master/docs/account_validation.md#Account_Validation)
- [Views genéricas](https://github.com/PauloE314/nocton/blob/master/docs/generic_views.md#Generic+Views)
- [Exceptions](https://github.com/PauloE314/nocton/blob/master/docs/exceptions.md#Exceptions)
- [Permissões](https://github.com/PauloE314/nocton/blob/master/docs/permissions.md#Permissions)
- [Validações de campos para models](https://github.com/PauloE314/nocton/blob/master/docs/validators.md#Validators)
- ["Observador" de arquivos](https://github.com/PauloE314/nocton/blob/master/docs/watchers.md/#Watcher)
- [Ferramentas úteis](https://github.com/PauloE314/nocton/blob/master/docs/tools.md#Tools)
