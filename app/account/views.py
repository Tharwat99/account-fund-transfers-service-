from decimal import Decimal
import csv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from rest_framework import generics,serializers
from .models import Account
from .serializers import AccountSerializer


@csrf_exempt
def import_accounts(request):
    if request.method == 'GET':
        # Render template form for import accounts file
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

def account_list(request):
    # Get all accounts
    all_accounts = Account.objects.all()

    # Set the number of accounts to display per page
    per_page = 10  # Adjust this value as needed

    # Create a Paginator instance
    paginator = Paginator(all_accounts, per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    # Get the accounts for the current page
    accounts = paginator.get_page(page)

    return render(request, 'account_list.html', {'accounts': accounts})

def get_account_details(request, id):
    account = get_object_or_404(Account, id=id)
    accounts = Account.objects.exclude(id=id)  # Exclude the current user's account
    return render(request, 'account_details.html', {'account': account, 'accounts':accounts})

@csrf_exempt
def transfer_funds(request):
    if request.method == 'POST':
        source_account_id = request.POST.get('source_account_id')
        target_account_id = request.POST.get('target_account_id')
        amount = Decimal(request.POST.get('amount'))
        try:
            accounts = Account.objects.exclude(id=source_account_id)  # Exclude the current user's account
            source_account = Account.objects.get(id=source_account_id)
            target_account = Account.objects.get(id=target_account_id)
            
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                return render(request, 'account_details.html', {'account': source_account, 'accounts':accounts})
            else:
                return HttpResponse('Insufficient balance in the source account.')
        except Account.DoesNotExist:
            return HttpResponse('Invalid account ID.')
    else:
        return HttpResponse('Invalid request method.')

# class AccountListView(generics.ListAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer

# class AccountRetrieveView(generics.RetrieveAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     lookup_field = 'id'
