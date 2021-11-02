Final Project Proposal
===

*CSCI 230* \
*Tuesday, Nov 2, 2021* \
*Andrew Chang-DeWitt*

Project Summary
---

- *[ ] Proposed project title:*

- *[ ] Longer description of project:*

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
