from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from ticketapi.models import User, Category, Ticket, Interaction

class CustomersAPITestCase(APITestCase):
    def setUp(self):
        self.adminUser = User.objects.create_superuser(username='testAdmin', password='admin')
        self.customerUser = User.objects.create_user(username='testCustomer', password='password')
        
        self.customers = [
            User.objects.create_user(username='customer1', password='senha'),
            User.objects.create_user(username='customer2', password='senha'),
            User.objects.create_user(username='customer3', password='senha'),
        ]

        self.attendant_group, created = Group.objects.get_or_create(name='Attendants')
        self.customer_group, created = Group.objects.get_or_create(name='Customers')
        self.adminUser.groups.add(self.attendant_group)
        self.customerUser.groups.add(self.customer_group)
        for customer in self.customers:
            customer.groups.add(self.customer_group)

        self.category = Category.objects.create(title="TestCategory")

        self.ticket = Ticket.objects.create(
            customer=self.customerUser,
            attendant=self.adminUser,
            title="Novo Ticket",
            description="Testando a inclusão de um novo ticket",
            category=self.category,
            priority=2,
            status=2
        )

        self.interaction = Interaction.objects.create(
            ticket=self.ticket,
            user=self.adminUser,
            message="Test Message"
        )
        
        self.list_url = reverse('customers-list')
        self.detail_url = reverse('customers-detail', kwargs={'pk' : self.customerUser.id})

    def test_get_customer_list_without_auth(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)
        print(response.json())

    def test_get_customers_list_from_admin(self):
        self.client.force_login(self.adminUser)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
    
    def test_get_customer_detail_from_admin(self):
        self.client.force_login(self.adminUser)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_get_customer_detail(self):
        self.client.force_login(self.customerUser)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
    
    def test_update_customer_detail(self):
        self.client.force_login(self.customerUser)
        data = {
            "username" : "newUserName",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())
    
    def test_partial_update_customer_detail(self):
        self.client.force_login(self.customerUser)
        data = {
            "email" : "testmail@mail.com",
        }
        response = self.client.put(self.list_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_user_with_admin(self):
        self.client.force_login(self.adminUser)
        data = {
            "username" : "newUser",
            "password" : "password"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_category_without_login(self):
        self.list_url = reverse('categories-list')
        data = {"title":"new test category"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 401)
        print(response.json())
    
    def test_create_category_with_customer(self):
        self.client.force_login(self.customerUser)
        self.list_url = reverse('categories-list')
        data = {"title":"new test category"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 403)
        print(response.json())

    def test_create_category_with_admin(self):
        self.client.force_login(self.adminUser)
        self.list_url = reverse('categories-list')
        data = {"title":"new test category"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 201)
        print(response.json())

    def test_update_category_with_customer(self):
        self.client.force_login(self.customerUser)
        self.detail_url = reverse('categories-detail', kwargs={'pk' : self.category.pk})
        data = {"title":"new category name"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, 403)
        print(response.json())

    def test_update_category_with_admin(self):
        self.client.force_login(self.adminUser)
        self.detail_url = reverse('categories-detail', kwargs={'pk' : self.category.pk})
        data = {"title":"new category name"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_update_category_without_data(self):
        self.client.force_login(self.adminUser)
        self.detail_url = reverse('categories-detail', kwargs={'pk' : self.category.pk})
        data = {}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, 400)
        print(response.json())

    def test_list_all_tickets(self):
        self.client.force_login(self.adminUser)
        self.list_url = reverse('tickets-list')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_ticket(self):
        self.client.force_login(self.customerUser)
        self.list_url = reverse('tickets-list')
        data = {
            "title" : "Creating new Test Ticket",
            "description" : "detailed ticket description",
            "category" : self.category.pk,
            "priority" : 1
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_ticket_missing_argument(self):
        self.client.force_login(self.customerUser)
        self.list_url = reverse('tickets-list')
        data = {
            "title" : "Creating new Test Ticket",
            "category" : self.category.pk,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 400)
        print(response.json())
    
    def test_update_ticket_status_as_admin(self):
        self.client.force_login(self.adminUser)
        self.list_url = reverse('tickets-detail', kwargs={'pk' : self.ticket.pk})
        data = {
            "status" : 3
        }
        response = self.client.patch(self.list_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())
    
    def test_update_ticket_status_as_customer(self):
        self.client.force_login(self.customerUser)
        self.list_url = reverse('tickets-detail', kwargs={'pk' : self.ticket.pk})
        data = {
            "status" : 3
        }
        response = self.client.patch(self.list_url, data)
        self.assertEqual(response.status_code, 403)
        print(response.json())

    def test_list_all_customer_tickets(self):
        self.client.force_login(self.customerUser)
        self.list_url = reverse('tickets-list')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_ticket_interaction_as_customer(self):
        self.client.force_login(self.customerUser)
        self.detail_url = reverse('tickets-interactions-create', kwargs={'pk' : self.ticket.pk})
        data = {
            "message" : "Creating new message as Customer",
        }
        response = self.client.post(self.detail_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_create_ticket_interaction_as_admin(self):
        self.client.force_login(self.adminUser)
        self.detail_url = reverse('tickets-interactions-create', kwargs={'pk' : self.ticket.pk})
        data = {
            "message" : "Creating new message as Admin",
        }
        response = self.client.post(self.detail_url, data)
        self.assertEqual(response.status_code, 200)
        print(response.json())
    
    def test_create_ticket_interaction_missing_parameter(self):
        self.client.force_login(self.customerUser)
        self.detail_url = reverse('tickets-interactions-create', kwargs={'pk' : self.ticket.pk})
        data = {}
        response = self.client.post(self.detail_url, data)
        self.assertEqual(response.status_code, 400)
        print(response.json())