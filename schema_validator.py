
from typing import Optional, List, Dict, Any, Callable
from functools import wraps
from pydantic import ValidationError
from flask import request


def _construct_error_message(errors: List[Dict]) -> Dict[str, Any]:
    """Extracts and formats the list of validation errors thrown by Pydantic ValidationError."""
    error_message = {}
    for error in errors:
        error_message[error['loc'][0]] = error['msg']
    return error_message


def validate_schema(request_model: Optional[Callable] = None,
                    response_model: Optional[Callable] = None) -> Callable:
    """Intercepts the Flask request and response and validates them against the pydantic models."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request_model is not None:
                try:
                    request_model(**request.json)
                except ValidationError as exc:
                    errors = _construct_error_message(exc.errors())
                    return {
                        'message': "Invalid request body.",
                        "errors": errors
                    }, 422
            if response_model is not None:
                response = f(*args, **kwargs)
                if isinstance(response, tuple):
                    response, status_code = f(*args, **kwargs)
                try:
                    response_body = response.get_json()
                    response_model(**response_body)
                except ValidationError as exc:
                    return {"message": "there was an error while processing you request."}, 500
                else:
                    return f(*args, **kwargs)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
