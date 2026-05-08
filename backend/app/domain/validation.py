from datetime import date
from enum import Enum

from app.domain.errors import DomainValidationError


def require_text(value: str | None, message: str) -> str:
    # Validate required text fields and keep the original value for the domain object.
    if value is None or value.strip() == "":
        raise DomainValidationError(message)
    return value


def require_date(value: date | None, message: str) -> date:
    # Validate required date fields for domain objects.
    if value is None:
        raise DomainValidationError(message)
    return value


def require_boolean(value: bool | None, message: str) -> bool:
    # Reject missing or non-boolean values instead of accepting truthy/falsy objects.
    if not isinstance(value, bool):
        raise DomainValidationError(message)
    return value


def normalize_required_value(value: str | None, required_message: str) -> str:
    # Prepare enum-like text by trimming spaces and normalizing case.
    if value is None or value.strip() == "":
        raise DomainValidationError(required_message)
    return value.strip().lower()


def enum_from_value(enum_type: type[Enum], value: str, unsupported_message: str):
    # Convert a normalized string into a supported Enum member.
    for item in enum_type:
        if item.value == value:
            return item
    raise DomainValidationError(unsupported_message)
