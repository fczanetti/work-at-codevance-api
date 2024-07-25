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

In construction

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