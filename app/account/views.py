from decimal import Decimal
import csv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework import generics,serializers
from django.db.utils import IntegrityError
from .models import Account
from .serializers import AccountSerializer

@csrf_exempt
def import_accounts(request):
    if request.method == 'GET':
        return render(request, 'import_accounts.html')
    if request.method == 'POST':
        accounts_file = request.FILES.get('accounts_file')
        if accounts_file:
            # Read the CSV file
            if not accounts_file.name.endswith('.csv'):
                return render(request, 'import_accounts.html', {'error_message': "Error: Invalid file type. Please upload a CSV file"})

            reader = csv.DictReader(accounts_file.read().decode('utf-8').splitlines())
            accounts = []
            
            # Process each row in the CSV file
            for row in reader:
                # Create an Account object from each row
                account = Account(id=row['ID'], name=row['Name'], balance=float(row['Balance']))
                accounts.append(account)
            try:    
                Account.objects.bulk_create(accounts)
            except IntegrityError as e:
                # Handle the IntegrityError
                error_message = "Error: some records already exists."
                return render(request, 'import_accounts.html', {'error_message': error_message})
        
            return render(request, 'import_accounts.html', {'success_message': "Success: The records inserted sucessfully."})
        
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

@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        source_account_id = request.POST.get('source_account_id')
        target_account_id = request.POST.get('target_account_id')
        amount = Decimal(request.POST.get('amount'))
        
        try:
            source_account = Account.objects.get(id=source_account_id)
            target_account = Account.objects.get(id=target_account_id)
            
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                return HttpResponse('Funds transferred successfully.')
            else:
                return HttpResponse('Insufficient balance in the source account.')
        except Account.DoesNotExist:
            return HttpResponse('Invalid account ID.')
    else:
        return HttpResponse('Invalid request method.')