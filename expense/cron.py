# tasks.py
from django.template.loader import render_to_string
from django.core.mail import send_mail
from account.models import User
from expense.models import Debt
from django.db.models import Sum

def send_weekly_summary_email():
    users = User.objects.all()
    for user in users:
        total_owed = Debt.objects.filter(to_user=user).aggregate(total_owed=Sum('amount'))['total_owed'] or 0
        total_owe = Debt.objects.filter(from_user=user).aggregate(total_owe=Sum('amount'))['total_owe'] or 0
        subject = 'Weekly Summary'
        message = render_to_string('weekly_summary_email.html', {
            'user': user,
            'total_owed': total_owed,
            'total_owe': total_owe,
        })
        from_email = 'your_email@example.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
