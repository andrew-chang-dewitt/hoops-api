Final Project Proposal
===

*CSCI 230* \
*Tuesday, Nov 2, 2021* \
*Andrew Chang-DeWitt*

Project Summary
---

- *[ ] Proposed project title:*

  Currently developing with the title "Hoops", which is the literal translation of a slang word for money in Taiwan. 
  Not really spending much time on the name yet, but I expect this to change eventually.

- *[ ] Longer description of project:*

  A back-end REST API serving JSON data for a budgeting application.
  The goal is to build something similar to the budgeting tools offered by a fintech I used to use before it was killed off in a merger.
  Starting with a simplified version that's based on the envelope system & intended to offer privacy to multiple users while allowing them to share a budget, if desired.
  
- *[x] Intended user:*
  
  My wife & I first, then eventually maybe either an OSS release for self-hosting or a SAAS hosted option.
  
- *[x] What problem is project trying to solve?:*

  Planning spending in a flexible, extensible, & low-friction fashion while being usable by multiple people simultaneously. 
  Modeled after my favorite now-defunct fintech's budgeting tools.

- *[x] Which technologies will you need (files, databases, GUIs?):*

  1. Database (SQLite or PostgreSQL)
  2. Web server (JSON REST API - Bottle or Flask)
  3. maybe a front-end, eventually (React/React Native)

### Use Case Analysis

I've written the following Use Case Analysis as "User stories":

> *NOTE:* In this context, a User is defined as a Client consuming the JSON API. 
> This means the UI of this application is the API itself.

1. When User creates an Account, they are given the new Account
2. When a User adds a Transaction to an Account, they are given the new Transaction
3. When a User requests their Transactions for a given Account, they are given a paginated list of Transactions
4. When a User requests their Transactions for all Accounts, they are given a paginated list of Transactions
5. When a User requests a list of all of their Accounts, they are given a paginated list of Accounts
6. When a User edits the name of an Account, they are given the new Account name & the existing id
7. When a User marks an Account as closed, they are given the id of the closed account
8. When a User edits the payee, description, &/or amount of a Transaction, they are given the updated Transaction
9. When a User moves a Transaction from one Account to another, they are given the updated Transaction
10. When a User deletes a Transaction, they are given the old Transaction id
11. When a User creates an Envelope, they are given the new Envelope
12. When a User moves money from their "available funds" to an Envelope, they are given their updated "avalable funds balance" & the updated Envelope
13. When a User moves funds from an Envelope back to "available", they are given their updated "avalable funds balance" & the updated Envelope
14. When a User changes the name of an Envelope, they are given the updated Envelope
15. When a User adds/changes/removes a description for an Envelope, they are given the updated Envelope
16. When a User marks an Envelope as closed, they are given the id of the closed Envelope
17. When a User marks a Transaction as "spent from" a given Envelope, they are given their updated "available funds balance", the updated Envelope balance, & the updated Transaction -- _**but this only happens if there are enough funds available in the Envelope**_ \
  *Note: If a Transaction is not "spent from" any Envelope, then it is deducted from the "available funds" balance.*
18. When a User requests the history of funds moving in & out of an Envelope, they are given a list of Envelope Changes (time funds were moved in/out & the amount moved) & Transactions marked as "spent from" the Envelope
19. When a User view how much funds are "available" (i.e. portion of total Balance not reserved in an Envelope)
20. When a User view their current, total Balance across all accounts (including funds reserved in an Envelope)
21. When a User login
22. When a User register
23. When a User update their username
24. When a User update their password
25. When a User delete their data
26. When a User create a Shared User
27. When a User invite another User to join a Shared User
28. When a User change profiles to manage the Accounts, Transactions, & Envelopes (i.e. do stories 1 through 20) of their Shared User (if they have one)
29. When a User leave a Shared User
30. When a User vote to delete the data of a Shared User (if all agree, then it will be deleted)

#### Stretch Goals

Eventually, I'd like the application to build the following stories as well:

1. When a User import Transactions from a csv
2. When a User sign up for new Transactions to be auto-imported from participating bank accounts (using Plaid)
3. When a User create a subset of an Envelope, called a Goal

  1. When a User set a target date for a Goal (but a Goal doesn't have to have a target date)
  2. When a User automatically schedule money to be moved into a Goal
  3. When a User set a priority on an Goal
  4. When a User move money in and out of being reserved for a Goal

4. When a User create a subset of an Envelope, called an Expense

  1. A User must set a frequency for the Expense to reoccur
  2. When a User automatically schedule money to be moved into an Expense
  3. When a User set a priority on an Expense
  4. When a User see how much is available now from an Expense
  5. When a User see how much is reserved so far for the next occur date for an Expense
  6. When a User move money in and out of being reserved for the next occur date for an Expense
  7. When a User move money in and out of being reserved for the currently available funds on an Expense


Data Design
---

- *[x] What data is your program really about?*

  Transactions, Envelopes, & Users. 
  Transactions are exactly what their name says: an amount of money either going in from or coming out to a specific payee at a specific time.
  Envelopes are concept that represents an amount of money reserved for a specific purpose (e.g. a savings goal like a vacation or an expense like rent or groceries).
  A User is also exactly what the name says: a person using this budgeting program.
  
  Besides those three core data types, the following ancilliary data types exist:
  
  - Accounts: 
    
    A bank account, credit card, cash hidden under the mattress, etc. 
    Individual Transactions belong to an Account.
    
  - Envelope changes:
  
    A record of each time the balance of a specific Envelope changes & how much it changed by.
    Used to analyze spending & saving over time.
  
  - Shared Users:
  
    A Shared User is simply a non-login User, that multiple login Users can act as. 
    This means a login User can have their own Accounts & Envelopes, then they can click a button to manage the Accounts & Envelopes of a Shared User that one or more other people may be able to manage as well.

- *[x] What is the best way to represent that data? (database, object, arrays)*

  Database

- *[x] Will the data need to be persistent? How will you make that happen?*

  Yes, using a database.

- *[x] Will the data need to be aggregated into a larger structure? How*

  Yes, at times an API response will need to return data from multiple data types (or tables).
  This will be done using JOIN queries & VIEWS.
  The application will conceptualize these VIEWS as Models to abstract the queries & data aggregation & validation away from the application logic.

The following Entity Relationship Diagram represents the database design:

![Entity Relationship Diagram](/data-er.svg)

UI Design
---

I'm not sure I actually plan to do a UI yet. 
The current phase is simply about building an application to store & make available the data, which can then be consumed by a separate front-end application (e.g. web app or mobile app).

...

*If your program has a GUI component, create a diagram for each page of the design. It doesn't need to be elaborate or beautiful, but it should give you enough information to make the programming easy:*

- [ ] *Name and type of each element on the page*
- [ ] *Layout hints if needed (row and column numbers for grid layout)*
- [ ] *Design - layout instructions (fonts, colors, borders, etc)*
- [ ] *Function for any buttons, menu items, or interactive elements*

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
