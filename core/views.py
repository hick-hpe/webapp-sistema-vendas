from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoriaForm, ProdutoForm
from .models import Categoria, Estoque, Produto
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required(login_url='/')
def vendas_view(request):
    return render(request, "vendas.html")


@login_required(login_url='/')
def compras_fiado_view(request):
    return render(request, "compras-fiado.html")


@login_required(login_url='/')
def logout_view(request):
    print('Fazendo logout...')
    logout(request)
    return redirect('login')