import csv
from rest_framework import generics,serializers
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Account
from .serializers import AccountSerializer

class AccountsFileUploadView(generics.GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]

    
    def post(self, request, *args, **kwargs):
        accounts_file = self.request.FILES.get('accounts_file')
        if accounts_file:
            # Read the CSV file
            reader = csv.DictReader(accounts_file.read().decode('utf-8').splitlines())
            accounts = []
            
            # Process each row in the CSV file
            for row in reader:
                print(row['Name'])
                # Create an Account object from each row
                account = Account(
                    id=row['ID'],
                    name=row['Name'],
                    balance=float(row['Balance'])
                )
                accounts.append(account)
            
            # Save the Account objects to the database
            Account.objects.bulk_create(accounts)
            return Response("File Uploaded Successfully")
            
        else:
            raise serializers.ValidationError('No CSV file provided.')