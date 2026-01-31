<h1 id="fastapi">FastAPI v0.1.0</h1>

Scroll down for code samples, example requests and responses.

# Authentication

- oAuth2 authentication. 

    - Flow: password

    - Token URL = [token](token)

<h1 id="fastapi-api-status">API Status</h1>

## Check API status.

<a id="opIdroot__get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json'
}

r = requests.get('/', headers = headers)

print(r.json())

```

`GET /`

Check API status.

### Example responses

> 200 Response

```json
{
  "message": "string",
  "ok": true
}
```

<h3 id="check-api-status.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Status](#schemastatus)|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-user">User</h1>

## Get the currently authenticated User.

<a id="opIdget_user_user_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/user', headers = headers)

print(r.json())

```

`GET /user`

Get the current user's information.

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="get-the-currently-authenticated-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[UserOut](#schemauserout)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Update the currently authenticated User's information.

<a id="opIdput_user_user_put"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/user', headers = headers)

print(r.json())

```

`PUT /user`

Update the current user's information.

### Body parameter

```json
{
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="update-the-currently-authenticated-user's-information.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UserChanges](#schemauserchanges)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="update-the-currently-authenticated-user's-information.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[UserOut](#schemauserout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Create a new User.

<a id="opIdpost_user_user_post"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}

r = requests.post('/user', headers = headers)

print(r.json())

```

`POST /user`

Save a new User to the database & return the new information.

### Body parameter

```json
{
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string",
  "password": "string"
}
```

<h3 id="create-a-new-user.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[UserIn](#schemauserin)|true|none|

### Example responses

> 201 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="create-a-new-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successful Response|[UserOut](#schemauserout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

## Delete the currently authenticated User.

<a id="opIddelete_user_user_delete"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.delete('/user', headers = headers)

print(r.json())

```

`DELETE /user`

Delete the current user from the database.

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="delete-the-currently-authenticated-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[UserOut](#schemauserout)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Update the currently authenticated User's password.

<a id="opIdput_password_user_password_put"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/user/password', headers = headers)

print(r.json())

```

`PUT /user/password`

Update the current user's password.

### Body parameter

```json
"string"
```

<h3 id="update-the-currently-authenticated-user's-password.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|string|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}
```

<h3 id="update-the-currently-authenticated-user's-password.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[UserOut](#schemauserout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-authentication">Authentication</h1>

## Get an authentication Token via an OAuth2 Request Form.

<a id="opIdpost_token_post"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/json'
}

r = requests.post('/token', headers = headers)

print(r.json())

```

`POST /token`

POST `/token` handler.

### Body parameter

```yaml
grant_type: string
username: string
password: string
scope: ""
client_id: string
client_secret: string

```

<h3 id="get-an-authentication-token-via-an-oauth2-request-form.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[Body_post_token_post](#schemabody_post_token_post)|true|none|

### Example responses

> 200 Response

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

<h3 id="get-an-authentication-token-via-an-oauth2-request-form.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Token](#schematoken)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="success">
This operation does not require authentication
</aside>

<h1 id="fastapi-account">Account</h1>

## Get the Accounts for the currently authenticated User.

<a id="opIdget_account_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/account', headers = headers)

print(r.json())

```

`GET /account`

Read all open accounts for given User.

### Example responses

> 200 Response

```json
[
  {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "name": "string",
    "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
    "closed": true
  }
]
```

