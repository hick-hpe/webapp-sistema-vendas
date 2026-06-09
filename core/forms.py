from django import forms
from .models import Categoria, Produto, Organizacao

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
        })
    )

    estoque_minimo = forms.IntegerField(
        label="Estoque mínimo",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estoque mínimo',
            'min': '0'
        })
    )

    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'preco', 'estoque_minimo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição do produto (opcional)', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço do produto', 'min': '0'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estoque mínimo', 'min': '0'})
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
        self.fields['categoria'].empty_label = "Escolha uma categoria"

# futuramente...
# class OrganizacaoForm(forms.ModelForm):
#     nome = forms.CharField(
#         label="Nome da organização",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da organização'})
#     )

#     descricao = forms.CharField(
#         label="Descrição da organização",
#         widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da organização (opcional)', 'rows': 3}),
#         required=False
#     )

#     class Meta:
#         model = Organizacao
#         fields = ['nome', 'descricao']
    

# class VendaForm(forms.Form):
#     cliente = forms.CharField(
#         label="Nome do cliente (opcional)",
#         required=False,
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente'})
#     )
