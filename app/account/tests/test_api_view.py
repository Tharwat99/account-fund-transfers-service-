import os 
from rest_framework.test import APITestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from ..models import Account  
from ..serializers import ImportAccountsSerializer


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