import csv
import openpyxl
import json
from ..models import Account

def handle_csv_file(accounts_file):
    accounts = []
    accounts_ids = Account.objects.all().values_list('id', flat=True)
    exists_records = 0
    inserted_records = 0

    reader = csv.DictReader(accounts_file.read().decode('utf-8').splitlines())
    
    for row in reader:
        if not row['ID'] not in accounts_ids:
            account = Account(id=row['ID'], name=row['Name'], balance=float(row['Balance']))
            accounts.append(account)
            inserted_records+=1
        else:
            exists_records +=1
    return accounts, inserted_records, exists_records

def handle_xls_file(accounts_file):
    
    accounts = []
    accounts_ids = Account.objects.all().values_list('id', flat=True)
    exists_records = 0
    inserted_records = 0
    wb = openpyxl.load_workbook(accounts_file)
    sheet = wb.active  # Assuming you're working with the active sheet

    is_header = True  # Flag to skip the first row (header)

    for row in sheet.iter_rows(values_only=True):
        if is_header:
            is_header = False  # Skip the first row (header)
            continue  # Skip processing this row
        
        if not row[0] not in accounts_ids:
            account = Account(id=row[0], name=row[1], balance=float(row[1]))
            accounts.append(account)
            inserted_records+=1
        else:
            exists_records +=1 
    return accounts, inserted_records, exists_records

def handle_json_file(accounts_file):
    accounts_ids = Account.objects.all().values_list('id', flat=True)
    exists_records = 0
    inserted_records = 0
    accounts = []

    data = accounts_file.read().decode('utf-8')
    records = json.loads(data)
   
    for record in records:
        if not record['ID'] not in accounts_ids:
            account = Account(id=record['ID'], name=record['Name'], balance=float(record['Balance']))
            accounts.append(account)
            inserted_records+=1
        else:
            exists_records +=1 
    return accounts, inserted_records, exists_records


