# Permissions
#### nocton.generics.permissions

### **CheckAuth**

Checa se as redenciais (username e senha) estão presentes no request.data, e, claro, checa se o usuário que as enviou é o mesmo das credenciais.

```json
{
    "authorization": {
        "username": "lorem",
        "password": "ipsum"
    }
    ...
}
```