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

**This project is in construction, and more details will be added soon.**

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
- [New value calculation](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#new-value-calculation)
- [How to deploy](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#how-to-deploy)

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

6 - Apply the database migrations. The database file (db.sqlite3) will be created when you run this command:

```
python manage.py migrate
```

7 - If you wish, you can [load some initial data](https://github.com/fczanetti/work-at-codevance-api?tab=readme-ov-file#initial-data) in order to make it easier for you to start making requests.

8 - Run tests to make sure everything is working fine:

```
pytest
```

9 - You can now start Django server and test some requests.

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

Here is a list of the available endpoints. Continue reading below if you need more details.

| Action | Endpoint | Method | Status Code |
| --- | --- | :---: | :---: |
| Generate token (JWT) | `/api/token/` | POST | 200 |
| Refresh token (JWT) | `api/token/refresh/` | POST | 200 |
| List payments | `/api/payments/` | GET | 200 |
| Create payments | `/api/payments/` | POST | 201 |
| Retrieve payments | `/api/payments/{payment_id}/` | GET | 200 |
| Create anticipations | `/api/anticipations/` | POST | 201 |
| Update anticipations | `/api/anticipations/{anticipation_id}/` | PATCH | 200 |

## Making requests

In construction

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

In construction
