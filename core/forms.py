from django import forms
from .models import Categoria, Produto, Fornecedor
#Organizacao
import re

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da categoria'})
        }


class ProdutoForm(forms.ModelForm):
    estoque = forms.IntegerField(
        label="Quantidade em estoque",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantidade em estoque',
            'min': '0'
        }),
        required=False
    )

    estoque_minimo = forms.IntegerField(
        label="Estoque mínimo",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estoque mínimo',
            'min': '0'
        }),
        required=False
    )

    preco_venda = forms.DecimalField(
        label='Preço de venda',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Preço de venda do produto',
            'min': '0'
        }),
        required=False
    )

    preco_custo = forms.DecimalField(
        label='Preço de custo',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Preço de custo do produto',
            'min': '0'
        }),
        required=False
    )

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'fornecedor', 'preco_venda', 'preco_custo', 'estoque_minimo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do produto (opcional)', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'fornecedor': forms.Select(attrs={
                'class': 'form-select',
            }),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estoque mínimo', 'min': '0'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
        self.fields['categoria'].empty_label = "Escolha uma categoria"
        self.fields['categoria'].required = False

        if user:
            self.fields['fornecedor'].queryset = Fornecedor.objects.filter(user=user)
        

    def clean_preco_venda(self):
        valor = self.cleaned_data.get('preco_venda')

        if valor is None:
            return 0

        return valor
    
    
    def clean_preco_custo(self):
        valor = self.cleaned_data.get('preco_custo')

        if valor is None:
            return 0

        return valor
    
    
    def clean_estoque_minimo(self):
        valor = self.cleaned_data.get('estoque_minimo')

        if valor is None:
            return 10

        return valor

class FornecedorForm(forms.ModelForm):

    distribuidora = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da distribuidora'}))
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do contato'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'placeholder': '(45) 99999-9999'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PR'}))

    # Opcionais (required=False)
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}))
    rua = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}))
    numero = forms.CharField(label='Número', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}))
    bairro = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}))
    cep = forms.CharField(label='CEP', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '85800-000'}))
    site = forms.URLField(required=False, widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://fornecedor.com'}))

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']

        pattern = r'^\(\d{2}\) \d{4,5}-\d{4}$'
        if not re.match(pattern, telefone):
            raise forms.ValidationError(
                'Informe o telefone com formato válido.'
            )
        
        return telefone


    def clean_distribuidora(self):
        distribuidora = self.cleaned_data['distribuidora']

        qs = Fornecedor.objects.filter(
            user=self.user,
            distribuidora__iexact=distribuidora
        )

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                'Já existe uma distribuidora com esse nome.'
            )

        return distribuidora

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Fornecedor
        fields = ['distribuidora', 'nome', 'telefone', 'email', 'rua', 'numero', 'bairro', 'cidade', 'estado', 'cep', 'site']


# futuramente...    

# class VendaForm(forms.Form):
#     cliente = forms.CharField(
#         label="Nome do cliente (opcional)",
#         required=False,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente'})
#     )
