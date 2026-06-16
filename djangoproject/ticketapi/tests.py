from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from ticketapi.models import User

# Auth tests
class UsersListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_superuser(username='admin', password='admin')
        attendant_group = Group.objects.create(name='Attendants')
        user1.groups.add(attendant_group)
        user2 = User.objects.create(username='customer1', password='customer1')
        customer_group = Group.objects.create(name='Customers')
        user2.groups.add(customer_group)
    def test_users_endpoint_retrieves_only_authenticated_admins(self):
        user = User.objects.get(username='admin')
        self.client.force_login(user)
        response = self.client.get(reverse('users'))

        assert response.status_code == 200
        data = response.json()
        print(data)

class CustomersListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_superuser(username='admin', password='admin')
        attendant_group = Group.objects.create(name='Attendants')
        user1.groups.add(attendant_group)
        user2 = User.objects.create(username='customer1', password='customer1')
        customer_group = Group.objects.create(name='Customers')
        user2.groups.add(customer_group)
    def test_users_endpoint_retrieves_only_authenticated_admins(self):
        user = User.objects.get(username='customer1')
        self.client.force_login(user)
        response = self.client.get(reverse('users'))

        assert response.status_code == 403
        data = response.json()
        print(data)