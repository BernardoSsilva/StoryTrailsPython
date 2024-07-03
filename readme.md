# Sobre o projeto

### Objetivo
O projeto StoryTrails foi um projeto de finalização de conteúdo para o primeiro semestre da matéria de programação para engenharia, no curso de engenharia da computação da universidade Unisatc

### Sinopse do projeto
O projeto visa ser um sistema de organizazção de leitura anual, onde o usuário poderá realizar o registro de livros, separando-os por coleções especificas, cada uma com seus objetivos especificos
O repositório em questão foi criado para armazenar o backend do projeto, desenvolvido em django.

### Conceitos aplicados

- API Rest
- Backend

## Tecnologias utilizadas

<img src="https://skillicons.dev/icons?i=git,py,django,postgres" />

# Instalação e Execução do Projeto

## Instalação

Para ter o código disponível em sua máquina, utilize o seguinte comando:

```bash
$ git clone https://github.com/BernardoSsilva/StoryTrails_backEnd.git
```

### Criando um Ambiente Virtual

Após clonar o repositório, crie um ambiente virtual Python dentro do projeto:

#### Windows

```bash
$ py -m venv venv
```

#### Linux

```bash
$ python3 -m venv venv
```

### Ativando o Ambiente Virtual

#### Windows

```bash
$ venv\Scripts\activate.bat
```

#### Linux

```bash
$ source venv/bin/activate
```

### Instalando Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:

```bash
(venv) $ pip install -r requirements.txt
```

## Execução do Projeto

Para executar o projeto, utilize o comando adequado ao seu sistema operacional:

### Windows

```bash
(venv) $ py manage.py runserver
```

### Linux

```bash
(venv) $ python3 manage.py runserver
```

Após isso, a API estará em funcionamento na porta `8000`. Você pode acessá-la no endereço `http://localhost:8000`.

### Acesso ao Perfil de Administrador

Para criar uma conta de superusuário e acessar o painel de administração, utilize o comando:

```bash
(venv) $ py manage.py createsuperuser
```

Depois de criar sua conta, acesse o painel de administração no link `http://localhost:8000/admin`.

## Resumo de Comandos

### Clonar o Repositório

```bash
$ git clone https://github.com/BernardoSsilva/StoryTrails_backEnd.git
```

### Criar e Ativar o Ambiente Virtual

#### Windows

```bash
$ py -m venv venv
$ venv\Scripts\activate.bat
```

#### Linux

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

### Instalar Dependências

```bash
(venv) $ pip install -r requirements.txt
```

### Executar o Servidor

#### Windows

```bash
(venv) $ py manage.py runserver
```

#### Linux

```bash
(venv) $ python3 manage.py runserver
```

### Criar Superusuário

```bash
(venv) $ py manage.py createsuperuser
```

Com esses passos, você estará pronto para desenvolver e testar o projeto StoryTrails BackEnd.
