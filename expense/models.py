from django.db import models
from django.conf import settings

# Create your models here.
class Debt(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.to_user.name} owes {self.amount} to {self.from_user.name}'

class Group(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    debts = models.ManyToManyField(Debt, null=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BillUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paid_share = models.IntegerField(default=0)
    owed_share = models.IntegerField(default=0)
    net_balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bill(models.Model):
    bill_name = models.CharField(max_length=20, default='bill-name')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    amount = models.IntegerField()
    split_type = models.CharField(max_length=20, default='EQUAL')
    date = models.DateField()
    status = models.CharField(max_length=20, default='PENDING')
    repayments = models.ManyToManyField(Debt)
    users = models.ManyToManyField(BillUser)
    image = models.ImageField(upload_to='bill_images/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
