from decimal import Decimal
import csv
import openpyxl
import json
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.utils import IntegrityError
from django.urls import reverse
from rest_framework.decorators import api_view
from ..models import Account



@api_view(['GET', 'POST'])
def import_accounts(request):
    if request.method == 'GET':
        # Render template form for import accounts file
        return render(request, 'import_accounts.html')

    if request.method == 'POST':
        accounts_file = request.FILES.get('accounts_file')
        if accounts_file:
            # Check the file extension
            if accounts_file.name.endswith('.csv'):
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
                    error_message = "Error: some records already exist."
                    return render(request, 'import_accounts.html', {'error_message': error_message})
                success_message = "Success: The records inserted successfully."
                return render(request, 'import_accounts.html', {'success_message': success_message})
            
            elif accounts_file.name.endswith('.xls') or accounts_file.name.endswith('.xlsx'):
                try:
                    wb = openpyxl.load_workbook(accounts_file)
                    sheet = wb.active  # Assuming you're working with the active sheet

                    accounts = []
                    is_header = True  # Flag to skip the first row (header)

                    for row in sheet.iter_rows(values_only=True):
                        if is_header:
                            is_header = False  # Skip the first row (header)
                            continue  # Skip processing this row
                        # Assuming the first column is 'ID', the second is 'Name', and the third is 'Balance'
                        account = Account(id=row[0], name=row[1], balance=float(row[2]))
                        accounts.append(account)

                    Account.objects.bulk_create(accounts)
                    success_message = "Success: The records inserted successfully."
                    return render(request, 'import_accounts.html', {'success_message': success_message})
                except Exception as e:
                    # Handle any exceptions, such as IntegrityError or file format issues
                    error_message = "Error: " + str(e)
                    return render(request, 'import_accounts.html', {'error_message': error_message})
            
            elif accounts_file.name.endswith('.json'):
                # Read a JSON file
                data = accounts_file.read().decode('utf-8')
                try:
                    records = json.loads(data)
                    accounts = []

                    for record in records:
                        account = Account(id=record['ID'], name=record['Name'], balance=float(record['Balance']))
                        accounts.append(account)

                    Account.objects.bulk_create(accounts)
                    success_message = "Success: The records inserted successfully."
                    return render(request, 'import_accounts.html', {'success_message': success_message})
                except json.JSONDecodeError:
                    error_message = "Error: Invalid JSON file."
                    return render(request, 'import_accounts.html', {'error_message': error_message})

            else:
                error_message = "Error: Invalid file type. Please upload a CSV, XLS, or JSON file."
                return render(request, 'import_accounts.html', {'error_message': error_message})
        else:
            error_message = "Error: No file provided."
            return render(request, 'import_accounts.html', {'error_message': error_message})
    else:
        error_message = "Error: No file provided."
        return render(request, 'import_accounts.html', {'error_message': error_message})

@api_view(['GET'])
def account_list(request):
    # Get all accounts
    all_accounts = Account.objects.all().order_by('id')

    # Set the number of accounts to display per page
    per_page = 10  # Adjust this value as needed

    # Create a Paginator instance
    paginator = Paginator(all_accounts, per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    # Get the accounts for the current page
    accounts = paginator.get_page(page)

    return render(request, 'account_list.html', {'accounts': accounts})

@api_view(['GET'])
def get_account_details(request, id):
    account = get_object_or_404(Account, id=id)
    accounts = Account.objects.exclude(id=id) 
    enable = account.balance > 0
    max_amount = account.balance
    return render(request, 'account_details.html', {'account': account, 'accounts':accounts, 'max_amount':max_amount, 'enable':enable})

@api_view(['POST'])
@csrf_exempt
def transfer_funds(request):
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
            return HttpResponseRedirect(reverse('get_account', args=[source_account.id]))
        else:
            error_message = "Error: Insufficient balance in the source account."
            return render(request, 'import_accounts.html', {'error_message': error_message})
    except Account.DoesNotExist:
        error_message = "Error: Invalid account ID."
        return render(request, 'import_accounts.html', {'error_message': error_message})
   
