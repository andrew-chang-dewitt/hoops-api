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

Planning spending in a flexible, extensible, & low-friction fashion while being usable by multiple people simultaneously. 
Modeled after my favorite now-defunct fintech's budgeting tools.

### Which technologies will you need (files, databases, GUIs?):

  1. Database (PostgreSQL&mdash;offers better types for currency via NUMERIC, UUID keys, & built-in password hashing tools)
  2. Web server (JSON REST API via Flask&mdash;offers better routing encapsulation via Blueprints)

Use Case Analysis
---

I've written the following Use Case Analysis as "User stories":

> *NOTE:* In this context, a User is defined as a Client consuming the JSON API. 
> This means the UI of this application is the API itself.

1. When User creates an Account, an Account is saved & they are given the new Account
    1. When a User requests a list of all of their Accounts, they are given a paginated list of Accounts
    6. When a User edits the name of an Account, the Account is updated & they are given the updated Account
    7. When a User marks an Account as closed, the account is updated & they are given the id & name of the closed account

2. When a User adds a Transaction to an Account, an Account is saved & they are given the new Transaction
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

UI Design
---

This app is the back-end REST API serving JSON only, with the User being a Client consuming the API over HTTPS.
This means the UI is a series of API endpoints used to achieve the stories written above in the [Use Case Analysis](#use-case-analysis) section.

> *NOTE:* This section still needs to be expanded to full documentation for the API by creating an exhaustive list of API endpoints, accepted arguments (POST body, query args, or URI args), & endpoint return schema.

Algorithm
---

*Once you've done the previous steps, you should be ready to start putting together your algorithm. Remember, an algorithm is simply a list of instructions written in English that are so detailed that they can be translated to programming code.*

*Most projects will benefit from an OOP design. Identify the main objects needed in your program. Generally each data element will be a class, and each screen of a GUI will be a class. For each class in your project:*

- [ ] *Define the data members - what are the key data elements of the class?*
- [ ] *Describe the initializer - Initializers always create and populate the data members. Will you read in parameters? Have default values? both?*
- [ ] *Describe any other housekeeping that may need to happen in the initializer*
- [ ] *Define access methods for all data members. Build appropriate getters and setters*
- [ ] *Define any properties or virtual properties you class may need*
- [ ] *Identify any methods your class will need beyond access modifiers*
- [ ] *Flesh out each method just like the function analysis below*
