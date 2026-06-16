from django.db import models
from .tickets import Ticket
from .users import User

class Interaction(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='ticket'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_ticket_interactions",
    )
    message = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)