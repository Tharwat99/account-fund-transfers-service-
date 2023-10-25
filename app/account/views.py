from django.http import HttpResponse, JsonResponse
import csv
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics,serializers
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer

@csrf_exempt
def import_accounts(request):
    if request.method == 'POST':
        accounts_file = request.FILES.get('accounts_file')
        if accounts_file:
            # Read the CSV file
            reader = csv.DictReader(accounts_file.read().decode('utf-8').splitlines())
            accounts = []
            
            # Process each row in the CSV file
            for row in reader:
                # Create an Account object from each row
                account = Account(
                    id=row['ID'],
                    name=row['Name'],
                    balance=float(row['Balance'])
                )
                accounts.append(account)
            
            # Save the Account objects to the database
            Account.objects.bulk_create(accounts)
            return HttpResponse("File Uploaded Successfully")
            
        else:
            raise serializers.ValidationError('No CSV file provided.')
    else:
        return HttpResponse('Invalid request method.')

class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountRetrieveView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'