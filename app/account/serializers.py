from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class ImportAccountsSerializer(serializers.Serializer):
    accounts_file = serializers.FileField()