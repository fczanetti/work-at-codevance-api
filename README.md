![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Fwork-at-codevance-api%2Fmain%2FPipfile.lock&query=%24._meta.requires.python_version&label=Python&labelColor=%232b5b84&color=%232d333b)
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Fwork-at-codevance-api%2Fmain%2FPipfile.lock&query=%24.default.django.version&label=Django&labelColor=%230c3c26&color=%232d333b)
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Fwork-at-codevance-api%2Fmain%2FPipfile.lock&query=%24.default.djangorestframework.version&label=Django%20REST%20framework&labelColor=%23a30000&color=%232d333b)
![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffczanetti%2Fwork-at-codevance-api%2Fmain%2FPipfile.lock&query=%24.default.celery.version&label=Celery&labelColor=%23348613&color=%232d333b)


![CI](https://github.com/fczanetti/work-at-codevance-api/actions/workflows/workflow.yml/badge.svg)
[![codecov](https://codecov.io/gh/fczanetti/work-at-codevance-api/graph/badge.svg?token=rVXgWFHtWW)](https://codecov.io/gh/fczanetti/work-at-codevance-api)

# Work at Codevance API

Welcome to Codevance API. This is a simple REST API built with Django REST framework, and it is supposed to help a company to deal with payments to its suppliers. 

Imagine that a company has a lot of suppliers, and it has to regularly pay them for their products. These payments have a specific date to be paid, but, if both sides agree, they can be paid before the due date with a discount in the original value. The discount calculation is based on a fixed interest rate and also the number of days in advance. The more days in advance, the bigger the discount. And using this API the company and its suppliers will be able to register payments, request anticipations, approve or deny them, each side with its own permissions.

If necessary, you can check the requirementes [here](https://github.com/fczanetti/work-at-codevance-api/blob/main/project_instructions.md).

# Content

- [Database models](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#database-models)
- [Folder structure](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#folder-structure)
- [Permissions](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#permissions)
   - [Common user](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#common-user)
   - [Supplier](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#supplier)
   - [Operator](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#operator)
   - [Admin / Django superuser / staff](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#admin--django-superuser--staff)
   - [Custom RequestPermission](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#custom-requestpermission)
- [How to install and test](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#how-to-install-and-test)
- [How to install and test with Docker](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#how-to-install-and-test-with-docker)
- [Initial data](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#initial-data)
- [API documentation](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#api-documentation)
   - [Listing elements](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-elements)
   - [Endpoints](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#endpoints)
   - [Making requests](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#making-requests)
      - [Generate token (JWT)](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#generating-a-new-jwt-token)
      - [Refresh token (JWT)](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#refreshing-the-jwt-token)
      - [List payments](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-payments)
      - [Filter payments](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#filtering-payments)
      - [Create payments](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#creating-payments)
      - [Retrieve payments](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#retrieving-payments)
      - [Create anticipations](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#creating-anticipations)
      - [Update anticipations](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#updating-anticipations)
      - [List requestLogs](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-requestlogs)
- [New value calculation](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#new-value-calculation)
- [How to deploy](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#how-to-deploy)
- [Integrations](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#integrations)
   - [AWS](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#aws)
   - [SendGrid](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#sendgrid)
   - [CloudAMQP](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#cloudamqp)
   - [Sentry](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#sentry)
- [Main libraries](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#main-libraries)

# Database models
 ```mermaid
 classDiagram
 direction RL
 
 User "1" <--> "1" Supplier
 RequestLog "*" <--> "1" Anticipation
 RequestLog "*" <--> "1" User
 Anticipation "1" <--> "1" Payment
 Payment "*" <--> "1" Supplier


 class User {
    - id ~int~, ~unique~
    - first_name ~str~
    - email ~str~, ~unique~
    - password ~str~
    - is_operator ~bool~
 }

 class Supplier {
    - id ~int~, ~unique~
    - user_id ~int~ FK
    - corporate_name ~str~
    - reg_number ~str~
 }

 class Payment {
    - id ~int~, ~unique~
    - supplier_id ~int~ FK
    - creation_date ~date~
    - due_date ~date~
    - value ~decimal~
 }

 class Anticipation {
    - id ~int~, ~unique~
    - payment_id ~int~ FK
    - creation_date ~date~
    - new_due_date ~date~
    - new_value ~decimal~
    - update_date ~date~
    - status ~str~
 }

 class RequestLog {
    - id ~int~, ~unique~
    - anticipation_id ~int~, FK
    - created_at ~date~
    - user_id ~int~, FK
    - action ~str~
 }

 ```

# Folder structure

Main folders and files:

```
├── 📂 work-at-codevance-api
|   ├── 📂 contrib
|   |   ├── env-sample
|   ├── manage.py
|   ├── Pipfile
|   ├── Pipfile.lock
|   ├── .flake8
|   ├── pytest.ini
|   ├── README.md
|   ├── 📂 codevance_api
|   |   ├── urls.py
|   |   ├── settings.py
|   |   ├── celery.py
|   |   ├── 📂 base
|   |   |   ├── 📂 migrations
|   |   |   ├── 📂 tests
|   |   |   ├── admin.py
|   |   |   ├── models.py
|   |   |   ├── views.py
|   |   ├── 📂 payments
|   |   |   ├── 📂 migrations
|   |   |   ├── 📂 templates
|   |   |   ├── 📂 tests
|   |   |   ├── 📂 fixtures
|   |   |   |   ├── initial_data.json
|   |   |   ├── admin.py
|   |   |   ├── models.py
|   |   |   ├── views.py
|   |   |   ├── payments.py
|   |   |   ├── permissions.py
|   |   |   ├── serializers.py
|   |   |   ├── tasks.py
|   |   |   ├── urls.py
|   |   |   ├── validators.py

```

# Permissions

There different kinds of users that can authenticate on this application, and here we are describing some details about their implementation:

### Common User

This is the base User, and it has no permissions at all. In order to create a Supplier, this common User instance needs to be created first, and then it has to be informed in the 'user' field of the new Supplier instance.

### Supplier

The Supplier, once created, has the following permissions:

- can create payments for himself;
- can create anticipations for his own payments;
- can list his own payments;
- can retrieve his payments using the payment ID.

### Operator

The Operator instance is one that has all permissions. It can:

- create payments for any suppliers;
- create anticipations for payments that belong to any Supplier;
- list payments from all Supplier;
- retrieve payments from any Supplier;
- approve or deny anticipations from payments that belong to any Supplier.

The procedure to create an Operator is almost the same as to create a Common User, we just need to mark the 'is_operator' option when creating via Admin page, or inform ```is_operator=True``` if creating via command line. 

### Admin / Django superuser / staff

This is the Django User that can access the Admin page. In this implementation, the Admin User can not make requests. In order to use this instance to make requests, you have to edit it by setting its 'is_operator' field to True.

### Custom RequestPermission

There is a custom permission implemented named RequestPermission, and this is the one that only allow requests from Supplier or Operator instances. It's located in the 'permissions.py' module inside 'payments' directory. Changing this implementation may cause problems in the application.

# How to install and test

The following instructions assume you are using pipenv as your virtual management tool, and also a Linux working environment.

1 - Clone this repository:

```
git clone git@github.com:fczanetti/work-at-codevance-api.git
```

2 - Install the required libraries. This command also creates a virtual environment:

```
pipenv sync -d
```

3 - Activate the virtual environment:

```
pipenv shell
```

4 - Copy the content from 'env-sample' file located inside 'contrib' directory to a new file called .env:

```
cp contrib/env-sample .env
```

5 - In the new .env file you have a variable called DATABASE_URL, and this is to be used with Docker. Comment it, so Django can connect with an sqlite3 database that it automatically creates for you.

6 - Comment another variable in your .env file called CELERY_BROKER_URL. This is not necessary now and, if not commented, can cause some errors when creating or updating anticipations;

7 - Apply the database migrations. The database file (db.sqlite3) will be created when you run this command:

```
python manage.py migrate
```

8 - If you wish, you can [load some initial data](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#initial-data) in order to make it easier for you to start making requests.

9 - Run tests to make sure everything is working fine:

```
pytest
```

10 - You can now start Django server and test some requests.

# How to install and test with Docker

Installing this application with Docker will allow you to use Celery to send asynchronous emails when creating or updating an Anticipation. In the root of the project there's a 'docker-compose.yml' file, and this one will be responsible for creating a PostgreSQL and RabbitMQ instances for us.

1 - Follow the steps 1 to 4 from [this tutorial](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#how-to-install-and-test);

2 - With your .env file created, start the Docker containers:

```
docker compose up -d
```

3 - Apply the database migrations:

```
python manage.py migrate
```

4 - If you wish, [load some initial data](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#initial-data) to the database:

```
python manage.py loaddata initial_data.json
```

5 - Run tests to make sure everything is working fine:

```
pytest
```

6 - Start celery worker to be able to send emails: 

```
celery -A codevance_api worker -l INFO
```

It's important to note that you won't send real emails by only doing this, the emails will only be printed in your command line, the same place where you started celery worker. This happens because of the EMAIL_BACKEND we have configured in our .env, that is a Django setting to be used during development. 

To send real emails, all the email settings listed on your .env file have to be properly configured.

7 - Start Django server and test some requests:

```
python manage.py runserver
```

# Initial data

In order to make it easier to test after installing, there are some initial data that can be loaded to the database using the following command:

```
python manage.py loaddata initial_data.json
```

By doing this, you'll create these instances (fake emails):

- User 01 - email: user01@email.com / password: user01
- User 02 - email: user02@email.com / password: user02
- Supplier 01 - user: User 01
- Supplier 02 - user: User 02
- Operator 01: email: operator01@email.com / password: operator01
- 3 different payments related to Supplier 01
- 3 different payments related to Supplier 02

# API documentation

## Listing elements

When listing elements via endpoints, payments for example, the max number of items returned will be 10 per page. If you need a different number, feel free to change it in settings.py. There is a setting in this module called REST_FRAMEWORK, and it is a dictionary with one of its keys named PAGE_SIZE. This is the value you have to change.

## Endpoints

Here is a list of the available endpoints. Continue reading or use the 'More details' links if you need more explanations.

| Action | Endpoint | Method | Status Code | Guide |
| --- | --- | :---: | :---: | :---: |
| Generate token (JWT) | `/api/token/` | POST | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#generating-a-new-jwt-token) |
| Refresh token (JWT) | `api/token/refresh/` | POST | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#refreshing-the-jwt-token) |
| List payments | `/api/payments/` | GET | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-payments) |
| Filter payments | `/api/payments/?status={status}` | GET | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#filtering-payments) |
| Create payments | `/api/payments/` | POST | 201 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#creating-payments) |
| Retrieve payments | `/api/payments/{payment_id}/` | GET | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#retrieving-payments) |
| Create anticipations | `/api/anticipations/` | POST | 201 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#creating-anticipations) |
| Update anticipations | `/api/anticipations/{anticipation_id}/` | PATCH | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#updating-anticipations) |
| List RequestLogs | `/api/logs/` | GET | 200 | [More details](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-requestlogs) |

## Making requests

All requests have to be authenticated to work, and the authentication is made via Json Web Token (JWT). Keep reading to see how to genereta a token and how to send authenticated requests.

### Generating a new JWT token

A JWT (Json Web Token) authentication was implemented in this API. Basically, you have to generate a token and include it in all requests in order to authenticate.

To create a new token the email and password are necessary, and a POST request has to be made to ```/api/token/``` as follows:

```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "<USER_EMAIL>", "password": "<USER_PASSWORD>"}' \
  http://127.0.0.1:8000/api/token/
```

If successfull, you will receive a 200 status code response with the following content:

```
{
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}
```

Once you have your access token, you can start making authenticated requests to protected views. Here is an example of a GET request:

```
curl \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  http://127.0.0.1:8000/api/payments/
```

### Refreshing the JWT token

When creating an access token as shown in the previous tutorial, we receive two different tokens, the access and the refresh ones. The access is used to authenticate requests, but it has a short expiration time. Once it expires, we have to use our refresh token to get a new one.

To have a new access token, make a POST request to ```/api/token/refresh/``` as shown in this example:

```
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<REFRESH_TOKEN>"}' \
  http://127.0.0.1:8000/api/token/refresh/
```

If successfull, you will receive a 200 status code response with the following content:

```
{
  "access": "<NEW_ACCESS_TOKEN>"
}
```

### Listing payments

To list payments, send a GET request to ```/api/payments/```. If successfull, you will receive a 200 status code response in the following format:

```
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "supplier": 1,
      "creation_date": "2024-07-26",
      "due_date": "2024-08-25",
      "value": "20000.00"
    },
    {
      "id": 3,
      "supplier": 1,
      "creation_date": "2024-07-26",
      "due_date": "2024-08-25",
      "value": "30000.00"
    }
  ]
}
```

If you are filtering payments using an Operator account, you will be able to see payments related to all suppliers. But, if you list payments using a Supplier account, you'll only see payments related to this specific Supplier.

### Filtering payments

You can also filter payments when listing. To do so, you have to inform the payment status as a URL query parameter. This is the format: ```/api/payments/?status={status}```.

You can see [here](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#database-models) that 'status' is not a field created for Payment model, it is just a parameter used to choose which payments to return. Here you have a more detailed explanation on how the filtering status work:

- **A**: this status is used to retrieve the payments that are available to anticipate. It means that these payments have no anticipations related/created to them, and their due_date was not reached yet;

- **U**: this is the status used to return all payments that are no longer available to anticipate (unavailable), what means that their due_date was already reached (less than or equal today). These payments can have an anticipation related, but the anticipation status can not be "A" (anticipated) or "D" (denied), it has to be "PC" (pending confirmation). This is to simulate occasions when an Anticipation is created but not approved or denied, and as time goes by the payment becomes unavailable because its due_date is reached;

- **PC**: if chosen, this status will return payments that has anticipations related, and the status of these anticipations are "PC" (pending confirmation). Also, the Payment due_date can not have been reached, otherwise it would be shown when filtering the unavailable for anticipation ones;

- **AN**: this is the status used to return payments that have anticipations related, and these anticipations must have a "A" (anticipated) status;

- **D**: finally, you can also filter payments that has anticipations related, but these anticipations were not approved, but denied (status="D").

The format of the response will be the same as when [listing payments](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#listing-payments).

### Creating payments

In order to create new payments, send a POST request to ```/api/payments/```. It will be necessary to inform a Supplier ID (int), a due date (ISO 8601 format) and a value (decimal). This is the format:

```
{
   "supplier": 1,
   "due_date": "2024-08-20",
   "value": 1000
}
```

If successfull, the response will have a 201 status code and the Payment created will return as follows:

```
{
  "id": 8,
  "supplier": 1,
  "creation_date": "2024-07-28",
  "due_date": "2024-08-20",
  "value": "1000.00"
}
```

Using an Operator account you can create payments to any Supplier, but using a Supplier account you can only create payments for this Supplier.

### Retrieving payments

To retrieve a Payment, send a GET request to ```/api/payments/{payment_id}/``` informing the Payment ID (int). If successfull, the response will have a 200 status code and will look like this:

```
{
  "id": 8,
  "supplier": 1,
  "creation_date": "2024-07-28",
  "due_date": "2024-08-20",
  "value": "1000.00"
}
```

Suppliers can only retrieve their own payments, but operators can retrieve payments from any Supplier.

### Creating anticipations

To create an Anticipation you'll have to send a POST request to ```/api/anticipations/``` informing a Payment ID (int) and a new due date (ISO 8601 format):

```
{
   "payment": 8,
   "new_due_date": "2024-08-10"
}
```

If successfull, a 201 status code response will return in the following format:

```
{
  "id": 11,
  "payment": 8,
  "creation_date": "2024-07-28",
  "new_due_date": "2024-08-10",
  "new_value": "990.00",
  "update_date": "2024-07-28",
  "status": "PC"
}
```

An Operator can create anticipations for payments that belong to any Supplier, but a Supplier can only create anticipations for his own payments. Only one Anticipation is allowed for a Payment.

### Updating anticipations

Anticipations, when created, have a default "PC" (pending confirmation) status. To approve or deny an Anticipation you have to update it to a status equal to "A" or "D" (approved or denied). These are the only allowed status to use when updating. 

To do so, send a PATCH request (partial update) to ```/api/anticipations/{anticipation_id}/``` informing the Anticipation ID in the URL. This request also needs a body in the following format:

```
{
   "status": "A"
}
```

If successfull, you'll receive a 200 status code response that looks like this:

```
{
  "id": 11,
  "payment": 8,
  "creation_date": "2024-07-28",
  "new_due_date": "2024-08-10",
  "new_value": "990.00",
  "update_date": "2024-07-28",
  "status": "A"
}
```

Anticipations can only be updated by operators.

### Listing requestlogs

Every time an Anticipation in created or updated a RequestLog is also created. To list them, send a GET request to ```/api/logs/```. If successfull, you will receive a 200 status code response in the following format:

```
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 11,
      "anticipation": 11,
      "created_at": "2024-07-28",
      "user": 3,
      "action": "R"
    },
    {
      "id": 12,
      "anticipation": 11,
      "created_at": "2024-07-28",
      "user": 3,
      "action": "A"
    }
  ]
}
```

Some considerations about this representation:

- user: this field shows the ID of the user that created or updated the Anticipation;
- action: this is the action that was taken, where "R" means "Requested", "A" means "Approved" and "D" means "Denied.

An Operator can list requestlogs from anticipations that belong to all suppliers, but a Supplier can only list the requestlogs that belongs to its own anticipations.

# New value calculation

When an Anticipation is created the number of days between the original due date and the new due date is used to calculate the amount of discount. Also, a fixed interest rate of 3% / month is used. Here is an example:

Formula:

- nv = new value
- ov = original value
- da = days in advance
- 0.03 = fixed interest rate

$$
nv = ov - (ov*\frac{(0.03)}{30} * da)
$$

- original due date: 2024-10-01
- new due date: 2024-09-15
- original value: 1000.00

$$
nv = 1000 - (1000*\frac{(0.03)}{30} * 16)
$$

$$
nv = 1000 - (16)
$$

$$
nv = 984.00
$$

# How to deploy

Here we have a procedure of how to deploy this application on [Heroku](https://www.heroku.com/home). We are going through a step by step that will be enough for this deployment, but if you need a more detailed explanation about each step taken you can [visit this link](https://devcenter.heroku.com/articles/getting-started-with-python).

### Requirements:

- A [verified account](https://signup.heroku.com/login) on Heroku;
- An [Eco dynos plan](https://devcenter.heroku.com/articles/eco-dyno-hours) subscription (the most basic one);
- Install the [Heroku Command Line Interface](https://devcenter.heroku.com/articles/heroku-cli) (CLI);
- An [AWS](https://aws.amazon.com/) account;
- A [SendGrid](https://sendgrid.com/en-us) account;
- A [CloudAMQP](https://www.cloudamqp.com/) account;

Having the first requirements attended, we can start following the next steps.

### 1 - Login to Heroku

Inside your project diretory and using your command line run the following command:

```
heroku login
```

### 2 - Create a Procfile

After authenticated, create a file in the root directory of the project named [Procfile](https://devcenter.heroku.com/articles/procfile). In this file, insert this content that will be responsible for starting our application server on Heroku, running the migrations to our new database and starting our Celery worker:

```
web: gunicorn codevance_api.wsgi
release: ./manage.py migrate --no-input
worker: python -m celery -A codevance_api worker -l info
```

OBS: this file is already created in our root directory.

### 3 - Create the application on Heroku

Having a Procfile set, we can create our application on Heroku using this command:

```
heroku apps:create <APP_NAME>
```

You can choose an APP_NAME that best suits you.

### 4 - Provision a database

With our new application created, we can [provision a database](https://devcenter.heroku.com/articles/provisioning-heroku-postgres) to it. The database we are going to use is PostgreSQL, and Heroku offers an add-on that we can take advantage of. The next command is enough for creating a database linked to our application, and a DATABASE_URL environment variable will be automatically created for us in the platform.

```
heroku addons:create heroku-postgresql:<PLAN_NAME>
```

The <PLAN_NAME> is the PostgreSQL plan we are choosing. The [essential-0](https://devcenter.heroku.com/articles/heroku-postgres-plans#essential-tier) is the most basic one in these days, and that is enough for us. This is the final command we can use to create the database:

```
heroku addons:create heroku-postgresql:essential-0
```

### 5 - Set the environment variables

We can use the next command to set the environment variables for our new application on Heroku, or we can also access the application page, go to settings and set it there in the 'Config Vars' section.

```
heroku config:set <VARIABLE>=<VALUE>
```

These are the required ones:

- DEBUG=False
- SECRET_KEY=
   - for the SECRET_KEY variable you can use a Django function to create a random one. This function is called 'get_random_secret_key()', and you can import it from 'django.core.management.utils'
- ALLOWED_HOSTS=
   - the value for this variable is the domain of your app. If you didn't configure a specific domain you have to use the one created by Heroku. You can find it in the settings page of you application, in the Domains section. For example: 'codevanceapi-25a5ebc88ad9.herokuapp.com'
- CELERY_BROKER_URL=
   - see the [integration with CloudAMQP](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#cloudamqp) to get this value
- CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS=True

- EMAIL_USE_TLS=True
- EMAIL_PORT=587
- EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
- EMAIL_HOST_USER=
- EMAIL_HOST=
- EMAIL_HOST_PASSWORD=
- DEFAULT_FROM_EMAIL=
   - see the [integration with SendGrid](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#sendgrid) to have the values for EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD and DEFAULT_FROM_EMAIL

- AWS_ACCESS_KEY_ID=
- AWS_SECRET_ACCESS_KEY=
- AWS_STORAGE_BUCKET_NAME=
   - see [integration with AWS](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#aws) to have the values for AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

### 6 - Deploy the application

With all the required environment variables set we can deploy the application.

```
git push heroku main
```

If you are not working on the main branch you can use this command:

```
git push heroku <BRANCHNAME>:main
```

### 7 - Start Celery worker on Heroku

Use this command to start the Celery worker that was defined in our Procfile:

```
heroku ps:scale worker=1
```

### 8 - Create a Django superuser

If everything worked fine so far our application is already running. We can create a Django superuser to be able to access the Admin page, create some users and start testing.

```
heroku run bash
```

This command allows you to access the machine where your application is placed, and then you can use the next command to create de superuser:

```
python manage.py superuser
```

### 9 - Connect with GitHub for continuous delivery

Check [this tutorial](https://devcenter.heroku.com/articles/github-integration) to see how you can deploy the application automatically every time you push new changes to the branch you choose (usually the 'main' branch).

# Integrations

### AWS

This application was integrated with AWS S3 in order to have the static files served in production environment. Follow these steps to have the values of the AWS environment variables that we have to configure on our app in Heroku.

- create en IAM user on AWS platform and attach to it a policy called AmazonS3FullAccess;
- create an access key for this user. This key has an ID (AWS_ACCESS_KEY_ID) and a value (AWS_SECRET_ACCESS_KEY), both will be used;
- create a bucket for the static files. On this bucket, attach a policy that allows the IAM user created to 'PutObject' in all its folders. You will have to choose a name for this bucket, and this is the value we use in our AWS_STORAGE_BUCKET_NAME environment variable.

### SendGrid

This integration was made in order to have an email server to deliver emails for us. Follow the next instructions to have all we need to configure our email environment variables.

- in 'Marketing' section, create a new 'Sender' to be used to send emails. You'll have to verify the email used to create the Sender;
- in 'Email API' section, click on the 'Integration Guide' link and choose the option 'SMTP Relay';
- create an API key filling a name, and then save the values shown: Server, Username and Password. These will be used to set the environment variables EMAIL_HOST, EMAIL_HOST_USER and EMAIL_HOST_PASSWORD respectively. The DEFAULT_FROM_EMAIL variable is the email used when creating the 'Sender'.

### CloudAMQP

In order to have a RabbitMQ service running, required to send emails, a suggestion is CloudAMQP platform. On their website, follow these steps:

- create a RabbitMQ free instance and access its main page;
- in 'AMQP details', copy and save the URL shown to be used as our CELERY_BROKER_URL environment variable.

### Sentry

This project also has an integration with Sentry in order to catch errors that may be raised in production environment. To have the errors catched by Sentry:

- create a project in Sentry platform:
- after creating, copy the 'dsn' value informed by Sentry and use it to define the SENTRY_DSN environment variable.

# Main libraries

- **Django**: main framework used to build the application;
- **Django REST framework**: used to build the REST API;
- **pytest-django**: used to write all the tests;
- **python-decouple**: used to deal with variables from development and production environments;
- **dj-database-url**: used to parse the DATABASE_URL;
- **Psycopg2**: used to connect Python and PostgreSQL database;
- **Celery**: send emails asynchronously;
- **djangorestframework-simplejwt**: JWT authentication;
- **Gunicorn**: application server for production environment;
- **django-storages**: used for static files storage in AWS S3 (Django Admin page);
- **Collectfast**: more efficient 'collectstatic' command;
- **Sentry**: catch errors in production environment;
- **flake8**: code styling;
- **pytest-cov**: generate test coverage reports;
- **codecov**: upload and save test coverage reports;
- **django-debug-toolbar**: analyse database queries in development environment.
