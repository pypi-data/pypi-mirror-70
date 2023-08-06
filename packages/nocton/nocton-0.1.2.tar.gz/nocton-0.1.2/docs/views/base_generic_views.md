# Base_Generic_Views
#### nocton.generics.views

Nessa página será especificado o funcionamento das classes genéricas bases para as views genéricas reais.

Nocton tem um sistema para facilitar ainda mais as views genéricas que o próprio django_rest_framework provem.
Para obter objetos especificos especificados pela url, é preciso mudar o path no urls.py, então foram criados dois tipos de views, as que retornam objetos são relacionados diretamente com o objeto de referência, e os que se relacionam com objetos que precisam ser especificados na url (ou listas de dados).

As ```SingleRelated_Views``` são views que se relacionam diretamente com o objeto de referência, isto é, através de um OneToOne ou que seja o próprio objeto. Um exemplo clássico seria a manipulação de profiles, com o objeto de referência sendo o user ou o próprio profile.

As ```Views``` são views que não se relacionam diretamente com o objeto de referência, isto é, através de um ManyToMany ou ForeignKeys. O dado requerido pode nem sequer estar relacionado com o objeto de referência, nesses casos, essas views funcionam como as views padrão do django_rest_framework. Essas views podem listar essse conjunto de dados ou, ainda, alterar um dado específico através de um parâmetro da url.

Para o funcionamento das views, algumas classes são usadas como parents delas:

## **Visualizer**

É uma classe com métodos úteis para filtrar campos nas listas ou objetos específicos.

### **Atributos**

#### **exclude_attrs**

Uma lista de campos que devem ser excluídos nas representações. Através de uma estrutura simples de dados, é possível excluir praticamente quaisquer campos específicos. Cada subcampo deve ser um dicionario especifico, não tente colocar dois campos no mesmo dicionario. Talvez funcione, mas não é indicado:

```python
#Não recomendado
exclude_attrs = [
    {
        'profile': 'age',
        'foo': 'bar'
    }
]

#Recomendado
exclude_attrs = [
    {
        'profile': 'age'
    },
    {
        'foo': 'bar'
    }
]

```

### **Métodos**

#### **delete_attrs**
O método que efetivamente vai excluir os campos.
#### 

```python
user = {
    'id': 1,
    'username': 'Exmaple',
    'profile': {
        'age': 20,
        'abbout_me': 'lorem ipsum dolor amet...',
        'proficional_exp': [
            'teacher',
            'driver',
            'cooker'
        ]
    },
}

deleter = Visualizer()
deleter.exclude_attrs = [
    {
        'profile': ['age', 'proficional_exp']
    }
]
```
<hr>

## **Basic_Generic**

Essa classe é a base das views genéricas e possui alguns métodos úteis para a lógica das views.

### **Atributos**

#### reference_object_url_field

Caso esse campo seja especificado, automaticamente a url_param correspondente a esse nome será usada para tentar encontrar o objeto pelo pk

```python
reference_object_url_field = 'user_pk'

#urls.py
...
    path('/users/<user_pk>', MyView.as_view()),
...
```

#### reference_object_model

Especifica o model utilizado para encontrar o objeto de referência. Por padrão, reference_object_model é setado para ser o auth_model especificado no settings.py.

#### reference_object_lookup

Especifica que campo deve ser usado para encontrar o objeto de referência no reference_object_model. Por padrão, procura através de pk.

#### automatic_self_user

Caso esse campo seja ```True```, o objeto de referência será o request.user.

```python
automatic_self_user = True
serializer_class = UserSerializer

>> {
    'id': 1,
    'username': 'Example'
    ...
}
```


#### referenece_object_relation

Atributo que deve especificar a relação do objeto de referência com os dados requeridos, sejam eles um queryset ou algum outro dado a ser utilizado pelas views. Essa string deve ser um atributo do objeto de referência.

```python
...
object_relation = 'profile'
serializer_class = ProfileSerializer

>> {
    'age': 20,
    'about_me': 'lorem ipsum dolor amet...'
}

# Agora a view usaria o atributo profile do objeto de referência (que, no exemplo, é um user)
```

### **Métodos**

#### get_reference_object(*args, **kwargs)
Esse método deve retornar o objeto de referência.

#### get_reference_object_relation(*args, **kwargs)
Esse método deve retornar o/os objeto/objetos que efetivamente serão manipulados pela view. Deve-se ter cuidado com esse campo porque as Generic_View requerem que ele retorne um queryset para executar seus processos, enquanto que as Generic_SingleRelated_Views requerem que retorne um único objeto.

<hr>

## **Generic_View**

A view genérica que se extende todas as views que se relacionam indiretamente com o objeto.

A filosofia dessas views se concentram na ideia de manter o get_object padrão do django_rest. O que será manipulado aqui será o get_queryset, ao invés de retornar o queryset padrão definido na view, é retornado um queryset que será processado com base nas informações previamente fornecidas (ou dinâmicas).
Dessa forma, "pegar" uma informação do queryset continua sendo igual às generic_views do django_rest. (especificando um pk)

