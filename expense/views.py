from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from expense import serializers, models
from account.models import User
from django.db.models import Sum, F, Q
from rest_framework.parsers import MultiPartParser, FormParser
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated 

# Create your views here.
def send_expense_notification_email(user, amount_owed, expense_name):
    subject = 'Expense Notification'
    message = f'You have been added to the expense "{expense_name}" and owe {amount_owed}.'
    html_message = render_to_string('expense_notification_email.html', {
        'user': user,
        'amount_owed': amount_owed,
        'expense_name': expense_name,
    })
    from_email = 'your_email@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

class CreateGroupApiView(APIView):
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request) -> Response:
        ids = request.data.get('members', [])
        user_ids = []
        for id in ids:
            user_ids.append(id)
        request.data['members'] = user_ids
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Group Created successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddUserToGroupApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request) -> Response:
        group_id = request.data.get('group_id')
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        group = models.Group.objects.get(id=group_id)
        if user not in group.members.all():
            group.members.add(user.id)
            return Response({'message': 'User successfully added to group'})
        return Response({'message': 'User already exists in the group'}, status=status.HTTP_400_BAD_REQUEST)

class CreateExpenseApiView(APIView):
    serializer_class = serializers.ExpenseSerializer
    permission_classes = (IsAuthenticated,)
    #parser_classes = (MultiPartParser, FormParser)
    def post(self, request) -> Response:
        all_users = request.data.get('users')
        all_users = User.objects.filter(id__in=all_users)
        paid_by = request.data.get('paid_by')
        paid_by_user = User.objects.filter(id=paid_by).first()
        amount = request.data.get('amount')
        date = request.data.get('date')
        group_id = request.data.get('group_id', None)
        bill_name = request.data.get('bill_name')
        split_type = request.data.get('split_type', 'equal')
        bill_image = request.data.get('bill_image', None)
        notes = request.data.get('notes')
        if amount > 100000000:
            return Response({
                "message": "Expense amount exceeds the maximum limit"
            }, status=status.HTTP_400_BAD_REQUEST)
        if len(all_users) > 1000:
            return Response({
                "message": "Number of participants exceeds the limit of 1000"
            }, status=status.HTTP_400_BAD_REQUEST)
        if models.Bill.objects.filter(bill_name=bill_name).count() > 0:
            return Response({
                "message": "Expense name should be unique"
            }, status=status.HTTP_400_BAD_REQUEST)
        group = None
        if group_id is not None:
            group = models.Group.objects.get(id=group_id)

        per_member_share = 0
        per_member_share_dict = {}

        if split_type == 'equal':
            per_member_share = amount / len(all_users)
            per_member_share_dict = {user: per_member_share for user in all_users}
        elif split_type == 'percentage':
            # Assuming percentages are provided in the request, adjust the logic accordingly
            percentages = request.data.get('percentages', None)
            if not percentages or len(percentages) != len(all_users):
                return Response({
                    "message": "Invalid percentage distribution"
                }, status=status.HTTP_400_BAD_REQUEST)

            total_percentage = sum(percentages)
            if total_percentage != 100:
                return Response({
                    "message": "Percentages must add up to 100"
                }, status=status.HTTP_400_BAD_REQUEST)

            per_member_share_dict = {user: (percentage / 100) * amount for user, percentage in zip(all_users, percentages)}
        elif split_type == 'exact':
            exact_amounts = request.data.get('exact_amounts', None)
            if not exact_amounts or len(exact_amounts) != len(all_users):
                return Response({
                    "message": "Invalid exact amount distribution"
                }, status=status.HTTP_400_BAD_REQUEST)

            per_member_share_dict = {user: exact_amount for user, exact_amount in zip(all_users, exact_amounts)}
        else:
            return Response({
                "message": "Invalid split type"
            }, status=status.HTTP_400_BAD_REQUEST)

        expense_users = []
        repayments = []
        for user in all_users:
            if user != paid_by_user:
                send_expense_notification_email(user, per_member_share_dict.get(user, per_member_share), bill_name)
                debt = models.Debt.objects.create(**{"from_user": paid_by_user,
                                                     "to_user": user,
                                                     "amount": per_member_share_dict.get(user, per_member_share)})
                repayments.append(debt)
                expense_user_dict = {"user": user,
                                     "paid_share": 0 if user != paid_by_user else per_member_share,
                                     "owed_share": per_member_share_dict.get(user, per_member_share),
                                     "net_balance": -per_member_share if user != paid_by_user else amount - per_member_share
                                     }
                expense_user = models.BillUser.objects.create(**expense_user_dict)
                expense_users.append(expense_user)

        # now create expense
        expense = {
            'group_id': group_id,
            'amount': amount,
            'bill_name': bill_name,
            'date': date,
            'split_type': split_type,
            'notes': notes,
        }
        expense = models.Bill.objects.create(**expense)
        if bill_image:
            expense.image = bill_image
        expense.repayments.set(repayments)
        expense.users.set(expense_users)
        expense.save()
        return Response({'message': 'Expense Created successfully'})

class ShowGroupDetailsApiView(APIView):
    def get(self, request) -> Response:
        group_id = request.GET.get('id')
        try:
            group = models.Group.objects.get(id=group_id)
            expenses = models.Bill.objects.filter(group_id=group)
            data = {}
            
            for expense in expenses:
                for repayment in expense.repayments.all():
                    if repayment.from_user != repayment.to_user and repayment.amount != 0:
                        key = f"{repayment.to_user.name} owes {repayment.from_user.name}"
                        if key in data:
                            data[key]['amount'] += repayment.amount
                            data[key]['details'].append(repayment.amount)
                        else:
                            data[key] = {'amount': repayment.amount, 'details': [repayment.amount]}
            
            consolidated_data = [{"message": [f"{user} {data[user]['amount']} ({' + '.join(map(str, data[user]['details']))})" for user in data]}]

            return Response(consolidated_data)
        except models.Group.DoesNotExist:
            return Response(
                {'message': 'Group Does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )
