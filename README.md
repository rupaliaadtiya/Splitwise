The Expense Tracker System described in the architecture diagram follows a standard API-based design using Django and Django Rest Framework (DRF). The key components of the system are:

1. Views (`views.py`):
   - `AddUserApiView`: Handles the creation of users.
   - `LoginApiView`: Handles user login and generates JWT tokens.
   - `CreateGroupApiView`: Handles the creation of groups.
   - `AddUserToGroupApiView`: Manages the addition of users to existing groups.
   - `CreateExpenseApiView`: Handles the creation of expenses, including the logic for splitting expenses among group members.
   - `ShowGroupDetailsApiView`: Retrieves and displays details of group expenses.

2. Models (`models.py`):
   - `User`: Represents a user.
   - `Group`: Represents a group of users.
   - `Bill`: Represents an expense bill, including details like amount, date, and split type.
   - `Debt`: Represents debts between users, used for tracking repayments.
   - `BillUser`: Represents individual user details for a bill, including their paid and owed shares.

3. URLs (`urls.py`):
   - Defines the API endpoints for adding users, logging in, creating groups, adding users to groups, creating expenses, and retrieving group details.

1. Add User
Endpoint: POST /api/addUser
Request:
json
Copy code
{
  "email": "rupali@gmail.com",
  "name": "Rupali",
  "mobile": "8872396530",
  "password": "Rupali@1234"
}