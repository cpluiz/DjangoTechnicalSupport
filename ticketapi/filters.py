import django_filters
from ticketapi.models import Ticket

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'status' : ['exact'],
            'priority' : ['exact', 'range'],
            'customer_id': ['exact'],
            'attendant_id' : ['exact'],
            'title' : ['iexact', 'icontains']
        }
