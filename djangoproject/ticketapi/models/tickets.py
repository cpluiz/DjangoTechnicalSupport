from django.db import models
from django.utils import timezone
from .users import User
from .categories import Category

class Ticket(models.Model):
    class StatusChoices(models.IntegerChoices):
        OPEN = 1, 'Aberto'
        ONGOING = 2, 'Em Atendimento'
        WAITING = 3, 'Aguardando Cliente'
        SOLVED = 4, 'Resolvido'
        CANCELLED = 5, 'Cancelado'
    
    class PriorityChoices(models.IntegerChoices):
        LOW = 0, 'Baixa'
        MEDIUM = 1, 'Média'
        HIGH = 2, 'Alta'
        CRITICAL = 3, 'Crítica'
        
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="customer_tickets",
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="category_tickets",
    )
    status = models.IntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN
    )
    priority = models.IntegerField(
        choices=PriorityChoices.choices,
        default=PriorityChoices.LOW
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attendant = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="attendant_tickets",
        null=True,
        blank=True
    )

    users = models.ManyToManyField(User, through="Interaction", related_name="tickets")

    def __str__(self):
        return self.title