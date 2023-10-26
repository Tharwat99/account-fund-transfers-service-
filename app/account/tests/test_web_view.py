import os
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient


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