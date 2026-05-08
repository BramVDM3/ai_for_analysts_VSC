from app.domain import Loan
from app.repositories.in_memory_data import LOANS


class InMemoryLoanRepository:
    def __init__(self, loans: list[Loan] | None = None) -> None:
        # Allow tests to inject loan records while production uses the seeded data.
        self.loans = LOANS if loans is None else loans

    def list_loans(self) -> list[Loan]:
        # Return a copy so callers cannot accidentally change the repository seed data.
        return list(self.loans)

    def add_loan(self, loan: Loan) -> Loan:
        self.loans.append(loan)
        return loan

    def update_loan(self, updated_loan: Loan) -> Loan:
        for index, loan in enumerate(self.loans):
            if loan.loanId == updated_loan.loanId:
                self.loans[index] = updated_loan
                return updated_loan
        self.loans.append(updated_loan)
        return updated_loan
