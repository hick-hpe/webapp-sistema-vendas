from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    

class Fornecedor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    distribuidora = models.CharField(max_length=100)
    nome = models.CharField(max_length=100, blank=True)

    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    rua = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)

    site = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.nome
    

class Produto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=500, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='produtos'
    )
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estoque_minimo = models.PositiveIntegerField(default=5, blank=True)

    @property
    def lucro(self):
        if self.preco_venda and self.preco_custo:
            return self.preco_venda - self.preco_custo
        return 0
    
    @property
    def margem_lucro(self):
        if self.preco_custo and self.preco_custo > 0:
            return (((self.preco_venda or 0) - self.preco_custo) / self.preco_custo) * 100
        return 0

    def __str__(self):
        return f'{self.nome} - R$ {self.preco_venda}'


class Compra(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT
    )

    STATUS_CHOICES = [
        ('A', 'Ativa'),
        ('C', 'Cancelada'),
    ]

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    data = models.DateField(auto_now_add=True)

    @property
    def valor_total(self):
        return sum(
            item.subtotal
            for item in self.itens.all()
        )

    def __str__(self):
        return f'Compra #{self.id}'


class ItemCompra(models.Model):
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='itens'
    )

    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='itens_compra'
    )

    quantidade = models.PositiveIntegerField(default=0)

    preco_custo = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.quantidade * self.preco_custo


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.quantidade} unidades - {self.produto.nome}'

    @property
    def status(self):
        if self.quantidade == 0:
            return "Esgotado"
        elif self.quantidade <= self.produto.estoque_minimo:
            return "Baixo"
        return "Normal"
    

class Venda(models.Model):
    PAGAMENTO_CHOICES = [
        ("dinheiro", "Dinheiro"),
        ("pix", "Pix"),
        ("dinheiro_pix", "Dinheiro + Pix"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descricao = models.TextField(max_length=500, blank=True, null=True)
    forma_pagamento = models.CharField(max_length=100, choices=PAGAMENTO_CHOICES, blank=True, null=True, default='pix')
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxa = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Venda #{self.id} - R$ {self.total}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    total_parcial = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
    

class VendaFiada(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("parcial", "Parcial"),
        ("pago", "Pago"),
    ]
    venda = models.OneToOneField(Venda, related_name='fiadas', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    total_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def total_pendente(self):
        return self.venda.total - self.total_pago

    def __str__(self):
        return f'Venda Fiada #{self.venda.id} - Status: {self.status}'
    
