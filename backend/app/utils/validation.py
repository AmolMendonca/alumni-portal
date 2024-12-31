# app/utils/validation.py
from typing import Dict, Any, TypedDict
import re
from urllib.parse import urlparse

class ValidationResult(TypedDict):
    valid: bool
    message: str

def validate_profile_data(data: Dict[str, Any], is_update: bool = False) -> ValidationResult:
    """
    Validate alumni profile data.
    
    Args:
        data: Dictionary containing profile fields
        is_update: Boolean indicating if this is an update operation
        
    Returns:
        Dictionary containing validation result and error message if any
    """
    # Required fields for new profiles
    required_fields = {
        'fullName': str,
        'currentRole': str,
        'company': str,
        'university': str,
        'highSchool': str,
        'linkedInURL': str
    }
    
    # For updates, we don't require all fields to be present
    if not is_update:
        # Check for missing required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return ValidationResult(
                valid=False,
                message=f"Missing required fields: {', '.join(missing_fields)}"
            )
    
    # Validate present fields
    for field, value in data.items():
        # Check if field is allowed
        if field not in required_fields:
            return ValidationResult(
                valid=False,
                message=f"Unknown field: {field}"
            )
        
        # Check field type
        if not isinstance(value, required_fields[field]):
            return ValidationResult(
                valid=False,
                message=f"Field '{field}' must be of type {required_fields[field].__name__}"
            )
        
        # Check if value is empty string
        if isinstance(value, str) and not value.strip():
            return ValidationResult(
                valid=False,
                message=f"Field '{field}' cannot be empty"
            )
    
    # Specific field validations
    if 'fullName' in data:
        if not validate_full_name(data['fullName']):
            return ValidationResult(
                valid=False,
                message="Full name must be 2-100 characters long and contain only letters, spaces, and hyphens"
            )
    
    if 'linkedInURL' in data:
        if not validate_linkedin_url(data['linkedInURL']):
            return ValidationResult(
                valid=False,
                message="Invalid LinkedIn URL format"
            )
    
    if 'currentRole' in data:
        if not validate_role(data['currentRole']):
            return ValidationResult(
                valid=False,
                message="Current role must be 2-100 characters long"
            )
    
    if 'company' in data:
        if not validate_company(data['company']):
            return ValidationResult(
                valid=False,
                message="Company name must be 2-100 characters long"
            )
    
    if 'university' in data:
        if not validate_institution(data['university']):
            return ValidationResult(
                valid=False,
                message="University name must be 2-200 characters long"
            )
    
    if 'highSchool' in data:
        if not validate_institution(data['highSchool']):
            return ValidationResult(
                valid=False,
                message="High school name must be 2-200 characters long"
            )
    
    return ValidationResult(valid=True, message="")

def validate_full_name(name: str) -> bool:
    """Validate full name format."""
    # Allow letters, spaces, and hyphens, 2-100 chars
    pattern = r'^[A-Za-z\s-]{2,100}$'
    return bool(re.match(pattern, name))

def validate_linkedin_url(url: str) -> bool:
    """Validate LinkedIn URL format."""
    try:
        # Parse URL
        parsed = urlparse(url)
        
        # Check basic URL structure
        if not all([parsed.scheme, parsed.netloc]):
            return False
        
        # Check if it's a LinkedIn URL
        if not parsed.netloc.lower() in ['www.linkedin.com', 'linkedin.com']:
            return False
        
        # Check profile path format
        if not re.match(r'^/in/[\w-]+/?$', parsed.path):
            return False
        
        return True
    except:
        return False

def validate_role(role: str) -> bool:
    """Validate role name."""
    # Allow letters, numbers, spaces, and basic punctuation, 2-100 chars
    return 2 <= len(role) <= 100

def validate_company(company: str) -> bool:
    """Validate company name."""
    # Allow letters, numbers, spaces, and basic punctuation, 2-100 chars
    return 2 <= len(company) <= 100

def validate_institution(institution: str) -> bool:
    """Validate educational institution name."""
    # Allow letters, numbers, spaces, and basic punctuation, 2-200 chars
    return 2 <= len(institution) <= 200

def validate_batch_profiles(profiles_data: list) -> ValidationResult:
    """
    Validate batch profile creation data.
    
    Args:
        profiles_data: List of profile dictionaries
        
    Returns:
        ValidationResult indicating if the batch data is valid
    """
    if not isinstance(profiles_data, list):
        return ValidationResult(
            valid=False,
            message="Profiles data must be a list"
        )
    
    if not profiles_data:
        return ValidationResult(
            valid=False,
            message="Profiles list cannot be empty"
        )
    
    if len(profiles_data) > 100:  # Limit batch size
        return ValidationResult(
            valid=False,
            message="Maximum 100 profiles allowed per batch"
        )
    
    # Validate each profile in the batch
    for i, profile in enumerate(profiles_data):
        result = validate_profile_data(profile)
        if not result['valid']:
            return ValidationResult(
                valid=False,
                message=f"Profile at index {i} is invalid: {result['message']}"
            )
    
    return ValidationResult(valid=True, message="")

def validate_search_params(data: Dict[str, Any]) -> ValidationResult:
    """Validate search request parameters"""
    if 'query' not in data:
        return ValidationResult(
            valid=False,
            message="Search query is required"
        )
        
    if not isinstance(data['query'], str) or not data['query'].strip():
        return ValidationResult(
            valid=False,
            message="Invalid search query"
        )
        
    # Validate limit and offset if present
    limit = data.get('limit', 10)
    offset = data.get('offset', 0)
    
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        return ValidationResult(
            valid=False,
            message="Limit must be between 1 and 100"
        )
        
    if not isinstance(offset, int) or offset < 0:
        return ValidationResult(
            valid=False,
            message="Offset must be non-negative"
        )
        
    return ValidationResult(valid=True, message="")