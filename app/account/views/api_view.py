import csv
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Account
from ..serializers import AccountSerializer, ImportAccountsSerializer

class ImportAccountsView(generics.GenericAPIView):
    serializer_class = ImportAccountsSerializer

    def post(self, request, format=None):
        serializer = ImportAccountsSerializer(data=request.data)

        if serializer.is_valid():
            accounts_file = serializer.validated_data['accounts_file']

            try:
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
                    return Response({'error': 'some records already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'Accounts imported successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Error processing the file'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AccountListView(generics.ListAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer

# class AccountRetrieveView(generics.RetrieveAPIView):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     lookup_field = 'id'
