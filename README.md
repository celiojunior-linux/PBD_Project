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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : 'db.sqlite3',
    }
}
...
```


- 8º - Configurar para conectar ao banco de dados _MySQL_:
  - É recomendado usar um arquivo .env para guardar as invormações sensíveis do projeto em variáveis de ambiente, para tanto, acompanhe o tutorial
  a seguir e entenda sobre: https://alicecampkin.medium.com/how-to-set-up-environment-variables-in-django-f3c4db78c55f
```python
# Arquivo: aml_ltda/settings.py (depois)
...
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'aml_db',
        'USER'    : 'aml_dbadmin',  
        'PASSWORD': 'secret123',
        'HOST'    : 'localhost',
        'PORT'    : '3306',
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