<h3 id="get-the-accounts-for-the-currently-authenticated-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get-the-accounts-for-the-currently-authenticated-user.-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Account Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Account Get|[[AccountOut](#schemaaccountout)]|false|none|[Fields returned by Account queries.]|
|» AccountOut|[AccountOut](#schemaaccountout)|false|none|Fields returned by Account queries.|
|»» id|string(uuid)|true|none|none|
|»» name|string|true|none|none|
|»» user_id|string(uuid)|true|none|none|
|»» closed|boolean|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Create a new Account for the currently authenticated User.

<a id="opIdpost_account_post"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/account', headers = headers)

print(r.json())

```

`POST /account`

Create a new account for given User.

### Body parameter

```json
{
  "name": "string"
}
```

<h3 id="create-a-new-account-for-the-currently-authenticated-user.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[AccountIn](#schemaaccountin)|true|none|

### Example responses

> 201 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "closed": true
}
```

<h3 id="create-a-new-account-for-the-currently-authenticated-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successful Response|[AccountOut](#schemaaccountout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Update the given Account.

<a id="opIdput_id_account__account_id__put"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/account/{account_id}', headers = headers)

print(r.json())

```

`PUT /account/{account_id}`

Update the given account with the given changes.

### Body parameter

```json
{
  "name": "string",
  "closed": true
}
```

<h3 id="update-the-given-account.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|account_id|path|string(uuid)|true|none|
|body|body|[AccountChanges](#schemaaccountchanges)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "closed": true
}
```

<h3 id="update-the-given-account.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[AccountOut](#schemaaccountout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Mark the given Account as closed.

<a id="opIdput_closed_account__account_id__closed_put"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/account/{account_id}/closed', headers = headers)

print(r.json())

```

`PUT /account/{account_id}/closed`

Mark the given account as closed.

<h3 id="mark-the-given-account-as-closed.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|account_id|path|string(uuid)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "closed": true
}
```

<h3 id="mark-the-given-account-as-closed.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[AccountOut](#schemaaccountout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get all closed Accounts for current User.

<a id="opIdget_closed_account_closed_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/account/closed', headers = headers)

print(r.json())

```

`GET /account/closed`

Mark the given account as closed.

### Example responses

> 200 Response

```json
[
  {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "name": "string",
    "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
    "closed": true
  }
]
```

<h3 id="get-all-closed-accounts-for-current-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get-all-closed-accounts-for-current-user.-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Closed Account Closed Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Closed Account Closed Get|[[AccountOut](#schemaaccountout)]|false|none|[Fields returned by Account queries.]|
|» AccountOut|[AccountOut](#schemaaccountout)|false|none|Fields returned by Account queries.|
|»» id|string(uuid)|true|none|none|
|»» name|string|true|none|none|
|»» user_id|string(uuid)|true|none|none|
|»» closed|boolean|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-transaction">Transaction</h1>

## Fetch all Transactions for the authenticated User.

<a id="opIdget_root_transaction_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/transaction', headers = headers)

print(r.json())

```

`GET /transaction`

Get all Transactions.

<h3 id="fetch-all-transactions-for-the-authenticated-user.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|account_id|query|string(uuid)|false|Only return Transactions belonging to this Account.|
|payee|query|string|false|Only return Transactions with matching payee.|
|minimum_amount|query|number|false|Only return Transactions greater than or equal to amount.|
|maximum_amount|query|number|false|Only return Transactions less than or equal to amount.|
|after|query|string(date-time)|false|Only return Transactions after the given date & time.|
|before|query|string(date-time)|false|Only return Transactions before the given date & time.|
|limit|query|integer|false|Only return specified number of Transactions.|
|page|query|integer|false|Return given page of Transactions.|
|sort|query|string|false|Sort Transactions by given column.|

### Example responses

> 200 Response

```json
[
  {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "amount": 0,
    "description": "string",
    "payee": "string",
    "timestamp": "2019-08-24T14:15:22Z",
    "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
    "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
  }
]
```

<h3 id="fetch-all-transactions-for-the-authenticated-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<h3 id="fetch-all-transactions-for-the-authenticated-user.-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Root Transaction Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Root Transaction Get|[[TransactionOut](#schematransactionout)]|false|none|[Fields used when reading a Transaction.]|
|» TransactionOut|[TransactionOut](#schematransactionout)|false|none|Fields used when reading a Transaction.|
|»» id|string(uuid)|true|none|none|
|»» amount|number|true|none|none|
|»» description|string|true|none|none|
|»» payee|string|true|none|none|
|»» timestamp|string(date-time)|true|none|none|
|»» account_id|string(uuid)|true|none|none|
|»» spent_from|string(uuid)|false|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Create a new Transaction for the given Account.

<a id="opIdpost_root_transaction_post"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/transaction', headers = headers)

print(r.json())

```

`POST /transaction`

Save given Transaction to database.

### Body parameter

```json
{
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}
```

<h3 id="create-a-new-transaction-for-the-given-account.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[TransactionIn](#schematransactionin)|true|none|

### Example responses

> 201 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}
```

<h3 id="create-a-new-transaction-for-the-given-account.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successful Response|[TransactionOut](#schematransactionout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Edit the given Transaction.

<a id="opIdput_id_transaction__transaction_id__put"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/transaction/{transaction_id}', headers = headers)

print(r.json())

```

`PUT /transaction/{transaction_id}`

Edit the given Transaction.

### Body parameter

```json
{
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}
```

<h3 id="edit-the-given-transaction.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|transaction_id|path|string(uuid)|true|none|
|body|body|[TransactionChanges](#schematransactionchanges)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}
```

<h3 id="edit-the-given-transaction.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[TransactionOut](#schematransactionout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Delete the given Transaction.

<a id="opIddelete_id_transaction__transaction_id__delete"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.delete('/transaction/{transaction_id}', headers = headers)

print(r.json())

```

`DELETE /transaction/{transaction_id}`

Delete the given Transaction.

<h3 id="delete-the-given-transaction.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|transaction_id|path|string(uuid)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}
```

<h3 id="delete-the-given-transaction.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[TransactionOut](#schematransactionout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-balance">Balance</h1>

## Get sum total Balance of all accounts for the current User.

<a id="opIdget_root_balance_total_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/balance/total', headers = headers)

print(r.json())

```

`GET /balance/total`

### Example responses

> 200 Response

```json
{
  "amount": 0,
  "collection": "string",
  "collection_id": "4bdef85c-3f50-4006-a713-2350da665f80",
  "collection_type": "account",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5"
}
```

<h3 id="get-sum-total-balance-of-all-accounts-for-the-current-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Balance](#schemabalance)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get the Balance for the given account.

<a id="opIdget_account_balance_account__account_id__get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/balance/account/{account_id}', headers = headers)

print(r.json())

```

`GET /balance/account/{account_id}`

<h3 id="get-the-balance-for-the-given-account.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|account_id|path|string(uuid)|true|none|

### Example responses

> 200 Response

```json
{
  "amount": 0,
  "collection": "string",
  "collection_id": "4bdef85c-3f50-4006-a713-2350da665f80",
  "collection_type": "account",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5"
}
```

<h3 id="get-the-balance-for-the-given-account.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Balance](#schemabalance)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get the balance of a given Envelope.

<a id="opIdget_envelope_balance_envelope__envelope_id__get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/balance/envelope/{envelope_id}', headers = headers)

print(r.json())

```

`GET /balance/envelope/{envelope_id}`

<h3 id="get-the-balance-of-a-given-envelope.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|envelope_id|path|string(uuid)|true|none|

### Example responses

> 200 Response

```json
{
  "amount": 0,
  "collection": "string",
  "collection_id": "4bdef85c-3f50-4006-a713-2350da665f80",
  "collection_type": "account",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5"
}
```

<h3 id="get-the-balance-of-a-given-envelope.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Balance](#schemabalance)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get the Available Balance.

<a id="opIdget_available_balance_available_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/balance/available', headers = headers)

print(r.json())

```

`GET /balance/available`

### Example responses

> 200 Response

```json
{
  "amount": 0,
  "collection": "string",
  "collection_id": "4bdef85c-3f50-4006-a713-2350da665f80",
  "collection_type": "account",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5"
}
```

<h3 id="get-the-available-balance.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[Balance](#schemabalance)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

<h1 id="fastapi-envelope">Envelope</h1>

## Get all Envelopes for current user.

<a id="opIdget_root_envelope_get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/envelope', headers = headers)

print(r.json())

```

`GET /envelope`

### Example responses

> 200 Response

```json
[
  {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "name": "string",
    "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
    "total_funds": 0
  }
]
```

<h3 id="get-all-envelopes-for-current-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|Inline|

<h3 id="get-all-envelopes-for-current-user.-responseschema">Response Schema</h3>

Status Code **200**

*Response Get Root Envelope Get*

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|Response Get Root Envelope Get|[[EnvelopeOut](#schemaenvelopeout)]|false|none|[Fields returned by Envelope queries.]|
|» EnvelopeOut|[EnvelopeOut](#schemaenvelopeout)|false|none|Fields returned by Envelope queries.|
|»» id|string(uuid)|true|none|none|
|»» name|string|true|none|none|
|»» user_id|string(uuid)|true|none|none|
|»» total_funds|number|true|none|none|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Create new Envelope.

<a id="opIdpost_root_envelope_post"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.post('/envelope', headers = headers)

print(r.json())

```

`POST /envelope`

### Body parameter

```json
{
  "name": "string"
}
```

<h3 id="create-new-envelope.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|[EnvelopeIn](#schemaenvelopein)|true|none|

### Example responses

> 201 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "total_funds": 0
}
```

<h3 id="create-new-envelope.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|Successful Response|[EnvelopeOut](#schemaenvelopeout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Get requested Envelope for current user.

<a id="opIdget_id_envelope__envelope_id__get"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.get('/envelope/{envelope_id}', headers = headers)

print(r.json())

```

`GET /envelope/{envelope_id}`

<h3 id="get-requested-envelope-for-current-user.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|envelope_id|path|string(uuid)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "total_funds": 0
}
```

<h3 id="get-requested-envelope-for-current-user.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[EnvelopeOut](#schemaenvelopeout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Update the given Envelope.

<a id="opIdput_id_envelope__envelope_id__put"></a>

### Code samples

```python
import requests
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/envelope/{envelope_id}', headers = headers)

print(r.json())

```

`PUT /envelope/{envelope_id}`

### Body parameter

```json
{
  "name": "string",
  "total_funds": 0
}
```

<h3 id="update-the-given-envelope.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|envelope_id|path|string(uuid)|true|none|
|body|body|[EnvelopeChanges](#schemaenvelopechanges)|true|none|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "total_funds": 0
}
```

<h3 id="update-the-given-envelope.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[EnvelopeOut](#schemaenvelopeout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

## Add given funds to Envelope.

<a id="opIdput_funds_envelope__envelope_id__funds__amount__put"></a>

### Code samples

```python
import requests
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer {access-token}'
}

r = requests.put('/envelope/{envelope_id}/funds/{amount}', headers = headers)

print(r.json())

```

`PUT /envelope/{envelope_id}/funds/{amount}`

<h3 id="add-given-funds-to-envelope.-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|envelope_id|path|string(uuid)|true|none|
|amount|path|number|true|none|
|source|query|string(uuid)|false|Where take funds from; default: Available Balance.|
|out|query|boolean|false|Move funds out of this Envelope.|

### Example responses

> 200 Response

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "total_funds": 0
}
```

<h3 id="add-given-funds-to-envelope.-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|Successful Response|[EnvelopeOut](#schemaenvelopeout)|
|422|[Unprocessable Entity](https://tools.ietf.org/html/rfc2518#section-10.3)|Validation Error|[HTTPValidationError](#schemahttpvalidationerror)|

<aside class="warning">
To perform this operation, you must be authenticated by means of one of the following methods:
OAuth2PasswordBearer
</aside>

# Schemas

<h2 id="tocS_AccountChanges">AccountChanges</h2>

<a id="schemaaccountchanges"></a>
<a id="schema_AccountChanges"></a>
<a id="tocSaccountchanges"></a>
<a id="tocsaccountchanges"></a>

```json
{
  "name": "string",
  "closed": true
}

```

AccountChanges

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|false|none|none|
|closed|boolean|false|none|none|

<h2 id="tocS_AccountIn">AccountIn</h2>

<a id="schemaaccountin"></a>
<a id="schema_AccountIn"></a>
<a id="tocSaccountin"></a>
<a id="tocsaccountin"></a>

```json
{
  "name": "string"
}

```

AccountIn

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|

<h2 id="tocS_AccountOut">AccountOut</h2>

<a id="schemaaccountout"></a>
<a id="schema_AccountOut"></a>
<a id="tocSaccountout"></a>
<a id="tocsaccountout"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "closed": true
}

```

AccountOut

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|none|none|
|name|string|true|none|none|
|user_id|string(uuid)|true|none|none|
|closed|boolean|true|none|none|

<h2 id="tocS_Balance">Balance</h2>

<a id="schemabalance"></a>
<a id="schema_Balance"></a>
<a id="tocSbalance"></a>
<a id="tocsbalance"></a>

```json
{
  "amount": 0,
  "collection": "string",
  "collection_id": "4bdef85c-3f50-4006-a713-2350da665f80",
  "collection_type": "account",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5"
}

```

Balance

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number|true|none|none|
|collection|string|false|none|none|
|collection_id|string(uuid)|false|none|none|
|collection_type|any|false|none|none|

anyOf

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

or

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» *anonymous*|string|false|none|none|

continued

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|user_id|string(uuid)|true|none|none|

#### Enumerated Values

|Property|Value|
|---|---|
|*anonymous*|account|
|*anonymous*|envelope|

<h2 id="tocS_Body_post_token_post">Body_post_token_post</h2>

<a id="schemabody_post_token_post"></a>
<a id="schema_Body_post_token_post"></a>
<a id="tocSbody_post_token_post"></a>
<a id="tocsbody_post_token_post"></a>

```json
{
  "grant_type": "string",
  "username": "string",
  "password": "string",
  "scope": "",
  "client_id": "string",
  "client_secret": "string"
}

```

Body_post_token_post

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|grant_type|string|false|none|none|
|username|string|true|none|none|
|password|string|true|none|none|
|scope|string|false|none|none|
|client_id|string|false|none|none|
|client_secret|string|false|none|none|

<h2 id="tocS_EnvelopeChanges">EnvelopeChanges</h2>

<a id="schemaenvelopechanges"></a>
<a id="schema_EnvelopeChanges"></a>
<a id="tocSenvelopechanges"></a>
<a id="tocsenvelopechanges"></a>

```json
{
  "name": "string",
  "total_funds": 0
}

```

EnvelopeChanges

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|false|none|none|
|total_funds|number|false|none|none|

<h2 id="tocS_EnvelopeIn">EnvelopeIn</h2>

<a id="schemaenvelopein"></a>
<a id="schema_EnvelopeIn"></a>
<a id="tocSenvelopein"></a>
<a id="tocsenvelopein"></a>

```json
{
  "name": "string"
}

```

EnvelopeIn

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|name|string|true|none|none|

<h2 id="tocS_EnvelopeOut">EnvelopeOut</h2>

<a id="schemaenvelopeout"></a>
<a id="schema_EnvelopeOut"></a>
<a id="tocSenvelopeout"></a>
<a id="tocsenvelopeout"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "name": "string",
  "user_id": "a169451c-8525-4352-b8ca-070dd449a1a5",
  "total_funds": 0
}

