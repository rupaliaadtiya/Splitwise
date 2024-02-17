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

{
	"info": {
		"_postman_id": "688a872e-2548-483a-a270-64caf9421860",
		"name": "Splitwise",
		"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
		"_exporter_id": "32996842"
	},
	"item": [
		{
			"name": "Add User",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"email\": \"rupali@gmail.com\",\n    \"name\": \"Rupali\",\n    \"mobile\": \"8872396530\",\n    \"password\": \"Rupali@1234\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{url}}/addUser",
					"host": [
						"{{url}}"
					],
					"path": [
						"addUser"
					]
				}
			},
			"response": []
		},
		{
			"name": "Login",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"email\": \"rupali@gmail.com\",\n    \"password\": \"Rupali@1234\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{url}}/login",
					"host": [
						"{{url}}"
					],
					"path": [
						"login"
					]
				}
			},
			"response": []
		},
		{
			"name": "Create Group",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"group_name\": \"CSB\",\n    \"members\": [\n        \"2\"\n    ]\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{url}}/createGroup",
					"host": [
						"{{url}}"
					],
					"path": [
						"createGroup"
					],
					"query": [
						{
							"key": "group_name",
							"value": "test1",
							"disabled": true
						}
					]
				}
			},
			"response": []
		},
		{
			"name": "Add member to Group",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"group_id\":\"1\",\n    \"user_id\": \"5\"\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{url}}/addUserToGroup",
					"host": [
						"{{url}}"
					],
					"path": [
						"addUserToGroup"
					]
				}
			},
			"response": []
		},
		{
			"name": "Add Group Expense",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\r\n    \"users\" : [\r\n        \"2\",\r\n        \"3\",\r\n        \"4\",\r\n        \"5\"\r\n    ],\r\n    \"amount\": 1000,\r\n    \"paid_by\": \"2\",\r\n    \"group_id\": \"1\",\r\n    \"date\":\"2024-02-16\",\r\n    \"bill_name\":\"Electricity Bill\",\r\n    \"split_type\":\"equal\",\r\n    \"notes\":\"Electricity Bill Paid By Rupali\"\r\n}",
					"options": {
						"raw": {
							"language": "json"
						}
					}
				},
				"url": {
					"raw": "{{url}}/addExpense",
					"host": [
						"{{url}}"
					],
					"path": [
						"addExpense"
					]
				}
			},
			"response": []
		},
		{
			"name": "Show Group Expenses",
			"request": {
				"method": "GET",
				"header": [],
				"url": {
					"raw": "{{url}}/groupDetails?id=1",
					"host": [
						"{{url}}"
					],
					"path": [
						"groupDetails"
					],
					"query": [
						{
							"key": "id",
							"value": "1"
						}
					]
				}
			},
			"response": []
		}
	],
	"event": [
		{
			"listen": "prerequest",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		},
		{
			"listen": "test",
			"script": {
				"type": "text/javascript",
				"exec": [
					""
				]
			}
		}
	],
	"variable": [
		{
			"key": "url",
			"value": "http://127.0.0.1:8000/api",
			"type": "string"
		}
	]
}