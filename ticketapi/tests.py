from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group
from ticketapi.models import User, Category

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