# Tools
#### nocton.tools

O Nocton tem algumas ferramentas que podem vir a ser úteis em alguns momentos.

### **print_f(\*texts, destac=True, remain=False lenght=50, separator='\n')**

Essa é uma forma de printar com mais destaque, nela é possível definir a largura da mensagem, se quer que ela seja destacada ou não e qual o separador entre os textos.

```python
print_f('Teste1', 'Teste2')

'''
=============================
            Teste1
            Teste2
=============================
'''
```
Nocton usa esse print para quase tudo. É possível desabilitar esse print pelo settings.py:

```python
NOCTON = {
    ...
    "alerts": False
}
```

Caso ```destac=False```, as barras nãos serão printadas. Caso ```remain=True```, o print não será ignorado mesmo com ```"alerts": False``` nas configurações de nocton

### **has_field(model, field_name)**

Checa se um model tem um campo ou não (booleano)

### **in_objects(instance, model)**

Checa se uma instancia está presente em um model.

### **check_related(model, field_name)**

Checa se o campo é o nome reverso de algum relacionamento de models (OneToOne, etc).


### **delete_from_dict(dict_delete, structure)**

É a função utilizada para filtrar os campos nas Generic_Views; com ela, é possível retirar itens de dentro de dicionários.
```python
my_dict = {
    'foo': {
        'key_1': 'item_1',
        'key_2': 'item_2'
    },
    'bar': 'item_3'
}

del_structure = [
    {'foo': 'key_1'}
]

delete_from_dict(my_dict, del_structure)
>> {
    'foo': {
        'key_2': 'item_2'
    },
    'bar': 'item_3'
}

```