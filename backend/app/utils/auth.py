# app/utils/auth.py
from functools import wraps
from typing import Optional, Callable, Any
from flask import request, jsonify, current_app
import jwt
from http import HTTPStatus
import os
from datetime import datetime, timezone

class AuthError(Exception):
    """Custom exception for authentication errors"""
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

def get_token_from_header() -> str:
    """Extract JWT token from the Authorization header"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header:
        raise AuthError('No authorization header', HTTPStatus.UNAUTHORIZED)
    
    parts = auth_header.split()
    
    if parts[0].lower() != 'bearer':
        raise AuthError('Authorization header must start with Bearer', HTTPStatus.UNAUTHORIZED)
    
    if len(parts) != 2:
        raise AuthError('Invalid authorization header format', HTTPStatus.UNAUTHORIZED)
        
    return parts[1]

def verify_token(token: str) -> dict:
    """
    Verify JWT token and return payload
    
    Args:
        token: JWT token string
        
    Returns:
        dict: Token payload if valid
        
    Raises:
        AuthError: If token is invalid or expired
    """
    try:
        # Get JWT secret from environment
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret:
            raise AuthError('JWT secret not configured', HTTPStatus.INTERNAL_SERVER_ERROR)
            
        # Decode and verify token
        payload = jwt.decode(
            token,
            jwt_secret,
            algorithms=['HS256'],
            options={'verify_exp': True}
        )
        
        # Check if token is expired
        exp = payload.get('exp')
        if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
            raise AuthError('Token has expired', HTTPStatus.UNAUTHORIZED)
            
        return payload
        
    except jwt.ExpiredSignatureError:
        raise AuthError('Token has expired', HTTPStatus.UNAUTHORIZED)
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token', HTTPStatus.UNAUTHORIZED)

def require_auth(f: Callable) -> Callable:
    """
    Decorator to require authentication for routes
    
    Verifies that a valid JWT token is present in the Authorization header
    """
    @wraps(f)
    async def decorated(*args: Any, **kwargs: Any) -> Any:
        try:
            # Get and verify token
            token = get_token_from_header()
            payload = verify_token(token)
            
            # Add user info to request context
            request.user = payload.get('sub')
            request.user_roles = payload.get('roles', [])
            
            return await f(*args, **kwargs)
            
        except AuthError as e:
            return jsonify({
                'status': 'error',
                'message': e.message
            }), e.status_code
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Internal server error'
            }), HTTPStatus.INTERNAL_SERVER_ERROR
            
    return decorated

def require_admin(f: Callable) -> Callable:
    """
    Decorator to require admin role for routes
    
    Must be used together with @require_auth
    """
    @wraps(f)
    async def decorated(*args: Any, **kwargs: Any) -> Any:
        try:
            # Check if user has admin role
            if 'admin' not in getattr(request, 'user_roles', []):
                raise AuthError('Admin access required', HTTPStatus.FORBIDDEN)
                
            return await f(*args, **kwargs)
            
        except AuthError as e:
            return jsonify({
                'status': 'error',
                'message': e.message
            }), e.status_code
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Internal server error'
            }), HTTPStatus.INTERNAL_SERVER_ERROR
            
    return decorated

def create_token(user_id: str, roles: list[str], expires_in: int = 3600) -> str:
    """
    Create a new JWT token
    
    Args:
        user_id: User identifier
        roles: List of user roles
        expires_in: Token expiration time in seconds (default 1 hour)
        
    Returns:
        str: Generated JWT token
    """
    try:
        jwt_secret = os.getenv('JWT_SECRET_KEY')
        if not jwt_secret:
            raise AuthError('JWT secret not configured', HTTPStatus.INTERNAL_SERVER_ERROR)
            
        now = datetime.now(timezone.utc)
        
        payload = {
            'sub': user_id,
            'roles': roles,
            'iat': now,
            'exp': now.timestamp() + expires_in
        }
        
        return jwt.encode(payload, jwt_secret, algorithm='HS256')
        
    except Exception as e:
        raise AuthError(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)

# Utility function to get current user ID
def get_current_user() -> Optional[str]:
    """Get current user ID from request context"""
    return getattr(request, 'user', None)

# Utility function to check if user has specific role
def has_role(role: str) -> bool:
    """Check if current user has specific role"""
    user_roles = getattr(request, 'user_roles', [])
    return role in user_roles