```

EnvelopeOut

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|none|none|
|name|string|true|none|none|
|user_id|string(uuid)|true|none|none|
|total_funds|number|true|none|none|

<h2 id="tocS_HTTPValidationError">HTTPValidationError</h2>

<a id="schemahttpvalidationerror"></a>
<a id="schema_HTTPValidationError"></a>
<a id="tocShttpvalidationerror"></a>
<a id="tocshttpvalidationerror"></a>

```json
{
  "detail": [
    {
      "loc": [
        "string"
      ],
      "msg": "string",
      "type": "string"
    }
  ]
}

```

HTTPValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|detail|[[ValidationError](#schemavalidationerror)]|false|none|none|

<h2 id="tocS_Status">Status</h2>

<a id="schemastatus"></a>
<a id="schema_Status"></a>
<a id="tocSstatus"></a>
<a id="tocsstatus"></a>

```json
{
  "message": "string",
  "ok": true
}

```

Status

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|message|string|true|none|none|
|ok|boolean|true|none|none|

<h2 id="tocS_Token">Token</h2>

<a id="schematoken"></a>
<a id="schema_Token"></a>
<a id="tocStoken"></a>
<a id="tocstoken"></a>

```json
{
  "access_token": "string",
  "token_type": "bearer"
}

```

Token

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|access_token|string|true|none|none|
|token_type|string|false|none|none|

<h2 id="tocS_TransactionChanges">TransactionChanges</h2>

<a id="schematransactionchanges"></a>
<a id="schema_TransactionChanges"></a>
<a id="tocStransactionchanges"></a>
<a id="tocstransactionchanges"></a>

```json
{
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}

