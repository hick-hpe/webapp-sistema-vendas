from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.nome} - R$ {self.preco}'


class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.quantidade} unidades - {self.produto.nome}'

    @property
    def status(self):
        if self.quantidade <= 5:
            return "Baixo"
        return "Normal"
    

class Venda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    data_venda = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descricao = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'Venda #{self.id} - R$ {self.total}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    total_parcial = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'
    

class VendaFiada(models.Model):
    venda = models.OneToOneField(Venda, on_delete=models.CASCADE)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quitado = models.BooleanField(default=False)

    def __str__(self):
        if self.quitado:
            return f'Venda #{self.venda.id} - Quitada'
        return f'Venda #{self.venda.id} - Pendente'

