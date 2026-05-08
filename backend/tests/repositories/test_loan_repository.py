from datetime import date

from app.domain import Loan
from app.repositories.in_memory_data import LOANS
from app.repositories.loan_repository import InMemoryLoanRepository


def test_in_memory_loan_repository_returns_seeded_loans():
    loans = InMemoryLoanRepository().list_loans()

    assert len(loans) == 12
    assert loans[0].loanId == "L001"
    assert loans[0].bookId == "B006"
    assert loans[0].memberId == "M001"
    assert loans[0].loanDate == date(2026, 1, 2)
    assert loans[0].dueDate == date(2026, 1, 23)
    assert loans[0].returnDate is None
    assert loans[0].status == "active"


def test_in_memory_loan_repository_derives_returned_status():
    loans = InMemoryLoanRepository().list_loans()

    returned_loan = next(loan for loan in loans if loan.loanId == "L005")

    assert returned_loan.returnDate == date(2025, 12, 20)
    assert returned_loan.status == "returned"


def test_in_memory_loan_repository_accepts_injected_loans():
    expected_loans = [
        Loan(
            loanId="L999",
            bookId="B001",
            memberId="M001",
            loanDate=date(2026, 1, 1),
            dueDate=date(2026, 1, 22),
            returnDate=None,
        )
    ]

    loans = InMemoryLoanRepository(expected_loans).list_loans()

    assert loans == expected_loans


def test_in_memory_loan_repository_accepts_an_empty_injected_loan_list():
    assert InMemoryLoanRepository([]).list_loans() == []


def test_in_memory_loan_repository_returns_a_copy_of_the_loan_list():
    loans = InMemoryLoanRepository().list_loans()

    loans.clear()

    assert len(LOANS) == 12
    assert len(InMemoryLoanRepository().list_loans()) == 12


def test_in_memory_loan_repository_adds_loan_to_current_state():
    repository = InMemoryLoanRepository([])
    loan = Loan(
        loanId="L001",
        bookId="B002",
        memberId="M001",
        loanDate=date(2026, 2, 1),
        dueDate=date(2026, 2, 22),
        returnDate=None,
    )

    created = repository.add_loan(loan)

    assert created == loan
    assert repository.list_loans() == [loan]
