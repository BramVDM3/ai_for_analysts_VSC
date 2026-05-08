class BookCatalogueUnavailableError(Exception):
    # Stable error code returned by the API when books cannot be loaded.
    code = "BOOK_CATALOGUE_UNAVAILABLE"

    def __init__(self, message: str = "Book catalogue data could not be loaded.") -> None:
        # Keep the default message readable for the frontend and end user.
        super().__init__(message)


class MemberListUnavailableError(Exception):
    # Stable error code returned by the API when members cannot be retrieved.
    code = "MEMBER_LIST_UNAVAILABLE"

    def __init__(self, message: str = "Member list data could not be loaded.") -> None:
        # Keep the default message readable for the frontend and end user.
        super().__init__(message)


class MemberNotFoundError(Exception):
    # Stable error code returned by the API when a requested member does not exist.
    code = "MEMBER_NOT_FOUND"

    def __init__(self, member_id: str) -> None:
        super().__init__(f"Member {member_id} was not found.")


class BookNotFoundError(Exception):
    code = "BOOK_NOT_FOUND"

    def __init__(self, book_id: str) -> None:
        super().__init__(f"Book {book_id} was not found.")


class MemberOverviewUnavailableError(Exception):
    # Stable error code returned by the API when a member overview cannot be built.
    code = "MEMBER_OVERVIEW_UNAVAILABLE"

    def __init__(self, message: str = "Member overview could not be loaded.") -> None:
        super().__init__(message)


class LoanListUnavailableError(Exception):
    # Stable error code returned by the API when loans cannot be retrieved.
    code = "LOAN_LIST_UNAVAILABLE"

    def __init__(self, message: str = "Loan list data could not be loaded.") -> None:
        # Keep the default message readable for the frontend and end user.
        super().__init__(message)


class ReferenceOnlyLoanError(Exception):
    code = "REFERENCE_ONLY"

    def __init__(self, message: str = "This book is reference-only and cannot be loaned.") -> None:
        super().__init__(message)


class BookUnavailableError(Exception):
    code = "BOOK_UNAVAILABLE"

    def __init__(self, message: str = "This book is unavailable and cannot be loaned.") -> None:
        super().__init__(message)


class BookAlreadyOnLoanError(Exception):
    code = "BOOK_ALREADY_ON_LOAN"

    def __init__(self, message: str = "This book already has an active loan.") -> None:
        super().__init__(message)


class InvalidLoanDatesError(Exception):
    code = "INVALID_LOAN_DATES"

    def __init__(self, message: str = "The due date must be on or after the loan date.") -> None:
        super().__init__(message)


class InvalidMemberStatusError(Exception):
    code = "INVALID_MEMBER_STATUS"

    def __init__(self, message: str = "The member status is invalid.") -> None:
        super().__init__(message)


class LoanNotAllowedError(Exception):
    code = "LOAN_NOT_ALLOWED"

    def __init__(self, message: str = "The loan could not be created.") -> None:
        super().__init__(message)


class LoanCreationUnavailableError(Exception):
    code = "LOAN_CREATION_UNAVAILABLE"

    def __init__(self, message: str = "Loan could not be created.") -> None:
        super().__init__(message)


class LoanNotFoundError(Exception):
    code = "LOAN_NOT_FOUND"

    def __init__(self, loan_id: str) -> None:
        super().__init__(f"Loan {loan_id} was not found.")


class LoanAlreadyReturnedError(Exception):
    code = "LOAN_ALREADY_RETURNED"

    def __init__(self, loan_id: str) -> None:
        super().__init__(f"Loan {loan_id} has already been returned.")


class InvalidReturnDateError(Exception):
    code = "INVALID_RETURN_DATE"

    def __init__(self, message: str = "The return date must be on or after the loan date.") -> None:
        super().__init__(message)


class LoanReturnUnavailableError(Exception):
    code = "LOAN_RETURN_UNAVAILABLE"

    def __init__(self, message: str = "Loan could not be marked as returned.") -> None:
        super().__init__(message)


class LendingPolicyUnavailableError(Exception):
    code = "LENDING_POLICY_UNAVAILABLE"

    def __init__(self, message: str = "Lending policy could not be loaded.") -> None:
        super().__init__(message)
