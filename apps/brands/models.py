from django.db import models
from django.contrib.auth.models import User

class BrandProfile(models.Model):
    NICHES = (
        ('dentista', 'Dentista'),
        ('estetica', 'Estética/Harmonização'),
        ('hamburgueria', 'Restaurantes/Hamburguerias'),
        ('personal', 'Personal Trainer'),
        ('nutricionista', 'Nutricionista'),
        ('imobiliaria', 'Imobiliária'),
        ('advogado', 'Advogado'),
        ('barbearia', 'Barbearia'),
        ('loja_feminina', 'Loja Feminina'),
        ('influenciador', 'Influenciador Local'),
        
    )
# Adicione isso dentro da sua classe BrandProfile (junto aos outros campos)
    credits = models.IntegerField(default=1, verbose_name="Créditos Restantes")
    generations_count = models.IntegerField(default=0, verbose_name="Total de Posts Gerados (Histórico)")
    generations_count = models.IntegerField(default=0, verbose_name="Posts Gerados")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_profile')
    niche = models.CharField('Nicho de Atuação', max_length=50, choices=NICHES)
    brand_name = models.CharField('Nome da Marca', max_length=100)
    tone_of_voice = models.CharField(
        'Tom de Voz', 
        max_length=100, 
        help_text="Ex: Divertido e informal, Sério e focado em vendas, etc."
    )
    primary_color = models.CharField(
        'Cor Principal', 
        max_length=7, 
        help_text="Código Hex. Ex: #FF0000"
    )
    city = models.CharField(
        'Cidade de Atuação', 
        max_length=100, 
        help_text="Fundamental para atrair público local. Ex: Porto Alegre"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand_name} - {self.get_niche_display()}"