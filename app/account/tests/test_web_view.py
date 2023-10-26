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

    def test_transfer_funds_success(self):
        source_account = Account.objects.create(id=uuid.uuid4(), name="Source Account", balance=1000.0)
        target_account = Account.objects.create(id=uuid.uuid4(), name="Target Account", balance=500.0)

        post_data = {
            'source_account_id': source_account.id,
            'target_account_id': target_account.id,
            'amount': 500.0
        }

        url = reverse('transfer_funds')  # Replace with the actual URL name

        response = self.client.post(url, post_data)

        self.assertEqual(response.url, reverse('get_account', args=[source_account.id]))

        # Verify that the balances have been updated
        source_account.refresh_from_db()
        target_account.refresh_from_db()
        self.assertEqual(source_account.balance, 500.0)  
        self.assertEqual(target_account.balance, 1000.0) 

    def test_transfer_funds_insufficient_balance(self):
        source_account = Account.objects.create(id=uuid.uuid4(), name="Source Account", balance=300.0)
        target_account = Account.objects.create(id=uuid.uuid4(), name="Target Account", balance=1000.0)

        post_data = {
            'source_account_id': source_account.id,
            'target_account_id': target_account.id,
            'amount': 450.0  # Amount greater than the source account's balance
        }

        url = reverse('transfer_funds')

        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Insufficient balance in the source account")
    
    def test_transfer_funds_invalid_account(self):
        target_account = Account.objects.create(id=uuid.uuid4(), name="Target Account", balance=1000.0)

        post_data = {
            'source_account_id': uuid.uuid4(),  # An ID that doesn't exist
            'target_account_id': target_account.id,
            'amount': 300.0
        }

        url = reverse('transfer_funds') 

        response = self.client.post(url, post_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid account ID")

    
    def test_transfer_funds_success(self):
        source_account = Account.objects.create(id=uuid.uuid4(), name='Source Account', balance=100.0)
        target_account = Account.objects.create(id=uuid.uuid4(), name='Target Account', balance=50.0)

        url = reverse('transfer_funds_api')

        data = {
            'source_account_id': source_account.id,
            'target_account_id': target_account.id,
            'amount': 30.0,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        # Reload the accounts from the database
        source_account.refresh_from_db()
        target_account.refresh_from_db()

        self.assertEqual(source_account.balance, 70.0)
        self.assertEqual(target_account.balance, 80.0)

    def test_transfer_funds_insufficient_balance(self):
        
        source_account = Account.objects.create(id=uuid.uuid4(), name='Source Account', balance=100.0)
        target_account = Account.objects.create(id=uuid.uuid4(), name='Target Account', balance=50.0)

        url = reverse('transfer_funds_api')

        data = {
            'source_account_id': source_account.id,
            'target_account_id': target_account.id,
            'amount': 200.0,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

        # Reload the accounts from the database
        source_account.refresh_from_db()

        # Check that the source account balance remains unchanged
        self.assertEqual(source_account.balance, 100.0)

    def test_transfer_funds_invalid_account(self):
        target_account = Account.objects.create(id=uuid.uuid4(), name='Target Account', balance=50.0)

        url = reverse('transfer_funds_api')

        data = {
            'source_account_id': uuid.uuid4(),
            'target_account_id': target_account.id,
            'amount': 200.0,
        }
        
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

 
