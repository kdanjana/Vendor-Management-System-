# Vendor-Management-System
Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.

Pre-requisite:
Python
DJango
Django REST Framework

Step1: 
$ mkdir vendor
$ cd vendor
#Create a Virtual Environment
$pip install virtualenv
$virtualenv venv
#Activate virual environment:
$venv\Scripts\Activate
#Install django and DRF:
$pip install django
$pip install djangorestframework

Step2:
Clone this repo

Step3:
Database migration
$python manage.py makemigrations
$python manage.py migrate

Step4:
Superuser creation and Token generation
$ python manage.py createsuperuser
$ python manage.py runserver
$curl -X POST -d "username=superuser_username&password=superuser_password" http://localhost:8000/api-token-auth/

Access as Django Admin:
http://127.0.0.1:8000/admin/ and log in using the superuser credentials.

Step5: Accessing API endpoints 
Here we are testing API endpoints using curl commands
1. POST /api/vendors/: Create a new vendor.
$ curl -H "Authorization: Token your_obtained_token" -X POST http://127.0.0.1:8000/api/vendors/ -d "vendor_code=1&name=Raja&contact_details=Contact1&address=Address1"
using httpie:
2. GET /api/vendors/: List all vendors.
$ curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/vendors/
3. GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
$ curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/vendors/{vendor_id}/
4. PUT /api/vendors/{vendor_id}/: Update a vendor's details.
$ curl -H "Authorization: Token your_obtained_token" -X PUT http://127.0.0.1:8000/api/vendors/{vendor_id}/ -d "vendor_code=updated code&name=Updated Vendor Name&contact_details=Updated Contact Details&address=Updated Address"
5. DELETE /api/vendors/{vendor_id}/: Delete a vendor.
$ curl -H "Authorization: Token your_obtained_token" -X DELETE http://127.0.0.1:8000/api/6. POST /api/purchase_orders/: Create a purchase order.
$ curl -H "Authorization: Token your_obtained_token" -X POST http://127.0.0.1:8000/api/purchase_orders/ -d "po_number=01&vendor=01&order_date=2024-05-01T12:00:00&delivery_date=2024-05-04T12:00:00&items=[{"item_name":"Item 1","quantity": 10 },{"item_name": 10 }]&quality_rating=4.5&issue_date=2024-05-01T12:00:00&status=updated&acknowledgment_date=2024-05-02T12:00:00"
7. GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.
$ curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/purchase_orders/
8. GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
$ curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/purchase_orders/{po_id}/
9. PUT /api/purchase_orders/{po_id}/: Update a purchase order.
$ curl -H "Authorization: Token your_obtained_token" -X PUT http://127.0.0.1:8000/api/purchase_orders/{po_id}/ -d "po_number=updatedno&vendor=updatedvno&order_date=2024-05-02T12:00:00&delivery_date=2024-05-15T12:00:00&items=[{"item_name": 10 },{"item_name":10}]&quality_rating=5&issue_date=2024-05-01T12:00:00&status=updated&acknowledgment_date=2024-05-01T12:00:00"
10. DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.
$ curl -H "Authorization: Token your_obtained_token" -X DELETE http://127.0.0.1:8000/api/purchase_orders/{po_id}/
11. GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.
$ curl -H "Authorization: Token your_obtained_token" http://127.0.0.1:8000/api/vendors/1/performance/
12. /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge
POs.
$ curl -H "Authorization: Token your_obtained_token" -X PATCH http://127.0.0.1:8000/api/purchase_orders/{po_id}/acknowledge/ --data "acknowledgment_date=2024-05-01T12:00:00Z"