O conjunto de dados (queryset) pode, agora, ser um queryset relativo ao objeto de referência, que pode ser o request.user, ou ser um objeto procurado em um model (ver sessão Base_Generic). Para especificar o qual a relação do queryset com o objeto de referência, utiliza-se o campo object_relation e, para casos mais complexos, pode-ser sobrepor o método get_reference_object.

Essa view não tem nenhum método especial, apenas checa se o método ```get_reference_object_relation``` retorna um objeto que pode ser usado como queryset.

- Extende: Base_Generic

Exemplo de como pegar uma música de um cantor específico.
```python
class View(Read_View):
    reference_object_relation = 'musics'

    automatic_self_user = False
    reference_object_url_field = 'singer_pk'
    reference_object_lookup = 'name'
    reference_object_model = SingersModel

    lookup_field = 'music_name' 
    serializer_class = MusicSerializer

#lorem.com/path/<signer_pk>/<music_name>
#lore.com/path/Chester/In_The_End
```
Read_View extende o Base_Generic, mais a frente explicaremos melhor seu uso

<hr>

## **Generic_SingleRelated_View**

Essa view tem uma diferença sutil da outra view base genérica, mas importante. Essa view é para os casos em que não se quer especificar o objeto pela url.

A filosofia dessas views se baseiam em deixar, praticamente, não utilizar o queryset padrão do django_rest. Ao invés de modificar o queryset para poder encontrar um conjunto de dados relacionado, de alguma forma, com um objeto de referência (normalmente um usuário); deve-se, agora, literalmente retornar o objeto desejado, que pode estar relacionado à um objeto de referência ou ser o próprio objeto.

Como anteriormente, o objeto de refência pode ser especificado pelo reference_object_model e reference_object_lookup (por padrão, utiliza o request.user) ou ainda, sobrepor o método get_reference_object.<br>
O campo reference_object_relation agora deve referênciar o objeto desejado em função do objeto de referência. O exemplo clássico é o profile, na extrema maioria das vezes, não se quer especificar o id do profile na url, mas utilizando essas views:

```python
class ProfileView(Read_SingleRelated_View):
    reference_object_relation = 'profile'

    automatic_self_user = False
    reference_object_model = User
    reference_object_url_field = 'pk'
    reference_object_lookup = 'username'

    serializer_class = ProfileSerializer


'''
lorem.com/path/Random_User_Name
>> {
    'age': 18,
    'user': 'Foo',
    ...
}
'''
```

Essas views são feitas para retornar apenas um objeto, caso o ```reference_object_relation``` não seja definido ou seja ```None```, o objeto que será manipulado será o próprio objeto de referência que, por padrão, caso nenhuma informação seja dada, será o próprio request.user.


<hr>


# **Views Básicas**
Essas views são as peças simples que representam o CRUD das aplicações

## **Retrieve**

Utilizado para ler um único elemeno. Basicamente herda as mesmas propriedades do RetrieveAPIView padrão, mas aplica o método delete_attrs no objeto visualizado.

- Métodos: GET
- Extende: Vizualiser, RetrieveAPIView

<hr>

## **Update**

Utilizado para dar um update inteiro ou parcial de um único elemento.

### **Atributos**

#### **always_partial**

Um campo booleando que torna todos os updates parcial, mesmo no PUT.

- Métodos: PUT, PATCH
- Extende: UpdateAPIView

<hr>

## **Delete**

Utilizado para deletar um único elemento.

- Extende: DestroyAPIView

<hr>


## **List**

Essa classe trás métodos fundamentais para o gerenciamento de listas

- Extende: Visualizer, Generic_View, List_API_View

Embora extenda a classe Visualizer, caso o sistema de paginação esteja ativo, o filtro não é aplicado, sendo necessário fazê-lo manualmente. O método ```delete_attrs``` pode ser usado muito bem para esse fim.


### **Atributos**

#### **searching**
Uma lista de campos que serão usados para filtrar os query_params do request.
Cada item da lista pode ser uma string ou um dicionário. 
<br>Caso seja uma string, será filtrado por padrão como o nome do campo e do queryparam, além disso, por padrão, a terminação dos filtros é ```i_contains```.
<br>Caso seja um dicionario, é possível especificar o nome do queryparam, o nome real que será filtrado e a terminação escolhida.

```python
class Users(List_View):
    queryset = user.object.all()
    serializer_class = user_serializer

    searching = [
        'username',
        {
            'field_name': 'profile__age',
            'search_name': "age",
            'endding': 'exactly' 
        }
    ]
    #foo.com/path/?username=Example&age=20
```

No caso acima, o campo de pesquisa na url seja **age**, no campo real, será pesquisado **profile__age** que é uma forma padrão do django de pesquisar campos de relacionamentos de bancos de dados.


#### **order**

Uma lista de campos que serão usados para a ordenação padrão dos objetos pesquisado.
<br> Por padrão, ordena por ```-pk```.

```python
#...
    order = ['username', 'profile__age']
```

### **Métodos**


#### <b>search(*args, queryset=default_queryset, **kwargs)</b>

Esse método implementa a pesquisa propriamente dita e retorna um queryset que será ordenado em seguida.

#### <b>ordernate(*args, queryset=searched_queryset, **kwargs)</b>

Esse método é responsável por ordenar o queryset depois de pesquisado e retornar o queryset.

