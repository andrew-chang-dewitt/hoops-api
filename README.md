Hoops - A simple budgeting application
===

*CSCI 23000* \
*Tuesday, Dec 7, 2021* \
*Andrew Chang-DeWitt*

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
