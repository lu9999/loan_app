from src.covenant import Covenant
from src.loan import Loan


class Facility:
    def __init__(self, id, amount, interest_rate, bank_id, covenant):
        self.id = id
        self.amount = float(amount)
        self.interest_rate = float(interest_rate)
        self.bank_id = bank_id
        self.covenant = None
        self.set_covenant(covenant)
        self.expected_yield = 0

    def set_covenant(self, covenant):
        if isinstance(covenant, Covenant):
            self.covenant = covenant

    def check_expect_yield_for_new_loan(self, loan):
        expected_yield = (1 - loan.default_likelihood) * loan.interest_rate * loan.amount \
                         - loan.default_likelihood * loan.amount \
                         - self.interest_rate * loan.amount
        return expected_yield

    def check_new_loan(self, loan):
        if isinstance(loan, Loan) and loan.amount <= self.amount:
            if loan.default_likelihood <= self.covenant.max_default_likelihood and loan.state not in self.covenant.banned_state_set:
                return True
        return False

    def add_new_loan(self, loan):
        if self.check_new_loan(loan):
            expected_yield = self.check_expect_yield_for_new_loan(loan)
            self.expected_yield += expected_yield
            self.amount -= loan.amount
            return True
        return False
