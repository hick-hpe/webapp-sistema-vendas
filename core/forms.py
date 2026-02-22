from django import forms
from .models import Categoria, Produto

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

    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do produto'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Preço do produto', 'min': '0'})
        }

    def __init__(self, user, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.filter(user=user)
        self.fields['categoria'].empty_label = "Escolha uma categoria"

