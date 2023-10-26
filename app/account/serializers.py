from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class ImportAccountsSerializer(serializers.Serializer):
    accounts_file = serializers.FileField()

class TransferFundsSerializer(serializers.Serializer):
    source_account_id = serializers.IntegerField()
    target_account_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)