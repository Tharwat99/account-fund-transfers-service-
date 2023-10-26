import os
import uuid
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Page
from rest_framework.test import APIClient
from account.models import Account


class WebViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_dir = settings.BASE_DIR

    def test_get_import_accounts_view(self):
        url = reverse('import_accounts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 

    def test_post_import_accounts_success(self):
        url = reverse('import_accounts')
        filename = "accounts.csv"
        filepath = os.path.join(self.base_dir, filename)
        data = {
            'accounts_file': open(filepath, 'rb') 
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 200) 
    
    def test_list_accounts_view(self):
        # Create Sample accounts
        for i in range(1, 21):
            account = Account(id=uuid.uuid4(), name=f'Account {i}', balance=100.0)
            account.save()

        url = reverse('list_accounts') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) 
        # Verify that the response contains a Page object with accounts
        self.assertTrue(isinstance(response.context['accounts'], Page))
    
    
    def test_get_account_details(self):
        account = Account.objects.create(id=uuid.uuid4(), name="Test Account", balance=100.0)
        url = reverse('get_account', args=[account.id])  

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        returned_account = response.context['account']
        self.assertEqual(account.id, returned_account.id)
        self.assertEqual(account.name, returned_account.name)
        self.assertEqual(account.balance, returned_account.balance)