```

TransactionChanges

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number|false|none|none|
|description|string|false|none|none|
|payee|string|false|none|none|
|timestamp|string(date-time)|false|none|none|
|account_id|string(uuid)|false|none|none|
|spent_from|string(uuid)|false|none|none|

<h2 id="tocS_TransactionIn">TransactionIn</h2>

<a id="schematransactionin"></a>
<a id="schema_TransactionIn"></a>
<a id="tocStransactionin"></a>
<a id="tocstransactionin"></a>

```json
{
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}

```

TransactionIn

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|amount|number|true|none|none|
|description|string|true|none|none|
|payee|string|true|none|none|
|timestamp|string(date-time)|true|none|none|
|account_id|string(uuid)|true|none|none|
|spent_from|string(uuid)|false|none|none|

<h2 id="tocS_TransactionOut">TransactionOut</h2>

<a id="schematransactionout"></a>
<a id="schema_TransactionOut"></a>
<a id="tocStransactionout"></a>
<a id="tocstransactionout"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "amount": 0,
  "description": "string",
  "payee": "string",
  "timestamp": "2019-08-24T14:15:22Z",
  "account_id": "449e7a5c-69d3-4b8a-aaaf-5c9b713ebc65",
  "spent_from": "592e0269-2897-444a-afc1-794f927c397a"
}

```

