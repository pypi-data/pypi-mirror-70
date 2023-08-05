# Generic_Views
#### nocton.generics.views

Essa página explica o funcionamento das views genéricas simples e compostas.

Assim como as views genéricas do django_rest_framework, existem as views simples e as complexas que simplesmente extendem as propriedades das views simples de forma unida.

## **Generic_Views**

### **List_View:**


- Métodos: GET
- Extende: List

<hr>

### **List_Create_View:**

- Métodos: GET, POST
- Extende: List, ListCreateAPIView

<hr>

### **Read_View:**

- Métodos: GET
- Extende: Generic_View, Retreive

<hr>


### **Update_View:**

- Métodos: PUT, PATCH
- Extende: Generic_View, Retreive

<hr>

### **Delete_View:**

- Métodos: DELETE
- Extende: Generic_View, Delete

<hr>

### **Read_Update_View**
- Métodos: GET, PUT, PATCH
- Extende: Read_View, Update_View

<hr>

### **Read_Delete_View**
- Métodos: GET, DELETE
- Extende: Read_View, Delete_View

<hr>

### **Update_Delete_View**
- Métodos: GET, DELETE
- Extende: Read_View, Delete_View

<hr>

### **Read_Update_Delete_View**
- Métodos: GET, PUT, PATCH, DELETE
- Extende: Read_View, Update_View, Delete_View


<hr><hr>

## **Generic_SingleRelated_Views**


### **Read_SingleRelated__View:**
- Métodos: GET
- Extende: Generic_SingleRelated_View, Retreive

<hr>


### **Update_SingleRelated_View:**

- Métodos: PUT, PATCH
- Extende: Generic_View, Retreive

<hr>

### **Delete_SingleRelated_View:**

- Métodos: DELETE
- Extende: Generic_SingleRelated_View, Delete

<hr>

### **Read_Update_SingleRelated_View**
- Métodos: GET, PUT, PATCH
- Extende: Read_SingleRelated_View, Update_SingleRelated_View

<hr>

### **Read_Delete_SingleRelated_View**
- Métodos: GET, DELETE
- Extende: Read_SingleRelated_View, Delete_SingleRelated_View

<hr>

### **Update_Delete_SingleRelated_View**
- Métodos: GET, DELETE
- Extende: Read_SingleRelated_View, Delete_SingleRelated_View

<hr>

### **Read_Update_Delete_SingleRelated_View**
- Métodos: GET, PUT, PATCH, DELETE
- Extende: Read_SingleRelated_View, Update_SingleRelated_View, Delete_SingleRelated_View