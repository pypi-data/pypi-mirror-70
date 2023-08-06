# Account_Validation

Nocton oferece um sistema simples de validação de conta (pensado para validação de email). Para utilizá-lo, será necessário adicionar ```app nocton.account_validation``` aos ```INSTALLED_APPS``` e adicionar os migrations.

<small>O app account_validation já vem com model de ActivationToken</small>

Também será necessário adicionar algumas configurações básicas no dicionário ```NOCTON``` no settings.py

```python
NOCTON = {
    ...
    'account_validation': {
        'active_by_default': True,
        'backends': [
            'nocton.account_validation.generic_backend.DesactiveUser'
            'my_app.handling_new_users.SendValidationEmail'
            ...
        ]
    }
}
```

#### active_by_default

Se esse campo for ```True```, toda vez que um novo usuário for criado, sua conta já será desativada e um token de ativação será gerado.

#### backends

Uma lista de instruções que devem ser executadas todas as vezes que um usuário for ativado ou desativado. Para isso, é provida uma classe chamada ```BasicBackend``` que vive em ```nocton.account_validation.backends```; essa  classe possui dois métodos: ```activating``` e ```deactivating```, um para cada caso. Deve-se passar o caminho e o nome da classe para dentro da lista.


### **Como funciona**

Toda vez que um token de ativação for criado, os backends serão executados tentando desativar a conta. Quando esse token for deletado, os backends serão novamente executados tentando ativar a conta.

<small>OBS: o sistema nocton não desativa a conta por padrão, mesmo que ```active_by_default``` estiver setado para ```True```.</small>

Para facilitar esse processo existe o campo ```active_by_default``` que automatiza o processo de criar o token. Além disso, o app ```nocton.account_validation``` possui uma class_based_view (```nocton.account_validation.views```) chamada ```ValidateAccount``` feita para a validação de conta.

```python
# myproject.urls.py
from nocton.account_validation.views import ValidateAccount

urlpatterns = [
    ...
    path('active-account', ValidateAccount.as_view()),
]
```

Essa view aceita apenas o método ```POST```, basta enviar o token de ativação.

```json
{
    "activation_token": "asdasd15s",
}
...
{
    "user_pk": 1,
    "username": "MyUser"
}
```

Essa view deleta o token de ativação.

### **AccountValidatorToken**
#### nocton.account_validation.models

É o model usado para validação de conta. Ele vivem em ```nocton.account_validation.models``` e, além das propriedades enfatizadas antes, possui o método chamado ```refresh_token``` que muda a key de um token aleatóriamente.