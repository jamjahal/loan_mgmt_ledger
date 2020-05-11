# Ledger_API

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

subsequent response definitions will only detail the expected value of the `data field`

 ### Get sum of one or more buckets

 **Definition**

 `GET /ledger/buckets/sum?loanId={loanId}&bucketids={list of bucket identifiers to sum}`

 Example:

 GET /ledger/buckets/sum?loanId=123&bucketids=accounts-receivable-interest,loan-commitment-liability

 **Response**

 - `200 OK` on success

 ```json
 [
    {
        "accounts-receivable-interest":123.0,
        "loan-commitment-laibility":32323.32
    }
 ]
```
### Create new Buckets

**Definition**

`POST /ledger/buckets/<identifier>`



**Arguments**

- `"identifier": string` a globally unique identifier for this company

Input structure:
 {
    “identifier”: “loan-commitment-liability”,
}

**Response**

-`201 Created` on success

```json
{
    "identifier":"loan-commitment-liability",
}
```

### List all entries for a specific loan

**Definition**

`GET /ledger/entries?loanId={LOAN ID}`

**Response**

- `404 Not Found` if the user does not exist
- `200 OK` on success

```json
{
	“entries”: [
		{
			“createdAt”: “XXX”,
			“effectiveDate”: “YYY”,
			“bucketId”: “ZZZ”,
			“value”: 123.0
		},
		{
			“createdAt”: “XXX”,
			“effectiveDate”: “YYY”,
			“bucketId”: “TTT”,
			“value”: 123.0
		},
	]
}
```

### Add a new entry pair to the ledger

**Definition**

`POST /ledger/entries - add a new entry pair to the ledger`

**Arguments**
**Each** entry within the entry pair requires the following arguements:

- `"createdAt": string` a string of date of origination of loan, formatted MM-DD-YYYY
- `"effectiveDate": string` a datetime when loan becomes effective, formatted MM-DD-YYYY
- `"credit_bucketId": string` a globally unique identifier for this bucket
- `"debit_bucketId": string` a globally unique identifier for this bucket
- `"value": float` the float amount of the loanId

**Response**

- `200 OK` on success
```json
[
    {
        “createdAt”: “XXX”,
        “effectiveDate”: “YYY”,
        “bucketId”: “ZZZ”,
        “value”: 123.0
    },
    {
        “createdAt”: “XXX”,
        “effectiveDate”: “YYY”,
        “bucketId”: “TTT”,
        “value”: 123.0
    },
]
```
