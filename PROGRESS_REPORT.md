Final Project Progress Report
===

*CSCI 230* \
*Tuesday, Dec 03, 2021* \
*Andrew Chang-DeWitt*

Features
---

The following is a list of features, written as user stories, that are planned for the project.
Features with a green check mark (✅) are complete, while those with a blue check mark (☑️ ) are  started, but not yet complete, & those with no check mark have yet to be started.

> *NOTE:* In this context, a User is defined as a Client consuming the JSON API. 
> This means the UI of this application is the API itself.

1. ✅ When User creates an Account, an Account is saved & they are given the new Account
    1. ✅ When a User requests a list of all of their Accounts, they are given a list of Accounts
    6. ✅ When a User edits the name of an Account, the Account is updated & they are given the updated Account
    7. ✅ When a User marks an Account as closed, the account is updated & they are given the id & name of the closed account

2. ✅ When a User adds a Transaction to an Account, a Transaction is saved & they are given the new Transaction
    1. ✅ When a User requests their Transactions for a given Account, they are given a paginated list of Transactions
    4. ✅ When a User requests their Transactions for all Accounts, they are given a paginated list of Transactions
    8. ✅ When a User edits the payee, description, &/or amount of a Transaction, the Transaction is updated & they are given the updated Transaction
    9. ✅ When a User moves a Transaction from one Account to another, the Transaction is updated & they are given the updated Transaction
    10. ✅ When a User deletes a Transaction, the Transaction is deleted they are given the old Transaction id, payee, timestamp, & amount
    17. When a User marks a Transaction as "spent from" a given Envelope, they are given their updated Available Funds Balance, the updated Envelope balance, & the updated Transaction -- _**but this only happens if there are enough funds available in the Envelope**_

11. ✅ When a User creates an Envelope, they are given the new Envelope
    1. When a User moves money from their Available Funds Balance to an Envelope, they are given their updated Available Funds Balance & the updated Envelope
    13. When a User moves funds from an Envelope back to their Available Funds Balance, they are given their updated Available Funds Balance & the updated Envelope
    14. ✅ When a User changes the name of an Envelope, they are given the updated Envelope

19. ✅ When a User requests their Available Funds Balance (i.e. how much funds are "available"&mdash;the portion of Total Balance not reserved in an Envelope), they are given their Available Funds Balance
20. ✅ When a User requests their Total Balance across all accounts (including funds reserved in an Envelope), they are given their Total Balance
22. ✅ When a User registers, they are given the username they just created (then should be asked to log in)
    1. ✅ When a User logs in, they are given a JWT, if they pass authentication
    23. ✅ When a User updates their username, they are given the updated User
    24. ✅ When a User updates their password, they are given a success message (~then their JWT should be revoked~ & they should be asked to log in again)

Stretch Goals
---

If there's still time after the above features are implemented, I'd like to implement as many of the following features as possible.

1. When a User adds/changes/removes a description for an Envelope, they are given the updated Envelope
1. When a User marks an Envelope as closed, they are given the id & name of the closed Envelope
1. When a User requests the history of an Envelope, they are given a paginated list of Transactions marked as "spent from" the Envelope
2. When a User deletes their data, confirmation is requested, then if they confirm, they are given a success message
1. When a User creates a Shared User, they are given the new Shared User
    1. When a User invites another User to join a Shared User, they are given a success message
    28. When a User accepts an invitation to join a Shared User, they are given the Shared User
    28. When a User changes profiles to manage the Accounts, Transactions, & Envelopes (i.e. do stories & sub-stories 1 through 5) of their Shared User (if they have one)
    29. When a User requests to leave a Shared User, they are given the old Shared User id & name
    30. When a User votes to delete the data of a Shared User, they are given a success message (and the other member Users are sent a notification; if all agree, then it will be deleted)
