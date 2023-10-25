from django.urls import path
from .views import import_accounts, AccountListView, AccountRetrieveView

urlpatterns = [
    path('accounts/import', import_accounts, name='import_accounts'),
    path('accounts', AccountListView.as_view(), name='list_accounts'),
    path('account/<uuid:id>/', AccountRetrieveView.as_view(), name='get_account'),
    
]