Hoops - A simple budgeting application
===

Quick Start
---

A live version of this applications is running at [hoops.andrew-chang-dewitt.dev](https://hoops.andrew-chang-dewitt.dev) and can be interacted with like any API.

### Authentication

There's a login feature implemented using OAuth2 compliant form input to get a JWT that needs to be included in the `Authorization` header of every request made to a protected endpoint.

#### Creating a User

To be able to log in, you'll first need to create a User by making a `POST` request to `/user` with a body complying with the following schema:

```
{
    handle: string
    full_name: string
    preferred_name: string (optional)
    password: string
}
```

An example using curl:

```
curl -X 'POST' \
  'https://hoops.andrew-chang-dewitt.dev/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "handle": "test",
  "full_name": "Test User",
  "preferred_name": "Testy",
  "password": "test"
}'
```


#### Logging in

You can get a token in one of two ways:

1. Manually constructing a `POST` request to `hoops.andrew-chang-dewitt.dev/token` manually that includes a valid username & password. An example using curl:

```
curl -X 'POST' \
  'https://hoops.andrew-chang-dewitt.dev/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=test&password=test&scope=&client_id=&client_secret='
```

You'll then need to save the token value that's returned in the Response at the key `access_token` on the Response body.
The body will look something like this:

```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhMWNiNjI5MS1kZDdmLTRkYTEtODFjYy04MzQ1ODlhZTAxZGUiLCJleHAiOjE2Mzg5MDQ4NDR9._8-EPf9k5Ry_akXGCIgBFI4c_n3qhRAWKBrsT1XQO0s",
  "token_type": "bearer"
}
```

2. Go to the live, interactive docs at [hoops.andrew-chang-dewitt.dev](https://hoops.andrew-chang-dewitt.dev) & use the "Authorize" button at the top right of the page to log in, then grab the token value the example created by making any authenticated query in the "Try it out" section of any protected endpoint.


Project Summary
---

Hoops is a back-end REST API serving JSON data for a budgeting application.
Inspired by the budgeting tools offered by a fintech I used to use before it was killed off in a merger, this API is essentially a CRUD web server with all the necessary endpoints to do basic "envelope-method" budget tracking & planning.
  
### Intended user:
  
A User of this project is defined as a client-side web-app that will consume this API over HTTPS. 
This means the UI of this application is the API itself.
The goal is for this hypothetical web application to be built later to create a GUI that can be used by my wife & I.
Then eventually this hypothetical web-app could be expanded as either an OSS release for self-hosting or a SAAS hosted option.
  
### What problem is project trying to solve?:

Planning & tracking spending in a flexible, extensible, & low-friction fashion while being usable by multiple people simultaneously. 
Modeled after my favorite now-defunct fintech's budgeting tools.

### Which technologies will you need (files, databases, GUIs?):

  1. Database (PostgreSQL&mdash;offers better types for currency via NUMERIC, UUID keys, & built-in password hashing tools)
  2. Web server (JSON REST API via FastAPI&mdash;offers better routing encapsulation via APIRouter & great type validation, API documentation, & is extensible via middleware functions)

### Hardware limitations

None that are of any concern for an app of this size & limited user-base.

### Visual design implications

There is no true visual design as this is just a RESTful API serving resources as JSON; however, the library used to create the server does automatically build out an interactive docs website.

Data Design
---

### Overall data structure

A PostgreSQL database containing the tables for the following data types.

Three core data types:

1. _**Transactions:**_ \
  Exactly what their name says: an amount of money either going in from or coming out to a specific payee at a specific time.
  
2. _**Envelopes:**_ \
  A concept that represents an amount of money reserved for a specific purpose (e.g. a savings goal like a vacation or an expense like rent or groceries).
  
3. _**Users:**_ \
  Also exactly what the name says: a person using this budgeting program.
  
Besides those three core data types, the following ancillary data types exist:
  
- _**Accounts:**_ \
  A bank account, credit card, cash hidden under the mattress, etc. 
  Individual Transactions belong to an Account.

The following Entity Relationship Diagram represents the database design:

![Entity Relationship Diagram](/data-er.svg)


### Implementation strategy

Data models are defined in SQL files & loaded into the database on application initialization. The application then uses a custom wrapper (one I wrote before this class) on aio-pg (which is itself a wrapper on psycopg2) to connect to the PostgreSQL database. Queries are constructed in application code as Model objects that organize queries by the data return type. Finally, the application creates API endpoints that use the Model objects' query methods to perform CRUD operations on user requests.

### Module structure

```
src
├── __init__.py
├── app.py
|     ^ *FastAPI application is defined here & router objects
|       (defined in src/routers/...) are added to the application
|       here as well*
├── config.py
|     ^ *simple configuration options are defined here*
├── database.py
|     ^ *database connection methods are defined here*
├── models
|   | ^ *data models, both SQL schemas & database queries (written
|   |   in python) are defined here*
│   ├── __init__.py
│   ├── account.py
│   ├── account.sql
│   ├── amount.py
|   |     ^ *a shared data type used in multiple Models*
│   ├── balance.py
│   ├── base.py
|   |     ^ *shared behavior for all Model objects here*
│   ├── envelope.py
│   ├── envelope.sql
│   ├── filters.py
│   ├── token.py
│   ├── transaction.py
│   ├── transaction.sql
│   ├── user.py
│   ├── user.sql
│   ├── z_relations.sql
│   └── z_view_balance.sql
|         ^ *I use a tool to manage database migrations for me and
|           it naively reads & executes sql files from src/models/ 
|           in alphabetical order, foreign key constrains & views
|           must be created after the tables they depend on, so 
|           the `z_` prefix ensures they're executed last*
├── routers
|   | ^ *endpoints are organized by the data type they're associated
|   |   with & placed in a file named for that data type here*
│   ├── __init__.py
│   ├── account.py
│   ├── balance.py
│   ├── envelope.py
│   ├── helpers
|   |   | ^ *methods for assisting in creating shared behavior 
|   |   |   between multiple routers here*
│   │   └── filters.py
│   ├── status.py
│   ├── token.py
│   ├── transaction.py
│   └── user.py
└── security.py
      ^ *functions for creating & authenticating JWT are here*
```


UI Design - API Reference
---

This app is the back-end REST API serving JSON only, with the User being a Client consuming the API over HTTPS.
This means the UI is a series of API endpoints used to achieve the stories written above in the [Use Case Analysis](#use-case-analysis) section.

See [hoops.andrew-chang-dewitt.dev/docs](https://hoops.andrew-chang-dewitt.dev) for an interactive & up to date version of the API endpoint & schema documentation.


Use Case Analysis
---

I've written the following Use Case Analysis as "User stories":

> *NOTE:* In this context, a User is defined as a Client consuming the JSON API. 
> This means the UI of this application is the API itself.


### Implemented so far:

1. When User creates an Account, an Account is saved & they are given the new Account
    1. When a User requests a list of all of their Accounts, they are given a list of Accounts
    6. When a User edits the name of an Account, the Account is updated & they are given the updated Account
    7. When a User marks an Account as closed, the account is updated & they are given the id & name of the closed account

2. When a User adds a Transaction to an Account, a Transaction is saved & they are given the new Transaction
    1. When a User requests their Transactions for a given Account, they are given a paginated list of Transactions
    4. When a User requests their Transactions for all Accounts, they are given a paginated list of Transactions
    8. When a User edits the payee, description, &/or amount of a Transaction, the Transaction is updated & they are given the updated Transaction
    9. When a User moves a Transaction from one Account to another, the Transaction is updated & they are given the updated Transaction
    10. When a User deletes a Transaction, the Transaction is deleted they are given the old Transaction id, payee, timestamp, & amount
    17. When a User marks a Transaction as "spent from" a given Envelope, they are given  the updated Transaction -- _**but this only happens if there are enough funds available in the Envelope**_

11. When a User creates an Envelope, they are given the new Envelope
    1. When a User moves money from their Available Funds Balance to an Envelope, they are given  the updated Envelope
    13. When a User moves funds from an Envelope back to their Available Funds Balance, they are given  the updated Envelope
    3. When a User moves funds from into one Envelope from another, both Envelopes are updated & they are given the updated target Envelope.
    14. When a User changes the name of an Envelope, they are given the updated Envelope

19. When a User requests their Available Funds Balance (i.e. how much funds are "available"&mdash;the portion of Total Balance not reserved in an Envelope), they are given their Available Funds Balance
20. When a User requests their Total Balance across all accounts (including funds reserved in an Envelope), they are given their Total Balance
22. When a User registers, they are given the username they just created (then should be asked to log in)
    1. When a User logs in, they are given a JWT, if they pass authentication
    23. When a User updates their username, they are given the updated User
    24. When a User updates their password, they are given a success message (~then their JWT should be revoked~ & they should be asked to log in again)


### Stretch Goals

Eventually, I'd like the application to build the following stories as well:

1. When a User creates a Shared User, they are given the new Shared User
    1. When a User invites another User to join a Shared User, they are given a success message
    28. When a User accepts an invitation to join a Shared User, they are given the Shared User
    28. When a User changes profiles to manage the Accounts, Transactions, & Envelopes (i.e. do stories & sub-stories 1 through 5) of their Shared User (if they have one)
    29. When a User requests to leave a Shared User, they are given the old Shared User id & name
    30. When a User votes to delete the data of a Shared User, they are given a success message (and the other member Users are sent a notification; if all agree, then it will be deleted)

1. When a User imports Transactions from a csv, the Transactions are added to a given Account & they are given the updated list of Transactions
2. When a User signs up for new Transactions to be auto-imported from participating bank accounts (using Plaid), Transactions are added to the account as they are received from Plaid & the user is given a success message
3. When a User creates a subset of an Envelope, called a Goal, they are given the new Goal
    1. When a User sets a target date for a Goal (but a Goal doesn't have to have a target date), they are given the updated Goal
    2. When a User requests to automatically schedule money to be moved into a Goal, they are given the updated Goal
    3. When a User sets the priority on an Goal, they are given the updated Goal
    4. When a User moves money in and out of being reserved for a Goal, they are given the updated Goal & Balance of the Envelope or Balance the money is moved in or out of

4. When a User creates a subset of an Envelope, called an Expense, they are given the new Expense
    1. When a User sets a frequency for the Expense to reoccur, they are given the updated Expense
    2. When a User requests to automatically schedule money to be moved into an Expense, they are given the updated Expense
    3. When a User sets a priority on an Expense, they are given the updated Expense
    4. When a User moves money in and out of being reserved for the next occur date for an Expense, they are given the updated Expense & Balance of the Envelope or Balance the money is moved in or out of
    5. When a User moves money in and out of being reserved for the currently available funds on an Expense, they are given the updated Expense & Balance of the Envelope or Balance the money is moved in or out of


CSCI 23000 Skills Used
---

- Data design
  - SQL databases
    - ER diagrams
    - Data normalization
    - CRUD
  - Data structures
    - lists/arrays
    - tuples
    - dictionaries
    - Objects (classes & instances)
  - Object Oriented Programming
    - Properties
    - Methods
    - Inheritance
- Algorithm design
- Web server construction
- Data serialization (JSON)
- Exception handling


External libraries used
---

All top-level dependencies are defined in `./requirements/dev.txt` & `./requirements/prod.txt`. Anything in `dev.txt` isn't used to actually build & run the application & isn't called or referenced in the source code. 

Some of these dependencies have their own sub-dependencies, but I don't necessarily interact with them directly in my source code. All dependencies, top-level & sub-dependencies are listed in the output from `pip freeze` below:

```
aiopg==1.3.3
anyio==3.3.4
asgi-lifespan==1.0.1
asgiref==3.4.1
astroid==2.8.5
async-timeout==4.0.1
autopep8==1.6.0
certifi==2021.10.8
cffi==1.15.0
charset-normalizer==2.0.7
click==8.0.3
cryptography==35.0.0
db-wrapper @ https://github.com/cheese-drawer/lib-python-db-wrapper/releases/download/2.3.0/db_wrapper-2.3.0-py3-none-any.whl
ecdsa==0.17.0
fastapi==0.70.0
h11==0.12.0
httpcore==0.13.7
httptools==0.2.0
httpx==0.20.0
idna==3.3
isort==5.10.1
lazy-object-proxy==1.6.0
mccabe==0.6.1
migra==3.0.1621480950
mypy==0.910
mypy-extensions==0.4.3
pathlib==1.0.1
platformdirs==2.4.0
psycopg2-binary==2.9.2
pyasn1==0.4.8
pycodestyle==2.8.0
pycparser==2.21
pydantic==1.8.2
pydocstyle==6.1.1
pylint==2.11.1
python-dotenv==0.19.2
python-jose==3.3.0
python-multipart==0.0.5
PyYAML==6.0
requests==2.26.0
rfc3986==1.5.0
rsa==4.7.2
schemainspect==3.0.1616029793
six==1.16.0
sniffio==1.2.0
snowballstemmer==2.1.0
SQLAlchemy==1.3.24
sqlbag==0.1.1579049654
starlette==0.16.0
toml==0.10.2
types-requests==2.25.12
typing-extensions==3.10.0.2
urllib3==1.26.7
uvicorn==0.15.0
uvloop==0.16.0
watchgod==0.7
websockets==10.0
wrapt==1.13.3
```
