from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm, ProdutoForm
from .models import Categoria, Estoque, Produto, Venda, ItemVenda, VendaFiada
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta, timedelta


# #######################################################################
#                           AUTENTICACAO
# #######################################################################
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario_obj = User.objects.get(email=email)
            username = usuario_obj.username
        except User.DoesNotExist:
            messages.error(request, 'Email ou senha inválidos.')
            return render(request, 'login.html')

        # autenticação
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'login.html')

# #######################################################################
#                              OFFLINE
# #######################################################################
def offline_view(request):
    return render(request, "offline.html")

# #######################################################################
#                              DASHBOARD
# #######################################################################
@login_required(login_url='/')
def dashboard_view(request):
    return render(request, "dashboard.html")


# #######################################################################
#                               CATEGORIAS
# #######################################################################

# categorias: GET/POST
@login_required(login_url='/')
def categorias_view(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = request.user
            categoria.save()
            return redirect('categorias')
    else:
        form = CategoriaForm()

    # Busca apenas categorias do usuário logado
    categorias = Categoria.objects.filter(user=request.user)

    buscar = request.GET.get('buscar')

    categorias = Categoria.objects.filter(user=request.user)

    if buscar:
        categorias = categorias.filter(nome__icontains=buscar)

    context = {
        'categorias': categorias,
        'form': form
    }
    return render(request, "categorias.html", context)


# categorias: PUT
@login_required(login_url='/')
def categorias_editar_view(request, id):
    categoria = get_object_or_404(Categoria, id=id, user=request.user)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.user = request.user
            categoria.save()
            return redirect('categorias_editar', id=categoria.id)
    else:
        form = CategoriaForm(instance=categoria)
        
    categorias = Categoria.objects.filter(user=request.user)

    context = {
        'categorias': categorias,
        'form': form,
        'categoria': categoria
    }
    return render(request, "categorias_editar.html", context)


# categorias: DELETE
@login_required(login_url='/')
def categorias_excluir_view(request, id):
    categoria = get_object_or_404(Categoria, id=id, user=request.user)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')
    return redirect('categorias')


# #######################################################################
#                               PRODUTOS
# #######################################################################
# produtos: GET/POST
@login_required(login_url='/')
def produtos_view(request):

    if request.method == 'POST':
        form = ProdutoForm(request.user, request.POST)

        if form.is_valid():
            produto = form.save(commit=False)
            produto.user = request.user
            produto.save()

            estoque_qtd = request.POST.get('estoque')
            estoque_obj = Estoque.objects.create(
                produto=produto,
                quantidade=estoque_qtd
            )
            return redirect('produtos')
    else:
        form = ProdutoForm(request.user)

    produtos = Produto.objects.filter(user=request.user)

    buscar = request.GET.get('buscar')
    categoria = request.GET.get('categoria')

    if buscar:
        produtos = produtos.filter(nome__icontains=buscar)

    if categoria:
        produtos = produtos.filter(categoria_id=categoria)
        
    context = {
        'produtos': produtos,
        'categorias': Categoria.objects.filter(user=request.user),
        'form': form,
    }
    return render(request, "produtos.html", context)


# produtos: PUT
@login_required(login_url='/')
def produtos_editar_view(request, id):
    produto = get_object_or_404(Produto, id=id, user=request.user)

    if request.method == 'POST':
        form = ProdutoForm(request.user, request.POST, instance=produto)
        if form.is_valid():
            produto = form.save(commit=False)
            produto.user = request.user
            produto.save()

            Estoque.objects.update_or_create(
                produto=produto,
                defaults={'quantidade': form.cleaned_data['estoque']}
            )
            
            return redirect('produtos')
    else:
        estoque_obj = getattr(produto, 'estoque', None)

        form = ProdutoForm(
            request.user,
            instance=produto,
            initial={
                'estoque': estoque_obj.quantidade if estoque_obj else 0
            }
        )

    context = {
        'produtos': Produto.objects.filter(user=request.user),
        'categorias': Categoria.objects.filter(user=request.user),
        'form': form,
        'produto': produto
    }
    return render(request, "produtos_editar.html", context)

# produtos: DELETE
@login_required(login_url='/')
def produtos_excluir_view(request, id):
    produto = get_object_or_404(Produto, id=id, user=request.user)
    if request.method == 'POST':
        produto.delete()
        return redirect('produtos')
    return redirect('produtos')


# #######################################################################
#                               VENDAS
# #######################################################################
@login_required(login_url='/')
def vendas_view(request):

    vendas = (
        Venda.objects
        .filter(user=request.user)
        .prefetch_related('itens__produto')
        .order_by('-data_venda')
    )

    buscar = request.GET.get('buscar')
    data = request.GET.get('data')

    if buscar:
        filtros = (
            Q(descricao__icontains=buscar) |
            Q(cliente__icontains=buscar)
        )

        if buscar.isdigit():
            filtros |= Q(id=int(buscar))

        vendas = vendas.filter(filtros)

    if data:
        try:
            data_base = datetime.strptime(data, "%Y-%m-%d")

            inicio = data_base
            fim = data_base + timedelta(days=1)

            vendas = vendas.filter(
                data_venda__gte=inicio,
                data_venda__lt=fim
            )

        except ValueError:
            pass

    context = {
        'vendas': vendas
    }

    return render(request, "vendas.html", context)


@transaction.atomic
@login_required(login_url='/')
def realizar_venda_view(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            itens = data.get("itens", [])
            fiado = data.get("fiado", False)
            cliente = data.get("clienteFiado")
            descricao = data.get("descricao")

            if not itens:
                print("Nenhum item enviado.")
                return JsonResponse(
                    {"status": "error", "message": "Nenhum item enviado."},
                    status=400
                )
            
            if len(descricao) > 255:
                return JsonResponse({
                    "status": "error",
                    "message": "Descrição muito longa."
                }, status=400)

            total_calculado = 0

            # primeiro valida tudo
            produtos_processados = []

            for item in itens:
                produto = get_object_or_404(
                    Produto,
                    id=item['id'],
                    user=request.user
                )

                quantidade = int(item['quantidade'])
                preco = float(item['preco'])

                if quantidade <= 0:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Quantidade inválida para {produto.nome}."
                    }, status=400)

                if produto.estoque.quantidade < quantidade:
                    return JsonResponse({
                        "status": "error",
                        "message": f"Estoque insuficiente para {produto.nome}. Estoque atual: {produto.estoque.quantidade}"
                    }, status=400)

                total_calculado += quantidade * preco

                produtos_processados.append(
                    (produto, quantidade, preco)
                )

            # cria a venda
            venda_obj = Venda.objects.create(
                cliente=cliente if fiado else None,
                total=total_calculado,
                descricao=descricao,
                user=request.user,
                data_venda=timezone.now()
            )

            # cria itens + baixa estoque
            for produto, quantidade, preco in produtos_processados:

                ItemVenda.objects.create(
                    venda=venda_obj,
                    produto=produto,
                    quantidade=quantidade,
                    total_parcial=preco
                )

                produto.estoque.quantidade -= quantidade
                produto.estoque.save()
            
            # venda fiada
            if fiado:
                print("Criando venda fiada...")
                print(f"Venda: {venda_obj.id}, Cliente: {cliente}, Total: {total_calculado}")
                VendaFiada.objects.create(
                    venda=venda_obj,
                    total_pago=0,
                    total_pendente=total_calculado,
                    status="pendente"
                )

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("Erro ao processar venda:", str(e))
            return JsonResponse({
                "status": "error",
                "message": str(e)
            }, status=400)

    context = {
        'produtos': Produto.objects.filter(user=request.user)
    }

    return render(request, "realizar-venda.html", context)


