from django.urls import path
from .views import AccountsFileUploadView

urlpatterns = [
    # Other URL patterns
    path('upload-accounts-file', AccountsFileUploadView.as_view(), name='upload-accounts-file'),
]