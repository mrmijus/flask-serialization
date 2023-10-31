# flask-serialization

Simple example how to create request and response validators for Flask REST API development


## Dependencies

In other for this to work you need to install the following dependencies:

```bash
pip install flask
pip install pydantic
```

## Example

Let's say we have a simple Flask endpoint that is tasked with creating a new user. 
The endpoint accepts a JSON payload with the following structure:

```json
{
    "name": "John Doe",
    "email": "something@mail.com",
    "age": 30
}
```

The endpoint should validate the request payload, create a new User,  
and return a response with the following structure:

```json
{
  "id": "e769fa67-f966-4782-b3b7-c40aedc15802",
  "name": "John Doe",
  "timestamp": "2021-08-15T15:00:00.000Z"
}
```

The response should be validated as well.

### Request validation

In order to make this work, we need to create the appropriate Pydantic models for the request and response payloads.

```python
from datetime import datetime
from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str
    age: int
    email: str


class UserResponse(BaseModel):
    id: str
    name: str
    timestamp: datetime
```

Now, once we have created our models, we need to inject them into our schema_validator decorator.

```python
from uuid import uuid4
from datetime import datetime

from flask import jsonify, request

from schema_validator import validate_schema

@app.route('/user', methods=['POST'])
@validate_schema(request_model=UserRequest, response_model=UserResponse)  # <-- Inject them into our decorator
def demo():
    return jsonify(
        {
            'id': str(uuid4()),
            'name': request.json['name'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         }
    ), 201
```

That's it! Your endpoint is now protected with request and response validators.

### Errors 

If the request payload is invalid, the endpoint will return an HTTP Status Code 422 Unprocessable Entity, 
along with the list of errors.

So, if you would make a POST with the following payload:

```json
{
  "email": "m.mijus@bc.com",
  "age": "not_a_number"
}
```
(Notice the 'NAME' field is missing, and the 'AGE' is not a valid integer.)

You would get the following response:

```json
{
   "message": "Invalid request body.",
   "errors": {
        "age": "Input should be a valid integer, unable to parse string as an integer",
        "name": "Field required"
    }
}
```

On the other hand, if the request pyload is valid, but the response payload is not,
the endpoint will return an HTTP Status Code 500 Internal Server Error, along with the error message.

```json
{
    "message": "there was an error while processing you request."
}
```

We attend to keep the error messages as generic as possible, in order to prevent any security issues,
but we actually know what exactly went wrong with formatting the response payload. That information
can be logged, so the API developers can fix the issue.


Thant's it! Happy coding! :)