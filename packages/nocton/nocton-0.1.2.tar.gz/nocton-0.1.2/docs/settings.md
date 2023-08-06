# Settings
#### nocton.setup

Nocton possibilita pegar as configurações do próprio nocton de forma mais simples.

### **load_nocton()**

Tenta carregar as configurações do nocton (o dicionário no settings.py). Caso consiga carregar, retorna o dicionário.

### **load_setting(setting, default=None)**

Tenta carregar alguma configuração principal do nocton, caso não consiga, retorna default.

### **load_watch_settings(default=None)**

Tenta carregar as configurações de watch do nocton, caso não consiga, retorna default.

### **load_account_validation_settings(default=None)**

Tenta carregar as configurações de account_validation do nocton, caso não consiga, retorna default