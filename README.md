## Шаблон для приложения на FastAPI.

Для создания ключей необходимо выполнить следующие команды в каталоге, в котором должны находиться сертификаты:

```shell
openssl genrsa -out jwt-private.pem 2048
```

```shell
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
