# 🛒 Sistema de Vendas

O **Sistema de Vendas** é uma aplicação web desenvolvida com o framework Django, projetada para auxiliar no controle e gestão de vendas, produtos e categorias.

O projeto também foi configurado como **Progressive Web App (PWA)**, permitindo que seja instalado em dispositivos móveis ou desktops e utilizado com suporte básico offline.

## 🎯 Objetivo
Oferecer uma plataforma simples e funcional para:

- Controle de produtos
- Gerenciamento de categorias
- Registro de vendas
- Controle de vendas fiado
- Visualização de dados no dashboard

Ideal para pequenos comércios ou uso pessoal.

## 🚀 Funcionalidades
- 📊 Dashboard com visão geral do sistema
- 📦 Cadastro e gerenciamento de produtos
- 🏷️ Organização por categorias
- 🛒 Registro de vendas
- 💳 Controle de vendas fiado
- 📱 Instalável como aplicativo (PWA)
- 🌐 Página offline (`offline.html`)
- 🔐 Sistema de autenticação de usuários

## Funcionalidades futuras

### 📦 Fornecedor
Permite registrar de quem você compra os produtos. Exemplo:
- Distribuidora ABC
- Mercado Atacado XYZ

> Saber quem fornece cada produto.


### 💰 Preço de custo
Valor que você pagou pelo produto.

| Produto   | Custo   | Venda    |
| --------- | ------- | -------- |
| Coca-Cola | R$ 6,00 | R$ 10,00 |

> Saber quanto realmente lucra.


### 🛒 Registro de compras
Cadastro das compras feitas aos fornecedores.

```
Fornecedor: ABC

10 Coca-Cola
20 Fanta

Total: R$ 300
```

> Histórico de reposições e gastos.


### 📥 Entrada automática no estoque
Quando uma compra é registrada, o estoque aumenta sozinho.

```
Èstoque atual:
Coca-Cola: 5

Compra:
+20 Coca-Cola

Novo estoque:
25
```

> Evita atualizar estoque manualmente.


### 📊 Relatórios de lucro
Mostra quanto foi vendido e quanto foi lucrado.

```
Receita: R$ 5.000
Custos:  R$ 3.000

Lucro:   R$ 2.000
```

> Saber se o negócio está realmente dando retorno.


### 🔔 Alertas de reposição
Verifica produtos abaixo do estoque mínimo.

```
Coca-Cola
Estoque atual: 2
Mínimo: 5
```

Exibe um alerta no dashboard.

> Evitar ficar sem produtos para vender.

### Prioridade
- Fornecedor
- Preço de custo
- Alertas de reposição
<!-- - Registro de compras
- Entrada automática no estoque
- Relatórios de lucro -->

## 🛠️ Tecnologias Utilizadas
- Django
- Bootstrap 5
- Bootstrap Icons
- django-pwa
- HTML5 + CSS3 + JavaScript

HTML5 + CSS3 + JavaScript

## 💻 Pré-requisitos

- Python 3.x  
- Django >= 4.0  
- Navegador moderno (Chrome, Edge, Firefox ou Safari)  

## 🛠️ Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/hick-hpe/webapp-sistema-vendas.git
    cd webapp-sistema-vendas
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

Abra o navegador em [http://localhost:8000/](http://localhost:8000/) para testar.

## 🌐 Servidor Online

O site está disponível em:  
[https://webapp-sistema-vendas.vercel.app/](https://webapp-sistema-vendas.vercel.app/)
