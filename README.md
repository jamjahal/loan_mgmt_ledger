# Savage View API

## Usage

All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

subsequent response definitions will only detail the expected value of the `data field`
 ### List all Users

 **Definition**

 `GET /user`

 **Response**

 - `200 OK` on success

 ```json
 [
    {
        "user_id":"123XXX678xxxXf",
        "username":"ChadPolo"
        "tracking": [
        {
        "identifier":"banana-republic",
        "name":"Banana Republic",
        "channels": [
        {"channel":"twitter",
        "metrics":
        {
            "likes":True,
            "retweets":True,
            "hashtags":False
        }
        },
        {"channel":"website",
        "metrics":{
            "blog":[{
                "url": "https://banana_republic.com/blog/free_bananas",
                "title":"Free Bananas this week at BR",
                "post_date": "05-05-2020_07:23:55"
            },
            {
                "url": "https://banana_republic.com/blog/new_feature_announcement",
                "title": "Announcing new line coming this fall",
                "post_date": "05-06-2020_07:24:55"
                }]
        }
        }
        ]
        }
        ]
    }
 ]

### Registering a new company

**Definition**

`POST /tracking/<identifier>`

**Arguments**

- `"identifier": string` a globally unique identifier for this company
- `"name": string` a friendly name for this company
- `"channels": list` the channels that are being tracked for this company


**Response**

-`201 Created` on success

```json
{
    "identifier":"banana-republic",
    "name":"Banana Republic",
    "channels": [
        {"channel":"twitter",
        "metrics":
        {
            "likes":True,
            "retweets":True,
            "hashtags":False
        }
        },
    ]
}
```

### Lookup company being tracked

**Definition**

`GET /tracking/<identifier>`

**Response**

- `404 Not Found` if the user does not exist
- `200 OK` on success

```json
{
    "identifier":"banana-republic",
    "name":"Banana Republic",
    "channels": [
        {"channel":"twitter",
        "metrics":
        {
            "likes":True,
            "retweets":True,
            "hashtags":False
        }
        },
    ]
}
```

### Delete company

**Definition**

`DELETE /tracking/<identifier>`

**Response**

- `404 Not Found` if the company does not exist
- `204 No Content` if the company exists, but there is no content



**Arguments**

- `"user_id": string` a globally unique identifier for this user
- `"username": string` a globally unique readable identifier for this user_id
- `""`

Endpoints:
    Collection: /user
        GET - View Users
        POST - Add Users
    Companies: /user/tracking
        GET - View companies being tracked
        POST - Add company to be tracked
    Resource: /user/tracking/<identifier>
        GET - View company data
        POST - Add company data
    Resource: /user/tracking/<identifier>/channels
        GET - View company data
        POST - Add company data
