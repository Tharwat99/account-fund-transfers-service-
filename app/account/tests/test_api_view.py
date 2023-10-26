import os 
import uuid
from rest_framework.test import APITestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from ..models import Account  
from ..serializers import AccountSerializer 


class ApiViewTestCase(APITestCase):
    
    def test_import_accounts_success(self):
    
        filename = "accounts.csv"
        filepath = os.path.join(settings.BASE_DIR, filename)
        data = {
            'accounts_file': open(filepath, 'rb') 
        }
        url = reverse('import_accounts_api')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_import_accounts_duplicate_records(self):

        filename = "accounts.csv"
        filepath = os.path.join(settings.BASE_DIR, filename)
        data = {
            'accounts_file': open(filepath, 'rb') 
        }
        url = reverse('import_accounts_api')
        response = self.client.post(url, data, format='multipart')
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 400)

    def test_account_list_view_success(self):

        Account.objects.create(id = uuid.uuid4(), name='Account1', balance=100.0)
        Account.objects.create(id = uuid.uuid4(), name='Account2', balance=50.0)
        url = reverse('list_accounts_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        serialized_data = AccountSerializer(Account.objects.all().order_by('-id'), many=True).data
        self.assertEqual(response.data['results'], serialized_data)

    def test_account_retrieve_view(self):
        
        account = Account.objects.create(id = uuid.uuid4(), name='Account1', balance=100.0)
        url = reverse('get_account_api', args=[account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        serialized_data = AccountSerializer(account).data
        self.assertEqual(response.data, serialized_data)

    def test_account_retrieve_view_not_found(self):
        
        url = reverse('get_account_api', args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)