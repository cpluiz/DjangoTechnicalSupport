from django.db import models
from .tickets import Ticket
from .users import User

class Interaction(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='interactions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
    )
    message = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Usuário: {self.user.username} - Mensagem: {self.message}"