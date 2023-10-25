from django.urls import path
from .views import import_accounts

urlpatterns = [
    # Other URL patterns
    path('accounts/import', import_accounts, name='accounts-import-file'),
]