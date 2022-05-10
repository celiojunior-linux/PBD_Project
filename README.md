# PBD_Project (Preciso Atualizar)

##Sobre
- O projeto foi desenvolvido utilizando  o framework _Django_;
- Optei por utilizar postgresql como banco de dados, pois o django dá melhor suporte.


## Ajustes Iniciais
Para fazer a instalação do sistema em sua máquina local, recomendo que esteja executando o python na versão 3.8 ou superior.
- Dentro da pasta do projeto, crie um ambiente virtual e ative-o.
```shell
$ python -m venv venv
```
- Ativação no windows:
```shell
$ venv\Scripts\activate
```
- Ativação em sistemas baseados em _Unix_:
````shell
$ source venv/bin/activate 
````
- Instale os requisitos do projeto:
```shell
$ pip install -r requirements.txt 
```


## Configurações

[Opcional]

O ORM do _Django_ é compatível com _MySQL_, e pode ser configurado da seguinte forma:

- 1º - Instale o _MySQL_ da forma que preferir:
  - Site Oficial: https://www.mysql.com/
  - XAMPP: https://www.apachefriends.org/pt_br/download.html
  

- 3º Instale o driver do _MySQL_ para o _Django_:
```shell
$ pip install mysqlclient
```

- 4º - Após configurar o servidor _MySQL_, crie um novo database:
```mysql
CREATE DATABASE aml_db;
```


- 5º - Crie um novo usuário:
```mysql
CREATE USER 'aml_dbadmin'@'localhost' IDENTIFIED BY 'secret123';
```


- 6º - Defina alguns privilégios administrativos para o usuário:
```mysql
GRANT ALL PRIVILEGES ON `aml_db` . * TO 'aml_dbadmin'@'localhost';
FLUSH PRIVILEGES; 
```


- 7º - Localize a variável "DATABASES" no arquivo settings.py do projeto
```python
# Arquivo: aml_ltda/settings.py (antes)
...
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}
...
```


- 8º - Altere a engine de para executar com o _MySQL_:
  - É recomendado usar um arquivo .env para guardar as invormações sensíveis do projeto em variáveis de ambiente, para tanto, acompanhe o tutorial
  a seguir e entenda sobre: https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f
```python
# Arquivo: aml_ltda/settings.py (depois)
...
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}
...
```


- 9º - Rode as migrations para criar as tabelas no banco de dados.
```shell
$ # Criação de tabelas
$ python manage.py makemigrations
$ python manage.py migrate
```


- 10º carregue os registros no projeto a partir do arquivo "dump.json" na pasta raíz:
```shell
$ python manage.py loaddata dump.json
```


- 11º - Execute o servidor local:
```
$ python manage.py runserver
```

- Pronto, o servidor _Django_ agora está executando com seu banco de dados _MySQL_, seja feliz.
(O processo de configuração do _PostgreSQL_ é bem similar, com exceção das configurações do driver, portanto
não irei detalhá-lo aqui).
---

### Notas para o professor:
- Na pasta do projeto eu incluí um arquivo .env com as configurações que utilizei no database, além das chaves para configurar o recaptcha.
Caso não seja possível utilizar o recaptcha, para removê-lo, vá até apps/authentication/views.py e substitua a variável form_class para "AuthenticationForm" (sem as aspas).


- Antes
```python
...
class AMLLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = AMLAuthenticationForm # Substituir aqui

    def form_valid(self, form):
        employee = authenticate(
            self.request,
            username=self.request.POST["username"],
            password=self.request.POST["password"],
        )
        login(self.request, employee, "apps.authentication.backends.EmployeeBackend")
        messages.success(self.request, "Login efetuado com sucesso!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(self.request, "CPF ou senha inválidos!")
        return super(AMLLoginView, self).form_invalid(form)
```


- Depois
```python
from django.contrib.auth.views import AuthenticationForm # Importar o formulário de autenticação padrão do django

class AMLLoginView(LoginView):
    template_name = "auth/login.html"
    form_class = AuthenticationForm

    def form_valid(self, form):
        employee = authenticate(
            self.request,
            username=self.request.POST["username"],
            password=self.request.POST["password"],
        )
        login(self.request, employee, "apps.authentication.backends.EmployeeBackend")
        messages.success(self.request, "Login efetuado com sucesso!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(self.request, "CPF ou senha inválidos!")
        return super(AMLLoginView, self).form_invalid(form)
```
