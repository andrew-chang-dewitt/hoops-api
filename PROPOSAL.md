Final Project Proposal
===

*CSCI 230* \
*Tuesday, Nov 2, 2021* \
*Andrew Chang-DeWitt*

Project Summary
---

### Proposed project title:

Currently developing with the title "Hoops", which is the literal translation of a slang word for money in Taiwan. 
Not really spending much time on the name yet, but I expect this to change eventually.

### Longer description of project:

A back-end REST API serving JSON data for a budgeting application.
The goal is to build something similar to the budgeting tools offered by a fintech I used to use before it was killed off in a merger.
Starting with a simplified version that's based on the envelope system & intended to offer privacy to multiple users while allowing them to share a budget, if desired.
  
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

Use Case Analysis
---

I've written the following Use Case Analysis as "User stories":

> *NOTE:* In this context, a User is defined as a Client consuming the JSON API. 
> This means the UI of this application is the API itself.

1. When User creates an Account, an Account is saved & they are given the new Account
    1. When a User requests a list of all of their Accounts, they are given a paginated list of Accounts
    6. When a User edits the name of an Account, the Account is updated & they are given the updated Account
    7. When a User marks an Account as closed, the account is updated & they are given the id & name of the closed account

2. When a User adds a Transaction to an Account, a Transaction is saved & they are given the new Transaction
    1. When a User requests their Transactions for a given Account, they are given a paginated list of Transactions
    4. When a User requests their Transactions for all Accounts, they are given a paginated list of Transactions
    8. When a User edits the payee, description, &/or amount of a Transaction, the Transaction is updated & they are given the updated Transaction
    9. When a User moves a Transaction from one Account to another, the Transaction is updated & they are given the updated Transaction
    10. When a User deletes a Transaction, the Transaction is deleted they are given the old Transaction id, payee, timestamp, & amount
    17. When a User marks a Transaction as "spent from" a given Envelope, they are given their updated Available Funds Balance, the updated Envelope balance, & the updated Transaction -- _**but this only happens if there are enough funds available in the Envelope**_

11. When a User creates an Envelope, they are given the new Envelope
    1. When a User moves money from their Available Funds Balance to an Envelope, they are given their updated Available Funds Balance & the updated Envelope
    13. When a User moves funds from an Envelope back to their Available Funds Balance, they are given their updated Available Funds Balance & the updated Envelope
    14. When a User changes the name of an Envelope, they are given the updated Envelope
    15. When a User adds/changes/removes a description for an Envelope, they are given the updated Envelope
    16. When a User marks an Envelope as closed, they are given the id & name of the closed Envelope
    18. When a User requests the history of an Envelope, they are given a paginated list of Transactions marked as "spent from" the Envelope

19. When a User requests their Available Funds Balance (i.e. how much funds are "available"&mdash;the portion of Total Balance not reserved in an Envelope), they are given their Available Funds Balance
20. When a User requests their Total Balance across all accounts (including funds reserved in an Envelope), they are given their Total Balance
22. When a User registers, they are given the username they just created (then should be asked to log in)
    1. When a User logs in, they are given a JWT, if they pass authentication
    23. When a User updates their username, they are given the updated User
    24. When a User updates their password, they are given a success message (then their JWT should be revoked & they should be asked to log in again)
    25. When a User deletes their data, confirmation is requested, then if they confirm, they are given a success message

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


Data Design
---

### What data is your program really about?

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

### What is the best way to represent that data? Will the data need to be persistent? How will you make that happen?

A Database is the best way to grant both data persistence & represent the data for storage.
The following Entity Relationship Diagram represents the database design:

### Will the data need to be aggregated into a larger structure? How?

Yes, at times an API response will need to return data from multiple data types (or tables).
This will be done using JOIN queries & VIEWS.
The application will conceptualize these VIEWS as Models to abstract the queries & data aggregation & validation away from the application logic.

The following Entity Relationship Diagram represents the database design:

![Entity Relationship Diagram](/data-er.svg)

UI Design - API Reference
---

