import csv
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Account
from ..serializers import AccountSerializer, ImportAccountsSerializer, TransferFundsSerializer
from ..paginations import ListAccountsPagination

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


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all().order_by('-id')
    serializer_class = AccountSerializer
    pagination_class = ListAccountsPagination

class AccountRetrieveView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'

class TransferFundsView(generics.CreateAPIView):
    serializer_class = TransferFundsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        source_account_id = serializer.validated_data['source_account_id']
        target_account_id = serializer.validated_data['target_account_id']
        amount = serializer.validated_data['amount']

        try:
            source_account = Account.objects.get(id=source_account_id)
            target_account = Account.objects.get(id=target_account_id)
            if source_account.balance >= amount:
                source_account.balance -= amount
                target_account.balance += amount
                source_account.save()
                target_account.save()
                return Response({'message': 'Funds transferred successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Insufficient balance in the source account'}, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({'error': 'Invalid account ID'}, status=status.HTTP_400_BAD_REQUEST)