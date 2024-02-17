from rest_framework import serializers
from expense import models

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Debt
        fields = ('id', 'from_user', 'to_user', 'amount')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'group_name', 'debts', 'members')

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bill
        fields = ('group_id', 'bill_name', 'date',
                  'date', 'users', 'repayments','notes')