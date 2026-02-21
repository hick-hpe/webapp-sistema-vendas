# Criando um PWA com Django

Este projeto é um exemplo de **Progressive Web App (PWA)** usando o **framework Django**.  
O objetivo é mostrar como transformar um site Django em um app instalável com funcionalidades básicas offline.

## 🎯 Funcionalidades

- Páginas instaláveis como aplicativo no celular ou desktop  
- Funciona offline com uma página de fallback (`offline.html`)  
- Estrutura simples para testes e aprendizado  
- Suporte a ícones e splash screens (configurado via `django-pwa`)  

## 💻 Pré-requisitos

- Python 3.x  
- Django >= 4.0  
- Navegador moderno (Chrome, Edge, Firefox ou Safari)  

## 🛠️ Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/hick-hpe/django-pwa-teste.git
    cd django-pwa-teste
    ```

2. Crie e ative um ambiente virtual:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux / Mac
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    # Windows
    pip install -r requirements.txt

    # Linux / Mac
    pip3 install -r requirements.txt
    ```

4. Rode o servidor:
    ```bash
    python manage.py runserver
    ```

Abra o navegador em [http://127.0.0.1:8000/](http://127.0.0.1:8000/) para testar.

## 🌐 Servidor Online

O site está disponível em:  
[https://palermo.pythonanywhere.com/](https://palermo.pythonanywhere.com/)