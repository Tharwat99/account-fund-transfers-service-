import csv
from django.db.utils import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from ..models import Account
from ..serializers import AccountSerializer, ImportAccountsSerializer, TransferFundsSerializer
from ..paginations import ListAccountsPagination
from ..utils.web_view_utils import handle_csv_file, handle_xls_file, handle_json_file

class ImportAccountsView(generics.GenericAPIView):
    serializer_class = ImportAccountsSerializer

    def post(self, request, format=None):
        serializer = ImportAccountsSerializer(data=request.data)

        if serializer.is_valid():
            accounts_file = serializer.validated_data['accounts_file']
            if accounts_file.name.endswith('.csv'):
                try:
                    accounts, inserted_records, exists_records = handle_csv_file(accounts_file)
                    Account.objects.bulk_create(accounts)
                    success_message = f"{inserted_records} records inserted successfully {exists_records} exists failed."
                    return Response({'message': success_message}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    error_message = "Error: Error processing the file."
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
            elif accounts_file.name.endswith('.xls') or accounts_file.name.endswith('.xlsx'):
                try:
                    accounts, inserted_records, exists_records = handle_xls_file(accounts_file)
                    Account.objects.bulk_create(accounts)
                    success_message = f"{inserted_records} records inserted successfully {exists_records} exists failed."
                    return Response({'message': success_message}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    error_message = "Error: Error processing the file."
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
            elif accounts_file.name.endswith('.json'):
                try:
                    accounts, inserted_records, exists_records = handle_json_file(accounts_file)
                    Account.objects.bulk_create(accounts)
                    success_message = f"{inserted_records} records inserted successfully {exists_records} exists failed."
                    return Response({'message': success_message}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    error_message = "Error: Error processing the file."
                    return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                error_message = "Error: Invalid file type. Please upload a CSV, XLS, or JSON file."
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
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