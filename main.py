from datetime import datetime
from flask import Flask, jsonify, request
from schema_validator import validate_schema
from pydantic import BaseModel
from uuid import uuid4


app = Flask(__name__)


# Define your Request and Response models using Pydantic
class User(BaseModel):
    name: str
    age: int
    email: str


class UserResponse(BaseModel):
    id: str
    name: str
    timestamp: datetime


@app.route('/user', methods=['POST'])
@validate_schema(request_model=User, response_model=UserResponse)  # <-- Inject them into our decorator
def demo():
    return jsonify(
        {
            'idd': str(uuid4()),
            'name': request.json['name'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         }
    ), 201


# Enjoy :)
if __name__ == '__main__':
    app.run(debug=True)
