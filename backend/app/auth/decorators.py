"""Authentication and role checks for API routes.

Provides the role_required decorator, a helper to read the logged-in user,
and handlers that return JWT errors in the API's normal error format.
"""

from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..errors import ApiError
from ..extensions import db
from ..models import User


def current_user():
    """The logged-in user for this request (set by role_required).

    Returns:
        User: the account that owns the access token.
    """
    return g.current_user


def role_required(*roles):
    """Require a valid token. With roles given, the user must have one of them.

        @role_required()                # any logged-in user
        @role_required("driver")        # drivers only

    Args:
        *roles: role names allowed to call the route. Empty means any role.

    Returns:
        A decorator that wraps the view function.
    """

    def decorator(view):
        """Wrap a view function with the token and role checks.

        Args:
            view: the Flask view function to protect.

        Returns:
            The wrapped view, keeping the original name via functools.wraps.
        """
        @wraps(view)
        def wrapper(*args, **kwargs):
            """Check the token and role on each request, then call the view.

            Stores the user on g so current_user() can return it.

            Raises:
                ApiError: 401 if the account no longer exists,
                    403 if the user's role is not allowed.
            """
            verify_jwt_in_request()
            user = db.session.get(User, int(get_jwt_identity()))
            if user is None:
                # Token is valid but the account no longer exists.
                raise ApiError(401, "unauthorized", "Please log in again.")
            if roles and user.role not in roles:
                raise ApiError(
                    403, "forbidden", f"Only {' or '.join(roles)} accounts can do this."
                )
            g.current_user = user
            return view(*args, **kwargs)

        return wrapper

    return decorator


def register_jwt_errors(jwt):
    """Return token problems in the API's normal error format, always as 401.

    Args:
        jwt: the app's flask_jwt_extended.JWTManager instance.
    """

    def unauthorized(message):
        """Build a 401 error response in the API's error format.

        Args:
            message: a user-friendly explanation of the problem.

        Returns:
            tuple: (error body, 401 status code).
        """
        return {"error": {"code": "unauthorized", "message": message}}, 401

    # No token was sent with the request.
    jwt.unauthorized_loader(lambda reason: unauthorized("Please log in to continue."))
    # The token is malformed or its signature does not match.
    jwt.invalid_token_loader(
        lambda reason: unauthorized("Your session is not valid. Log in again.")
    )
    # The token was valid but has expired.
    jwt.expired_token_loader(
        lambda header, payload: unauthorized("Your session has expired. Log in again.")
    )
