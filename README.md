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

API Contracts

**POST /addUser**
----
  Add user in the system.
* **URL Params**  
  None
* **Data Params**  
{
    "email": "rupali@gmail.com",
    "name": "Rupali",
    "mobile": "8872396530",
    "password": "Rupali@1234"
}
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
    "message": "User added successfully",
    "data": {
        "id": 3,
        "email": "rupali@gmail.com",
        "name": "Rupali",
        "mobile": "8872396530"
    }
}
```

**POST /login**
----
  Login user in the system.
* **URL Params**  
  None
* **Data Params**  
{
    "email": "rupali@gmail.com",
    "password": "Rupali@1234"
}
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
    "user_id": 2,
    "email": "rupali@gmail.com",
    "name": "Rupali",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwODI1MDMyNSwiaWF0IjoxNzA4MTYzOTI1LCJqdGkiOiJhMjdmNjEyMWQzZWY0ZmY4YmY4MzY4Y2Y5YTk2OThmOCIsInVzZXJfaWQiOjJ9.vcUo3C0tEJCGSmXD4V6qQwTpBlDYVV7WGPVsjxJ_ki0",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MTY2OTI1LCJpYXQiOjE3MDgxNjM5MjUsImp0aSI6ImVhN2JiMzI5ZjYzNDRmNDI4ODY5YjA0NDY1OWI3YzcxIiwidXNlcl9pZCI6Mn0.QAqwuehDViyzt66m8fP9O1VN6MuW7xLGksH5IQSj-7M"
}
```

**POST /createGroup**
----
  Create a group.
* **URL Params**  
  None
* **Data Params**  
{
    "group_name": "Party",
    "members": [
        "2"
    ]
}
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
    "message": "Group Created successfully"
}
```

**POST /addUserToGroup**
----
  Add a user to a group.
* **URL Params**  
  None
* **Data Params**  
{
    "group_id":"2",
    "user_id": "5"
}
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
    "message": "User successfully added to group"
}
```

**POST /addExpense**
----
  Add an expense, including splitting among group members.
* **URL Params**  
  None
* **Data Params**  
{
    "users" : [
        "2",
        "3",
        "4",
        "5"
    ],
    "amount": 1000,
    "paid_by": "2",
    "group_id": "1",
    "date":"2024-02-16",
    "bill_name":"Electricity Bill",
    "split_type":"equal",
    "notes":"Electricity Bill Paid By Rupali"
}
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
{
    "message": "Expense Created successfully"
}
```

**POST /groupDetails**
----
  Retrieve details of group expenses.
* **URL Params**  
    *Required:* `id=[integer]`
* **Data Params**  
None
* **Headers**  
  Content-Type: application/json  
* **Success Response:**  
* **Code:** 200  
  **Content:**  
```
[
    {
        "message": [
            "Shivani owes Rupali 500 (250 + 250)",
            "Ritisha owes Rupali 500 (250 + 250)",
            "Sakshi owes Rupali 500 (250 + 250)"
        ]
    }
]
```