This app is the back-end REST API serving JSON only, with the User being a Client consuming the API over HTTPS.
This means the UI is a series of API endpoints used to achieve the stories written above in the [Use Case Analysis](#use-case-analysis) section.

> *NOTE:* This section still needs to be expanded to full documentation for the API by creating an exhaustive list of API endpoints, accepted arguments (POST body, query args, or URI args), & endpoint return schema.


Algorithm
---

### Model Objects

Objects that encapsulate CRUD operations on different database tables.

#### ModelABC:

**Properties:**

These objects have no public properties, they simply encapsulate functions for getting information from the database.

**Initializer:**

All models have roughly the same initializer behavior:

1. save the given table name as a private instance attribute
2. build the read, create, update, & delete attributes to contain methods for all database queries for that model

**Methods:** 

All models have the same shared methods:

- create.one
  1. create empty `columns` & `values` lists
  2. iterate over key, value pairs of dictionary made using `.items()` method on given data object's `.dict()` method
    1. append keys to `columns`
    2. append values to `values`
  3. format `columns` & `values` lists as lists of columns & values enclosed by parenthesis for use in SQL INSERT INTO table {columns} VALUES {values}; query
  4. build INSERT query using formatted lists
  5. execute & commit query
  6. build appropriate Data Object or list of Data Objects using query results
  7. return object or list

- read.one_by_id
  1. build SELECT query using given id
  2. execute & commit query
  3. build appropriate Data Object using query results
  4. return object

- update.one_by_id
  1. compose list of changes as `{column} = {new_value}` & join into comma separated string
  2. build UPDATE...SET...WHERE query using instance table name, given changes, & given id
  3. execute & commit query
  4. build appropriate Data Object using query results
  5. return object

- delete.one_by_id
  1. build `DELETE FROM {table} WHERE id = {id} RETURNING *` query from instance table name & given id
  2. execute & commit query
  3. build appropriate Data Object using query results
  4. return object

#### TransactionModel(ModelABC)

CRUD operations on table `transaction`.
  
**Methods:** 

- read.many_by_account
  1. build `SELECT * FROM {table} where account_id = {id}` query from instance table name & given account id
  2. execute & commit query
  3. build appropriate list of Data Objects using query results
  4. return list

#### EnvelopeModel(ModelABC)

CRUD operations on table `envelope`.
  
**Methods:** 

- read.many_by_user
  1. build `SELECT * FROM {table} where user_id = {id}` query from instance table name & given user id
  2. execute & commit query
  3. build appropriate list of Data Objects using query results
  4. return list

#### UserModel(ModelABC)

CRUD operations on table `user`.
  
**Methods:**

- OVERLOAD create.one
  1. build `INSERT INTO {table}(handle, password, full_name, preferred_name) VALUES({handle}, crypt({password}, gen_salt('bf')), {full_name}, {preferred_name})` query using handle, password, full_name, & preferred_name attributes on given UserDataIn object with encryption done by PostgreSQL's pgycrypto extension's `crypt` & `gen_salt` procedures
  2. execute & commit query
  3. build appropriate UserDataOut object using query results
  4. return object

- read.authenticate
  1. build `SELECT * FROM {table} WHERE handle = {given_handle} AND password = crypt({given_password}, password);` query using given User handle & password with password decryption done by PostgreSQL's pgycrypto extension's `crypt` procedure
  2. execute & commit query
  3. build appropriate UserDataOut object using query results
  4. return object


#### AccountModel(ModelABC)

CRUD operations on table `account`.
  
**Methods:** 

- read.many_by_user
  1. build `SELECT * FROM {table} where user_id = {id}` query from instance table name & given user id
  2. execute & commit query
  3. build appropriate list of Data Objects using query results
  4. return list

### Data Objects

All methods on a given Model object return it's corresponding Data Object
(e.g. TransactionModel.read.one_by_id returns an instance of TransactionData).
All data objects will be inherited from Pydantic's BaseModel to perform type validation on object creation automatically.

Data objects have no initializer beyond the one provided by BaseModel.

#### TransactionData

**Properties:**

- id: a unique identifier (UUID)
- amount: the monetary value of the transaction (Decimal)
- payee: the person/entity the transaction was paid to/received from (str)
- timestamp: the date & time the transaction occurred (datetime)
- description: any extra information (str)
- account_id: the id of the Account the Transaction belongs to (UUID)

#### EnvelopeData

**Properties:**

- id: a unique identifier (UUID)
- name: the name given to the Envelope (str)
- total_funds: the total amount of funds put into the Envelope (Decimal)
  _Note:_ this isn't the same thing as how much funds are available
- user_id: the id of the User the Envelope belongs to (UUID)

#### UserDataIn

**Properties:**

- id: a unique identifier (UUID)
- handle: a unique username (str)
- password: a hashed & salted password (str)
- full_name: user's full name (str)
- preferred_name: user's preferred name (optional[str])

#### UserDataOut

**Properties:**

All of UserDataIn's properties except password.
Never send a user their UserDataIn object as this would send their plaintext password.

#### AccountData

**Properties:**

- id: a unique identifier (UUID)
- name: a human readable name for the account (str)
- user_id: the id of the User who owns the Account (UUID)

### Routing Objects

The following objects encapsulate route handlers that will be used by the API's web server framework to respond to requests.

#### RoutesABC

Defines shared initializer behavior for all Routing Objects.

**Initializer:**

#### TransactionRoutes(RoutesABC)

Encapsulates all routes under `/transaction`.

**Methods:**

- post_one: save given data as new Transaction  & return the resulting TransactionData object
- get_one: fetch a TransactionData from the db by the given id
- put_one: update the transaction that matches the given id with the given data
- delete_one: remove the transaction with the given id from the database

_**NOTE:**_ All routes under `/transaction` will be guarded by an authentication method using `FastAPI.middleware()` & a client-provided JWT.

#### EnvelopeRoutes(RoutesABC)

Encapsulates all routes under `/envelope`.

- post_one: save given data as new Envelope belonging to user_id held in auth token & return the resulting EnvelopeData object
- get_one: fetch a EnvelopeData from the db by the given id
- get_many: fetch many EnvelopeData objects from the database where their user_id matches the id in the token, paginated & sorted by date in descending order
- put_one: update the Envelope that matches the given id with the given data
- delete_one: remove the Envelope with the given id from the database

_**NOTE:**_ All routes under `/envelope` will be guarded by an authentication method using `FastAPI.middleware()` & a client-provided JWT.

#### AccountRoutes(RoutesABC)

Encapsulates all routes under `/account`.

- post_one: save given data as new Account belonging to user_id held in auth token & return the resulting AccountData object
- get_one: fetch a AccountData from the db by the given id
- get_many: fetch many AccountData objects from the database where their user_id matches the id in the token, paginated & sorted by date in descending order
- get_transactions: fetch many transactions for a given account_id, return a list of TransactionData objects, paginated & sorted by date in descending order

_**NOTE:**_ All routes under `/envelope` will be guarded by an authentication method using `FastAPI.middleware()` & a client-provided JWT.

#### UserRoutes(RoutesABC)

Encapsulates all routes under `/user/{user_id}`.

- get_accounts: get all accounts for the given user_id & return a list of AccountData objects, paginated & sorted by date in descending order by name
- get_transactions: get all transactions for all accounts for the given user_id & return a list of TransactionData objects, paginated & sorted by date in descending order by timestamp
- post_user: create a new User from given data & return new User's handle, full_name, & preferred_name--does not authenticate user, they will still have to log in with their newly created handle & password via `POST /authenticate`

_**NOTE:**_ All routes under `/envelope` will be guarded by an authentication method using `FastAPI.middleware()` & a client-provided JWT.

#### AuthenticationRoutes(RoutesABC)

Encapsulates all routes under `/authenticate`.

- post_auth: authenticate user with given handle & password via postgres's pgycrypto extension & return a JWT if valid, else 401
- delete_auth: log a user out by marking the given JWT as invalid in database, return 205 to tell the client to refresh


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
