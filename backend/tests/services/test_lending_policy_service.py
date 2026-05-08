from app.services.lending_policy_service import LendingPolicyService


def test_lending_policy_service_returns_pricing_and_lending_defaults():
    policy = LendingPolicyService().get_policy()

    assert policy.supportedMemberStatuses == ("default", "student", "senior")
    assert policy.defaultLoanDays == 21
    assert policy.studentLoanDays == 14
    assert policy.seniorLoanDays == 28
    assert policy.studentInitialLoanPrice == 0.0
    assert policy.dailyLoanPrice == 1.0
    assert policy.studentOverdueDailyPrice == 1.0
    assert policy.dailyOverdueFine == 0.25
    assert policy.maxOverdueFine == 10.0
    assert policy.maxActiveLoans == 5
    assert policy.currency == "EUR"