TransactionOut

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|none|none|
|amount|number|true|none|none|
|description|string|true|none|none|
|payee|string|true|none|none|
|timestamp|string(date-time)|true|none|none|
|account_id|string(uuid)|true|none|none|
|spent_from|string(uuid)|false|none|none|

<h2 id="tocS_UserChanges">UserChanges</h2>

<a id="schemauserchanges"></a>
<a id="schema_UserChanges"></a>
<a id="tocSuserchanges"></a>
<a id="tocsuserchanges"></a>

```json
{
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}

```

UserChanges

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|handle|string|false|none|none|
|full_name|string|false|none|none|
|preferred_name|string|false|none|none|

<h2 id="tocS_UserIn">UserIn</h2>

<a id="schemauserin"></a>
<a id="schema_UserIn"></a>
<a id="tocSuserin"></a>
<a id="tocsuserin"></a>

```json
{
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string",
  "password": "string"
}

```

UserIn

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|handle|string|true|none|none|
|full_name|string|true|none|none|
|preferred_name|string|true|none|none|
|password|string|true|none|none|

<h2 id="tocS_UserOut">UserOut</h2>

<a id="schemauserout"></a>
<a id="schema_UserOut"></a>
<a id="tocSuserout"></a>
<a id="tocsuserout"></a>

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "handle": "string",
  "full_name": "string",
  "preferred_name": "string"
}

```

UserOut

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|id|string(uuid)|true|none|none|
|handle|string|true|none|none|
|full_name|string|true|none|none|
|preferred_name|string|true|none|none|

<h2 id="tocS_ValidationError">ValidationError</h2>

<a id="schemavalidationerror"></a>
<a id="schema_ValidationError"></a>
<a id="tocSvalidationerror"></a>
<a id="tocsvalidationerror"></a>

```json
{
  "loc": [
    "string"
  ],
  "msg": "string",
  "type": "string"
}

```

ValidationError

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|loc|[string]|true|none|none|
|msg|string|true|none|none|
|type|string|true|none|none|


