from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from ticketapi.models import User, Category, Ticket, Interaction

class Command(BaseCommand):
    help = 'Creates basic application data - update default user latter'

    def handle(self, *args, **kwargs):
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='admin')
            user.groups.add(Group.objects.get(name="Attendants"))
            self.stdout.write(self.style.SUCCESS(f'Successfully populated db with admin user'))

        ThroughModel = User.groups.through

        customers = [
            User(username='customer1', email='teste@teste.com', password=make_password('senha')),
            User(username='customer2', email='teste@teste.com', password=make_password('senha')),
            User(username='customer3', email='teste@teste.com', password=make_password('senha')),
        ]
        created_customers = User.objects.bulk_create(customers)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated db with mock customers'))

        customer_objs = [
            ThroughModel(user_id=user.id, group_id=Group.objects.get(name="Customers").id)
            for user in created_customers
        ]
        ThroughModel.objects.bulk_create(customer_objs)
        self.stdout.write(self.style.SUCCESS(f'Successfully added customers on user groups'))

        attendants = [
            User(username='attendant1', email='teste@teste.com', password=make_password('senha')),
            User(username='attendant2', email='teste@teste.com', password=make_password('senha')),
            User(username='attendant3', email='teste@teste.com', password=make_password('senha')),
        ]
        created_attendants = User.objects.bulk_create(attendants)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated db with mock attendants'))

        attendant_objs = [
            ThroughModel(user_id=user.id, group_id=Group.objects.get(name="Attendants").id)
            for user in created_attendants
        ]
        ThroughModel.objects.bulk_create(attendant_objs)
        self.stdout.write(self.style.SUCCESS(f'Successfully added attendants on user groups'))

        categories = [
            Category(title="Erro no sistema"),
            Category(title="Solicitação de acesso"),
            Category(title="Problema financeiro"),
            Category(title="Suporte técnico"),
            Category(title="Dúvida geral"),
        ]
        Category.objects.bulk_create(categories)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated db with categories'))

        tickets = [
            Ticket(title='Ticket 1', description='Descrição do problema', category_id=5, customer_id=3, attendant_id=5, status=Ticket.StatusChoices.CANCELLED, priority=Ticket.PriorityChoices.LOW),
            Ticket(title='Ticket 2', description='Descrição do problema', category_id=1, customer_id=3, attendant_id=6, status=Ticket.StatusChoices.SOLVED, priority=Ticket.PriorityChoices.CRITICAL),
            Ticket(title='Ticket 3', description='Descrição do problema', category_id=2, customer_id=2, attendant_id=7, status=Ticket.StatusChoices.ONGOING, priority=Ticket.PriorityChoices.MEDIUM),
            Ticket(title='Ticket 4', description='Descrição do problema', category_id=4, customer_id=2, attendant_id=6, status=Ticket.StatusChoices.WAITING, priority=Ticket.PriorityChoices.MEDIUM),
            Ticket(title='Ticket 5', description='Descrição do problema', category_id=3, customer_id=4, attendant_id=5, priority=Ticket.PriorityChoices.HIGH),
        ]
        Ticket.objects.bulk_create(tickets)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated db with mocked tickets'))

        interactions = [
            Interaction(ticket_id=1, user_id=5, message='Ticket 1 - Resposta 1'),
            Interaction(ticket_id=1, user_id=3, message='Ticket 1 - Resposta 2'),
            Interaction(ticket_id=2, user_id=3, message='Ticket 2 - Resposta 1'),
            Interaction(ticket_id=2, user_id=6, message='Ticket 2 - Resposta 2'),
            Interaction(ticket_id=2, user_id=3, message='Ticket 2 - Resposta 3'),
            Interaction(ticket_id=2, user_id=6, message='Ticket 2 - Resposta 4'),
            Interaction(ticket_id=3, user_id=2, message='Ticket 3 - Resposta 1'),
            Interaction(ticket_id=3, user_id=7, message='Ticket 3 - Resposta 2'),
            Interaction(ticket_id=3, user_id=7, message='Ticket 3 - Resposta 3'),
            Interaction(ticket_id=4, user_id=6, message='Ticket 4 - Resposta 1'),
            Interaction(ticket_id=4, user_id=2, message='Ticket 4 - Resposta 2'),
            Interaction(ticket_id=4, user_id=6, message='Ticket 4 - Resposta 3'),
            Interaction(ticket_id=5, user_id=4, message='Ticket 5 - Resposta 1'),
        ]
        Interaction.objects.bulk_create(interactions)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated db with mocked interactions'))