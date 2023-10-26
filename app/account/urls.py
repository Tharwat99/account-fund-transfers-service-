from django.urls import path
from .views.web_view import import_accounts, account_list, get_account_details, transfer_funds
from .views.api_view import ImportAccountsView, AccountListView, AccountRetrieveView, TransferFundsView

urlpatterns = [
    path('accounts/import', import_accounts, name='import_accounts'),
    path('accounts', account_list, name='list_accounts'),
    path('account/<uuid:id>/', get_account_details, name='get_account'),   
    path('transfer', transfer_funds, name='transfer_funds'),
    path('api/accounts/import', ImportAccountsView.as_view()),
    path('api/accounts', AccountListView.as_view()),
    path('api/account/<uuid:id>/', AccountRetrieveView.as_view()),
    path('api/transfer', TransferFundsView.as_view())
]