# vendas: DELETE
@login_required(login_url='/')
def vendas_excluir_view(request, id):
    venda = get_object_or_404(Venda, id=id, user=request.user)

    if request.method == 'POST':
        # restaura estoque
        for item in venda.itens.all():
            produto = item.produto
            produto.estoque.quantidade += item.quantidade
            produto.estoque.save()

        venda.delete()

        return redirect('vendas')
    
    return redirect('vendas')


# #######################################################################
#                           VENDAS FIADO
# #######################################################################
# vendas_fiado: GET
@login_required(login_url='/')
def vendas_fiado_view(request):
    vendas_fiado = VendaFiada.objects.filter(
        venda__user=request.user
    ).select_related('venda').order_by('-venda__data_venda')

    buscar = request.GET.get('buscar')
    data = request.GET.get('data')

    if buscar:
        filtros = (
            Q(venda__descricao__icontains=buscar) |
            Q(venda__cliente__icontains=buscar)
        )

        if buscar.isdigit():
            filtros |= Q(id=int(buscar))

        vendas_fiado = vendas_fiado.filter(filtros)

    if data:
        try:
            data_base = datetime.strptime(data, "%Y-%m-%d")

            inicio = data_base
            fim = data_base + timedelta(days=1)

            vendas_fiado = vendas_fiado.filter(
                venda__data_venda__gte=inicio,
                venda__data_venda__lt=fim
            )

        except ValueError:
            pass
    
    context = {
        "vendas_fiado": vendas_fiado
    }
    return render(request, "vendas-fiado.html", context)


# vendas_fiado: PAY
@login_required(login_url='/')
def vendas_fiado_pagar_view(request, id):

    venda_fiado = get_object_or_404(
        VendaFiada,
        id=id,
        venda__user=request.user
    )

    if request.method == 'POST':

        try:
            valor_pago = Decimal(request.POST.get('valor_pago', '0'))
        except InvalidOperation:
            messages.error(request, "Valor inválido.")
            return redirect('vendas_fiado')

        if valor_pago <= 0:
            messages.error(request, "Valor de pagamento inválido.")
            return redirect('vendas_fiado')

        venda_fiado.total_pago += valor_pago

        if venda_fiado.total_pago >= venda_fiado.venda.total:
            venda_fiado.status = "pago"
            venda_fiado.total_pago = venda_fiado.venda.total
        else:
            venda_fiado.status = "parcial"

        venda_fiado.save()

        return redirect('vendas_fiado')

    return redirect('vendas_fiado')


# vendas_fiado: DELETE
@login_required(login_url='/')
def vendas_fiado_excluir_view(request, id):
    venda_fiado = get_object_or_404(VendaFiada, id=id, venda__user=request.user)

    if request.method == 'POST':
        venda_fiado.venda.delete()
        return redirect('vendas_fiado')
    
    return redirect('vendas_fiado')

# #######################################################################
#                               LOGOUT
# #######################################################################
@login_required(login_url='/')
def logout_view(request):
    print('Fazendo logout...')
    logout(request)
    return redirect('login')